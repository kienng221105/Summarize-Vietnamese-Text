# Tài liệu Kiến trúc Hệ thống

---

  

## 1️ Sơ đồ Kiến trúc Tổng thể

  

Mô tả sự giao tiếp tĩnh giữa các cụm thành phần chính. Dữ liệu phi cấu trúc đi vào kho Vector, dữ liệu có trạng thái (Stateful - User, History) đi vào Relational DB.

  

```mermaid

flowchart TD

  Client[Headless Drupal AI] -->|REST API| API[FastAPI Backend / API Gateway]

  API --> Auth[Xác thực]

  API --> Admin[Quản trị viên]

  API --> Core[Lõi AI]

  Auth --> RDB[PostgreSQL/Users/Sessions]

  Admin --> RDB

  Core --> RDB

  Core --> ExtProcessor[Xuất và xử lý document]

  Core --> Embed[Mô hình Embedding]

  Embed --> VDB[(ChromaDB)]

  Core --> ViT5[ViT5/PhoGPT]

```

  

---

  

## 2️ Sơ đồ Cơ sở Dữ liệu

  

Thiết kế CSDL SQL cốt lõi phục vụ tính năng lưu trữ lịch sử phân nhánh, đảm bảo duy trì được luồng hội thoại liên tục cho người dùng.

  

```mermaid

erDiagram

  USERS ||--o{ CONVERSATIONS : "owns"

  USERS {

    uuid id PK

    string email

    string password_hash

    string role "USER or ADMIN"

    datetime created_at

    boolean is_active

  }

  CONVERSATIONS ||--o{ MESSAGES : "contains"

  CONVERSATIONS {

    uuid id PK

    uuid user_id FK

    string title

    datetime updated_at

  }

  MESSAGES {

    uuid id PK

    uuid conversation_id FK

    string sender_type "USER or AI"

    text content

    datetime created_at

  }

  CONVERSATIONS ||--o{ DOCUMENTS : "attaches"

  DOCUMENTS {

    uuid id PK

    uuid conversation_id FK

    string filename

    string vector_collection_id

  }

```

  

---

  

## 3️ Luồng Người dùng Cơ bản

  

Áp dụng thêm luồng kiểm tra uỷ quyền (Authorization). User lấy lại context cũ hoặc tạo mới context thông qua phân loại đầu vào.

  

```mermaid

flowchart TD

  U[User] --> L{Đã đăng nhập?}

  L -->|Chưa| Login[Đăng nhập / Đăng ký]

  L -->|Rồi| Main[Trang chủ Web UI]

  Main --> Action{Chọn Thao tác}

  Action -->|Xem Lịch sử| Hist[Tải lại Hội thoại cũ]

  Action -->|Text mới| T[Nhập / Dán đoạn Text]

  Action -->|File mới| F[Upload Tài liệu]

  T --> Process[Prompt]

  F --> Document[RAG]

  Process --> Gen[Sinh Tóm tắt]

  Document --> Gen

  Gen --> Save[(Lưu vào DB Lịch sử SQL)]

  Save --> UI[Hiển thị lên Giao diện]

  UI --> Chat[Chat tương tác Follow-up]

  Chat --> Save

```

  

---

  

## 4️ Pipeline cho Prompt Engineering (Document ngắn)

  

Kiến trúc hệ thống dành cho Request nhỏ không cần VectorDB. Tối ưu độ trễ (Latency).

  

```mermaid

flowchart TD

  A[Nhập Văn bản từ Frontend] --> B[Gắn Context / Prompt Template]

  B --> C[Finetuned ViT5]

  C --> D[Văn bản Tóm tắt]

  D --> E[(Lưu Log Message vào CSDL SQL)]

  E --> F[Trả về Frontend UI]

```

  

---

  

## 5️ Pipeline cho RAG (Document dài)

  

Kiến trúc chuẩn cho luồng truy xuất thông tin phân mảnh với RAG (Retrieval-Augmented Generation). Đã tích hợp gắn mã mapping với History DB.

  

```mermaid

flowchart TD

  %% Nhánh 1: Upload và lưu trữ

  A[Upload file PDF / DOCX] --> B[Extrator - Rút trích Text]

  B --> C[Text Splitter - Chia nhỏ Chunking]

  C --> D[Embedding Model]

  C --> E[(Vector DB - ChromaDB)]

  D --> E

  %% Nhánh 2: Truy vấn

  Q[User Query / Câu hỏi] --> QE[Embedding Model]

  QE --> F[Retriever - Truy xuất Vector]

  E -. So khớp tương đồng .-> F

  %% Nhánh 3: Hội tụ & Trả lời

  F --> G[Các đoạn Text liên quan nhất top-k]

  G --> I[PhoGPT]

  H[Prompt Template] --> I

  Q --> H

  I --> J[Kết quả Tóm tắt / Phản hồi]

  J --> K[(Lưu bản ghi vào SQL DB)]

  K --> L[Trả về kết quả tới Frontend UI]

```
  

---

  

## 6️ Kiến trúc luồng Backend API

  

Sơ đồ phân định trách nhiệm các Router và Service của Backend theo chuẩn kiến trúc nguyên khối mô-đun hoá (Modular Monolith).

  

```mermaid

flowchart TD

  UI[Frontend UI Web/Mobile] --> API[FastAPI Application]

  API --> M{Router Switch Layer}

  M -->|/api/auth| AuthC[Authentication Router]

  M -->|/api/admin| AdminC[Dashboard/Admin Router]

  M -->|/api/chat| ChatC[Chat History Router]

  M -->|/api/ai| AIC[AI & RAG Router]

  AuthC --> PG[(SQL Database)]

  AdminC --> PG

  ChatC --> PG

  AIC --> File[Document Loader Worker]

  File --> Embed[Embedding Generator] --> VDB[(Chroma Vector DB)]

  VDB --> Ret[Similarity Retriever] --> RAG[RAG Service]

  AIC --> Prompt[Standard Prompt Service]

  Prompt --> LLM[LLM Calling Module]

  RAG --> LLM

  LLM --> SaveDB[(Ghi lịch sử vào SQL)]

  SaveDB --> Res[Trả JSON Response]

  Res --> UI

```

  

---

  

## 7️ Luồng Lưu trữ và Tái tạo Lịch sử Hội thoại (Chat History Flow)

  

Quy trình logic phía dưới UI để tái tạo lại hoàn toàn ngữ cảnh AI như lúc người dùng ngưng chat ở phiên làm việc trước.

  

```mermaid

sequenceDiagram

  actor User

  participant Frontend as Web Client

  participant API as Backend Server

  participant DB as Relational DB

  participant Chroma as Vector DB

  

  User->>Frontend: Mở Sidebar "Lịch sử cuộc gọi"

  Frontend->>API: GET /api/chat/conversations

  API->>DB: Query Conversations by user_id

  DB-->>API: Array of Conversations

  API-->>Frontend: Danh sách JSON

  Frontend-->>User: Hiển thị Sidebar

  

  User->>Frontend: Chọn Conversation có đính kèm PDF

  Frontend->>API: GET /api/chat/{id}/messages

  API->>DB: Fetch Messages & Linked Document info

  DB-->>API: Historical Messages + Vector ID

  API-->>Frontend: Context Data Payload

  Frontend-->>User: Hiển thị khung chat sẵn sàng

  Note over API, Chroma: Hệ thống tự động trỏ RAG Search<br/>sang Vector Collection tương ứng của hội thoại này if needed.

```

  

---

  

## 8️ Luồng Quản trị Hệ thống

  

Bộ module dành riêng cho Quyền Admin quản trị người dùng, vận hành và phân tích feedback an toàn, khép kín.

  

```mermaid

flowchart TD

  Admin[Quản trị viên] --> Login[Đăng nhập Portal /auth/admin]

  Login --> Dash[Bảng điều khiển - Admin Dashboard]

  Dash --> Action{Chọn Phân hệ vụ}

  Action -->|Thống kê Hệ thống| Metrics[Xem RPS, Latency, Data Logs]

  Action -->|Quản lý Người dùng| Users[Tải Danh sách Người dùng]

  Action -->|Quản lý Đánh giá| Review[Xem Feedback 1-5 Sao của User]

  Users --> SelectU[Chọn User Cụ thể]

  SelectU --> Modify{Thực thi Lệnh}

  Modify -->|Ban / Unblock Tài khoản| UpdateDB[(Cập nhật cờ is_active vào SQL)]

  Modify -->|Kiểm tra Quota Limit| ViewInfo[Truy vấn Traffic cá nhân]

  UpdateDB --> Log[(Lưu Audit Log để truy vết)]

  Log --> Dash

```

---

  

## 9️ Luồng Phân tích Dữ liệu Hệ thống

  

Kiến trúc luồng trích xuất dữ liệu và trực quan hóa (Data Visualization) thông qua PowerBI. Phục vụ việc theo dõi các chỉ số quan trọng như: Usage Trend, Error Rate, Average Rating, và TPS/Latency.

  

```mermaid

flowchart TD

  DB[("Cơ sở dữ liệu SQL\nChứa Users, Logs, Ratings")] --> Connector["PowerBI Data Connector\n(DirectQuery / Import)"]

  Connector --> Transform["Power Query / Data Modeling"]

  Transform --> Dataset["Dataset Nội bộ PowerBI\nĐã được chuẩn hóa"]

  Dataset --> Report{"Báo cáo & Dashboard"}

  Report --> Usage["Usage Trend\nBiểu đồ Requests per day"]

  Report --> Error["Error Rate\nTỷ lệ lỗi theo thời gian"]

  Report --> Rating["Average Rating\nPhân bổ 1-5 sao từ thẻ Feedback"]

  Report --> Perf["System Performance\nLatency < 5s, TPS"]

  Admin["Admin / Data Analyst"] -->|Truy cập, Phân tích| Report

```
