from typing import Dict, List, Any

class OperationalDecisionEngine:
    """
    Hệ Thống Tự Động Ra Quyết Định & Chỉ Đạo Điều Hành Nông Nghiệp Thông Minh
    (Smart Operations & Agricultural Decision Intelligence Engine).
    Chuyển đổi dữ liệu khí tượng và rủi ro thời gian thực thành phương án ứng phó,
    bảo vệ mùa màng, thủy lợi và an toàn ngư nghiệp.
    """
    @staticmethod
    def evaluate_operational_decisions(metrics: Dict[str, Any], anomalies: List[str]) -> List[Dict[str, Any]]:
        decisions = []

        temp_avg = metrics.get("temp_avg", 25.0)
        humidity_avg = metrics.get("humidity_avg", 70.0)
        pressure_avg = metrics.get("pressure_avg", 1013.0)
        pressure_trend = metrics.get("pressure_trend_hpa", 0.0)
        wind_speed = metrics.get("wind_speed_avg", 3.0)
        wind_gust = metrics.get("wind_gust_max", 3.0)
        rainfall = metrics.get("rainfall_avg_mm_h", 0.0)
        heat_index = metrics.get("heat_index_c", temp_avg)
        pm25 = metrics.get("pm25_avg", 20.0)

        # 1. THỦY LỢI & TIÊU THOÁT NƯỚC ĐỒNG RUỘNG
        if rainfall > 40.0 or "HEAVY_TORRENTIAL_RAIN" in anomalies:
            decisions.append({
                "sector": "THỦY LỢI & TIÊU ÚNG",
                "severity": "CRITICAL",
                "action": "Vận hành tối đa công suất các trạm bơm tiêu úng đầu mối",
                "details": f"Lượng mưa đo được {rainfall} mm/h có nguy cơ ngập úng lúa và hoa màu. Mở tối đa cống xả tiêu, hạ mực nước đệm trong hệ thống kênh mương.",
                "automated_command": "EXEC_DRAINAGE_PUMPS_MAX_POWER"
            })
        elif rainfall > 15.0:
            decisions.append({
                "sector": "THỦY LỢI & TIÊU ÚNG",
                "severity": "WARNING",
                "action": "Chuyển hệ thống thủy nông sang trạng thái sẵn sàng tiêu thoát nước",
                "details": f"Mưa vừa đến mưa to ({rainfall} mm/h). Kiểm tra cao trình các hồ chứa thủy lợi và cống lấy nước.",
                "automated_command": "SET_DRAINAGE_STANDBY_MODE"
            })

        # 2. THỦY SẢN & AN TOÀN ĐỘI TÀU KHAI THÁC BIỂN
        if wind_gust >= 18.0 or pressure_avg < 990.0 or "RAPID_BAROMETRIC_DROP_STORM_SURGE" in anomalies:
            decisions.append({
                "sector": "THỦY SẢN & TÀU THUYỀN",
                "severity": "CRITICAL",
                "action": "CẤM BIỂN - Yêu cầu toàn bộ tàu thuyền và lồng bè vào nơi trú ẩn an toàn",
                "details": f"Gió giật cực đại {wind_gust} m/s và khí áp sụt giảm {pressure_avg} hPa báo hiệu bão/áp thấp nhiệt đới mạnh. Gia cố lồng bè nuôi trồng thủy sản ven biển.",
                "automated_command": "HALT_PORT_CRANES_AND_VESSEL_DISPATCH"
            })
        elif wind_gust >= 12.0:
            decisions.append({
                "sector": "THỦY SẢN & TÀU THUYỀN",
                "severity": "WARNING",
                "action": "Phát thông báo gió mạnh cho tàu thuyền hoạt động gần bờ",
                "details": f"Gió giật {wind_gust} m/s. Hạn chế thả lưới và vận chuyển thủy sản trên biển.",
                "automated_command": "ALERT_HARBOR_LOGISTICS"
            })

        # 3. TRỒNG TRỌT & BẢO VỆ MÙA MÀNG
        if heat_index >= 40.0 or temp_avg >= 38.0:
            decisions.append({
                "sector": "TRỒNG TRỌT & BẢO VỆ THỰC VẬT",
                "severity": "HIGH",
                "action": "Kích hoạt hệ thống tưới phun sương làm mát và giữ ẩm đất",
                "details": f"Chỉ số nhiệt (Heat Index) đạt {heat_index}°C gây sốc nhiệt cây trồng và khô hạn đất canh tác. Tăng tần suất tưới vào sáng sớm và chiều mát.",
                "automated_command": "TRIGGER_PRECISION_MISTING_IRRIGATION"
            })
        elif temp_avg <= 8.0:
            decisions.append({
                "sector": "TRỒNG TRỌT & CHĂN NUÔI",
                "severity": "HIGH",
                "action": "Triển khai biện pháp che chắn chống rét hại, sương muối cho mạ và vật nuôi",
                "details": f"Nhiệt độ xuống thấp {temp_avg}°C có nguy cơ sương giá vùng cao. Che phủ nilon luống mạ, ủ ấm chuồng trại gia súc, ngừng chăn thả rông.",
                "automated_command": "ENABLE_GREENHOUSE_FROST_PROTECTION"
            })
        elif wind_speed < 4.0 and rainfall == 0.0 and humidity_avg < 80.0:
            decisions.append({
                "sector": "TRỒNG TRỌT & BẢO VỆ THỰC VẬT",
                "severity": "INFO",
                "action": "Thời tiết thuận lợi cho công tác chăm sóc, bón phân và phun chế phẩm sinh học",
                "details": f"Gió nhẹ {wind_speed} m/s, không mưa, độ ẩm {humidity_avg}% tạo điều kiện lý tưởng cho cây trồng hấp thu dinh dưỡng.",
                "automated_command": "NOTIFY_OPTIMAL_FARMING_WINDOW"
            })

        # 4. LÂM NGHIỆP & PHÒNG CHỐNG CHÁY RỪNG
        if temp_avg >= 37.0 and humidity_avg <= 45.0:
            decisions.append({
                "sector": "LÂM NGHIỆP & PHÒNG CHÁY RỪNG",
                "severity": "CRITICAL",
                "action": "Báo động nguy cơ cháy rừng cấp V (Cực kỳ nguy hiểm)",
                "details": f"Nhiệt độ cao {temp_avg}°C kết hợp độ ẩm thấp {humidity_avg}%. Nghiêm cấm phát dọn thực bì và sử dụng lửa trong rừng.",
                "automated_command": "ALERT_WILDFIRE_PREVENTION_LEVEL_5"
            })

        return decisions
