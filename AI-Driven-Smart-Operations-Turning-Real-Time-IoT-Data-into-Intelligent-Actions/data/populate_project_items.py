import subprocess
import json

PROJECT_NUMBER = "18"
OWNER = "Pen1112003"

ITEMS = [
    {
        "title": "📡 [EPIC-01] Xây dựng Lớp Tiếp Nhận Đa Giao Thức IoT (MQTT :1883 & CoAP :5683 UDP -> Kafka Bridge)",
        "body": """### 🎯 Mục Tiêu
Triển khai tầng Ingestion tiếp nhận dữ liệu thời tiết thời gian thực từ mạng lưới cảm biến IoT phân tán sử dụng hai giao thức chuẩn công nghiệp là MQTT và CoAP, sau đó chuẩn hóa và đẩy vào Apache Kafka / Redpanda.

### 📐 Kiến Trúc & Chi Tiết Kỹ Thuật
1. **MQTT Broker (Eclipse Mosquitto :1883)**:
   - Các trạm thời tiết đẩy dữ liệu định kỳ tới topic: `iot/weather/{station_id}`.
   - Payload JSON định dạng chuẩn hóa:
     ```json
     {
       "station_id": "STN_HN_01",
       "temp": 32.4,
       "humidity": 78.0,
       "pressure": 1008.5,
       "wind_speed": 4.2,
       "rainfall_mm_h": 0.0,
       "event_time": 1723478900.12
     }
     ```
2. **CoAP Gateway (:5683 UDP)**:
   - Nhận gói tin UDP Constrained Application Protocol từ cảm biến năng lượng thấp (đo chỉ số UV, bụi mịn PM2.5).
   - Tiếp nhận qua CoAP resource `POST /telemetry` hoặc direct UDP packet.
3. **Kafka / Redpanda Bridge**:
   - `src/ingestion/mqtt_bridge.py` và `src/ingestion/coap_gateway.py` kết nối tới broker `localhost:9092` hoặc container `redpanda:29092`.
   - Gắn thêm metadata: `ingestion_timestamp`, `protocol: "MQTT" | "CoAP"`.
   - Đẩy vào topic trung tâm: `weather-raw`.

### ✅ Tiêu Chí Đạt Chuẩn (Acceptance Criteria)
- [x] Mosquitto broker khởi chạy ổn định trên cổng `1883`.
- [x] CoAP server tiếp nhận và giải mã chính xác gói tin UDP trên cổng `5683`.
- [x] Dữ liệu từ 2 nguồn được đóng gói đúng schema và đẩy vào Kafka topic `weather-raw` với độ trễ < 15ms.
"""
    },
    {
        "title": "⚙️ [EPIC-02] Triển khai Thuật Toán Watermarking (Bounded-Out-Of-Orderness) Xử Lý Dữ Liệu Trễ Mạng",
        "body": """### 🎯 Mục Tiêu
Xây dựng cơ chế Watermark quản lý thời gian sự kiện (Event-Time) để xử lý tình huống các gói tin IoT bị mất thứ tự hoặc trễ mạng (Network Jitter, Packet Drop).

### 📐 Thuật Toán & Công Thức
- **Cơ chế Bounded-Out-Of-Orderness**:
  $$Watermark(t) = \\max_{i}(EventTime_i) - T_{allowed\\_delay}$$
  - Cấu hình mặc định: $T_{allowed\\_delay} = 5.0\\text{ giây}$.
- **Phân loại bản ghi**:
  - **On-time Record**: Nếu $EventTime \\ge Watermark$, dữ liệu được đưa vào các Window đang hoạt động.
  - **Late-Arriving Record**: Nếu $EventTime < Watermark$, bản ghi bị trễ sau khi Watermark đã đi qua. Hệ thống ghi log cảnh báo và chuyển vào Side-Output stream để audit.

### 💻 Mã nguồn tham chiếu
- File cài đặt: `src/stream_engine/watermark.py`
- Lớp: `WatermarkManager`
- Phương thức: `process_event(record)` trả về `(is_on_time, event_time, current_watermark)`

### ✅ Tiêu Chí Đạt Chuẩn (Acceptance Criteria)
- [x] Bộ Watermark tự động tịnh tiến theo thời gian lớn nhất quan sát được.
- [x] Phát hiện chính xác 100% các gói tin trễ được giả lập cố ý.
- [x] Cung cấp API thống kê tỷ lệ dữ liệu trễ (`late_percentage`) theo thời gian thực.
"""
    },
    {
        "title": "🪟 [EPIC-03] Thiết Kế & Vận Hành Stream Windowing: Tumbling 1m & Sliding 5m",
        "body": """### 🎯 Mục Tiêu
Triển khai mô hình cửa sổ dòng dữ liệu (Stream Windowing) để tổng hợp các chỉ số khí tượng vi mô (Microclimate) phục vụ phát hiện sớm các hiện tượng thời tiết cực đoan.

### 📐 Mô Hình Cửa Sổ (Windowing Models)
1. **Tumbling Window (1 Phút - Cố định không chồng lấn)**:
   - Tính toán nhanh các thông số trung bình, min, max của nhiệt độ, độ ẩm, tốc độ gió và lượng mưa.
   - Công thức xác định bucket: $WindowID = \\lfloor EventTime / 60 \\rfloor$.
   - Kích hoạt đóng và tính toán (Trigger) khi: $Watermark \\ge (WindowID + 1) \\times 60$.
2. **Sliding Window (5 Phút, Trượt 1 Phút)**:
   - Duy trì bộ nhớ đệm (State Store) 300 giây và trượt mỗi 60 giây.
   - Mục đích: Tính toán đạo hàm biến thiên áp suất khí quyển (Barometric Pressure Tendency) $\\Delta P / \\Delta t$ và gió giật cực đại (Peak Wind Gust).

### 💻 Mã nguồn tham chiếu
- File cài đặt: `src/stream_engine/windowing.py`
- Lớp: `WindowManager`
- Phương thức: `advance_watermark_and_trigger(current_watermark)`

### ✅ Tiêu Chí Đạt Chuẩn (Acceptance Criteria)
- [x] Window state được phân vùng độc lập theo `station_id` (Station-keyed partitioning).
- [x] Tự động giải phóng bộ nhớ (State Eviction) khi cửa sổ đã hoàn tất tính toán để tránh rò rỉ RAM.
- [x] Xuất dữ liệu tổng hợp ra topic Kafka: `weather-aggregated`.
"""
    },
    {
        "title": "📊 [EPIC-04] Xây Dựng Hàm Tính Toán Chỉ Số Khí Tượng: NOAA Heat Index, Dew Point & Barometric Trend",
        "body": """### 🎯 Mục Tiêu
Tích hợp các phương trình khí tượng học chuẩn quốc tế vào Stream Engine để đánh giá chính xác độ nguy hiểm của thời tiết đối với đời sống và công nghiệp.

### 📐 Công Thức Khí Tượng Học Chuẩn
1. **Chỉ số nhiệt NOAA Heat Index (Nhiệt độ cảm nhận thực tế)**:
   - Sử dụng phương trình hồi quy đa biến Rothfusz:
     $$HI = -42.379 + 2.04901523 T + 10.14333127 RH - 0.22475541 T \\cdot RH - 0.00683783 T^2 - 0.05481717 RH^2 + \\dots$$
   - Khi $HI \\ge 41^\\circ\\text{C}$: Cảnh báo nguy hiểm sốc nhiệt (Heat Stroke Hazard).
2. **Điểm sương (Dew Point)**:
   - Tính theo phương trình Magnus-Tetens:
     $$T_{dp} = \\frac{237.7 \\times \\alpha}{17.27 - \\alpha}, \\quad \\alpha = \\frac{17.27 T}{237.7 + T} + \\ln\\left(\\frac{RH}{100}\\right)$$
3. **Độ dốc áp suất khí quyển (Barometric Pressure Trend)**:
   - $\\Delta P = P_{hiện\\_tại} - P_{bắt\\_đầu\\_cửa\\_sổ}$.
   - Khi $\\Delta P \\le -2.0\\text{ hPa}$ hoặc $P < 995\\text{ hPa} \\rightarrow$ Kích hoạt cờ `RAPID_BAROMETRIC_DROP_STORM_SURGE` báo trước tâm bão/áp thấp.

### 💻 Mã nguồn tham chiếu
- File cài đặt: `src/stream_engine/aggregators.py`

### ✅ Tiêu Chí Đạt Chuẩn (Acceptance Criteria)
- [x] Kiểm thử hàm tính toán chính xác tuyệt đối theo bảng đối chiếu của NOAA.
- [x] Tự động sinh danh sách nhãn bất thường (`anomalies`) đính kèm trong mỗi bản ghi tổng hợp.
"""
    },
    {
        "title": "🧠 [EPIC-05] Tích Hợp AI Weather Forecaster (Google Gemini API / OpenAI) & Fallback Engine",
        "body": """### 🎯 Mục Tiêu
Xây dựng module Trí tuệ Nhân tạo tiếp nhận dòng dữ liệu tổng hợp theo các Time Window, đưa ra dự báo xu thế thời tiết vi mô 6h - 24h và tính điểm số rủi ro (Risk Score 1-100).

### 📐 Chi Tiết Tích Hợp
1. **Cloud LLM API Integration**:
   - Sử dụng **Google Gemini API** (`gemini-1.5-flash`) hoặc **OpenAI API** (`gpt-4o-mini`).
   - Xây dựng Prompt chuyên gia khí tượng thủy văn, yêu cầu trả về JSON có cấu trúc rõ ràng:
     ```json
     {
       "weather_condition": "Bão nhiệt đới tiếp cận",
       "risk_score": 85,
       "risk_level": "CRITICAL",
       "synoptic_analysis": "Áp suất khí quyển giảm sâu kèm mưa dồn dập...",
       "forecast_horizons": {
         "6_hours": "Gió giật tăng mạnh, lượng mưa tích lũy có thể vượt 120mm...",
         "24_hours": "Tâm bão đổ bộ trực tiếp sau đó suy yếu..."
       }
     }
     ```
2. **Offline Heuristic Meteorological Engine (Dự phòng tự động)**:
   - Triển khai tại `src/ai_intelligence/fallback_forecaster.py`.
   - Nếu không có API Key hoặc mất kết nối mạng, hệ thống tự động sinh dự báo thông minh dựa trên mô hình toán khí tượng mà không gây gián đoạn luồng stream.

### ✅ Tiêu Chí Đạt Chuẩn (Acceptance Criteria)
- [x] Tự động nạp cấu hình `GEMINI_API_KEY` hoặc `OPENAI_API_KEY` từ file `.env`.
- [x] Tự chuyển đổi sang Fallback Heuristic Engine mượt mà với 0 giây gián đoạn.
- [x] Đẩy kết quả phân tích AI vào topic Kafka `weather-forecasts`.
"""
    },
    {
        "title": "🚨 [EPIC-06] Xây Dựng Bộ Quy Tắc Ra Quyết Định Vận Hành Thông Minh (Smart Operations Decision Intelligence)",
        "body": """### 🎯 Mục Tiêu
Chuyển hóa dữ liệu thời tiết và phân tích rủi ro của AI thành các mệnh lệnh hành động tự động cụ thể cho các ngành kinh tế trọng yếu.

### 🏢 Danh Mục Quy Tắc Vận Hành Đã Triển Khai
1. **Hạ tầng Đô thị & Thoát nước (Municipal Drainage)**:
   - Điều kiện: Lượng mưa $> 40\\text{ mm/h}$ hoặc có cảnh báo mưa xối xả.
   - Lệnh tự động: `EXEC_DRAINAGE_PUMPS_MAX_POWER` (Kích hoạt toàn bộ trạm bơm cưỡng bức chống ngập úng, hạ van ngăn triều).
2. **Hàng hải & Cảng biển (Maritime & Harbor)**:
   - Điều kiện: Gió giật $\\ge 18\\text{ m/s}$ (Cấp 6+) hoặc áp suất $< 990\\text{ hPa}$.
   - Lệnh tự động: `HALT_PORT_CRANES_AND_VESSEL_DISPATCH` (Cấm biển tuyệt đối, khóa chốt cẩu trục container).
3. **Nông nghiệp Thông minh (Smart Agriculture)**:
   - Điều kiện: Heat Index $\\ge 40^\\circ\\text{C} \\rightarrow$ `TRIGGER_PRECISION_MISTING_IRRIGATION` (Tưới phun sương làm mát).
   - Điều kiện: Nhiệt độ $\\le 8^\\circ\\text{C} \\rightarrow$ `ENABLE_GREENHOUSE_FROST_PROTECTION` (Sưởi ấm chống sương muối).
4. **An toàn Lao động & Xây dựng (Construction OSHA)**:
   - Điều kiện: Heat Index $\\ge 42^\\circ\\text{C} \\rightarrow$ `MANDATE_OUTDOOR_WORK_REST_CYCLE` (Ngừng làm việc ngoài trời nắng gắt).

### 💻 Mã nguồn tham chiếu
- File cài đặt: `src/ai_intelligence/decision_rules.py`

### ✅ Tiêu Chí Đạt Chuẩn (Acceptance Criteria)
- [x] Mỗi quyết định có trường `sector`, `severity`, `action`, `details` và `automated_command`.
- [x] Phát cảnh báo khẩn cấp sang Kafka topic `weather-alerts`.
"""
    },
    {
        "title": "🖥️ [EPIC-07] Xây Dựng Web UI Dashboard Thời Gian Thực (Glassmorphic Dark UI & WebSockets)",
        "body": """### 🎯 Mục Tiêu
Xây dựng giao diện Dashboard hiện đại chuẩn UI/UX cao cấp (Glassmorphic Dark Mode) để giám sát bản đồ vệ tinh, biểu đồ dòng dữ liệu và bảng khuyến nghị AI theo thời gian thực.

### 🎨 Thiết Kế Giao Diện & Công Nghệ
- **Frontend Stack**: HTML5, Vanilla CSS Glassmorphism (`backdrop-filter: blur(16px)`), Font Inter/Outfit/JetBrains Mono, FontAwesome Icons.
- **Bản đồ Trạm Khí tượng**: Tích hợp Leaflet.js hiển thị vị trí 6 trạm IoT (Hà Nội, TP.HCM, Đà Nẵng, Sa Pa, Singapore, Tokyo) kèm vòng tròn rủi ro màu sắc.
- **Biểu đồ Dòng Dữ Liệu**: Sử dụng Chart.js cập nhật trực tiếp biến thiên nhiệt độ thô, trung bình cửa sổ trượt 5m, và áp suất khí quyển.
- **Giao tiếp Real-Time**: WebSocket hai chiều nối từ FastAPI `/ws/telemetry` giúp đẩy dữ liệu mới mỗi 1.5 giây mà không cần reload trang.
- **Bộ Chuyển Đổi Kịch Bản (Scenario Switcher)**: Cho phép chọn nhanh: Normal, Typhoon, Heatwave, Flood, Cold Front.

### 💻 Mã nguồn tham chiếu
- Backend: `src/backend/main.py`
- Frontend: `src/backend/static/index.html`, `style.css`, `app.js`

### ✅ Tiêu Chí Đạt Chuẩn (Acceptance Criteria)
- [x] Giao diện đạt chuẩn thẩm mỹ cao, hiển thị mượt mà trên mọi kích thước màn hình.
- [x] Nút bấm *Phân tích AI ngay* gọi API trực tiếp và cập nhật ngay trên giao diện.
"""
    },
    {
        "title": "🐳 [EPIC-08] Đóng Gói Toàn Bộ Hệ Thống Bằng Docker & Docker Compose",
        "body": """### 🎯 Mục Tiêu
Container hóa toàn diện tất cả các dịch vụ (Message Bus, Ingestion Bridges, Stream Processing Engine, Simulator, Web Dashboard) để triển khai chỉ với 1 câu lệnh duy nhất.

### 📦 Danh Sách Container Trong `docker-compose.yml`
1. `redpanda`: Message Broker hiệu năng cao (Port `9092`).
2. `redpanda-console`: Giao diện Web quản trị Topic Kafka (Port `8080`).
3. `mosquitto`: MQTT Broker (Port `1883`).
4. `mqtt-bridge`: Cầu nối MQTT sang Kafka.
5. `coap-gateway`: Cổng tiếp nhận UDP CoAP (Port `5683/udp`).
6. `stream-engine`: Engine xử lý dòng dữ liệu & Watermarking.
7. `weather-simulator`: Bộ giả lập phát dữ liệu IoT đa trạm.
8. `web-dashboard`: FastAPI Web Server & UI (Port `8000`).

### 🚀 Lệnh Khởi Chạy
```bash
docker compose up --build -d
```

### ✅ Tiêu Chí Đạt Chuẩn (Acceptance Criteria)
- [x] Dockerfile đa năng tối ưu kích thước, hỗ trợ Python 3.11.
- [x] Các service tự động khởi động lại khi có sự cố (`restart: on-failure`).
- [x] Mạng ảo `weather-net` liên kết liền mạch toàn bộ các container.
"""
    },
    {
        "title": "🏆 [GUIDE-09] Bảng Tiêu Chí Đánh Giá Dự Án Dành Cho Thí Sinh (Competition Scoring Rubric)",
        "body": """### 🎯 Hướng Dẫn & Bảng Điểm Tham Khảo
Bảng tiêu chuẩn đánh giá chất lượng sản phẩm phần mềm dành cho ban giám khảo và thí sinh:

| Hạng Mục Đánh Giá | Trọng Số | Yêu Cầu Kỹ Thuật Chi Tiết |
| :--- | :---: | :--- |
| **1. Ingestion Protocols** | 20% | Hỗ trợ chuẩn MQTT và CoAP; có cơ chế đệm Kafka/Redpanda chịu tải cao; dữ liệu không bị thất thoát. |
| **2. Stream Engine & Watermarking** | 25% | Triển khai đúng công thức Watermark Event-Time; phân định chính xác dữ liệu đến trễ; tính toán đúng cửa sổ Tumbling & Sliding. |
| **3. Thuật Toán Khí Tượng** | 15% | Cài đặt chuẩn xác Heat Index, Dew Point, phát hiện sụt áp suất báo bão $\\Delta P/\\Delta t$. |
| **4. AI Forecasting & Decisions** | 20% | Tích hợp thành công Gemini/OpenAI API; có cơ chế Fallback Heuristic tự động; sinh khuyến nghị vận hành thực tiễn có giá trị. |
| **5. Giao Diện & Trực Quan Hóa** | 10% | Dashboard thời gian thực đẹp mắt, cập nhật qua WebSockets, có bản đồ và biểu đồ trực quan. |
| **6. Docker & Code Quality** | 10% | Cấu trúc code sạch sẽ chuẩn PEP 8; có tài liệu README đầy đủ; chạy 1 lệnh `docker compose up`. |

*Chúc các thí sinh và đội thi hoàn thành xuất sắc bài thi của mình!*
"""
    }
]

def main():
    print(f"Adding {len(ITEMS)} items to GitHub Project {PROJECT_NUMBER} for owner {OWNER}...")
    for idx, item in enumerate(ITEMS, 1):
        title = item["title"]
        body = item["body"]
        cmd = [
            "gh", "project", "item-create", PROJECT_NUMBER,
            "--owner", OWNER,
            "--title", title,
            "--body", body,
            "--format", "json"
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            out_json = json.loads(res.stdout)
            item_id = out_json.get("id", "OK")
            print(f"[{idx}/{len(ITEMS)}] Created: {title[:50]}... (ID: {item_id})")
        except Exception as e:
            print(f"[{idx}/{len(ITEMS)}] Error creating item: {e}")

if __name__ == "__main__":
    main()
