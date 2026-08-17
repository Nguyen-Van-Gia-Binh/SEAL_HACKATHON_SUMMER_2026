import time
import math
from typing import Dict, Any, List
from src.ai_intelligence.decision_rules import OperationalDecisionEngine

class FallbackWeatherForecaster:
    """
    Mô Hình Dự Báo Khí Tượng Thủy Văn & Điều Hành Nông Nghiệp Thông Minh (Heuristic AI Engine).
    Phân tích nhiệt động lực học khí quyển, gradient khí áp và vi khí hậu phục vụ sản xuất nông nghiệp.
    """
    @staticmethod
    def generate_forecast(aggregated_data: Dict[str, Any]) -> Dict[str, Any]:
        station_name = aggregated_data.get("station_name", "Trạm Khí Tượng IoT")
        station_id = aggregated_data.get("station_id", "STN_00")
        region = aggregated_data.get("region", "Việt Nam")
        metrics = aggregated_data.get("metrics", {})
        anomalies = aggregated_data.get("anomalies", [])

        temp = metrics.get("temp_avg", 28.0)
        humidity = metrics.get("humidity_avg", 75.0)
        pressure = metrics.get("pressure_avg", 1012.0)
        pressure_trend = metrics.get("pressure_trend_hpa", 0.0)
        wind_speed = metrics.get("wind_speed_avg", 3.5)
        wind_gust = metrics.get("wind_gust_max", 5.0)
        rain_rate = metrics.get("rainfall_avg_mm_h", 0.0)
        heat_index = metrics.get("heat_index_c", temp)
        pm25 = metrics.get("pm25_avg", 35.0)

        # Risk scoring algorithm (0 - 100)
        risk_score = 10.0
        if pressure < 1000.0:
            risk_score += (1000.0 - pressure) * 2.5
        if pressure_trend < -1.5:
            risk_score += abs(pressure_trend) * 8.0
        if wind_gust > 15.0:
            risk_score += (wind_gust - 15.0) * 3.5
        if rain_rate > 20.0:
            risk_score += (rain_rate - 20.0) * 1.2
        if heat_index > 40.0:
            risk_score += (heat_index - 40.0) * 4.0
        if pm25 > 100.0:
            risk_score += 15.0
        risk_score = min(100.0, max(5.0, round(risk_score, 1)))

        # Determine Weather State & 6h-24h trend projection with refined agricultural terminology
        if pressure < 995.0 or "RAPID_BAROMETRIC_DROP_STORM_SURGE" in anomalies:
            weather_condition = "Áp thấp nhiệt đới / Bão nhiệt đới mạnh"
            summary_vi = (f"CẢNH BÁO THIÊN TAI: Trạm {station_name} ghi nhận khí áp giảm nhanh xuống {pressure} hPa "
                          f"kèm gió giật {wind_gust} m/s và mưa lớn {rain_rate} mm/h. Vùng hoàn lưu xoáy thuận nhiệt đới đang tiến sát đất liền.")
            trend_6h = "Gió bão tiếp tục tăng cấp, mưa lớn dồn dập có thể gây ngập lụt vùng trũng thấp ven sông và sạt lở đồi rừng."
            trend_24h = "Bão gây mưa diện rộng trên toàn lưu vực sông trước khi suy yếu dần thành vùng áp thấp."
        elif heat_index >= 41.0 or "DANGEROUS_HEAT_INDEX" in anomalies:
            weather_condition = "Nắng nóng gay gắt / Nguy cơ khô hạn"
            summary_vi = (f"NẮNG NÓNG CỰC ĐOAN: Nhiệt độ trung bình {temp}°C kết hợp độ ẩm {humidity}% đẩy chỉ số nhiệt (Heat Index) "
                          f"lên ngưỡng nguy hiểm {heat_index}°C. Nguy cơ bốc thoát hơi nước mạnh trên đồng ruộng và cảnh báo cháy rừng.")
            trend_6h = "Nền nhiệt duy trì ở mức cao trên 38°C đến chiều muộn. Chiều tối có khả năng xuất hiện dông nhiệt cục bộ."
            trend_24h = "Nắng nóng tiếp tục mở rộng trên diện rộng, lượng nước bốc hơi lớn cần chủ động điều tiết nguồn nước tưới."
        elif rain_rate >= 35.0 or "HEAVY_TORRENTIAL_RAIN" in anomalies:
            weather_condition = "Mưa to đến rất to / Nguy cơ ngập úng mùa màng"
            summary_vi = (f"MƯA LỚN KÉO DÀI: Cường độ mưa đạt {rain_rate} mm/h. Độ ẩm không khí bão hòa {humidity}%. Nguy cơ ngập úng cục bộ diện tích lúa và hoa màu.")
            trend_6h = "Mưa xối xả kéo dài trong 3-5 giờ tới, mực nước trên các sông nội đồng và kênh dẫn dâng cao."
            trend_24h = "Mưa có xu hướng giảm dần về cường độ, chuyển sang mưa rào rải rác từng đợt."
        elif temp <= 10.0:
            weather_condition = "Rét đậm / Rét hại & Sương muối vùng núi"
            summary_vi = (f"RÉT ĐẬM VÙNG CAO: Nhiệt độ giảm sâu xuống {temp}°C, gió mùa Đông Bắc {wind_speed} m/s, sương mù dày đặc ảnh hưởng đến mạ và gia súc.")
            trend_6h = "Nhiệt độ ban đêm tiếp tục giảm sâu về 4-6°C. Khả năng xuất hiện sương muối và băng giá tại các vùng núi cao."
            trend_24h = "Không khí lạnh tiếp tục tăng cường, rét buốt kéo dài sang ngày hôm sau."
        else:
            weather_condition = "Thời tiết ổn định / Thuận lợi sản xuất nông nghiệp"
            summary_vi = (f"Điều kiện khí tượng tại {station_name} duy trì ổn định. Nhiệt độ {temp}°C, độ ẩm {humidity}%, "
                          f"gió nhẹ {wind_speed} m/s, áp suất cân bằng {pressure} hPa. Thuận lợi cho cây trồng sinh trưởng.")
            trend_6h = "Thời tiết duy trì trạng thái tốt, mây thay đổi, không mưa, gió nhẹ, thuận lợi cho việc chăm sóc đồng ruộng."
            trend_24h = "Thời tiết quang đãng ban ngày, mát mẻ về đêm và sáng sớm, các chỉ số khí tượng nằm trong ngưỡng tối ưu."

        # Compute Operational Decisions
        decisions = OperationalDecisionEngine.evaluate_operational_decisions(metrics, anomalies)

        return {
            "source": "AI_FALLBACK_METEOROLOGICAL_ENGINE",
            "station_id": station_id,
            "station_name": station_name,
            "region": region,
            "weather_condition": weather_condition,
            "risk_score": risk_score,
            "risk_level": "CRITICAL" if risk_score > 70 else ("HIGH" if risk_score > 45 else ("MODERATE" if risk_score > 25 else "LOW")),
            "synoptic_analysis": summary_vi,
            "forecast_horizons": {
                "6_hours": trend_6h,
                "24_hours": trend_24h
            },
            "smart_operational_decisions": decisions,
            "generated_at": time.time()
        }
