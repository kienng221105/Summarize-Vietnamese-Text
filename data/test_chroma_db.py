from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# 1. BẮT BUỘC: Gọi lại đúng mô hình Embedding mà bạn đã dùng ở bước trước
print("Đang tải mô hình Embedding...")
embedding_model = HuggingFaceEmbeddings(model_name="keepitreal/vietnamese-sbert")

# 2. Kết nối vào thư mục ChromaDB đã tạo
print("Đang kết nối Database...")
db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_model)

# 3. Đặt một câu hỏi thử nghiệm (Hãy thay bằng một câu hỏi liên quan đến paper của bạn)
query = "Hà Mĩ Linh?"
print(f"\nCâu hỏi của User: '{query}'")

# 4. Thực hiện tìm kiếm: Lấy ra 3 đoạn chunk có ngữ nghĩa giống với câu hỏi nhất
results = db.similarity_search(query, k=3)

# 5. In kết quả ra màn hình để nghiệm thu
print(f"\nTìm thấy {len(results)} đoạn văn bản phù hợp:")
for i, doc in enumerate(results):
    print(f"\n--- ĐOẠN {i+1} ---")
    print(f"📄 Nguồn (Metadata): {doc.metadata}")
    print(f"📝 Nội dung trích xuất: {doc.page_content}")
    print("-" * 50)