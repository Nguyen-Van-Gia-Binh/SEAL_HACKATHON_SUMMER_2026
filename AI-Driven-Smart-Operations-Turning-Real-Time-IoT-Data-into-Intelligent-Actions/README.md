# AI-Driven Smart Operations: Weather IoT Real-Time Streaming & AI Intelligence

Hệ thống Data Pipeline hoàn chỉnh thu thập dữ liệu quan trắc thời tiết IoT theo thời gian thực (Real-Time Ingestion), xử lý dòng dữ liệu (Stream Processing Engine với Watermarking, Windowing, Aggregation), tích hợp AI API (Gemini/OpenAI) để sinh dự báo khí tượng và đề xuất quyết định vận hành thông minh (Smart Operations Decision Intelligence), được cấu hình toàn diện qua Docker Compose.

---

## 1. Kiến Trúc Tổng Thể Hệ Thống (Architecture)

```
[IoT Weather Stations]
      │
      ├───> MQTT (:1883) ───> [MQTT Bridge] ──────┐
      │                                           ▼
      └───> CoAP (:5683/UDP) > [CoAP Gateway] ─> [Redpanda/Kafka :9092]
                                                  │ (Topic: weather-raw)
                                                  ▼
                                       [Stream Processing Engine]
                                         ├── Watermarking (Late data handling)
                                         ├── Tumbling & Sliding Windows
                                         └── Meteorological Aggregations
                                                  │
                                                  ├──> Topic: weather-aggregated
                                                  ▼
                                       [AI Forecasting & Decisions]
                                         ├── Gemini / OpenAI API
                                         └── Fallback Meteorological Engine
                                                  │
                                                  ├──> Topic: weather-forecasts
                                                  ├──> Topic: weather-alerts
                                                  ▼
                                       [FastAPI & Web Dashboard]
                                         ├── WebSocket Live Telemetry
                                         ├── Leaflet Interactive Map
                                         ├── Stream Windowing Chart
                                         └── Smart Operations Action Cards
```

---

## 2. Các Thành Phần Công Nghệ Chính

### 2.1 Ingestion Protocols (Giao thức thu thập dữ liệu)
1. **MQTT (Eclipse Mosquitto :1883)**:
   - Các trạm thời tiết phát dữ liệu định kỳ tới topic `iot/weather/{station_id}`.
   - `src/ingestion/mqtt_bridge.py`: Subscribe Mosquitto, chuẩn hóa payload, gắn metadata và đẩy vào Kafka topic `weather-raw`.
2. **CoAP (Constrained Application Protocol :5683/UDP)**:
   - Tối ưu cho thiết bị IoT biên năng lượng thấp (quan trắc UV, bụi mịn PM2.5).
   - `src/ingestion/coap_gateway.py`: Nhận gói tin UDP/CoAP và đẩy vào Kafka `weather-raw`.
3. **Kafka / Redpanda (:9092) & Redpanda Console (:8080)**:
   - Message bus phân tán hiệu năng cao, không phụ thuộc JVM, khởi động tức thì.
   - Redpanda Console UI cho phép trực tiếp xem tin nhắn và schema trên từng topic.

### 2.2 Stream Processing Engine
- **Watermarking Engine (`src/stream_engine/watermark.py`)**:
  - Triển khai thuật toán *Bounded-Out-Of-Orderness Watermark*: $Watermark = \max(EventTime) - T_{delay}$.
  - Tự động gắn nhãn và xử lý các sự kiện trễ (late-arriving data) do đường truyền chập chờn.
- **Windowing Models (`src/stream_engine/windowing.py`)**:
  - **Tumbling Window (1 phút)**: Cửa sổ cố định không chồng lấn tính min, max, avg nhiệt độ, độ ẩm, lượng mưa.
  - **Sliding Window (5 phút, trượt 1 phút)**: Cửa sổ trượt tính xu hướng biến thiên áp suất ($\Delta P / \Delta t$) nhằm phát hiện sớm bão và lốc xoáy.
- **Stateful Aggregations (`src/stream_engine/aggregators.py`)**:
  - Tính toán chỉ số nhiệt **NOAA Heat Index** theo phương trình hồi quy Rothfusz.
  - Tính điểm sương (**Dew Point**) theo công thức Magnus-Tetens.
  - Phát hiện bất thường: Sụt áp suất báo bão (`RAPID_BAROMETRIC_DROP`), gió giật (`GALE_FORCE_WIND_GUST`), nhiệt độ nguy hiểm (`DANGEROUS_HEAT_INDEX`).

### 2.3 AI Forecasting & Smart Operations Decision Intelligence
- **AI Forecasting Engine (`src/ai_intelligence/forecaster.py`)**:
  - Tích hợp **Google Gemini API** (`gemini-1.5-flash`) và **OpenAI API**.
  - Tự động chuyển đổi sang **Offline Heuristic Meteorological Engine** (`fallback_forecaster.py`) nếu không có API key.
  - Sinh dự báo 6 giờ và 24 giờ tiếp theo kèm điểm số rủi ro (Risk Score 1-100).
- **Smart Operations Decision Engine (`src/ai_intelligence/decision_rules.py`)**:
  - **Hạ tầng đô thị (Municipal Drainage)**: Điều tiết trạm bơm cưỡng bức chống ngập úng khi mưa $> 40$ mm/h.
  - **Cảng biển & Logistics (Maritime Ports)**: Dừng cẩu trục bốc dỡ và cấm tàu xuất bến khi gió giật cấp $6+$ ($> 18$ m/s).
  - **Nông nghiệp chính xác (Smart Agriculture)**: Kích hoạt hệ thống phun sương chống sốc nhiệt hoặc che phủ chống sương muối.
  - **An toàn lao động (Construction & Health)**: Cảnh báo dừng thi công ngoài trời khi Heat Index $\ge 42^\circ\text{C}$.

---

## 3. Cấu Trúc Thư Mục Source Code (`src/`)

```
.
├── docker-compose.yml              # Cấu hình khởi chạy toàn bộ hệ thống bằng Docker
├── Dockerfile                      # Container build definition
├── requirements.txt                # Danh sách thư viện Python
├── .env.example                    # File mẫu cấu hình biến môi trường
├── config/
│   └── mosquitto.conf              # Cấu hình Mosquitto MQTT broker
├── data/
│   ├── stations.json               # Metadata trạm quan trắc IoT
│   └── historical_weather_sample.json # Dataset mẫu đa vùng khí hậu
├── src/
│   ├── config.py                   # Cấu hình nạp biến môi trường
│   ├── ingestion/
│   │   ├── mqtt_bridge.py          # MQTT Subscriber -> Kafka Producer
│   │   ├── coap_gateway.py         # CoAP Server (UDP) -> Kafka Producer
│   │   └── simulator.py            # Giả lập phát đa trạm IoT (Normal, Typhoon, Heatwave, Flood)
│   ├── stream_engine/
│   │   ├── watermark.py            # Quản lý Watermark & Late Data
│   │   ├── windowing.py            # Tumbling & Sliding Window Manager
│   │   ├── aggregators.py          # Tính Heat Index, Dew Point, Barometric Trend
│   │   └── processor.py            # Vòng lặp Stream Processing chính
│   ├── ai_intelligence/
│   │   ├── forecaster.py           # Client kết nối Gemini / OpenAI API
│   │   ├── decision_rules.py       # Bộ quy tắc ra quyết định vận hành
│   │   └── fallback_forecaster.py  # AI Heuristic Fallback khi chạy Offline
│   └── backend/
│       ├── main.py                 # FastAPI Web Server + WebSockets
│       └── static/
│           ├── index.html          # Dashboard giao diện Dark Glassmorphism
│           ├── style.css           # CSS Styling hiệu ứng kính mờ
│           └── app.js              # Logic Leaflet Map, Chart.js & WebSocket
└── README.md
```

---

## 4. Hướng Dẫn Cài Đặt & Chạy Hệ Thống

### Cách 1: Khởi chạy nhanh bằng Docker Compose (Khuyên dùng)

1. Sao chép file cấu hình môi trường:
   ```bash
   cp .env.example .env
   ```
   *(Tùy chọn: Nhập `GEMINI_API_KEY` hoặc `OPENAI_API_KEY` vào file `.env` nếu muốn sử dụng Cloud LLM).*

2. Khởi chạy toàn bộ hệ sinh thái:
   ```bash
   docker compose up --build -d
   ```

3. Truy cập các dịch vụ:
   - **Modern Web Dashboard**: [http://localhost:8000](http://localhost:8000)
   - **Redpanda Stream Console UI**: [http://localhost:8080](http://localhost:8080)
   - **FastAPI OpenAPI Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Cách 2: Chạy trực tiếp trên máy cục bộ (Local Python Development)

1. Cài đặt các gói phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```

2. Khởi động broker Redpanda & Mosquitto:
   ```bash
   docker compose up -d redpanda redpanda-console mosquitto
   ```

3. Chạy từng service trong các terminal riêng:
   ```bash
   # Terminal 1: Ingestion Bridges
   python -m src.ingestion.mqtt_bridge
   python -m src.ingestion.coap_gateway

   # Terminal 2: Stream Processing Engine
   python -m src.stream_engine.processor

   # Terminal 3: Web Dashboard Backend
   python -m src.backend.main

   # Terminal 4: IoT Weather Simulator
   python -m src.ingestion.simulator
   ```

---

## 5. Thử Nghiệm Các Kịch Bản Khí Tượng Cực Đoan

Trên giao diện Dashboard [http://localhost:8000](http://localhost:8000), bạn có thể chuyển đổi menu **Scenario**:
- **☀️ Bình thường (Normal Summer)**: Telemetry dao động nhẹ, rủi ro thấp.
- **🌀 Bão nhiệt đới (Typhoon Surge)**: Áp suất sụt mạnh $< 990$ hPa, gió giật $> 20$ m/s, mưa $> 50$ mm/h $\rightarrow$ Kích hoạt cảnh báo cấm biển và dừng cẩu cảng.
- **🔥 Nắng nóng cực đoan (Heatwave)**: Nhiệt độ $> 40^\circ\text{C}$, Heat Index $> 44^\circ\text{C}$, UV $> 11 \rightarrow$ Kích hoạt hệ thống tưới phun sương nông nghiệp và cảnh báo an toàn lao động.
- **🌧️ Mưa lũ ngập úng (Flash Flood)**: Mưa dồn dập $> 80$ mm/h $\rightarrow$ Kích hoạt trạm bơm thoát nước cưỡng bức.
