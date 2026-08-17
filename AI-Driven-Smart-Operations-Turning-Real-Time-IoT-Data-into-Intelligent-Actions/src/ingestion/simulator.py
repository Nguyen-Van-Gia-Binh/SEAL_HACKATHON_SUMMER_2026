import asyncio
import json
import logging
import math
import os
import random
import socket
import time
from pathlib import Path
import paho.mqtt.client as mqtt
from kafka import KafkaProducer
from src.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] (Simulator) %(message)s")
logger = logging.getLogger("simulator")

STATIONS_FILE = Path(__file__).parent.parent.parent / "data" / "stations.json"

class WeatherSimulator:
    def __init__(self):
        self.stations = self._load_stations()
        self.mqtt_client = mqtt.Client(client_id="weather-iot-simulator", protocol=mqtt.MQTTv311)
        self.mqtt_client.on_message = self.on_mqtt_message
        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.kafka_producer = None
        self.current_scenario = "normal"  # normal, typhoon, heatwave, flood, cold_front
        self.scenario_start_time = time.time()
        self.tick_count = 0
        self.is_running = False

    def _load_stations(self):
        if STATIONS_FILE.exists():
            with open(STATIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def on_mqtt_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Simulator connected to MQTT broker.")
            client.subscribe("iot/simulator/control")
            logger.info("Simulator subscribed to iot/simulator/control")

    def on_mqtt_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            if "scenario" in payload:
                self.set_scenario(payload["scenario"])
        except Exception as e:
            logger.error(f"Error handling control message: {e}")

    def set_scenario(self, scenario_name: str):
        valid = ["normal", "typhoon", "heatwave", "flood", "cold_front"]
        if scenario_name in valid:
            self.current_scenario = scenario_name
            self.scenario_start_time = time.time()
            logger.info(f"==> Switched Weather Scenario to: {scenario_name.upper()} <==")
            return True
        return False

    def connect_mqtt(self):
        try:
            self.mqtt_client.connect(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT, keepalive=60)
            self.mqtt_client.loop_start()
            logger.info(f"Simulator connected to MQTT ({settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT})")
        except Exception as e:
            logger.warning(f"Could not connect simulator to MQTT broker: {e}")

    def init_kafka(self):
        try:
            self.kafka_producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS.split(","),
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda k: k.encode("utf-8") if k else None
            )
            logger.info("Simulator initialized direct Kafka producer fallback.")
        except Exception as e:
            logger.warning(f"Kafka direct producer not available: {e}")

    def send_coap_packet(self, payload: dict):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            msg_bytes = json.dumps(payload).encode("utf-8")
            sock.sendto(msg_bytes, (settings.COAP_HOST if settings.COAP_HOST != "0.0.0.0" else "127.0.0.1", settings.COAP_PORT))
            sock.close()
        except Exception as e:
            logger.debug(f"Failed to send CoAP datagram: {e}")

    def generate_station_reading(self, station: dict) -> dict:
        now = time.time()
        self.tick_count += 1
        
        t_cycle = (now % 86400) / 86400 * 2 * math.pi
        diurnal_temp = math.sin(t_cycle - math.pi / 2) * 4.0
        
        temp = 28.0 + diurnal_temp + random.uniform(-0.5, 0.5)
        humidity = max(30.0, min(99.0, 75.0 - (diurnal_temp * 3) + random.uniform(-2, 2)))
        pressure = 1012.0 + random.uniform(-0.8, 0.8)
        wind_speed = max(0.5, 3.0 + random.uniform(-1.0, 2.0))
        wind_direction = random.choice(["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
        rainfall = 0.0
        uv_index = max(0.0, min(12.0, (5.0 + diurnal_temp * 1.5)))
        pm25 = max(5.0, 32.0 + random.uniform(-8, 8))
        solar_radiation = max(0.0, 450.0 + diurnal_temp * 80.0)

        elevation = station.get("elevation_m", 0)
        temp -= (elevation / 1000.0) * 6.5
        pressure -= (elevation / 100.0) * 11.0

        if self.current_scenario == "typhoon":
            pressure -= random.uniform(24.0, 30.0) # Drops down to ~982 hPa
            wind_speed = random.uniform(20.0, 34.0) # High wind gale
            rainfall = random.uniform(50.0, 110.0)  # Torrential downpour
            humidity = random.uniform(94.0, 99.0)
            uv_index = random.uniform(0.1, 1.0)
        elif self.current_scenario == "heatwave":
            temp += random.uniform(9.0, 13.0)       # Reaches 40 - 43°C
            humidity = max(25.0, humidity - 25.0)
            uv_index = random.uniform(11.0, 13.5)
            pm25 += random.uniform(60.0, 120.0)
            rainfall = 0.0
        elif self.current_scenario == "flood":
            rainfall = random.uniform(75.0, 140.0)
            humidity = 99.0
            wind_speed = random.uniform(12.0, 20.0)
        elif self.current_scenario == "cold_front":
            temp -= random.uniform(14.0, 20.0)
            wind_speed = random.uniform(9.0, 16.0)
            humidity = random.uniform(85.0, 95.0)

        event_time = now
        is_late = False
        if random.random() < 0.05:
            delay = random.uniform(3.0, 8.0)
            event_time = now - delay
            is_late = True

        reading = {
            "station_id": station["station_id"],
            "station_name": station["station_name"],
            "region": station.get("region", "Default"),
            "climate_zone": station.get("climate_zone", "Tropical"),
            "lat": station.get("lat", 0.0),
            "lon": station.get("lon", 0.0),
            "elevation_m": elevation,
            "temp": round(temp, 2),
            "humidity": round(humidity, 1),
            "pressure": round(pressure, 2),
            "wind_speed": round(wind_speed, 2),
            "wind_direction": wind_direction,
            "rainfall_mm_h": round(rainfall, 2),
            "uv_index": round(uv_index, 1),
            "pm25": round(pm25, 1),
            "solar_radiation": round(solar_radiation, 1),
            "scenario": self.current_scenario,
            "is_simulated_late": is_late,
            "event_time": event_time,
            "created_at": now
        }
        return reading

    def emit_reading(self, station: dict, reading: dict):
        protocol = station.get("ingestion_protocol", "MQTT")
        station_id = station["station_id"]

        if protocol == "MQTT":
            topic = f"iot/weather/{station_id}"
            try:
                self.mqtt_client.publish(topic, json.dumps(reading))
                logger.debug(f"[MQTT Published] {station_id} -> {topic} (Temp: {reading['temp']}°C)")
            except Exception as e:
                logger.debug(f"MQTT publish failed: {e}")
        elif protocol == "CoAP":
            self.send_coap_packet(reading)
            logger.debug(f"[CoAP Sent UDP] {station_id} -> Port {settings.COAP_PORT}")

        if self.kafka_producer:
            try:
                reading_copy = dict(reading)
                reading_copy["protocol"] = protocol + " (Direct)"
                reading_copy["ingestion_timestamp"] = time.time()
                self.kafka_producer.send(settings.TOPIC_RAW, key=station_id, value=reading_copy)
            except Exception:
                pass

    def run_loop(self, interval_sec: float = 2.0):
        self.is_running = True
        self.connect_mqtt()
        self.init_kafka()
        logger.info(f"Starting weather simulation loop for {len(self.stations)} stations (Interval: {interval_sec}s)...")

        while self.is_running:
            for station in self.stations:
                reading = self.generate_station_reading(station)
                self.emit_reading(station, reading)
            time.sleep(interval_sec)

if __name__ == "__main__":
    sim = WeatherSimulator()
    sim.run_loop(interval_sec=2.0)
