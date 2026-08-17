import json
import logging
import os
import time
from typing import Dict, Any
from src.config import settings
from src.ai_intelligence.fallback_forecaster import FallbackWeatherForecaster
from src.ai_intelligence.decision_rules import OperationalDecisionEngine

logger = logging.getLogger("ai_forecaster")

class AIWeatherForecaster:
    """
    Intelligent AI Meteorological Forecaster and Smart Operations Agent.
    Leverages Gemini / OpenAI API with fallback heuristic engine.
    """
    def __init__(self):
        self.gemini_client = None
        self.openai_client = None
        self._init_clients()

    def _init_clients(self):
        # Initialize Gemini if key present
        if settings.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.gemini_client = genai.GenerativeModel(settings.AI_MODEL_NAME or "gemini-1.5-flash")
                logger.info(f"Gemini AI Forecaster initialized successfully with model: {settings.AI_MODEL_NAME}")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {e}")

        # Initialize OpenAI if key present
        if settings.OPENAI_API_KEY:
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
                logger.info("OpenAI Forecaster initialized successfully.")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")

    def generate_weather_intelligence(self, aggregated_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates short-term weather forecast, risk assessment, and smart operational decisions.
        """
        # If Gemini is configured and available
        if self.gemini_client and settings.GEMINI_API_KEY:
            try:
                return self._call_gemini(aggregated_data)
            except Exception as e:
                logger.warning(f"Gemini API error ({e}). Falling back to Heuristic Engine.")

        # If OpenAI is configured
        if self.openai_client and settings.OPENAI_API_KEY:
            try:
                return self._call_openai(aggregated_data)
            except Exception as e:
                logger.warning(f"OpenAI API error ({e}). Falling back to Heuristic Engine.")

        # Fallback Heuristic Meteorological Engine
        return FallbackWeatherForecaster.generate_forecast(aggregated_data)

    def _build_prompt(self, data: Dict[str, Any]) -> str:
        station_name = data.get("station_name", "IoT Weather Station")
        metrics = data.get("metrics", {})
        anomalies = data.get("anomalies", [])
        window_type = data.get("window_type", "STREAM_WINDOW")

        prompt = f"""
Bạn là Chuyên gia Khí tượng Thủy văn & Kỹ sư Vận hành Đô thị Thông minh (AI Smart Operations Meteorologist).
Dưới đây là dữ liệu tổng hợp từ hệ thống Stream Processing IoT ({window_type} Window):

- Trạm quan trắc: {station_name} (Khu vực: {data.get('region', 'N/A')})
- Nhiệt độ trung bình: {metrics.get('temp_avg')} °C (Min: {metrics.get('temp_min')}°C, Max: {metrics.get('temp_max')}°C)
- Độ ẩm trung bình: {metrics.get('humidity_avg')} %
- Áp suất khí quyển: {metrics.get('pressure_avg')} hPa (Độ biến thiên áp suất: {metrics.get('pressure_trend_hpa')} hPa)
- Tốc độ gió: {metrics.get('wind_speed_avg')} m/s (Gió giật max: {metrics.get('wind_gust_max')} m/s)
- Lượng mưa: {metrics.get('rainfall_avg_mm_h')} mm/h
- Bụi mịn PM2.5: {metrics.get('pm25_avg')} µg/m3 | UV Index: {metrics.get('uv_index_max')}
- Heat Index (Chỉ số nhiệt): {metrics.get('heat_index_c')} °C | Điểm sương: {metrics.get('dew_point_c')} °C
- Cảnh báo bất thường từ Stream Engine: {json.dumps(anomalies, ensure_ascii=False)}

Hãy phân tích dữ liệu trên và trả về kết quả dưới định dạng JSON với cấu trúc bắt buộc sau:
{{
  "weather_condition": "Tên hình thái thời tiết chính (vd: Bão nhiệt đới, Nắng nóng gay gắt, Thời tiết ổn định)",
  "risk_score": 75, // Điểm số rủi ro từ 0 đến 100
  "risk_level": "LOW|MODERATE|HIGH|CRITICAL",
  "synoptic_analysis": "Đoạn phân tích khí tượng chuyên sâu 2-3 câu bằng tiếng Việt",
  "forecast_horizons": {{
    "6_hours": "Dự báo chi tiết trong 6 giờ tới",
    "24_hours": "Dự báo xu thế trong 24 giờ tới"
  }}
}}
Chỉ trả về JSON thuần, không chèn markdown ```json ... ```.
"""
        return prompt

    def _call_gemini(self, data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = self._build_prompt(data)
        response = self.gemini_client.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        parsed = json.loads(text.strip())
        
        # Attach operational decisions
        metrics = data.get("metrics", {})
        anomalies = data.get("anomalies", [])
        decisions = OperationalDecisionEngine.evaluate_operational_decisions(metrics, anomalies)
        
        parsed["source"] = f"GEMINI_AI ({settings.AI_MODEL_NAME})"
        parsed["station_id"] = data.get("station_id")
        parsed["station_name"] = data.get("station_name")
        parsed["region"] = data.get("region")
        parsed["smart_operational_decisions"] = decisions
        parsed["generated_at"] = time.time()
        return parsed

    def _call_openai(self, data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = self._build_prompt(data)
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        text = response.choices[0].message.content.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        parsed = json.loads(text.strip())
        
        metrics = data.get("metrics", {})
        anomalies = data.get("anomalies", [])
        decisions = OperationalDecisionEngine.evaluate_operational_decisions(metrics, anomalies)

        parsed["source"] = "OPENAI_GPT"
        parsed["station_id"] = data.get("station_id")
        parsed["station_name"] = data.get("station_name")
        parsed["region"] = data.get("region")
        parsed["smart_operational_decisions"] = decisions
        parsed["generated_at"] = time.time()
        return parsed
