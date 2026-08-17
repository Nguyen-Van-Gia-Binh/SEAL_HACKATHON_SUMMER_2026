# WORKSHOP PRESENTATION SCRIPT & SLIDE DECK (BẢN TOÀN DIỆN CHUYÊN SÂU)
## AI-Driven Smart Operations: From Real-Time IoT Data to Intelligent Decisions

- **Chủ đề (Topic):** AI-Driven Smart Operations: From Real-Time IoT Data to Intelligent Decisions
- **Sự kiện (Event):** SEAL Hackathon Summer 2026
- **Thời gian (Duration):** 20:00 - 21:30, August 13, 2026 (90 Phút)
- **Hình thức (Platform):** Trực tuyến qua Google Meet (Link: `https://meet.google.com/zbr-tktz-bea`)
- **Diễn giả (Sole Speaker):** Nguyễn Đức Tuấn (Backend Lead / System Architect, FPT Software & Cựu Google Student Ambassador)
- **Kho lưu trữ mã nguồn mẫu:** `https://github.com/Pen1112003/AI-Driven-Smart-Operations-Turning-Real-Time-IoT-Data-into-Intelligent-Actions`

---

# MỤC LỤC TỔNG QUAN

1. **PHẦN I: TỔNG QUAN WORKSHOP & PHÂN BỔ THỜI LƯỢNG (90 MINUTES TIMETABLE)**
2. **PHẦN II: NGUYÊN LÝ CỐT LÕI - PHƯƠNG PHÁP XÁC ĐỊNH ĐÚNG/SAI TRONG VẬN HÀNH THÔNG MINH (GROUND TRUTH & ANOMALY BOUNDARIES)**
3. **PHẦN III: KỊCH BẢN THUYẾT TRÌNH CHI TIẾT THEO TỪNG PHẦN (PRESENTATION SCRIPT & TECHNICAL DEEP-DIVE)**
   - Phần 1: Khai mạc, Giới thiệu & Bối cảnh Smart Operations (10 phút)
   - Phần 2: Kiến trúc Thu thập & Xử lý Luồng Dữ liệu IoT Thời gian thực (20 phút)
   - Phần 3: Trí tuệ Nhân tạo & AI Agents trong Vận hành Tự động (25 phút)
   - Phần 4: Kiến trúc Tham chiếu (Reference Architecture) & Chiến lược Hackathon (15 phút)
   - Phần 5: Q&A Kỹ thuật & Giải đáp Thắc mắc (20 phút)
4. **PHẦN IV: BỘ 18 SLIDE THUYẾT TRÌNH CHUẨN MỰC (CÓ ĐỊNH NGHĨA, ƯU/NHƯỢC ĐIỂM, LƯU Ý, VISUAL DESIGN NỀN TRẮNG CHỮ ĐEN & SPEAKER NOTES)**
5. **PHẦN V: BẢNG TRA CỨU CÔNG NGHỆ CHUYÊN SÂU & MA TRẬN SO SÁNH (COMPREHENSIVE TECH STACK MATRIX)**
6. **PHẦN VI: CHECKLIST VẬN HÀNH & BẢNG TIÊU CHÍ CHẤM ĐIỂM HACKATHON**

---

# PHẦN I: TỔNG QUAN WORKSHOP & PHÂN BỔ THỜI LƯỢNG (90 MINUTES)

| Mốc thời gian | Thời lượng | Phân đoạn | Nội dung trọng tâm | Diễn giả |
| :--- | :---: | :--- | :--- | :---: |
| **20:00 - 20:10** | 10 phút | **Phần 1** | **Khai mạc, Giới thiệu & Bối cảnh Smart Operations**<br>• Chào mừng thí sinh SEAL Hackathon Summer 2026.<br>• Giới thiệu diễn giả & lộ trình 90 phút.<br>• Sự chuyển dịch từ giám sát thụ động sang vận hành thông minh bằng AI. | Nguyễn Đức Tuấn |
| **20:10 - 20:30** | 20 phút | **Phần 2** | **Kiến trúc Thu thập & Xử lý Luồng Dữ liệu IoT Thời gian thực**<br>• Giao thức thu thập: MQTT, CoAP, Kafka/Redpanda.<br>• Stream Processing Engine: Watermarking, Windowing (Tumbling/Sliding), Aggregation.<br>• Xử lý dữ liệu trễ mạng (Late Data) và chống rò rỉ dữ liệu. | Nguyễn Đức Tuấn |
| **20:30 - 20:55** | 25 phút | **Phần 3** | **Trí tuệ Nhân tạo & AI Agents trong Vận hành Tự động**<br>• Chuỗi 5 bước: Feature Extraction $\rightarrow$ Anomaly Detection $\rightarrow$ RCA $\rightarrow$ AI Agent $\rightarrow$ Action.<br>• Giải thuật: Isolation Forest, Autoencoder, Causal Graph, SHAP.<br>• Điều phối hành động tự động có kiểm soát an toàn (Safety Guardrails). | Nguyễn Đức Tuấn |
| **20:55 - 21:10** | 15 phút | **Phần 4** | **Kiến trúc Tham chiếu (Reference Architecture) & Tối ưu Hackathon**<br>• Blueprint chuẩn triển khai trong 2 giờ với Docker Compose.<br>• Tech stack tối ưu: FastAPI, Paho-MQTT, TimescaleDB, Grafana.<br>• Kỹ thuật "Live Anomaly Injection" tạo điểm nhấn trước Giám khảo. | Nguyễn Đức Tuấn |
| **21:10 - 21:30** | 20 phút | **Phần 5** | **Phiên Q&A & Giải đáp Trực tiếp cho Đội thi**<br>• Trực tiếp tháo gỡ vướng mắc kiến trúc, streaming, AI models.<br>• Cảnh báo các bẫy phần cứng phổ biến và hướng dẫn bảo vệ đề tài. | Nguyễn Đức Tuấn |

---

# PHẦN II: NGUYÊN LÝ CỐT LÕI - PHƯƠNG PHÁP XÁC ĐỊNH ĐÚNG/SAI (GROUND TRUTH)

> **Câu hỏi lớn của thí sinh:** *"Làm sao trong một hệ sinh thái IoT với hàng ngàn cảm biến gửi dữ liệu liên tục, hệ thống biết được đâu là dữ liệu ĐÚNG (Bình thường), đâu là SAI (Bất thường/Lỗi cảm biến/Sự cố hệ thống) mà không gây ra báo động giả?"*

Để xác định **ĐÚNG / SAI** trong Smart Operations, hệ thống áp dụng **Ma trận Kiểm định Đa tầng (Multi-Layer Verification Matrix)** gồm 4 trục tiêu chuẩn:

```
[Raw IoT Sensor Telemetry]
           │
           ▼
[Tầng 1: Kiểm Tra Giới Hạn Vật Lý (Physical Range Bounds)]
  ├── Ngưỡng hợp lý: 0 <= Humidity <= 100%, 800 <= Pressure <= 1080 hPa
  └── Vi phạm -> Loại trừ ngay, gắn cờ SENSOR_OUT_OF_BOUNDS
           │
           ▼
[Tầng 2: Tương Quan Đa Biến Vật Lý (Multivariate Cross-Correlation)]
  ├── Định luật nhiệt động lực học: Sụt áp nhanh -> Tốc độ gió tăng -> Mưa tăng
  └── Chỉ 1 cảm biến nhảy vọt đơn độc -> Gắn cờ SENSOR_NOISE (Không dừng máy)
           │
           ▼
[Tầng 3: Độ Lệch Mô Hình Học Máy (ML Deviations & Reconstruction Error)]
  ├── Isolation Forest: Anomaly Score s(x, n) > 0.65
  └── Autoencoder: Sai số tái tạo MSE = ||x - x_hat||^2 > Threshold
           │
           ▼
[Tầng 4: Lớp Kiểm Soát An Toàn AI & Causal Graph (Safety Guardrails)]
  ├── Đối chiếu Causal Graph: Xác định linh kiện gốc rễ (Root Cause)
  └── Safety Policy: Ngăn chặn LLM ra lệnh nguy hiểm vượt giới hạn kỹ thuật
           │
           ▼
     [Phân Định Rõ Ràng]
  ├── BÌNH THƯỜNG (Normal): Vận hành thường quy
  ├── LỖI CẢM BIẾN (Sensor Fault): Cách ly cảm biến, tự nội suy dữ liệu thay thế
  └── SỰ CỐ HỆ THỐNG THỰC TẾ (True Anomaly): Kích hoạt AI Agent & Điều hành tự động
```

---

# PHẦN III: KỊCH BẢN THUYẾT TRÌNH CHI TIẾT (PRESENTATION SCRIPT)

*(Toàn bộ diễn giải mở đầu, phân tích bối cảnh, kiến trúc luồng dữ liệu 4 tầng, chuỗi AI 5 bước, và chiến lược demo live anomaly injection đã được tích hợp đầy đủ và đồng bộ hoàn hảo với 18 slide dưới đây).*

---

# PHẦN IV: BỘ 18 SLIDE THUYẾT TRÌNH CHUẨN MỰC (ĐẦY ĐỦ CHI TIẾT)

---

### SLIDE 01: TITLE SLIDE
- **Slide Title:** AI-Driven Smart Operations: From Real-Time IoT Data to Intelligent Decisions
- **Subtitle:** Engineering Scalable Event-Driven Architectures, Stream Analytics, and Agentic Remediation
- **Metadata:** Speaker: Nguyen Duc Tuan | Backend Lead & System Architect (FPT Software) • SEAL Hackathon Summer 2026 • 90 Minutes
- **Key Concepts Covered:**
  - Chuyển dịch từ Giám sát thụ động (Passive Telemetry) sang Vận hành thông minh tự hành (AI-Driven Smart Operations).
  - Tích hợp toàn diện: IoT Ingestion $\rightarrow$ Event Streaming $\rightarrow$ Time-Series Analytics $\rightarrow$ Machine Learning $\rightarrow$ AI Agents.
- **Visual Design (Nền Trắng Chữ Đen):**
  - *Màu nền:* Trắng tinh khiết (`#FFFFFF`).
  - *Tiêu đề chính:* Chữ đen đậm (`#0F172A`, Font Outfit/Inter, size 32pt, Bold).
  - *Subtitle & Metadata:* Xanh lá đậm Bộ Nông nghiệp (`#15803D`) và Xanh dương công nghệ (`#0284C7`).
  - *Bố cục:* Căn giữa trang trọng; logo biểu tượng bánh răng kết hợp nút mạng IoT và nơ-ron AI đối xứng; khung viền mỏng (`#E2E8F0`) bo tròn tinh tế.
- **Speaker Notes (Tiếng Việt):**
  > *"Nhiệt liệt chào mừng các đội thi, các kỹ sư và các bạn sinh viên tài năng của SEAL Hackathon Summer 2026! Tôi là Nguyễn Đức Tuấn. Tối nay, chúng ta sẽ cùng giải quyết bài toán cốt lõi: Làm thế nào để chuyển hóa luồng dữ liệu cảm biến thời gian thực thành những quyết định điều hành thông minh tự động mang lại giá trị cao nhất cho bài thi của các bạn!"*

---

### SLIDE 02: WORKSHOP AGENDA (90-MINUTE ROADMAP)
- **Slide Title:** Workshop Agenda: 90-Minute Technical Roadmap
- **Slide Content (English):**
  1. **Overview & Evolution of Smart Operations (10 Mins):** The 3 phases of operational telemetry and ground truth definition.
  2. **Real-Time IoT Streaming Pipeline Architecture (20 Mins):** Ingestion protocols (MQTT/CoAP), distributed buffers (Kafka/Redpanda), and stream windowing with watermarks.
  3. **AI Decision Engine & Agentic Workflows (25 Mins):** The 5-step pipeline: Feature extraction, Isolation Forest/Autoencoders, RCA with SHAP/Causal Graphs, and LLM Guardrails.
  4. **End-to-End Reference Architecture & Hackathon Strategy (15 Mins):** 1-Click Docker Compose blueprint and the winning "Live Anomaly Injection" demo technique.
  5. **Live Technical Q&A & Mentor Guidance (20 Mins):** One-on-one architectural reviews and debugging pitfalls.
- **Visual Design (Nền Trắng Chữ Đen):**
  - *Màu nền:* Trắng (`#FFFFFF`), chữ đen (`#0F172A`).
  - *Bố cục:* Timeline ngang hoặc lưới 5 thẻ (Grid 5 cards). Mỗi thẻ có số thứ tự tròn màu xanh lá (`#15803D`), tiêu đề in đậm, mốc thời gian nổi bật với huy hiệu vàng hổ phách (`#B45309`).
- **Speaker Notes (Tiếng Việt):**
  > *"Lộ trình 90 phút tối nay được thiết kế bám sát thực tế phát triển dự án: Đi từ tư duy giao thức, kiến trúc streaming chống nghẽn, đến các thuật toán AI chẩn đoán và chiến lược pitching trực tiếp trước Ban Giám Khảo."*

---

### SLIDE 03: THE EVOLUTION OF OPERATIONAL MONITORING
- **Slide Title:** The Evolution of Operational Monitoring: From Passive to Autonomous
- **Detailed Concept & Comparison:**
  - **Phase 1: Passive Monitoring ("What happened?"):**
    - *Định nghĩa:* Thu thập dữ liệu cảm biến thô và vẽ biểu đồ đường trên Dashboard.
    - *Ưu điểm:* Đơn giản, dễ triển khai, lưu lại dữ liệu lịch sử.
    - *Nhược điểm:* Hoàn toàn thụ động, phụ thuộc 100% vào con người quan sát 24/7; gây mệt mỏi thị giác (Operator Fatigue); phát hiện sự cố quá muộn khi thiệt hại đã xảy ra.
  - **Phase 2: Reactive Threshold Alerting ("Is it broken right now?"):**
    - *Định nghĩa:* Đặt các quy tắc tĩnh cố định (ví dụ: `IF Nhiệt_độ > 80°C THEN Gửi_Email`).
    - *Ưu điểm:* Tự động hóa cảnh báo cơ bản, phản hồi nhanh hơn con người.
    - *Nhược điểm:* Gây ra "Bão cảnh báo giả" (Alert Storms / Alert Fatigue); không phát hiện được sự suy thoái từ từ (Drift) hoặc sự cố đa biến phi tuyến tính.
  - **Phase 3: AI-Driven Smart Operations ("Why did it happen & What action to take?"):**
    - *Định nghĩa:* Kết hợp Real-time Data Streaming + Machine Learning Anomaly Detection + Root Cause Analysis + AI Agent closed-loop control.
    - *Ưu điểm:* Dự báo trước hư hỏng (Predictive Maintenance); tự động thực thi hành động khắc phục trong vài giây; phân biệt lỗi cảm biến và lỗi hệ thống.
    - *Lưu ý thực chiến:* Cần xây dựng lớp Safety Guardrails để ngăn AI ra quyết định sai.
- **Visual Design (Nền Trắng Chữ Đen):**
  - *Màu nền:* Trắng (`#FFFFFF`), bảng so sánh 3 cột (Grid-3 Columns).
  - *Cột 1 (Phase 1):* Nền xám nhạt (`#F1F5F9`), chữ đen, viền xám (`#CBD5E1`).
  - *Cột 2 (Phase 2):* Nền vàng cam nhạt (`#FEF3C7`), chữ đen, viền cam (`#F59E0B`).
  - *Cột 3 (Phase 3):* Nền xanh lá nhạt (`#DCFCE7`), chữ đen, viền xanh lá đậm (`#15803D`) nổi bật với icon AI Agent.
- **Speaker Notes (Tiếng Việt):**
  > *"Nếu sản phẩm Hackathon của các bạn chỉ dừng lại ở việc hiển thị biểu đồ, các bạn đang ở Phase 1. Để đạt giải cao, bắt buộc phải đưa giải pháp sang Phase 3: Hệ thống không chỉ biết 'có lỗi' mà còn biết 'tại sao lỗi' và 'tự động xử lý thế nào'!"*

---

### SLIDE 04: REAL-TIME IOT DATA PIPELINE ARCHITECTURE
- **Slide Title:** Real-Time IoT Streaming Pipeline Architecture
- **Layer-by-Layer Technical Breakdown:**
  - **Layer 1: Edge & Ingestion:** Sensor Nodes $\rightarrow$ MQTT Broker (`:1883`) & CoAP Gateway (`:5683 UDP`).
  - **Layer 2: Distributed Buffer:** Redpanda / Apache Kafka (`:9092`) - Message bus phân tán hấp thụ xung đột lưu lượng (Burst Spikes), bảo đảm Zero Data Loss.
  - **Layer 3: Stream Processing Engine:** Python Async Windowing / Apache Flink - Quản lý Bounded Watermarking, Tumbling (1m) & Sliding (5m) Windows, tính toán Heat Index, Dew Point, $\Delta P / \Delta t$.
  - **Layer 4: Dual Storage & AI Engine:**
    - *Hot Path:* In-Memory Cache (Redis Streams) phục vụ AI inference tức thì $< 5\text{ms}$.
    - *Cold Path:* TimescaleDB Hypertables nén $90\%$ dung lượng lưu trữ lịch sử dài hạn.
- **Visual Design (Nền Trắng Chữ Đen):**
  - *Màu nền:* Trắng (`#FFFFFF`), chữ đen than chì (`#0F172A`).
  - *Sơ đồ kiến trúc:* Sơ đồ khối 4 tầng từ trên xuống dưới (Top-to-Bottom Flowchart) với các đường viền rõ nét (`#334155`), mũi tên chuyển dữ liệu màu xanh dương (`#0284C7`), các protocol badge màu xanh lá (`#15803D`).
- **Speaker Notes (Tiếng Việt):**
  > *"Dữ liệu IoT có tính chất High-velocity và Burst. Một tầng Buffer phân tán như Redpanda là điều kiện tiên quyết giúp tách biệt hoàn toàn tốc độ nhận tin với tốc độ xử lý AI, chống sập hệ thống khi có bão dữ liệu."*

---

### SLIDE 05: INGESTION PROTOCOLS & BROKERS (MQTT, COAP, KAFKA/REDPANDA)
- **Slide Title:** Ingestion Technologies: MQTT, CoAP, and Event Streaming
- **Deep-Dive Concepts, Pros, Cons & Gotchas:**
  - **1. MQTT (Message Queuing Telemetry Transport - Eclipse Mosquitto / EMQX):**
    - *Định nghĩa:* Giao thức Pub/Sub chạy trên TCP, overhead header siêu nhẹ chỉ $2$ bytes, hỗ trợ QoS 0 (At most once), QoS 1 (At least once), QoS 2 (Exactly once).
    - *Ưu điểm:* Cực kỳ tiết kiệm băng thông, kết nối liên tục (Keepalive), hỗ trợ Last Will and Testament (LWT) để phát hiện node cảm biến mất kết nối.
    - *Nhược điểm:* Chạy trên TCP nên tốn pin hơn UDP đối với các thiết bị siêu nhỏ; QoS 2 có độ trễ cao do quá trình bắt tay 4 bước (Handshake).
    - *Lưu ý (Gotchas):* Trong Hackathon, nên dùng **QoS 1** kết hợp gắn `event_time` để đảm bảo không mất tin mà không bị chậm mạng. Không đặt tên topic quá sâu (tránh `a/b/c/d/e/f/g`).
  - **2. CoAP (Constrained Application Protocol - Port 5683 UDP):**
    - *Định nghĩa:* Giao thức nhị phân chuyển giao trạng thái RESTful (GET/POST/PUT) chạy trên UDP, tối ưu cho vi điều khiển 8-bit/16-bit và mạng LPWAN/NB-IoT.
    - *Ưu điểm:* Tiết kiệm pin tối đa, gói tin tiêu đề chỉ $4$ bytes, không mất công duy trì kết nối TCP.
    - *Nhược điểm:* Chạy trên UDP nên dễ bị mất gói (Packet Loss) trên mạng kém ổn định; cần tầng ứng dụng tự xử lý ACK nếu cần tin cậy.
  - **3. Apache Kafka vs Redpanda (Port 9092):**
    - *Định nghĩa:* Hệ thống hàng chờ phân tán dạng Commit Log bất biến, tổ chức theo Topic và Partition.
    - *So sánh Kafka vs Redpanda:*
      - *Apache Kafka:* Chuẩn công nghiệp số 1, chịu tải hàng triệu msg/s. Nhược điểm: Phụ thuộc máy ảo Java (JVM), ngốn RAM (tối thiểu 2GB-4GB), cấu hình phức tạp.
      - *Redpanda:* Viết hoàn toàn bằng **C++**, tương thích 100% Kafka API, không cần JVM, độ trễ p99 thấp hơn Kafka 10 lần, khởi động trong 2 giây, ngốn chưa tới 200MB RAM.
    - *Lưu ý (Gotchas):* Bắt buộc dùng `station_id` làm **Partition Key** để đảm bảo dữ liệu của cùng 1 trạm luôn được ghi vào cùng 1 Partition theo đúng thứ tự thời gian! Cấu hình `retention.ms=86400000` (1 ngày) để tránh đầy ổ cứng trong khi chạy test.
- **Visual Design (Nền Trắng Chữ Đen):**
  - *Màu nền:* Trắng (`#FFFFFF`), chữ đen (`#0F172A`).
  - *Bố cục:* 3 thẻ so sánh (Grid-3). Thẻ 1: MQTT (Icon Tower xanh lá), Thẻ 2: CoAP (Icon Microchip xanh dương), Thẻ 3: Redpanda/Kafka (Icon Network đỏ gạch). Dưới mỗi thẻ có bảng mini 2 hàng (Xanh: Ưu điểm | Đỏ: Lưu ý Gotchas).
- **Speaker Notes (Tiếng Việt):**
  > *"MQTT giúp cảm biến gửi tin siêu nhẹ, CoAP tối ưu cho thiết bị chạy pin, còn Redpanda viết bằng C++ là 'cứu cánh' giúp các bạn chạy trơn tru message bus phân tán trên máy laptop mà không lo bị tràn RAM máy ảo Java!"*

---

### SLIDE 06: STREAM PROCESSING, WATERMARKING & WINDOWING
- **Slide Title:** Stream Processing: Watermarking & Time-Windowing Analytics
- **Deep-Dive Concepts, Formulas & Mechanics:**
  - **1. Event-Time vs Processing-Time:**
    - *Event-Time ($T_{\text{event}}$):* Thời điểm cảm biến vật lý ghi nhận dữ liệu tại biên.
    - *Processing-Time ($T_{\text{proc}}$):* Thời điểm server nhận và xử lý gói tin.
    - *Nguyên tắc vàng:* **Luôn luôn xử lý phân tích theo Event-Time** để bảo đảm tính chính xác khi có độ trễ mạng!
  - **2. Bounded-Out-Of-Orderness Watermarking:**
    - *Công thức:*
      $$\text{Watermark}(t) = \max_{i}(T_{\text{event}, i}) - T_{\text{allowed\_delay}}$$
    - *Cơ chế:* Hệ thống chấp nhận chờ dữ liệu đến trễ trong khoảng $T_{\text{allowed\_delay}}$ (ví dụ $5\text{s}$). Khi Watermark vượt qua mốc kết thúc của cửa sổ ($W(t) \ge T_{\text{end}}$), cửa sổ được kích hoạt đóng và xuất kết quả tính toán.
    - *Xử lý Late Data cực trễ:* Dữ liệu đến sau khi cửa sổ đã đóng sẽ được chuyển hướng vào **Side-Output / Dead-Letter Queue** để không làm sai lệch kết quả đã chốt.
  - **3. Mô hình Cửa Sổ (Windowing Models):**
    - *Tumbling Window (Cửa sổ cố định 1 phút):* Cửa sổ thời gian $[T, T+60\text{s})$ không chồng lấn, dùng để tính Min, Max, Mean nhiệt độ, lượng mưa tích lũy.
    - *Sliding Window (Cửa sổ trượt 5 phút, bước trượt 1 phút):* Cửa sổ $[T-300\text{s}, T)$ gối đầu liên tục, dùng để tính đạo hàm tốc độ biến thiên khí áp ($\Delta P / \Delta t$) và độ lệch chuẩn rung động.
- **Visual Design (Nền Trắng Chữ Đen):**
  - *Màu nền:* Trắng (`#FFFFFF`), chữ đen (`#0F172A`).
  - *Bố cục:* 2 phần. Phần trên là biểu đồ dòng thời gian (Timeline Graph) minh họa Watermark đẩy dần theo trục thời gian; Phần dưới là 2 hình chữ nhật minh họa Tumbling Window (các khối hộp nối đuôi nhau) và Sliding Window (các khối hộp gối chồng lên nhau $80\%$).
- **Speaker Notes (Tiếng Việt):**
  > *"Trong môi trường IoT thực tế, mạng 4G/Wifi luôn chập chờn khiến gói tin đến lộn xộn. Thuật toán Bounded Watermarking là chìa khóa vàng giúp hệ thống của bạn kiên nhẫn đợi gói tin trễ mà không làm sụp đổ tính đúng đắn của chuỗi thời gian."*

---

### SLIDE 07: TIME-SERIES STORAGE: REDIS HOT CACHE VS TIMESCALEDB
- **Slide Title:** Storage Hierarchy: In-Memory Hot Cache vs Cold Time-Series Hypertables
- **Deep-Dive Concepts, Pros, Cons & Gotchas:**
  - **1. Redis Streams & In-Memory Hot Cache:**
    - *Khái niệm:* Cấu trúc dữ liệu Log trong bộ nhớ RAM, độ trễ truy xuất cực thấp ($< 1\text{ms}$).
    - *Ưu điểm:* Cung cấp ngay lập tức Rolling Feature Vectors cho mô hình AI suy luận thời gian thực; hỗ trợ Consumer Groups (`XREADGROUP`).
    - *Nhược điểm:* Dữ liệu lưu trong RAM nên chi phí đắt đỏ; nguy cơ mất dữ liệu nếu RAM bị đầy (Memory Eviction Policy `OOM`).
    - *Lưu ý (Gotchas):* Luôn dùng lệnh `XADD` với tham số giới hạn độ dài `MAXLEN ~ 1000` để giới hạn bộ nhớ đệm.
  - **2. TimescaleDB (PostgreSQL Extension for Time-Series):**
    - *Khái niệm:* Mở rộng PostgreSQL thành CSDL chuỗi thời gian thông qua cơ chế **Hypertables** - tự động chia nhỏ bảng dữ liệu thành các phân vùng thời gian (Chunks) ẩn bên dưới.
    - *Ưu điểm:* Hỗ trợ $100\%$ cú pháp SQL chuẩn (JOIN, GROUP BY, Window functions); tính năng **Columnar Compression** nén dữ liệu cũ giảm hơn $90\%$ dung lượng đĩa; hỗ trợ Continuous Aggregates tự động tính sẵn trung bình theo giờ/ngày.
    - *Nhược điểm:* Tốn tài nguyên CPU/RAM hơn các CSDL NoSQL thuần khi lượng ghi đồng thời vượt hàng triệu dòng/giây.
    - *Lưu ý (Gotchas):* Thiết lập `chunk_time_interval = INTERVAL '1 day'` để tối ưu hiệu năng ghi và nén.
  - **3. InfluxDB (Giải pháp thay thế):**
    - *Đặc điểm:* CSDL Time-Series chuyên dụng với TSM Engine, ghi cực nhanh nhưng bị lỗi thắt cổ chai khi độ đa dạng nhãn quá cao (High Cardinality Problem) và đòi hỏi học ngôn ngữ Flux mới.
- **Visual Design (Nền Trắng Chữ Đen):**
  - *Màu nền:* Trắng (`#FFFFFF`), chữ đen (`#0F172A`).
  - *Bố cục:* Bảng phân tầng 2 tầng (Hot Layer ở trên màu cam nhạt `#FFFBEB`, Cold Layer ở dưới màu xanh biển nhạt `#F0F9FF`), đường ranh giới phân tách rõ ràng; cột so sánh chi tiết Latency, Retention, Compression và Use Case.
- **Speaker Notes (Tiếng Việt):**
  > *"Đừng bắt AI truy vấn ngược về CSDL đĩa cứng để lấy dữ liệu tính toán! Hãy dùng Redis làm bộ đệm RAM để AI suy luận dưới 5 mili-giây, và đẩy bản ghi lịch sử vào TimescaleDB nén 90% để phục vụ phân tích dài hạn."*

---

### SLIDE 08: THE 5-STEP AI DECISION PIPELINE OVERVIEW
- **Slide Title:** The 5-Step AI Decision Pipeline: From Raw Signal to Autonomous Action
- **The Closed-Loop Sequence:**
  1. **Bước 1: Feature Extraction (Trích xuất đặc trưng):** Chuyển đổi dữ liệu chuỗi thô thành các vector thống kê ($\mu, \sigma$, Skewness, Kurtosis) và phổ tần số FFT.
  2. **Bước 2: Real-Time Anomaly Detection (Phát hiện bất thường):** Isolation Forest & Autoencoder tính điểm bất thường ($s > \theta$) hoặc sai số tái tạo ($\text{MSE} > \epsilon$).
  3. **Bước 3: Root Cause Analysis - RCA (Chẩn đoán nguyên nhân gốc rễ):** Sử dụng SHAP values và Causal Knowledge Graph để chỉ mặt đặt tên linh kiện đang bị hư hỏng.
  4. **Bước 4: AI Agent & Safety Guardrails (Lập luận & Kiểm soát an toàn):** LLM tổng hợp ngữ cảnh chẩn đoán, đối chiếu quy trình SOP và chạy qua bộ kiểm duyệt an toàn tiền định.
  5. **Bước 5: Automated Action Execution (Thực thi hành động tự động):** Phát lệnh điều khiển khép kín qua MQTT hoặc gửi báo cáo đề xuất hành động 1-chạm cho người vận hành.
- **Visual Design (Nền Trắng Chữ Đen):**
  - *Màu nền:* Trắng (`#FFFFFF`), chữ đen (`#0F172A`).
  - *Bố cục:* 5 khối hình chữ nhật liên hoàn dạng Chevron/Flowchart nối nhau bằng mũi tên xanh đậm (`#15803D`). Mỗi khối có số thứ tự lớn, tiêu đề in hoa rõ nét và 2 dòng mô tả tóm tắt giải thuật cốt lõi.
- **Speaker Notes (Tiếng Việt):**
  > *"Đây chính là trái tim và linh hồn của bài toán Smart Operations! 5 bước nối tiếp nhau một cách toán học và chặt chẽ, biến những dao động điện áp hay áp suất thô thành một lệnh đóng mở van chính xác mà không cần con người can thiệp."*

---

### SLIDE 09: STEP 1 & 2: FEATURE EXTRACTION & ANOMALY DETECTION
- **Slide Title:** Anomaly Detection Algorithms: Isolation Forest vs Autoencoders
- **Algorithmic Deep-Dive, Pros, Cons & Gotchas:**
  - **1. Feature Extraction (Trích xuất đặc trưng thời gian thực):**
    - *Miền thời gian:* Rolling Mean, Rolling Variance, Đạo hàm biến thiên tốc độ $\Delta x / \Delta t$, Z-Score chuẩn hóa.
    - *Miền tần số:* Biến đổi Fast Fourier Transform (FFT) trích xuất biên độ các đỉnh tần số hài (Harmonic Peaks) đặc trưng cho độ rơ trục động cơ.
  - **2. Isolation Forest (Scikit-Learn - Thuật toán cây phân lập):**
    - *Cơ chế:* Phân lập các điểm dị biệt bằng cách chọn ngẫu nhiên thuộc tính và giá trị cắt. Vì điểm bất thường nằm thưa thớt ở vùng biên nên số lần chia nhánh cây $h(x)$ ngắn hơn rõ rệt so với điểm bình thường:
      $$s(x, n) = 2^{-\frac{E(h(x))}{c(n)}}$$
    - *Ưu điểm:* Cực kỳ nhanh, độ phức tạp $\mathcal{O}(n \log n)$, chạy mượt mà trên CPU, không cần dữ liệu gắn nhãn (Unsupervised).
    - *Nhược điểm:* Khó học các quan hệ phi tuyến phức tạp trong không gian đa chiều cao; nhạy cảm với tham số tỷ lệ nhiễm bẩn `contamination`.
    - *Lưu ý (Gotchas):* Đặt `contamination=0.03` (3%) và `n_estimators=100` cho dữ liệu cảm biến thời tiết/cơ khí.
  - **3. Autoencoder Neural Network (PyTorch / TensorFlow):**
    - *Cơ chế:* Mạng nơ-ron gồm Encoder nén dữ liệu vào Latent Bottleneck $z = \sigma(Wx + b)$ và Decoder giải nén $\hat{x} = \sigma(W'z + b')$.
    - *Tiêu chuẩn bất thường:* Sai số tái tạo bình phương trung bình (Reconstruction Mean Squared Error):
      $$\text{MSE} = \frac{1}{d} \sum_{i=1}^d (x_i - \hat{x}_i)^2$$
      Khi máy gặp lỗi lạ chưa từng có trong tập huấn luyện, Decoder không thể tái tạo lại $\rightarrow \text{MSE}$ tăng vọt vượt ngưỡng $\text{Threshold}$.
    - *Lưu ý (Gotchas):* Luôn xuất mô hình sang **ONNX Runtime** để tăng tốc độ suy luận dưới $5\text{ms}$ và giảm $80\%$ dung lượng bộ nhớ.
- **Visual Design (Nền Trắng Chữ Đen):**
  - *Màu nền:* Trắng (`#FFFFFF`), chữ đen (`#0F172A`).
  - *Bố cục:* Chia đôi màn hình (Grid-2). Bên trái là biểu đồ cây phân lập Isolation Forest; Bên phải là sơ đồ mạng nơ-ron Autoencoder dạng thắt nút cổ chai (Hourglass Architecture) với công thức MSE đóng khung vàng hổ phách (`#FEF3C7`).
- **Speaker Notes (Tiếng Việt):**
  > *"Isolation Forest là lựa chọn hoàn hảo để làm Baseline cực nhanh trong Hackathon. Nếu muốn điểm cộng kỹ thuật, hãy huấn luyện Autoencoder trong PyTorch và nén qua ONNX Runtime để suy luận thời gian thực!"*

---

### SLIDE 10: STEP 3: ROOT CAUSE ANALYSIS (RCA) & EXPLAINABLE AI
- **Slide Title:** Root Cause Analysis (RCA) & Explainable AI (XAI)
- **Deep-Dive Concepts, Pros, Cons & Gotchas:**
  - **1. SHAP Values (SHapley Additive exPlanations):**
    - *Khái niệm:* Phương pháp lý thuyết trò chơi (Game Theory) đo lường mức độ đóng góp cận biên của từng cảm biến vào điểm số bất thường tổng thể.
    - *Ứng dụng:* Bóc tách chính xác: Cảm biến rung trục đóng góp $78\%$, Cảm biến áp suất đóng góp $14\%$, Cảm biến nhiệt độ đóng góp $8\% \rightarrow$ Khẳng định ngay nguyên nhân chính là **Lệch trục cơ khí**, không phải do quá nhiệt môi trường.
    - *Ưu điểm:* Minh bạch, giải thích được lý do mô hình AI ra quyết định (Explainable AI - XAI).
    - *Nhược điểm:* Tính toán KernelSHAP cho mô hình phức tạp có thể chậm; nên dùng **TreeSHAP** để đạt tốc độ mili-giây.
  - **2. Causal Knowledge Graphs (Đồ thị tri thức nhân quả):**
    - *Khái niệm:* Biểu diễn sơ đồ quan hệ phụ thuộc vật lý giữa các module thiết bị dưới dạng đồ thị có hướng (DAG):
      $$\text{Tắc Van Bơm A} \xrightarrow{\text{Gây ra}} \text{Tăng Áp Suất Kênh B} \xrightarrow{\text{Dẫn đến}} \text{Quá Nhiệt Tản Nhiệt C}$$
    - *Ưu điểm:* Phân biệt được đâu là "Nguyên nhân gốc rễ" (Root Cause) và đâu chỉ là "Triệu chứng lan truyền" (Symptom Propagation).
- **Visual Design (Nền Trắng Chữ Đen):**
  - *Màu nền:* Trắng (`#FFFFFF`), chữ đen (`#0F172A`).
  - *Bố cục:* 2 khối thẻ. Thẻ trái: Biểu đồ thanh ngang SHAP Waterfall biểu diễn thanh % đóng góp của từng cảm biến. Thẻ phải: Sơ đồ đồ thị các nút mạng tròn (Nodes) kết nối với nhau bằng các mũi tên nhân quả màu đỏ chỉ vào nút gốc rễ.
- **Speaker Notes (Tiếng Việt):**
  > *"Đừng bao giờ để AI báo lỗi chung chung! Hãy dùng SHAP để chứng minh cho Giám khảo thấy linh kiện nào chịu trách nhiệm cho 80% sự cố, giúp đội bảo trì sửa đúng chỗ ngay trong lần đầu tiên."*

---

### SLIDE 11: STEP 4: AI AGENT REASONING & SAFETY GUARDRAILS
- **Slide Title:** AI Agent Reasoning, LLMs, and Deterministic Safety Guardrails
- **Deep-Dive Concepts, Pros, Cons & Gotchas:**
  - **1. LLM Reasoning Engine (Google Gemini / OpenAI):**
    - *Cơ chế:* Tiếp nhận đầu vào có cấu trúc (Structured Prompt) gồm: Chỉ số cảm biến thời gian thực, Kết quả RCA từ SHAP, Lịch sử vận hành và Cẩm nang quy trình kỹ thuật (SOPs).
    - *Nhiệm vụ:* Lập luận logic, đánh giá mức độ rủi ro (Risk Score 1-100), sinh báo cáo tóm tắt tình hình và lựa chọn hành động khắc phục phù hợp (Function Calling / Tool Use).
  - **2. Lớp Kiểm Soát An Toàn (Deterministic Safety Guardrails):**
    - *Vấn đề cốt tử:* Mô hình ngôn ngữ lớn (LLM) có thể bị ảo giác (Hallucination) hoặc sinh ra lệnh vượt quá ngưỡng chịu tải an toàn của thiết bị.
    - *Giải pháp:* **Bắt buộc bọc LLM bên trong Rule Engine & Safety Policy Layer**:
      - *Quy tắc an toàn 1:* "Không bao giờ phát lệnh đóng van chính nếu áp lực đường ống đang vượt $100\text{ bar}$."
      - *Quy tắc an toàn 2:* "Lệnh kích hoạt trạm bơm tiêu úng tối đa công suất chỉ được duyệt khi lượng mưa đo được $> 40\text{ mm/h}$."
    - *Nguyên tắc:* Safety Guardrails có quyền **Phủ Quyết (Override)** tuyệt đối bất kỳ quyết định nào của LLM nếu vi phạm chính sách an toàn!
- **Visual Design (Nền Trắng Chữ Đen):**
  - *Màu nền:* Trắng (`#FFFFFF`), chữ đen (`#0F172A`).
  - *Bố cục:* Kiến trúc dạng 3 lớp bảo vệ đồng tâm (Shield/Concentric Architecture): Lớp lõi là LLM Reasoning (`#E0F2FE`), Lớp bao bọc trung gian là Safety Guardrails (`#FEF3C7` viền đỏ `#DC2626`), Lớp ngoài cùng là Physical Actuators (`#DCFCE7`).
- **Speaker Notes (Tiếng Việt):**
  > *"Mô hình ngôn ngữ lớn rất thông minh trong việc lập luận ngữ cảnh, nhưng tuyệt đối không bao giờ được để LLM kết nối trực tiếp vào thiết bị vật lý! Lớp Safety Guardrails là 'chiếc phanh an toàn' bắt buộc phải có trong mọi hệ thống công nghiệp."*

---

### SLIDE 12: STEP 5: AUTOMATED ACTION EXECUTION & CLOSED-LOOP CONTROL
- **Slide Title:** Closed-Loop Remediation & Automated Control Execution
- **Operational Modes & Implementation:**
  - **1. Chế độ Tự động hóa hoàn toàn (Automated Closed-Loop Control):**
    - Áp dụng cho các sự cố khẩn cấp có độ trễ yêu cầu $< 1\text{s}$:
      - Phát lệnh MQTT `iot/control/pumps` kích hoạt trạm bơm tiêu úng khi phát hiện bão/ngập úng.
      - Gửi lệnh ngắt điện biến tần khi phát hiện kẹt ổ bi rung động nguy hiểm.
      - Bật hệ thống tưới phun sương làm mát khi chỉ số nhiệt Heat Index vượt $40^\circ\text{C}$.
  - **2. Chế độ Bán tự động có con người xác nhận (Human-in-the-Loop Escalation):**
    - Áp dụng cho các quyết định có chi phí cao hoặc tác động diện rộng:
      - Đẩy tin nhắn định dạng Markdown phong phú về Telegram/Slack/Dashboard.
      - Kèm bảng chẩn đoán nguyên nhân, dự báo xu hướng 6h-24h và nút bấm webhook **"Xác Nhận Thực Hiện (Approve Action)"** hoặc **"Từ Chối (Override)"** 1-chạm cho kỹ sư trưởng.
- **Visual Design (Nền Trắng Chữ Đen):**
  - *Màu nền:* Trắng (`#FFFFFF`), chữ đen (`#0F172A`).
  - *Bố cục:* Sơ đồ vòng lặp khép kín (Closed-Loop Cycle). Một mũi tên tròn khổng lồ màu xanh lá (`#15803D`) quay từ cảm biến IoT $\rightarrow$ AI Agent $\rightarrow$ Thiết bị điều khiển Actuator $\rightarrow$ Cảm biến ghi nhận trạng thái mới đã an toàn.
- **Speaker Notes (Tiếng Việt):**
  > *"Vòng lặp hoàn chỉnh! Từ một hạt mưa hay một dao động áp suất nhỏ, hệ thống đã tự động tính toán, chẩn đoán và phát lệnh xử lý kịp thời trước khi sự cố biến thành thảm họa."*

---

### SLIDE 13: END-TO-END HACKATHON REFERENCE ARCHITECTURE
- **Slide Title:** End-to-End Hackathon Reference Architecture Blueprint
- **Component Blueprint (100% Dockerized):**
  - **Data Producer:** `weather-simulator` (Python asyncio phát đa trạm thời gian thực).
  - **Ingestion Gateways:** `weather-mqtt-bridge` (Mosquitto :1883) & `weather-coap-gateway` (UDP :5683).
  - **Event Broker:** `weather-redpanda` (:9092) + `weather-redpanda-console` (:8088 Web UI).
  - **Stream Analytics & AI:** `weather-stream-engine` (Bounded Watermarking, Window Aggregators, ONNX / Heuristic AI Engine).
  - **Backend & UI:** `weather-web-dashboard` (FastAPI, WebSockets, Leaflet Map, Glassmorphic UI :8000).
- **Visual Design (Nền Trắng Chữ Đen):**
  - *Màu nền:* Trắng (`#FFFFFF`), chữ đen (`#0F172A`).
  - *Bố cục:* Sơ đồ kiến trúc tổng thể toàn diện (Full System Blueprint) với các khối container có viền nét đứt (`#94A3B8`), cổng port được đánh dấu rõ ràng trong thẻ màu vàng (`#FEF3C7`).
- **Speaker Notes (Tiếng Việt):**
  > *"Các bạn hãy chụp lại slide này! Đây chính là Blueprint mẫu được tối ưu hóa toàn diện, sẵn sàng khởi chạy bằng đúng một câu lệnh `docker compose up -d` trong chưa đầy 2 phút."*

---

### SLIDE 14: RECOMMENDED HACKATHON TECH STACK DEEP-DIVE
- **Slide Title:** Production-Grade Lightweight Tech Stack Deep-Dive
- **Component Analysis & Rationale:**
  - **FastAPI (Python Backend):** Async I/O gốc, tốc độ xử lý hàng chục nghìn request/s, hỗ trợ WebSockets hai chiều và tự động tạo tài liệu OpenAPI Swagger tại `/docs`.
  - **Paho-MQTT (Python Client):** Thư viện client nhẹ nhất thế giới để tích hợp MQTT pub/sub vào simulator và backend.
  - **Chart.js & Leaflet.js (Frontend Visuals):** Vẽ biểu đồ dòng dữ liệu trượt 60fps mượt mà và hiển thị bản đồ trạm địa lý mà không cần cài đặt framework frontend cồng kềnh.
  - **PyTorch $\rightarrow$ ONNX Runtime:** Huấn luyện mô hình dễ dàng trong PyTorch rồi xuất ra định dạng nhị phân ONNX để suy luận với tốc độ C++.
- **Visual Design (Nền Trắng Chữ Đen):**
  - *Màu nền:* Trắng (`#FFFFFF`), chữ đen (`#0F172A`).
  - *Bố cục:* Lưới 4 thẻ công nghệ (Grid-4). Mỗi thẻ có logo công nghệ, danh sách 3 tính năng cốt lõi và thanh đánh giá hiệu năng (Performance Bar) màu xanh lá.
- **Speaker Notes (Tiếng Việt):**
  > *"Toàn bộ tech stack này được lựa chọn dựa trên 3 tiêu chí sống còn của Hackathon: Tối đa hiệu năng, tiêu tốn ít RAM nhất và cực kỳ dễ debug trong 48 giờ thi căng thẳng."*

---

### SLIDE 15: SECRET WEAPON: THE "LIVE ANOMALY INJECTION" PITCH
- **Slide Title:** Winning Hackathon Strategy: The Live Anomaly Injection Pitch
- **The 5-Minute Pitching Storyboard for Judges:**
  - **Phút 0:00 - 1:00 (Bình Thường):** Giới thiệu đề tài, mở Dashboard chứng minh hệ thống đang chạy ổn định với các luồng dữ liệu màu xanh.
  - **Phút 1:00 - 2:00 (Tiêm Sự Cố):** Bấm nút **"Tiêm Kịch Bản Bão Nhiệt Đới / Nắng Nóng Cực Đoan"** ngay trên giao diện Web.
  - **Phút 2:00 - 3:00 (Stream Phản Hồi):** Chỉ cho Giám khảo thấy áp suất sụt nhanh, cửa sổ trượt 5 phút phát hiện bất thường, cờ cảnh báo đổi sang màu cam/đỏ tức thì.
  - **Phút 3:00 - 4:00 (AI Chẩn Đoán):** AI Agent phân tích ngữ cảnh, xuất hiện chẩn đoán nguyên nhân gốc rễ và bảng phương án điều hành trong $<100\text{ms}$.
  - **Phút 4:00 - 5:00 (Thực Thi Lệnh):** Hệ thống tự động gửi lệnh MQTT kích hoạt trạm bơm tiêu úng và cấm biển, hoàn thành bài thi với tràng pháo tay của Giám khảo!
- **Visual Design (Nền Trắng Chữ Đen):**
  - *Màu nền:* Trắng (`#FFFFFF`), chữ đen (`#0F172A`).
  - *Bố cục:* Kịch bản phân cảnh 5 bước (5-Step Storyboard) với các hình mockup giao diện trước và sau khi tiêm lỗi, làm nổi bật nút bấm tiêm lỗi màu đỏ (`#DC2626`).
- **Speaker Notes (Tiếng Việt):**
  > *"Ban Giám Khảo chấm hàng chục đội thi và họ chỉ có 5 phút cho mỗi đội. Đừng bắt Giám khảo nghe lý thuyết suông! Hãy tiêm lỗi trực tiếp và để AI tự động xử lý ngay trước mắt họ để ghi điểm tuyệt đối!"*

---

### SLIDE 16: COMMON HACKATHON PITFALLS TO AVOID
- **Slide Title:** Common Hackathon Pitfalls & How to Avoid Them
- **Do's & Don'ts Matrix:**
  - ❌ **Bẫy 1: Quá sa đà vào hàn mạch phần cứng:**
    - *Hậu quả:* Dành $80\%$ thời gian ngồi hàn chân cảm biến ESP32/Arduino, mạng chập chờn không gửi được tin, không còn thời gian làm AI.
    - *Giải pháp đúng:* Dùng Python IoT Simulator giả lập đa trạm với đầy đủ mô hình toán học vật lý phát qua MQTT/CoAP.
  - ❌ **Bẫy 2: Dùng mô hình LLM/Deep Learning quá nặng:**
    - *Hậu quả:* Triển khai mô hình 70B tham số khiến mỗi lần gọi API mất $30\text{s}$, giao diện bị treo cứng khi Giám khảo đang xem.
    - *Giải pháp đúng:* Dùng mô hình nhẹ (Gemini-1.5-Flash / GPT-4o-mini) kết hợp **Heuristic Fallback Engine** chạy offline tức thì.
  - ❌ **Bẫy 3: Làm Dashboard tĩnh thiếu vòng lặp hành động:**
    - *Hậu quả:* Chỉ vẽ biểu đồ mà không có logic tự động ra quyết định $\rightarrow$ Bị đánh giá là bài thi IoT sơ cấp Phase 1.
    - *Giải pháp đúng:* Thiết kế các thẻ hành động tự động (Smart Operations Action Cards) và feedback loop qua MQTT.
- **Visual Design (Nền Trắng Chữ Đen):**
  - *Màu nền:* Trắng (`#FFFFFF`), chữ đen (`#0F172A`).
  - *Bố cục:* Bảng 2 cột so sánh trực quan (Cột trái: ❌ Sai lầm phổ biến màu đỏ nhạt `#FEE2E2` | Cột phải: ✅ Giải pháp khắc phục màu xanh lá nhạt `#DCFCE7`).
- **Speaker Notes (Tiếng Việt):**
  > *"Hãy ghi nhớ: Đây là cuộc thi AI-Driven Smart Operations, không phải cuộc thi hàn mạch phần cứng. Hãy đầu tư thời gian vào kiến trúc dữ liệu và trí tuệ nhân tạo để tạo ra giá trị khác biệt!"*

---

### SLIDE 17: LIVE TECHNICAL Q&A & MENTORSHIP
- **Slide Title:** Live Technical Q&A & Architecture Mentorship
- **Open Floor Discussion Topics:**
  - Kỹ thuật tối ưu hóa độ trễ luồng dữ liệu (Stream Latency Optimization).
  - Lựa chọn giải thuật Anomaly Detection phù hợp với tập dữ liệu của từng đội.
  - Cách thiết kế Prompt và Safety Guardrails chuẩn cho AI Agent.
  - Tư vấn kiến trúc 1-1 trực tiếp cho từng ý tưởng đề tài.
- **Visual Design (Nền Trắng Chữ Đen):**
  - *Màu nền:* Trắng (`#FFFFFF`), chữ đen (`#0F172A`).
  - *Bố cục:* Thiết kế mở với biểu tượng micro và bong bóng trò chuyện (Chat Bubbles), thông tin liên hệ và link Google Meet được đóng khung trang trọng ở giữa.
- **Speaker Notes (Tiếng Việt):**
  > *"Bây giờ là khoảng thời gian quý báu dành riêng cho các bạn! Bất kỳ khó khăn nào về Docker, Kafka, thuật toán AI hay cách trình bày, hãy thoải mái bật mic hoặc đặt câu hỏi trong khung chat để chúng ta cùng giải quyết ngay tại đây!"*

---

### SLIDE 18: CLOSING & BEST WISHES
- **Slide Title:** Build Smart, Scale Fast, and Drive Intelligent Action!
- **Closing Credentials & Links:**
  - **Speaker:** Nguyen Duc Tuan (Backend Lead / System Architect, FPT Software)
  - **Event:** SEAL Hackathon Summer 2026
  - **Repository Mã Nguồn:** `https://github.com/Pen1112003/AI-Driven-Smart-Operations-Turning-Real-Time-IoT-Data-into-Intelligent-Actions`
  - **Thông điệp truyền cảm hứng:** *"Hãy biến dữ liệu cảm biến thời gian thực thành những hành động thông minh thay đổi thế giới!"*
- **Visual Design (Nền Trắng Chữ Đen):**
  - *Màu nền:* Trắng (`#FFFFFF`), chữ đen than chì (`#0F172A`).
  - *Bố cục:* Slide bế mạc trang nhã; thông điệp truyền cảm hứng in đậm nổi bật màu xanh lá (`#15803D`); mã QR Code và đường dẫn GitHub repository nằm ở vị trí trung tâm dễ quét.
- **Speaker Notes (Tiếng Việt):**
  > *"Chúc tất cả các đội thi của SEAL Hackathon Summer 2026 tự tin, sáng tạo, hoàn thành xuất sắc bài thi và đem đến những giải pháp Vận hành Thông minh đột phá nhất! Xin trân trọng cảm ơn!"*

---

# PHẦN V: BẢNG TRA CỨU CÔNG NGHỆ CHUYÊN SÂU & MA TRẬN SO SÁNH

| Tầng Kiến Trúc | Công Nghệ | Định Nghĩa & Cơ Chế | Ưu Điểm (Pros) | Nhược Điểm (Cons) | Lưu Ý Thực Chiến (Gotchas / Best Practices) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Ingestion** | **MQTT** | Giao thức Pub/Sub TCP, header 2B. | Tiết kiệm băng thông, Keepalive, QoS 0/1/2. | Phụ thuộc TCP, QoS 2 chậm. | Dùng QoS 1 + event_time; cấu hình LWT phát hiện rớt mạng. |
| | **CoAP** | Giao thức RESTful nhị phân chạy UDP. | Header 4B, siêu tiết kiệm pin. | Dễ rớt gói trên mạng kém ổn định. | Thích hợp cảm biến môi trường/nông nghiệp pin yếu. |
| **Streaming Buffer**| **Redpanda** | Distributed Commit Log viết bằng C++. | Zero JVM, p99 latency thấp gấp 10x Kafka, khởi động 2s. | Mới hơn Kafka truyền thống. | ⭐ **Khuyên dùng số 1 cho Hackathon**; đặt key theo `station_id`. |
| | **Apache Kafka** | Distributed Event Streaming trên JVM. | Chuẩn công nghiệp, chịu tải cực lớn. | Ngốn 2GB+ RAM, cấu hình JVM nặng. | Cần máy cấu hình mạnh; cẩn thận lỗi OOM. |
| | **Redis Streams** | Append-only Log trong RAM. | Độ trễ $<1\text{ms}$, cực nhẹ. | Dữ liệu giới hạn trong RAM. | Luôn dùng `XADD MAXLEN ~ 1000` để chống tràn bộ nhớ. |
| **Stream Engine** | **Async Window Engine** | Xử lý dòng dữ liệu phi đồng bộ Python. | Tích hợp trực tiếp AI, kiểm soát Watermark linh hoạt. | Cần tự quản lý bộ đệm trạng thái. | Cấu hình allowed_delay $5\text{s}$ để gom dữ liệu trễ mạng. |
| | **Apache Flink** | Stateful stream engine chuẩn mực. | Xử lý Exactly-once, đồ thị stream phức tạp. | Khởi động nặng, tốn thời gian cấu hình. | Dùng cho hệ thống lớn cấp Enterprise. |
| **Time-Series DB** | **TimescaleDB** | PostgreSQL Extension với Hypertables. | SQL chuẩn, tự động phân vùng, nén 90%. | Tốn tài nguyên như Postgres. | Cấu hình chunk 1 ngày và bật Columnar Compression. |
| | **InfluxDB** | CSDL Time-series chuyên dụng TSM. | Tốc độ ghi cực nhanh. | Lỗi High Cardinality, học ngôn ngữ Flux. | Chỉ dùng khi đã quen thuộc với hệ sinh thái Influx. |
| **AI Anomaly** | **Isolation Forest** | Phân lập điểm dị biệt qua cây ngẫu nhiên. | Nhanh $\mathcal{O}(n \log n)$, chạy trên CPU, Unsupervised. | Khó học tương quan phi tuyến sâu. | Đặt `contamination=0.03`, kết hợp trích xuất đặc trưng FFT. |
| | **Autoencoder** | Mạng nơ-ron nén và tái tạo tín hiệu. | Học được quan hệ phức tạp, bắt lỗi mới lạ. | Cần chuẩn hóa dữ liệu cẩn thận. | Export sang **ONNX Runtime** để suy luận $<5\text{ms}$. |
| **RCA & XAI** | **SHAP** | Phân bổ Shapley từ lý thuyết trò chơi. | Chỉ rõ % đóng góp của từng cảm biến vào lỗi. | Tính toán lâu nếu nhiều biến. | Dùng TreeSHAP để tính toán trong mili-giây. |
| | **Causal Graph** | Đồ thị có hướng mô tả quan hệ vật lý. | Phân biệt nguyên nhân gốc vs triệu chứng. | Phải am hiểu kiến trúc cơ khí/vật lý. | Dựng sơ đồ DAG đơn giản từ tài liệu kỹ thuật máy. |
| **AI Agent** | **LLM Reasoning** | Mô hình ngôn ngữ lớn (Gemini/OpenAI). | Tổng hợp ngữ cảnh, phân tích đa chiều. | Có thể bị ảo giác (Hallucination). | Bắt buộc bọc qua **Safety Guardrails** trước khi phát lệnh! |

---

# PHẦN VI: CHECKLIST VẬN HÀNH & BẢNG TIÊU CHÍ CHẤM ĐIỂM HACKATHON

### Bảng Tiêu Chí Giúp Thí Sinh Đạt Điểm Tuyệt Đối
1. **Kiến trúc phân tầng rõ ràng (20%):** Tách biệt Ingestion, Buffer, Stream Engine, Storage và AI Layer.
2. **Kỹ thuật Stream Processing chuẩn xác (25%):** Có xử lý Watermark Event-Time, có cửa sổ Tumbling & Sliding.
3. **Mô hình AI & Giải thích được (Explainable AI) (25%):** Áp dụng Anomaly Detection kết hợp trích xuất đặc trưng và chỉ ra nguyên nhân lỗi qua SHAP/Causal Graph.
4. **Tự động hóa hành động khép kín (15%):** AI Agent tự động phát lệnh điều khiển khắc phục sự cố có kiểm soát an toàn.
5. **Kỹ năng Demo & Trực quan hóa (15%):** Trình diễn kịch bản tiêm lỗi (Live Anomaly Injection) trực tiếp trên Dashboard mượt mà.
