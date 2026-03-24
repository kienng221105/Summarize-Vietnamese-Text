# Tài liệu Kiến trúc Hệ thống

---

## 1️ Sơ đồ Kiến trúc Tổng thể

Mô tả sự giao tiếp tĩnh giữa các cụm thành phần chính. Dữ liệu phi cấu trúc đi vào kho Vector, dữ liệu có trạng thái (Stateful - User, History) đi vào Relational DB.

```mermaid
flowchart TD

  Client -->|REST API| API[FastAPI Backend / API Gateway]

  API --> Auth[Xác thực]
  API --> Admin[Quản trị viên]
  API --> Core[Lõi AI]
  API --> History
  API --> Rating

  Auth --> RDB[PostgreSQL/Users/Sessions]
  Admin --> RDB
  History --> RDB
  Core --> RDB
  Rating --> RDB
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
  USERS ||--o{ RATINGS : "gives"
  USERS ||--o{ USER_ACTIVITIES : "performs"

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
    boolean is_user
    datetime created_at
  }

  CONVERSATIONS ||--o{ DOCUMENTS : "attaches"
  CONVERSATIONS ||--o| RATINGS : "receives"

  DOCUMENTS {
 uuid id PK  
 uuid conversation_id FK  
   
 string filename  
 string file_type  
 string file_path
   
 string vector_collection_id  
   
 integer chunk_count  
 string embedding_model  
   
 datetime created_at    
  }

  RATINGS {
    uuid id PK
    uuid user_id FK
    uuid conversation_id FK
    integer rating
    text feedback
    datetime created_at
  }

  SYSTEM_LOGS {
    uuid id PK
    string endpoint
    string method
    integer status_code
    integer response_time
    uuid user_id FK
    text error_message
    datetime created_at
  }

  USER_ACTIVITIES {
    uuid id PK
    uuid user_id FK
    string action
    text details
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


B --> Clean[Làm sạch dữ liệu] 

Clean --> C[Chunking dữ liệu]  

%% Embedding + Storage  

C --> D[Mô hình embedding]  

D --> E[(Vector Database)]  

%% User Options  

O[Lựa chọn tóm tắt<br/>Length / Bullet / Paragraph] --> H[Khuôn mẫu câu lệnh]  

%% Query  

A --> Q[Query Embedding]  

%% Retrieval  

Q --> F[Retriever - Tìm kiếm tương đồng]  

E --> F  

F --> G[Top k đoạn liên quan nhất]  

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
Router -->|/api/rating| RatingC[Rating Controller]
  
AuthC --> PG[(SQL Database)]  
AdminC --> PG  
HistoryC --> PG  
RatingC --> PG  
  
  
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

## 7️ Sơ đồ Lớp (Class Diagram)

Sơ đồ lớp kiến trúc mô tả chi tiết các thành phần cấu trúc (Routers, Services, Models), các phương thức (methods) và mối quan hệ của chúng trong ứng dụng FastAPI Backend.

```mermaid
classDiagram

    %% Interface / API Layer
    class AuthRouter {
        +register(user, db)
        +login(form_data, db)
    }
    class AIRouter {
        +post_summarize(request, db, current_user)
        +get_history(conversation_id, db, current_user)
    }
    class RatingRouter {
        +rate(rating_data, db, current_user)
        +get_rate(conversation_id, db, current_user)
    }
    class HistoryRouter {
        +list_conversations(db, current_user)
        +delete_conv(conversation_id, db, current_user)
    }
    class AdminRouter {
        +list_users(db, current_admin)
        +get_logs(db, current_admin)
    }

    %% Business Logic Layer
    class AuthService {
        +verify_password(plain_password, hashed_password)
        +get_password_hash(password)
        +create_access_token(data, expires_delta)
    }
    class AIService {
        +create_conversation(db, user_id, title)
        +create_message(db, conversation_id, content)
        +get_messages(db, conversation_id)
    }
    class UserService {
        +get_user_by_email(db, email)
        +get_user(db, user_id)
        +create_user(db, user)
    }
    class HistoryService {
        +get_user_conversations(db, user_id)
        +get_user_activities(db, user_id)
        +delete_conversation(db, conversation_id, user_id)
    }
    class RatingService {
        +create_rating(db, user_id, rating_data)
        +get_rating(db, conversation_id)
    }
    class DocumentService {
        +upload_document(file, user_id)
        +get_document_status(document_id)
    }

    %% Data Access / Models Layer
    class AppUser {
        +UUID id
        +String email
        +String password_hash
        +String role
        +Boolean is_active
        +DateTime created_at
    }
    class Conversation {
        +UUID id
        +UUID user_id
        +String title
        +DateTime updated_at
    }
    class Message {
        +UUID id
        +UUID conversation_id
        +String content
        +Boolean is_user
        +DateTime created_at
    }
    class Document {
        +UUID id
        +UUID conversation_id
        +String filename
        +String file_type
        +String file_path
        +String vector_collection_id
        +Integer chunk_count
        +String embedding_model
        +DateTime created_at
    }
    class Rating {
        +UUID id
        +UUID user_id
        +UUID conversation_id
        +Integer rating
        +String feedback
        +DateTime created_at
    }
    class SystemLog {
        +UUID id
        +String endpoint
        +String method
        +Integer status_code
        +Integer response_time
        +UUID user_id
        +String error_message
        +DateTime created_at
    }
    class UserActivity {
        +UUID id
        +UUID user_id
        +String action
        +String details
        +DateTime created_at
    }

    %% Relationships (Dependencies & Associations)
    AuthRouter --> AuthService : uses
    AuthRouter --> UserService : uses
    AIRouter --> AIService : uses
    RatingRouter --> RatingService : uses
    HistoryRouter --> HistoryService : uses
    AdminRouter --> UserService : uses

    UserService ..> AppUser : queries/mutates
    HistoryService ..> Conversation : queries/mutates
    HistoryService ..> UserActivity : queries
    RatingService ..> Rating : manages
    AIService ..> Conversation : manages
    AIService ..> Message : manages
    DocumentService ..> Document : manages
    
    %% Entity Relationships
    AppUser "1" *-- "0..*" Conversation : owns
    AppUser "1" *-- "0..*" UserActivity : performs
    AppUser "1" *-- "0..*" Rating : gives
    Conversation "1" *-- "0..*" Message : contains
    Conversation "1" *-- "0..*" Document : attaches
    Conversation "1" *-- "0..1" Rating : receives
```

---

## 8️ Sơ đồ Trạng thái (State Diagram)

Sơ đồ này mô tả vòng đời (lifecycle) ở mức chi tiết của từng đối tượng chính trong hệ thống, được bố trí theo chiều ngang để dễ theo dõi.

```mermaid
stateDiagram-v2
    direction LR

    state "Trạng thái User" as UserLifecycle {
        direction LR
        [*] --> Khach
        Khach : Khách vãng lai
        DaDangNhap : Đã đăng nhập
        TuongTac : Đang hoạt động
        
        Khach --> DaDangNhap : Đăng nhập
        DaDangNhap --> TuongTac : Gọi API
    }

    state "Trạng thái Document" as DocLifecycle {
        direction LR
        [*] --> DaTaiLen
        DaTaiLen : Đã tải lên
        DocFile : Đang đọc file
        TachDoan : Tách đoạn 
        VectorHoa : Vector hóa
        DaLuuDoc : Lưu ChromaDB
        
        DaTaiLen --> DocFile : Đọc PDF/Word
        DocFile --> TachDoan : Xử lý Text
        TachDoan --> VectorHoa : Mô hình Embedding
        VectorHoa --> DaLuuDoc : Lưu CSDL
        DaLuuDoc --> [*]
    }

    state "Trạng thái Conversation" as ConvLifecycle {
        direction LR
        [*] --> KhoiTao
        KhoiTao : Khởi tạo
        DangXuLy : Đang tóm tắt
        ThanhCong : Thành công
        ThatBai : Thất bại
        DaDanhGia : Đã đánh giá
        
        KhoiTao --> DangXuLy : Gọi AI
        DangXuLy --> ThanhCong : Xong
        DangXuLy --> ThatBai : Báo lỗi API
        ThanhCong --> DaDanhGia : User phản hồi
        DaDanhGia --> [*]
    }

    state "Trạng thái Message (Kết quả AI)" as MsgLifecycle {
        direction LR
        [*] --> ChoXuLy
        ChoXuLy : Chờ đợi
        DangChay : Đang chạy ViT5
        CoKetQua : Có kết quả thô
        DaLuuMsg : Lưu DB
        
        ChoXuLy --> DangChay : Trigger LLM
        DangChay --> CoKetQua : Response
        CoKetQua --> DaLuuMsg : Insert SQL
        DaLuuMsg --> [*]
    }
```

---
