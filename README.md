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

  Core --> Options[Summary Options<br/>Length % / Output Format]

  Core --> Embed[Mô hình Embedding]
  Embed --> VDB[(ChromaDB)]

  Core --> ViT5[ViT5]
```

---

## 2️ Sơ đồ Cơ sở Dữ liệu

Thiết kế CSDL SQL phục vụ lưu trữ lịch sử tóm tắt.

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

Luồng người dùng dành cho hệ thống tóm tắt văn bản.

```mermaid
flowchart TD

  U[User] --> L{Đã đăng nhập?}

  L -->|Chưa| Login[Đăng nhập / Đăng ký]

  L -->|Rồi| Main[Trang chủ Web UI]

  Main --> Action{Chọn Thao tác}

  Action -->|Xem Lịch sử| Hist[Tải lại lịch sử tóm tắt]

  Action -->|Text mới| T[Nhập / Dán đoạn Text]

  Action -->|File mới| F[Upload Tài liệu]

  T --> Options[Chọn Summary Options]

  F --> Document[RAG]

  Options --> Process[Prompt]

  Document --> Process

  Process --> Gen[Sinh Tóm tắt]

  Gen --> Save[(Lưu vào DB Lịch sử SQL)]

  Save --> UI[Hiển thị lên Giao diện]
```

---

## 4️ Pipeline cho Prompt Engineering (Document ngắn)

Kiến trúc dành cho request nhỏ không cần VectorDB.

```mermaid
flowchart TD

  A[Nhập Văn bản từ Frontend]

  A --> O[Summary Options<br/>Length % / Output Format]

  O --> B[Gắn Context / Prompt Template]

  B --> C[Finetuned ViT5]

  C --> D[Văn bản Tóm tắt]

  D --> E[(Lưu Log Message vào CSDL SQL)]

  E --> F[Trả về Frontend UI]
```

---

## 5️ Pipeline cho RAG (Document dài)

Kiến trúc chuẩn cho tóm tắt tài liệu dài.

```mermaid
flowchart TD

  %% Upload
  A[Upload file PDF / DOCX] --> B[Extractor - Rút trích Text]

  B --> C[Text Splitter - Chunking]

  C --> D[Embedding Model]

  C --> E[(Vector DB - ChromaDB)]

  D --> E

  %% Summary Options
  O[Summary Options] --> H[Prompt Template]

  %% Retrieval
  E -. Similarity Search .-> F[Retriever]

  F --> G[Top-k Relevant Chunks]

  G --> I[Finetuned ViT5]

  H --> I

  %% Output
  I --> J[Kết quả Tóm tắt]

  J --> K[(Lưu vào SQL DB)]

  K --> L[Trả về Frontend UI]
```

---

## 6️ Kiến trúc luồng Backend API

```mermaid
flowchart TD

  UI[Frontend UI Web/Mobile]

  UI --> API[FastAPI Application]

  API --> M{Router Switch Layer}

  M -->|/api/auth| AuthC[Authentication Router]

  M -->|/api/admin| AdminC[Dashboard/Admin Router]

  M -->|/api/history| ChatC[Summary History Router]

  M -->|/api/ai| AIC[AI & RAG Router]

  AuthC --> PG[(SQL Database)]

  AdminC --> PG

  ChatC --> PG

  AIC --> File[Document Loader Worker]

  File --> Embed[Embedding Generator]

  Embed --> VDB[(Chroma Vector DB)]

  VDB --> Ret[Similarity Retriever]

  Ret --> RAG[RAG Service]

  AIC --> Prompt[Prompt Builder<br/>Length % + Format]

  Prompt --> LLM[LLM Calling Module]

  RAG --> LLM

  LLM --> SaveDB[(Ghi lịch sử vào SQL)]

  SaveDB --> Res[Trả JSON Response]

  Res --> UI
```

---

## 7️ Luồng Phân tích Dữ liệu Hệ thống

Kiến trúc trích xuất dữ liệu và trực quan hóa qua PowerBI.

```mermaid
flowchart TD

  DB[("Cơ sở dữ liệu SQL\nUsers, Logs, Ratings")]

  DB --> Connector["PowerBI Data Connector\n(DirectQuery / Import)"]

  Connector --> Transform["Power Query / Data Modeling"]

  Transform --> Dataset["PowerBI Dataset"]

  Dataset --> Report{"Dashboard"}

  Report --> Usage["Usage Trend"]

  Report --> Error["Error Rate"]

  Report --> Rating["Average Rating"]

  Report --> Perf["System Performance\nLatency / TPS"]

  Admin["Admin / Data Analyst"] -->|Phân tích| Report
```

---
