import asyncio
import json
import logging
import os
import threading
import time
from pathlib import Path
from typing import Dict, List, Any, Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from kafka import KafkaConsumer, KafkaProducer
import paho.mqtt.client as mqtt

from src.config import settings
from src.ai_intelligence.forecaster import AIWeatherForecaster
from src.ai_intelligence.fallback_forecaster import FallbackWeatherForecaster

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] (FastAPI-Backend) %(message)s")
logger = logging.getLogger("backend")

app = FastAPI(title="Hệ Thống Quan Trắc Thời Tiết IoT & Điều Hành Nông Nghiệp Thông Minh", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIONS_FILE = Path(__file__).parent.parent.parent / "data" / "stations.json"
STATIC_DIR = Path(__file__).parent / "static"

# Global In-Memory State
latest_telemetry: Dict[str, Dict[str, Any]] = {}
latest_aggregations: Dict[str, Dict[str, Any]] = {}
latest_forecasts: Dict[str, Dict[str, Any]] = {}
recent_alerts: List[Dict[str, Any]] = []
connected_websockets: Set[WebSocket] = set()

ai_forecaster = AIWeatherForecaster()
mqtt_ctrl_client = mqtt.Client(client_id="backend-controller", protocol=mqtt.MQTTv311)

class ScenarioRequest(BaseModel):
    scenario: str # normal, typhoon, heatwave, flood, cold_front

def load_stations():
    if STATIONS_FILE.exists():
        with open(STATIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def kafka_consumer_worker():
    retries = 15
    consumer = None
    while retries > 0:
        try:
            consumer = KafkaConsumer(
                settings.TOPIC_RAW,
                settings.TOPIC_AGGREGATED,
                settings.TOPIC_ALERTS,
                settings.TOPIC_FORECASTS,
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS.split(","),
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                group_id="dashboard-backend-group",
                auto_offset_reset="latest"
            )
            logger.info("Backend Kafka consumer thread connected successfully.")
            break
        except Exception as e:
            logger.warning(f"Backend Kafka consumer waiting ({settings.KAFKA_BOOTSTRAP_SERVERS})... {e}")
            time.sleep(2)
            retries -= 1

    if not consumer:
        logger.warning("Kafka consumer disabled in backend (running in mock/standalone mode).")
        return

    for msg in consumer:
        try:
            topic = msg.topic
            data = msg.value
            station_id = data.get("station_id", "UNKNOWN")

            if topic == settings.TOPIC_RAW:
                latest_telemetry[station_id] = data
            elif topic == settings.TOPIC_AGGREGATED:
                latest_aggregations[station_id] = data
            elif topic == settings.TOPIC_FORECASTS:
                latest_forecasts[station_id] = data
            elif topic == settings.TOPIC_ALERTS:
                recent_alerts.insert(0, data)
                if len(recent_alerts) > 50:
                    recent_alerts.pop()
        except Exception as e:
            logger.error(f"Error in backend kafka consumer: {e}")

@app.on_event("startup")
async def startup_event():
    t = threading.Thread(target=kafka_consumer_worker, daemon=True)
    t.start()

    try:
        mqtt_ctrl_client.connect(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT, keepalive=60)
        mqtt_ctrl_client.loop_start()
    except Exception as e:
        logger.warning(f"Could not connect backend to MQTT for control: {e}")

    stations = load_stations()
    for stn in stations:
        sid = stn["station_id"]
        sample_reading = {
            "station_id": sid,
            "station_name": stn["station_name"],
            "region": stn.get("region"),
            "lat": stn.get("lat"),
            "lon": stn.get("lon"),
            "temp": 28.5,
            "humidity": 75.0,
            "pressure": 1012.0,
            "wind_speed": 3.4,
            "wind_direction": "SE",
            "rainfall_mm_h": 0.0,
            "uv_index": 6.0,
            "pm25": 28.0,
            "protocol": stn.get("ingestion_protocol", "MQTT"),
            "event_time": time.time()
        }
        latest_telemetry[sid] = sample_reading
        
        initial_agg = {
            "station_id": sid,
            "station_name": stn["station_name"],
            "region": stn.get("region"),
            "metrics": {
                "temp_avg": 28.5, "temp_min": 26.0, "temp_max": 31.0,
                "humidity_avg": 75.0, "pressure_avg": 1012.0,
                "pressure_trend_hpa": 0.1, "wind_speed_avg": 3.4,
                "wind_gust_max": 5.2, "rainfall_avg_mm_h": 0.0,
                "pm25_avg": 28.0, "uv_index_max": 6.0,
                "heat_index_c": 31.2, "dew_point_c": 23.5
            },
            "anomalies": []
        }
        latest_forecasts[sid] = FallbackWeatherForecaster.generate_forecast(initial_agg)

# REST API Endpoints
@app.get("/api/stations")
def get_stations():
    return load_stations()

@app.get("/api/state")
def get_current_state():
    return {
        "telemetry": latest_telemetry,
        "aggregations": latest_aggregations,
        "forecasts": latest_forecasts,
        "alerts": recent_alerts[:15]
    }

@app.post("/api/simulator/scenario")
def set_simulator_scenario(req: ScenarioRequest):
    valid_scenarios = ["normal", "typhoon", "heatwave", "flood", "cold_front"]
    if req.scenario not in valid_scenarios:
        raise HTTPException(status_code=400, detail=f"Invalid scenario. Choose from: {valid_scenarios}")
    
    logger.info(f"Broadcasting scenario switch to: {req.scenario}")
    try:
        mqtt_ctrl_client.publish("iot/simulator/control", json.dumps({"scenario": req.scenario}))
    except Exception as e:
        logger.warning(f"Could not publish scenario change via MQTT: {e}")

    return {"status": "SUCCESS", "scenario": req.scenario}

@app.post("/api/ai/analyze/{station_id}")
def analyze_station(station_id: str):
    stations = {s["station_id"]: s for s in load_stations()}
    if station_id not in stations:
        raise HTTPException(status_code=404, detail="Station not found")
    
    cur_telem = latest_telemetry.get(station_id, {})
    temp = cur_telem.get("temp", 28.0)
    humidity = cur_telem.get("humidity", 70.0)
    pressure = cur_telem.get("pressure", 1012.0)
    
    agg_payload = {
        "station_id": station_id,
        "station_name": stations[station_id]["station_name"],
        "region": stations[station_id].get("region", "Việt Nam"),
        "metrics": {
            "temp_avg": temp,
            "temp_min": round(temp - 2.0, 1),
            "temp_max": round(temp + 2.0, 1),
            "humidity_avg": humidity,
            "pressure_avg": pressure,
            "pressure_trend_hpa": -2.8 if pressure < 1000 else 0.1,
            "wind_speed_avg": cur_telem.get("wind_speed", 3.5),
            "wind_gust_max": cur_telem.get("wind_speed", 3.5) * 1.5,
            "rainfall_avg_mm_h": cur_telem.get("rainfall_mm_h", 0.0),
            "pm25_avg": cur_telem.get("pm25", 25.0),
            "uv_index_max": cur_telem.get("uv_index", 5.0),
            "heat_index_c": round(temp + 3.0, 1),
            "dew_point_c": 22.0
        },
        "anomalies": ["RAPID_BAROMETRIC_DROP_STORM_SURGE"] if pressure < 995 else []
    }
    
    forecast = ai_forecaster.generate_weather_intelligence(agg_payload)
    latest_forecasts[station_id] = forecast
    return forecast

# Real-Time WebSocket for Dashboard
@app.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.add(websocket)
    logger.info(f"WebSocket client connected. Total clients: {len(connected_websockets)}")
    try:
        while True:
            payload = {
                "type": "STATE_UPDATE",
                "timestamp": time.time(),
                "telemetry": latest_telemetry,
                "aggregations": latest_aggregations,
                "forecasts": latest_forecasts,
                "alerts": recent_alerts[:10]
            }
            await websocket.send_text(json.dumps(payload))
            await asyncio.sleep(1.5)
    except WebSocketDisconnect:
        connected_websockets.remove(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if websocket in connected_websockets:
            connected_websockets.remove(websocket)

# Mount Static Files
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.backend.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=False)
