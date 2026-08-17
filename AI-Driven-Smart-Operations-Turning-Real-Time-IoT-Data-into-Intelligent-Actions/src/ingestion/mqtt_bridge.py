import json
import logging
import time
import paho.mqtt.client as mqtt
from kafka import KafkaProducer
from src.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] (MQTT-Bridge) %(message)s")
logger = logging.getLogger("mqtt_bridge")

class MQTTKafkaBridge:
    def __init__(self):
        self.mqtt_client = mqtt.Client(client_id="weather-mqtt-bridge", protocol=mqtt.MQTTv311)
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.producer = None
        self.is_running = False

    def init_kafka(self):
        retries = 15
        while retries > 0:
            try:
                self.producer = KafkaProducer(
                    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS.split(","),
                    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                    key_serializer=lambda k: k.encode("utf-8") if k else None,
                    retries=5
                )
                logger.info(f"Connected to Kafka at {settings.KAFKA_BOOTSTRAP_SERVERS}")
                return
            except Exception as e:
                logger.warning(f"Waiting for Kafka ({settings.KAFKA_BOOTSTRAP_SERVERS})... {e}")
                time.sleep(2)
                retries -= 1
        logger.error("Failed to connect to Kafka after retries.")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info(f"Connected to MQTT Broker ({settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT})")
            client.subscribe(settings.MQTT_TOPIC_WEATHER)
            logger.info(f"Subscribed to topic: {settings.MQTT_TOPIC_WEATHER}")
        else:
            logger.error(f"MQTT connection failed with code {rc}")

    def on_message(self, client, userdata, msg):
        try:
            payload_str = msg.payload.decode("utf-8")
            data = json.loads(payload_str)
            
            # Enrich metadata
            station_id = data.get("station_id", "STN_UNKNOWN")
            data["protocol"] = "MQTT"
            data["mqtt_topic"] = msg.topic
            data["ingestion_timestamp"] = time.time()
            if "event_time" not in data:
                data["event_time"] = time.time()

            if self.producer:
                self.producer.send(
                    settings.TOPIC_RAW,
                    key=station_id,
                    value=data
                )
                logger.debug(f"Bridged MQTT -> Kafka [{settings.TOPIC_RAW}] Station: {station_id}, Temp: {data.get('temp')}")
        except Exception as e:
            logger.error(f"Error handling MQTT message: {e}")

    def start(self):
        self.init_kafka()
        self.is_running = True
        logger.info(f"Connecting to MQTT Broker at {settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT}...")
        
        while self.is_running:
            try:
                self.mqtt_client.connect(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT, keepalive=60)
                self.mqtt_client.loop_forever()
            except Exception as e:
                logger.warning(f"MQTT connection error: {e}. Retrying in 3 seconds...")
                time.sleep(3)

    def stop(self):
        self.is_running = False
        if self.mqtt_client:
            self.mqtt_client.disconnect()
        if self.producer:
            self.producer.flush()
            self.producer.close()
        logger.info("MQTT Bridge stopped.")

if __name__ == "__main__":
    bridge = MQTTKafkaBridge()
    bridge.start()
