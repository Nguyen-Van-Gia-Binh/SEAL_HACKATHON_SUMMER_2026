# 🌦️ AI-Driven Smart Operations: Weather IoT Real-Time Streaming & AI Intelligence

Chào mừng các bạn thí sinh và kỹ sư tham khảo nền tảng kiến trúc mẫu cho đề tài **Xử lý dòng dữ liệu quan trắc thời tiết IoT (Real-Time Ingestion), Stream Processing Engine (Watermarking, Windowing, Aggregations) kết hợp Trí tuệ Nhân tạo AI đưa ra dự báo và chỉ đạo quyết định vận hành thông minh (Smart Operations Decision Intelligence)**.

---

## 🎯 Mục Tiêu Dự Án & Chuẩn Kiến Trúc

Dự án này là chuẩn tham chiếu (Reference Architecture) giải quyết 4 bài toán kỹ thuật trọng tâm:

1. **Đa giao thức thu thập IoT (Multi-Protocol Ingestion)**: Tiếp nhận đồng thời qua **MQTT (Mosquitto :1883)**, **CoAP (:5683 UDP)** và tập trung về **Kafka / Redpanda (:9092)**.
2. **Xử lý dòng dữ liệu chuẩn xác theo Event-Time (Stream Processing Engine)**:
   - Cơ chế **Bounded-Out-Of-Orderness Watermark** triệt tiêu lỗi trễ mạng và sắp xếp dữ liệu mất thứ tự.
   - Mô hình **Tumbling Window (1 phút)** & **Sliding Window (5 phút, trượt 1 phút)**.
   - Tổng hợp chỉ số nhiệt động học: **NOAA Heat Index**, **Dew Point**, **Độ dốc sụt áp suất ($\Delta P / \Delta t$)**.
3. **AI Weather Forecasting & Decision Intelligence**:
   - Tích hợp **Google Gemini API** / **OpenAI API** cùng cơ chế Fallback Heuristic tự động.
   - Tự động sinh quyết định: Trạm bơm chống ngập, cấm cảng biển khi gió bão cấp 6+, tưới phun sương nông nghiệp chính xác.
4. **Trực quan hóa & Container hóa**:
   - Giao diện **Modern Glassmorphic Dark Dashboard** thời gian thực (Leaflet Map, Chart.js, WebSockets).
   - 100% Dockerized qua **Docker Compose** chỉ với một câu lệnh (`docker compose up --build -d`).

---

## 🗺️ Bản Đồ Roadmap & Các Module Kỹ Thuật (Work Breakdown Structure)

| STT | Module / Task | Công Nghệ | Mô Tả & Tiêu Chí Đạt Chuẩn |
| :--- | :--- | :--- | :--- |
| **01** | **IoT Ingestion Layer** | MQTT, CoAP, Kafka | Tiếp nhận dữ liệu từ các trạm quan trắc, chuẩn hóa schema, chuyển tiếp vào topic `weather-raw`. |
| **02** | **Watermarking Engine** | Python / Event-Time | Bounded-Out-Of-Orderness Watermarking xử lý độ trễ $T_{delay}=5\text{s}$, phân luồng late data. |
| **03** | **Windowing & Aggregations** | Tumbling, Sliding | Tính toán trung bình, cực trị, xu hướng khí áp, chỉ số nhiệt độ ẩm NOAA Heat Index. |
| **04** | **AI Weather Forecaster** | Gemini API / Heuristic | Phân tích dòng dữ liệu cửa sổ, sinh dự báo 6h/24h và tính điểm rủi ro Risk Score (1-100). |
| **05** | **Smart Operations Engine** | Rule-based / Actionable | Sinh lệnh điều phối tự động: trạm bơm ngập lụt, cẩu trục cảng biển, tưới tiêu nông nghiệp. |
| **06** | **Real-Time Web Dashboard** | FastAPI, WebSockets, Leaflet | Trực quan hóa bản đồ vệ tinh, biểu đồ dòng dữ liệu, đồng hồ telemetry, bảng cảnh báo AI. |
| **07** | **Docker Orchestration** | Docker Compose | Tích hợp Redpanda, Redpanda Console (:8080), Mosquitto (:1883), Gateways, Engine, Dashboard (:8000). |

---

## ⚡ Hướng Dẫn Nhanh Dành Cho Thí Sinh (Quick Start)

### 1. Khởi chạy toàn bộ hệ thống bằng Docker:
```bash
# Clone repository và khởi chạy
docker compose up --build -d
```

### 2. Các cổng dịch vụ:
- 🌐 **Web Dashboard thời gian thực**: `http://localhost:8000`
- 📊 **Redpanda Stream Console UI**: `http://localhost:8080`
- 📡 **MQTT Broker**: `localhost:1883`
- 🛰️ **CoAP Server**: `localhost:5683/udp`
- 📖 **FastAPI Swagger API Documentation**: `http://localhost:8000/docs`

---

*Tham khảo các Task Cards chi tiết bên dưới để nắm rõ yêu cầu và code mẫu của từng thành phần!*
