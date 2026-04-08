import json
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

class VectorIngestionPipeline:
    def __init__(self, json_path="data_cleaned.json", db_path="./chroma_db"):
        self.json_path = json_path
        self.db_path = db_path
        
        # Cấu hình bộ cắt chữ (Chunking)
        # chunk_size: Số ký tự tối đa cho mỗi đoạn (khoảng 200-300 từ)
        # chunk_overlap: Số ký tự chồng lấn lên nhau giữa 2 đoạn liên tiếp (chống đứt gãy ngữ nghĩa)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", " ", ""] # Ưu tiên ngắt ở đầu đoạn, sau đó đến câu, từ...
        )
        
        # Cấu hình mô hình Embedding (Dùng mô hình tiếng Việt chạy offline miễn phí)
        print("Đang tải mô hình Embedding (Có thể mất chút thời gian lần đầu)...")
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="keepitreal/vietnamese-sbert" 
        )

    def run_pipeline(self):
        # 1. ĐỌC DỮ LIỆU ĐÃ LÀM SẠCH
        if not os.path.exists(self.json_path):
            print(f"[Lỗi] Không tìm thấy file {self.json_path}")
            return
            
        with open(self.json_path, 'r', encoding='utf-8') as f:
            cleaned_data = json.load(f)
            
        all_documents = []
        
        # 2. CHUNKING & GÁN METADATA
        print("Bắt đầu cắt nhỏ văn bản (Chunking)...")
        for item in cleaned_data:
            text = item.get("cleaned_data", "")
            file_name = item.get("file_name", "Unknown")
            
            if not text:
                continue
                
            # Cắt text thành nhiều mẩu nhỏ
            chunks = self.text_splitter.split_text(text)
            
            # Gói từng mẩu thành object 'Document' của LangChain kèm theo Metadata
            for i, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "source": file_name,
                        "chunk_id": i
                    }
                )
                all_documents.append(doc)
                
        print(f"-> Đã chia thành {len(all_documents)} đoạn chunks.")

        # 3. EMBEDDING & LƯU VÀO CHROMADB
        print("Đang đưa dữ liệu vào Vector Database (ChromaDB)...")
        # Hàm này sẽ tự động gọi embedding_model để mã hóa 'all_documents' và lưu xuống ổ cứng
        vector_db = Chroma.from_documents(
            documents=all_documents,
            embedding=self.embedding_model,
            persist_directory=self.db_path
        )
        
        print(f"[Thành công] Toàn bộ dữ liệu đã được nạp vào thư mục: {self.db_path}")

if __name__ == "__main__":
    # Chạy pipeline
    ingestor = VectorIngestionPipeline()
    ingestor.run_pipeline()