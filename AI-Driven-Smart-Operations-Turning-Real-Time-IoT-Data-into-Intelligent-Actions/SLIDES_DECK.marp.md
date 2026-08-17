---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
  section {
    font-family: 'Inter', sans-serif;
    background-color: #ffffff;
    color: #0f172a;
    padding: 30px 48px;
    background-image: radial-gradient(at 0% 0%, rgba(21, 128, 61, 0.05) 0px, transparent 50%), radial-gradient(at 100% 100%, rgba(2, 132, 199, 0.05) 0px, transparent 50%);
  }
  h1 { font-family: 'Outfit', sans-serif; color: #15803d; font-size: 2.0rem; font-weight: 800; }
  h2 { font-family: 'Outfit', sans-serif; color: #0f172a; font-size: 1.45rem; font-weight: 700; border-bottom: 2px solid #15803d; padding-bottom: 4px; margin-bottom: 12px; }
  h3 { font-family: 'Outfit', sans-serif; color: #0369a1; font-size: 1.15rem; font-weight: 600; }
  p, li { font-size: 0.90rem; line-height: 1.45; color: #334155; }
  strong { color: #0f172a; font-weight: 700; }
  code { font-family: 'JetBrains Mono', monospace; background: #f1f5f9; color: #0284c7; padding: 2px 6px; border-radius: 4px; font-size: 0.85rem; border: 1px solid #e2e8f0; }
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
  .card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
  .card-green { border-left: 4px solid #15803d; background: #f0fdf4; }
  .card-blue { border-left: 4px solid #0284c7; background: #f0f9ff; }
  .card-orange { border-left: 4px solid #b45309; background: #fffbeb; }
  .card-red { border-left: 4px solid #dc2626; background: #fef2f2; }
  .visual-box { background: #f8fafc; border: 1px dashed #94a3b8; border-radius: 6px; padding: 8px 12px; font-size: 0.8rem; color: #475569; margin-top: 8px; }
  .badge { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 700; background: #dcfce7; color: #15803d; }
  footer { font-size: 0.72rem; color: #64748b; }
---

<!-- _class: lead -->
# AI-Driven Smart Operations
### From Real-Time IoT Data to Intelligent Decisions

**Speaker:** Nguyen Duc Tuan | Backend Lead & System Architect (FPT Software)  
**Event:** SEAL Hackathon Summer 2026 • August 13, 2026 (90 Minutes)  
**Platform:** Google Meet (`meet.google.com/zbr-tktz-bea`)

<div class="visual-box">
<b>Visual Design (Nền Trắng Chữ Đen):</b> Nền trắng tinh khiết (#FFFFFF), tiêu đề chữ đen xanh lá (#15803D), logo bánh răng kết hợp nút mạng IoT đối xứng trang trọng.
</div>

---

## Slide 02: Workshop Agenda (90-Minute Roadmap)

<div class="grid-2">
<div class="card card-blue">

### 1. Introduction & Context (10 Mins)
- From Passive Telemetry to Active AI Operations
- Multi-Layer Ground Truth Verification

### 2. Real-Time Streaming Pipeline (20 Mins)
- Ingestion: MQTT (:1883), CoAP (:5683), Kafka/Redpanda
- Stateful Stream Processing, Watermarking & Windowing
</div>

<div class="card card-green">

### 3. AI Decision Engine & Agents (25 Mins)
- 5-Step Pipeline: Extraction $\rightarrow$ Detection $\rightarrow$ RCA $\rightarrow$ Agent $\rightarrow$ Action
- Isolation Forest, Autoencoders, Causal Graphs, Guardrails

### 4. Reference Architecture & Strategy (15 Mins)
- Docker Blueprint & Live Anomaly Injection Pitching

### 5. Technical Q&A & Mentorship (20 Mins)
</div>
</div>

<div class="visual-box">
<b>Visual Design:</b> Lưới 2 cột nền trắng (#FFFFFF), viền thẻ xanh dương (#0284C7) và xanh lá (#15803D), thời lượng hiển thị huy hiệu vàng hổ phách (#B45309).
</div>

<!-- speaker: "Agenda 5 phần được thiết kế mạch lạc từ tư duy kiến trúc đến triển khai code thực tế cho cuộc thi." -->

---

## Slide 03: The Evolution of Operational Monitoring

<div class="grid-3">
<div class="card">

### Phase 1: Passive
**"What happened?"**
- Collect raw sensor data.
- Static visual line charts.
- High operator fatigue.
- **Zero proactive action**.
</div>

<div class="card card-orange">

### Phase 2: Reactive
**"Is it broken right now?"**
- Static rules: `IF Temp > 80C`.
- False Positive storms.
- Blind to multivariate trends.
- Slow incident escalation.
</div>

<div class="card card-green">

### Phase 3: Smart Ops
**"Why & How to fix?"**
- Multivariate anomaly score.
- Root Cause Analysis (RCA).
- Remaining Useful Life (RUL).
- **Closed-Loop Remediation**.
</div>
</div>

<div class="visual-box">
<b>Visual Design:</b> Bảng 3 cột tiến hóa (Xám nhạt -> Vàng cam nhạt -> Xanh lá nhạt #DCFCE7), chữ đen đậm, biểu tượng bánh đà tăng trưởng.
</div>

<!-- speaker: "Nếu sản phẩm của bạn chỉ hiển thị biểu đồ, bạn đang ở Phase 1. Để thắng giải, bạn cần đưa sản phẩm sang Phase 3: AI chủ động ra quyết định." -->

---

## Slide 04: Real-Time IoT Streaming Pipeline Architecture

```
[IoT Sensor Nodes] ──> (MQTT / CoAP) ──> [Mosquitto / EMQX Broker]
                                                   │ (Gắn Ingestion Timestamp)
                                                   ▼
                                      [Apache Kafka / Redpanda Buffer]
                                                   │
                                                   ▼
                                      [Stream Processing Engine]
                                        ├── Bounded Watermarking (Late Data)
                                        ├── Tumbling (1m) & Sliding (5m) Windows
                                        └── Feature Extraction & Aggregations
                                                   │
                                  ┌────────────────┴────────────────┐
                                  ▼                                 ▼
                     [Time-Series Storage]              [Real-Time AI Decision Engine]
                     (TimescaleDB Hypertables)          (Inference Latency < 5ms)
```

<div class="visual-box">
<b>Visual Design:</b> Sơ đồ khối 4 tầng nền trắng, viền hộp than chì (#334155), mũi tên luồng dữ liệu màu xanh dương (#0284C7), badge giao thức màu xanh lá (#15803D).
</div>

<!-- speaker: "Dữ liệu IoT có tính chất High-velocity. Một tầng Buffer phân tán như Redpanda là điều kiện tiên quyết để chống nghẽn hệ thống." -->

---

## Slide 05: Ingestion Technologies: MQTT, CoAP & Kafka/Redpanda

<div class="grid-3">
<div class="card card-green">

### MQTT (:1883)
- **Cơ chế:** Pub/Sub trên TCP, header 2B.
- **Ưu:** Tiết kiệm băng thông, Keepalive, LWT.
- **Nhược:** Chạy TCP tốn pin hơn UDP.
- **Lưu ý:** Dùng QoS 1 + `event_time`.
</div>

<div class="card card-blue">

### CoAP (:5683 UDP)
- **Cơ chế:** RESTful nhị phân trên UDP.
- **Ưu:** Header 4B, siêu tiết kiệm pin.
- **Nhược:** Dễ rớt gói trên mạng chập chờn.
- **Lưu ý:** Phù hợp node cảm biến môi trường.
</div>

<div class="card card-orange">

### Redpanda / Kafka (:9092)
- **Cơ chế:** Commit Log phân tán bất biến.
- **Ưu:** Redpanda C++ zero JVM, p99 thấp 10x.
- **Nhược:** Cần cấu hình key partition.
- **Lưu ý:** Dùng `station_id` làm Partition Key!
</div>
</div>

<div class="visual-box">
<b>Visual Design:</b> Lưới 3 cột nền trắng, thẻ bo góc có viền màu phân biệt (Xanh lá, Xanh dương, Vàng cam), bảng mini so sánh Ưu/Nhược điểm/Lưu ý.
</div>

<!-- speaker: "MQTT giúp cảm biến gửi tin siêu nhẹ, CoAP tối ưu pin, còn Redpanda C++ là cứu cánh giúp bạn chạy Kafka mượt mà trên laptop." -->

---

## Slide 06: Stream Processing: Watermarking & Time Windowing

<div class="grid-2">
<div class="card card-blue">

### Bounded Watermarking
- **Khái niệm:** Đo lường tiến độ Event-Time của luồng:
  $$\text{Watermark}(t) = \max_{i}(T_{\text{event}, i}) - T_{\text{allowed\_delay}}$$
- **Cơ chế:** Chấp nhận gói tin trễ trong $5\text{s}$. Dữ liệu đến sau khi chốt sổ đưa vào **Side-Output**.
- **Lợi ích:** Đảm bảo thứ tự thời gian không bị sai lệch.
</div>

<div class="card card-green">

### Windowing Models
- **Tumbling Window (Cố định 1 phút):**
  Phân đoạn không gối đầu $[T, T+60\text{s})$ để tính trung bình, cực trị chu kỳ.
- **Sliding Window (Trượt 5 phút, bước 1 phút):**
  Vùng đệm $[T-300\text{s}, T)$ gối đầu $80\%$ để tính đạo hàm tốc độ sụt áp $\Delta P / \Delta t$ báo bão.
</div>
</div>

<div class="visual-box">
<b>Visual Design:</b> Nền trắng (#FFFFFF), biểu đồ trục thời gian minh họa Watermark trễ và 2 sơ đồ cửa sổ Tumbling (nối đuôi) vs Sliding (gối đầu).
</div>

<!-- speaker: "Watermarking là vũ khí giải quyết triệt để bài toán mạng chập chờn, giúp cửa sổ phân tích thời gian thực không bao giờ bị tính sai." -->

---

## Slide 07: Storage Strategy: Redis Hot Cache vs TimescaleDB

<div class="grid-2">
<div class="card card-orange">

### Redis Streams (In-Memory Hot Cache)
- **Độ trễ:** Sub-millisecond ($< 1\text{ms}$).
- **Vai trò:** Cung cấp ngay Rolling Feature Vectors cho AI Model suy luận.
- **Nhược điểm:** Dung lượng giới hạn trong RAM.
- **Lưu ý:** Luôn cấu hình `XADD MAXLEN ~ 1000` chống tràn bộ nhớ.
</div>

<div class="card card-blue">

### TimescaleDB (Cold Time-Series Engine)
- **Cơ chế:** PostgreSQL Hypertables tự động phân vùng theo thời gian.
- **Ưu điểm:** Nén **Columnar Compression 90%+**, hỗ trợ $100\%$ SQL chuẩn.
- **Lưu ý:** Thiết lập `chunk_time_interval = INTERVAL '1 day'`.
</div>
</div>

<div class="visual-box">
<b>Visual Design:</b> Bảng so sánh phân tầng Hot (Vàng cam nhạt #FFFBEB) ở trên và Cold (Xanh biển nhạt #F0F9FF) ở dưới, chữ đen rõ nét.
</div>

<!-- speaker: "Mô hình Hot/Cold phân tách rõ ràng: Redis phục vụ AI suy luận dưới 5ms, còn TimescaleDB lưu trữ toàn bộ lịch sử phục vụ đào tạo lại mô hình." -->

---

## Slide 08: The 5-Step AI Decision Pipeline Overview

<div class="grid-3">
<div class="card card-blue">

### 1. Feature Extraction
Rolling Mean, Variance, FFT Harmonics, Cross-Sensor Correlation Ratios.
</div>

<div class="card card-green">

### 2. Anomaly Detection
Unsupervised Isolation Forest & Autoencoder Reconstruction Error ($\text{MSE} > \theta$).
</div>

<div class="card card-orange">

### 3. Root Cause Analysis
SHAP feature attribution & Causal Knowledge Graphs chỉ rõ linh kiện lỗi.
</div>
</div>

<br>

<div class="grid-2">
<div class="card card-purple">

### 4. AI Agent (LLM + Guardrails)
Lập luận logic có bọc **Deterministic Safety Guardrails** chống ảo giác.
</div>

<div class="card card-green">

### 5. Automated Execution
Closed-loop MQTT control dispatches & bảng điều hành khuyến nghị tự động.
</div>
</div>

<div class="visual-box">
<b>Visual Design:</b> Quy trình 5 khối hình chữ nhật liên hoàn dạng Chevron nối bằng mũi tên xanh lá (#15803D), số thứ tự in đậm, chữ đen than chì.
</div>

<!-- speaker: "Đây là linh hồn của buổi workshop. 5 bước nối tiếp chuyển hóa hoàn toàn dữ liệu cảm biến thô thành hành động tự động." -->

---

## Slide 09: Step 1 & 2: Feature Extraction & Anomaly Detection

<div class="grid-2">
<div class="card card-green">

### Isolation Forest (Scikit-Learn)
- **Cơ chế:** Cắt ngẫu nhiên thuộc tính; điểm lỗi bị cô lập nhanh hơn:
  $$s(x, n) = 2^{-\frac{E(h(x))}{c(n)}}$$
- **Ưu điểm:** Cực nhanh $\mathcal{O}(n \log n)$, chạy trên CPU, không cần nhãn.
- **Lưu ý:** Cấu hình `contamination=0.03`.
</div>

<div class="card card-blue">

### Autoencoder Neural Network (PyTorch)
- **Cơ chế:** Encoder nén Latent Space $\rightarrow$ Decoder giải nén.
- **Tiêu chuẩn lỗi:** Sai số tái tạo $\text{MSE} = \frac{1}{d}\sum(x_i - \hat{x}_i)^2 > \text{Threshold}$.
- **Lưu ý:** Export sang **ONNX Runtime** để suy luận $< 5\text{ms}$.
</div>
</div>

<div class="visual-box">
<b>Visual Design:</b> Chia đôi màn hình (Grid-2), bên trái là biểu đồ cây phân lập, bên phải là mô hình mạng Autoencoder thắt nút cổ chai (Hourglass).
</div>

<!-- speaker: "Isolation Forest rất nhẹ và sẵn sàng dùng ngay. Nếu dùng Deep Learning Autoencoder, hãy export ra ONNX Runtime để suy luận nhanh." -->

---

## Slide 10: Step 3: Root Cause Analysis (RCA) & Explainability

<div class="grid-2">
<div class="card card-orange">

### SHAP (Shapley Additive exPlanations)
- **Khái niệm:** Bóc tách mức độ đóng góp % của từng cảm biến:
  * Rung trục động cơ: **+78%**
  * Áp suất thủy lực: **+14%**
  * Nhiệt độ vỏ: **+8%**
- **Giá trị:** Giải thích tường minh lý do AI cảnh báo (Explainable AI - XAI).
</div>

<div class="card card-blue">

### Causal Knowledge Graphs
- **Khái niệm:** Đồ thị DAG mô tả quan hệ nhân quả vật lý:
  $$\text{Tắc Van A} \rightarrow \text{Tăng Áp B} \rightarrow \text{Quá Nhiệt C}$$
- **Giá trị:** Phân biệt chính xác **Nguyên nhân gốc rễ** vs **Triệu chứng lan truyền**.
</div>
</div>

<div class="visual-box">
<b>Visual Design:</b> Nền trắng (#FFFFFF), thẻ trái có biểu đồ thanh ngang SHAP Waterfall, thẻ phải có đồ thị nút mạng (Nodes) nối mũi tên đỏ chỉ vào nút gốc.
</div>

<!-- speaker: "Đừng chỉ báo lỗi chung chung! Hãy dùng SHAP để chỉ rõ cho Giám khảo thấy linh kiện nào đang gây ra 80% nguyên nhân sự cố." -->

---

## Slide 11: Step 4: AI Agents, LLMs & Safety Guardrails

<div class="grid-2">
<div class="card card-blue">

### LLM Agent Reasoning (Gemini / OpenAI)
- **Đầu vào:** Chỉ số thời gian thực + Kết quả RCA SHAP + Cẩm nang quy trình SOPs.
- **Nhiệm vụ:** Lập luận ngữ cảnh, sinh báo cáo tóm tắt và lên phương án hành động (Function Calling).
</div>

<div class="card card-red">

### Deterministic Safety Guardrails
- **Vấn đề:** LLM có thể bị ảo giác (Hallucination) phát lệnh nguy hiểm.
- **Chốt chặn:** Rule Engine kiểm duyệt bắt buộc:
  * *"Không tắt bơm làm mát chính nếu nhiệt độ lò $> 90^\circ\text{C}$."*
- **Quyền hạn:** **Phủ quyết (Override)** tuyệt đối mọi lệnh vi phạm!
</div>
</div>

<div class="visual-box">
<b>Visual Design:</b> Sơ đồ 3 lớp bảo vệ đồng tâm nền trắng, lớp lõi LLM (Xanh dương), lớp bao bọc Guardrails (Vàng viền đỏ #DC2626), lớp ngoài Actuators (Xanh lá).
</div>

<!-- speaker: "Mô hình ngôn ngữ lớn rất giỏi suy luận nhưng không thể để nó tự do gửi lệnh vật lý. Lớp Safety Guardrails là chốt chặn an toàn bắt buộc." -->

---

## Slide 12: Step 5: Automated Action Execution & Closed-Loop Control

<div class="grid-2">
<div class="card card-green">

### 🤖 Automated Closed-Loop Control
- **Độ trễ yêu cầu:** $< 1\text{s}$ cho sự cố khẩn cấp.
- **Hành động:**
  * Phát lệnh MQTT `iot/control/pumps` mở tối đa cống xả và trạm bơm tiêu úng khi mưa lớn $> 40\text{ mm/h}$.
  * Bật hệ thống tưới phun sương làm mát khi Heat Index $\ge 40^\circ\text{C}$.
</div>

<div class="card card-blue">

### 👨‍✈️ Human-in-the-Loop Escalation
- **Áp dụng:** Quyết định có chi phí cao hoặc tác động diện rộng.
- **Hành động:**
  * Báo cáo Markdown gửi về Telegram/Dashboard.
  * Tích hợp nút bấm Webhook 1-chạm **"Xác Nhận (Approve)"** hoặc **"Từ Chối (Override)"** cho kỹ sư.
</div>
</div>

<div class="visual-box">
<b>Visual Design:</b> Nền trắng (#FFFFFF), sơ đồ mũi tên vòng lặp khép kín tuần hoàn lớn màu xanh lá (#15803D) từ Cảm biến -> AI Agent -> Actuator -> Trạng thái an toàn.
</div>

<!-- speaker: "Vòng lặp hoàn tất: Dữ liệu cảm biến vào -> AI chẩn đoán -> Lệnh tự động kích hoạt thiết bị xử lý mà không cần con người can thiệp thủ công." -->

---

## Slide 13: End-to-End Hackathon Reference Architecture

```
[IoT Python Simulator (paho-mqtt)]
      │
      ├───> MQTT (:1883) ───> [Mosquitto Broker] ──┐
      │                                            ▼
      └───> CoAP (:5683/UDP) > [CoAP Gateway] ──> [Redpanda / Kafka :9092]
                                                   │
                                                   ▼
                                        [Stream Processing Engine]
                                          ├── Watermarking & Windowing
                                          ├── ONNX Model Inference (< 5ms)
                                          └── AI Agent & Rule Engine
                                                   │
                                                   ▼
                                        [FastAPI Web Dashboard :8000]
                                          ├── WebSocket Live Telemetry
                                          ├── Leaflet Map & Chart.js
                                          └── Automated Operational Cards
```

<div class="visual-box">
<b>Visual Design:</b> Sơ đồ Blueprint toàn diện nền trắng, các container đóng khung viền nét đứt (#94A3B8), cổng kết nối đóng khung vàng (#FEF3C7).
</div>

<!-- speaker: "Các bạn có thể chụp lại Slide này! Đây chính là Blueprint hoàn chỉnh có thể dựng ngay bằng Docker Compose trong 2 giờ." -->

---

## Slide 14: Recommended Hackathon Tech Stack Deep-Dive

<div class="grid-2">
<div class="card card-green">

### FastAPI & Paho-MQTT
- **FastAPI:** Async I/O cực nhanh, hỗ trợ WebSocket 2 chiều, tự sinh OpenAPI Swagger `/docs`.
- **Paho-MQTT:** Client siêu nhẹ kết nối simulator phát dữ liệu.
</div>

<div class="card card-blue">

### Leaflet.js & Chart.js
- **Leaflet.js:** Bản đồ địa lý trạm quan trắc không tốn API key.
- **Chart.js:** Biểu đồ dòng trượt 60fps mượt mà trên trình duyệt.
</div>
</div>

<br>

<div class="grid-2">
<div class="card card-orange">

### PyTorch $\rightarrow$ ONNX Runtime
- Huấn luyện dễ dàng trong PyTorch $\rightarrow$ Xuất sang file `.onnx` nhị phân để suy luận tốc độ C++ $< 5\text{ms}$.
</div>

<div class="card card-green">

### Docker Compose
- Đóng gói toàn bộ 8 services trong 1 file cấu hình, chạy 1-Click `docker compose up -d`.
</div>
</div>

<div class="visual-box">
<b>Visual Design:</b> Lưới 4 thẻ công nghệ (Grid-4) nền trắng, icon nhận diện thương hiệu, danh sách 3 tính năng cốt lõi và thanh đánh giá hiệu năng.
</div>

<!-- speaker: "Toàn bộ stack được lựa chọn theo tiêu chí: Nhẹ, dễ debug, không tốn RAM và khởi động trong vài giây." -->

---

## Slide 15: Secret Weapon: The "Live Anomaly Injection" Pitch

<div class="card card-red">

### Kịch Bản 5 Phút Thuyết Phục Ban Giám Khảo Tuyệt Đối:
1. **0:00 - 1:00 (Bình thường):** Mở Dashboard chứng minh hệ thống chạy ổn định, biểu đồ màu xanh an toàn.
2. **1:00 - 2:00 (Tiêm sự cố):** Bấm nút **"Tiêm Kịch Bản Bão Nhiệt Đới / Nắng Nóng Cực Đoan"** trên UI.
3. **2:00 - 3:00 (Phản hồi dòng):** Cửa sổ trượt 5 phút phát hiện sụt áp $\rightarrow$ Đồ thị chuyển cam $\rightarrow$ Cảnh báo kích hoạt.
4. **3:00 - 4:00 (AI chẩn đoán):** AI Agent phân tích nguyên nhân gốc rễ và đánh giá rủi ro trong $<100\text{ms}$.
5. **4:00 - 5:00 (Xử lý tự động):** Hệ thống tự động gửi lệnh MQTT mở bơm tiêu úng và cấm biển thành công!
</div>

<div class="visual-box">
<b>Visual Design:</b> Kịch bản phân cảnh 5 bước (5-Step Storyboard) nền trắng, nút bấm tiêm lỗi nổi bật màu đỏ rực (#DC2626), mũi tên tiến trình rõ ràng.
</div>

<!-- speaker: "Khi chấm thi, Giám khảo chỉ có 5 phút. Hãy cho Giám khảo thấy sự cố xảy ra và hệ thống AI tự động xử lý ngay trước mắt họ!" -->

---

## Slide 16: Common Hackathon Pitfalls to Avoid

<div class="grid-3">
<div class="card card-red">

### ❌ Bẫy Phần Cứng
- Dành $80\%$ thời gian hàn mạch ESP32/Arduino, mạng chập chờn không gửi được tin.
- **Khắc phục:** Dùng Python IoT Simulator giả lập đa trạm vật lý qua MQTT.
</div>

<div class="card card-orange">

### ❌ AI Quá Nặng
- Triển khai mô hình 70B tham số khiến API đơ $30\text{s}$ khi demo.
- **Khắc phục:** Dùng model nhẹ (Gemini-Flash) + Heuristic Fallback offline.
</div>

<div class="card card-green">

### ❌ Dashboard Tĩnh
- Chỉ vẽ biểu đồ mà không có vòng lặp tự động hóa hành động.
- **Khắc phục:** Xây dựng thẻ hành động điều hành tự động qua MQTT.
</div>
</div>

<div class="visual-box">
<b>Visual Design:</b> Bảng 3 cột so sánh lỗi sai (Đỏ nhạt #FEE2E2, Vàng cam nhạt #FEF3C7) và giải pháp chuẩn (Xanh lá nhạt #DCFCE7), chữ đen rõ ràng.
</div>

<!-- speaker: "Hãy nhớ: Cuộc thi đánh giá giải pháp AI-Driven Smart Operations, không phải thi hàn mạch phần cứng!" -->

---

## Slide 17: Live Technical Q&A & Mentorship

<div class="grid-2">
<div class="card card-blue">

### Chủ Đề Thảo Luận Mở
- Tối ưu hóa độ trễ Stream Processing & Watermarking.
- Lựa chọn mô hình Anomaly Detection & RCA SHAP.
- Triển khai Docker & Kết nối WebSockets Dashboard.
- Chiến lược bảo vệ đề tài trước Ban Giám Khảo.
</div>

<div class="card card-green">

### Hỗ Trợ Kỹ Thuật 1-1
- **Diễn giả:** Nguyễn Đức Tuấn
- **GitHub / Email:** `@Pen1112003`
- **Google Meet:** `meet.google.com/zbr-tktz-bea`
- Mở mic đặt câu hỏi trực tiếp cho đội thi của bạn!
</div>
</div>

<div class="visual-box">
<b>Visual Design:</b> Nền trắng (#FFFFFF), chữ đen than chì, biểu tượng micro và bong bóng trò chuyện (Chat Bubbles), khung thông tin liên hệ trang trọng.
</div>

<!-- speaker: "Bây giờ là thời gian cho các bạn! Hãy đặt bất kỳ câu hỏi nào về khó khăn kỹ thuật mà đội thi của bạn đang gặp phải." -->

---

<!-- _class: lead -->
# Build Smart, Scale Fast & Drive Intelligent Action!

### Cảm ơn các đội thi SEAL Hackathon Summer 2026!
**Chúc tất cả các đội thi xây dựng được những sản phẩm Vận Hành Thông Minh xuất sắc!**

🔗 **Repository Mã Nguồn Mẫu:**  
`https://github.com/Pen1112003/AI-Driven-Smart-Operations-Turning-Real-Time-IoT-Data-into-Intelligent-Actions`

<div class="visual-box">
<b>Visual Design:</b> Slide bế mạc nền trắng trang nhã, thông điệp truyền cảm hứng in đậm màu xanh lá (#15803D), mã link repository nổi bật ở trung tâm.
</div>
