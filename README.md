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
	string file_type  
	integer file_size  
	  
	string vector_collection_id  
	  
	integer chunk_count  
	string embedding_model  
	  
	datetime created_at	   
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

  F --> Options[Chọn Summary Options]

  Options --> Process[Prompt]

  Process --> Gen[Sinh Tóm tắt]

  Gen --> Save[(Lưu vào DB Lịch sử SQL)]

  Save --> UI[Hiển thị lên Giao diện]

```

---


## 4 Pipeline cho RAG


```mermaid
flowchart TD  
  
%% Input  
A[Nhập text / Upload file PDF / DOCX] --> B[Extractor - Rút trích Text]  
  
%% Chunking  
B --> C[Text Splitter - Recursive Chunking]  
  
%% Embedding + Storage  
C --> D[Embedding Model]  
D --> E[(Vector Database)]  
  
%% User Options  
O[Summary Options<br/>Length / Bullet / Paragraph] --> H[Prompt Template]  
  
%% Query  
A --> Q[Query Embedding]  
  
%% Retrieval  
Q --> F[Retriever - Similarity Search]  
E --> F  
  
F --> G[Top-k Relevant Chunks]  
  
%% Generation  
G --> I[Finetuned ViT5]  
H --> I  
  
%% Output  
I --> J[Kết quả Tóm tắt]  
  
J --> K[(Lưu vào SQL Database)]  
  
K --> L[Trả về Frontend UI]

```

---
## 5 Kiến trúc luồng Backend API

```mermaid
flowchart TD  
  
UI[Frontend Web/Mobile]  
  
UI --> API[FastAPI Application]  
  
API --> Router{Router Layer}  
  
Router -->|/api/auth| AuthC[Authentication Controller]  
Router -->|/api/admin| AdminC[Admin Controller]  
Router -->|/api/history| HistoryC[History Controller]  
Router -->|/api/ai| AIC[AI & RAG Controller]  
  
AuthC --> PG[(SQL Database)]  
AdminC --> PG  
HistoryC --> PG  
  
  
%% USER INPUT  
AIC --> Input{Input Type}  
  
Input -->|Paste Text| TextInput[User Text]  
Input -->|Upload File| Document[Document Loader]  
  
Document --> Extract[Text Extraction]  
  
Extract --> Content[Document Content]  
TextInput --> Content  
  
  
%% OPTIONS  
Content --> Opt[Summary Options<br/>Length / Format]  
  
  
%% RAG PIPELINE  
Opt --> Splitter[Recursive Chunking]  
  
Splitter --> Embed[Embedding Generator]  
  
Embed --> VDB[(Vector Database)]  
  
Opt --> QueryEmbed[Query Embedding]  
  
QueryEmbed --> Retriever[Similarity Retriever]  
  
VDB --> Retriever  
  
Retriever --> RAG[RAG Service]  
  
RAG --> LLM[Finetuned ViT5]  
  
LLM --> SaveDB[(Lưu lịch sử SQL)]  
  
SaveDB --> Response[JSON Response]  
  
Response --> UI
```

---

## 6 Luồng Phân tích Dữ liệu Hệ thống

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
