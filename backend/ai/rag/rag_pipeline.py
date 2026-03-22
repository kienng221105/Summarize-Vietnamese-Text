from backend.ai.rag.chunker import TextChunker
from backend.ai.rag.embedder import Embedder
from backend.ai.rag.retriever import Retriever

class RAGPipeline:
    def __init__(self):
        self.chunker = TextChunker()
        self.embedder = Embedder()
        self.retriever = Retriever()
        # TODO: Lấy _vit5_model và _vit5_tokenizer từ ModelLoader ở đây hoặc truyền vào tùy ý

    def process_document(self, text: str, collection_name: str):
        """
        Xử lý tài liệu: cắt văn bản -> nhúng vector -> lưu vào CSDL.
        """
        # TODO: Cài đặt toàn bộ luồng xử lý tài liệu vào Vector DB
        pass

    def answer_query(self, query: str, collection_name: str) -> str:
        """
        Trả lời truy vấn dùng RAG: nhúng câu hỏi -> tìm ngữ cảnh -> tạo prompt -> gọi model.generate() của ViT5.
        """
        # TODO: Cài đặt luồng tìm kiếm và gọi model.generate() với ViT5 Tokenizer
        return "Chưa được cài đặt."
