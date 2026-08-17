import json
import logging
import time
from typing import Dict, Any
from kafka import KafkaConsumer, KafkaProducer
from src.config import settings
from src.stream_engine.watermark import WatermarkManager
from src.stream_engine.windowing import WindowManager
from src.ai_intelligence.forecaster import AIWeatherForecaster

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] (Stream-Engine) %(message)s")
logger = logging.getLogger("stream_processor")

class StreamProcessingEngine:
    def __init__(self):
        self.watermark_mgr = WatermarkManager(max_out_of_orderness_sec=settings.WATERMARK_DELAY_SECONDS)
        self.window_mgr = WindowManager(
            tumbling_size_sec=settings.TUMBLING_WINDOW_SIZE_SEC,
            sliding_size_sec=settings.SLIDING_WINDOW_SIZE_SEC,
            sliding_step_sec=settings.SLIDING_WINDOW_SLIDE_SEC
        )
        self.ai_forecaster = AIWeatherForecaster()
        self.consumer = None
        self.producer = None
        self.is_running = False
        self.last_ai_eval_time: Dict[str, float] = {}

    def init_kafka(self):
        retries = 20
        while retries > 0:
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS.split(","),
                    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                    key_serializer=lambda k: k.encode("utf-8") if k else None
                )
                self.consumer = KafkaConsumer(
                    settings.TOPIC_RAW,
                    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS.split(","),
                    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                    group_id="weather-stream-processing-group",
                    auto_offset_reset="latest",
                    enable_auto_commit=True
                )
                logger.info(f"Stream Engine connected to Kafka brokers: {settings.KAFKA_BOOTSTRAP_SERVERS}")
                return
            except Exception as e:
                logger.warning(f"Waiting for Kafka ({settings.KAFKA_BOOTSTRAP_SERVERS})... {e}")
                time.sleep(2)
                retries -= 1
        logger.error("Could not connect Stream Engine to Kafka.")

    def process_raw_event(self, record: Dict[str, Any]):
        station_id = record.get("station_id", "UNKNOWN")
        is_on_time, event_time, current_watermark = self.watermark_mgr.process_event(record)

        # Ingestion into window states
        if is_on_time:
            self.window_mgr.assign_tumbling_window(station_id, record, event_time)
            self.window_mgr.assign_sliding_window(station_id, record, event_time)
        else:
            # Handle late arriving event (side-output / late tracking)
            logger.info(f"[LATE DATA DROPPED FROM NORMAL WINDOW] Station: {station_id}, EventTime: {event_time:.1f}, Watermark: {current_watermark:.1f}")

        # Check and trigger window closings
        emitted_windows = self.window_mgr.advance_watermark_and_trigger(current_watermark)
        for agg in emitted_windows:
            self._handle_aggregated_window(agg)

    def _handle_aggregated_window(self, agg: Dict[str, Any]):
        station_id = agg.get("station_id")
        win_type = agg.get("window_type")
        anomalies = agg.get("anomalies", [])
        
        logger.info(f"[WINDOW CLOSED: {win_type}] Station: {station_id} | Temp: {agg['metrics']['temp_avg']}°C | Press: {agg['metrics']['pressure_avg']}hPa | Anomalies: {len(anomalies)}")

        # 1. Publish to aggregated topic
        if self.producer:
            self.producer.send(settings.TOPIC_AGGREGATED, key=station_id, value=agg)

        # 2. Trigger AI Intelligence & Forecasting
        now = time.time()
        last_eval = self.last_ai_eval_time.get(station_id, 0.0)
        
        # Trigger AI if anomalies exist or periodically (every 30s per station)
        if len(anomalies) > 0 or (now - last_eval >= 30.0):
            self.last_ai_eval_time[station_id] = now
            try:
                forecast = self.ai_forecaster.generate_weather_intelligence(agg)
                logger.info(f"[AI FORECAST] Station {station_id} -> {forecast.get('weather_condition')} (Risk: {forecast.get('risk_score')}/100)")

                if self.producer:
                    self.producer.send(settings.TOPIC_FORECASTS, key=station_id, value=forecast)
                    
                    # If high risk or critical anomalies, emit alert
                    if forecast.get("risk_score", 0) >= 45 or len(anomalies) > 0:
                        alert = {
                            "station_id": station_id,
                            "station_name": agg.get("station_name"),
                            "severity": forecast.get("risk_level", "HIGH"),
                            "condition": forecast.get("weather_condition"),
                            "anomalies": anomalies,
                            "synoptic": forecast.get("synoptic_analysis"),
                            "decisions": forecast.get("smart_operational_decisions", []),
                            "created_at": now
                        }
                        self.producer.send(settings.TOPIC_ALERTS, key=station_id, value=alert)
            except Exception as e:
                logger.error(f"Error in AI forecast evaluation: {e}")

    def run(self):
        self.init_kafka()
        self.is_running = True
        logger.info("Starting Stream Processing Engine loop...")

        try:
            for message in self.consumer:
                if not self.is_running:
                    break
                try:
                    record = message.value
                    self.process_raw_event(record)
                except Exception as e:
                    logger.error(f"Error processing record from Kafka: {e}")
        except KeyboardInterrupt:
            logger.info("Stream Engine interrupted.")
        finally:
            if self.producer:
                self.producer.flush()
                self.producer.close()
            if self.consumer:
                self.consumer.close()

if __name__ == "__main__":
    engine = StreamProcessingEngine()
    engine.run()
