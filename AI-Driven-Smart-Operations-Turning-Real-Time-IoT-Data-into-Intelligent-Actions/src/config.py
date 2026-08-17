import os
from pydantic import BaseModel

class Settings(BaseModel):
    # Kafka / Redpanda settings
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    TOPIC_RAW: str = os.getenv("TOPIC_RAW", "weather-raw")
    TOPIC_AGGREGATED: str = os.getenv("TOPIC_AGGREGATED", "weather-aggregated")
    TOPIC_ALERTS: str = os.getenv("TOPIC_ALERTS", "weather-alerts")
    TOPIC_FORECASTS: str = os.getenv("TOPIC_FORECASTS", "weather-forecasts")

    # MQTT Settings
    MQTT_BROKER_HOST: str = os.getenv("MQTT_BROKER_HOST", "localhost")
    MQTT_BROKER_PORT: int = int(os.getenv("MQTT_BROKER_PORT", "1883"))
    MQTT_TOPIC_WEATHER: str = os.getenv("MQTT_TOPIC_WEATHER", "iot/weather/#")

    # CoAP Settings
    COAP_HOST: str = os.getenv("COAP_HOST", "0.0.0.0")
    COAP_PORT: int = int(os.getenv("COAP_PORT", "5683"))

    # Stream Processing Engine Settings
    WATERMARK_DELAY_SECONDS: float = float(os.getenv("WATERMARK_DELAY_SECONDS", "5.0"))
    TUMBLING_WINDOW_SIZE_SEC: int = int(os.getenv("TUMBLING_WINDOW_SIZE_SEC", "60"))
    SLIDING_WINDOW_SIZE_SEC: int = int(os.getenv("SLIDING_WINDOW_SIZE_SEC", "300"))
    SLIDING_WINDOW_SLIDE_SEC: int = int(os.getenv("SLIDING_WINDOW_SLIDE_SEC", "60"))

    # AI Forecast API Settings
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "gemini") # "gemini", "openai", "fallback"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    AI_MODEL_NAME: str = os.getenv("AI_MODEL_NAME", "gemini-1.5-flash")

    # Web Dashboard Settings
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")

settings = Settings()
