from typing import List

class Embedder:
    def __init__(self, model_name: str = None):
        self.model_name = model_name
        # TODO: Khởi tạo mô hình embedding (nhúng vector)

    def embed_chunks(self, chunks: List[str]) -> List[List[float]]:
        """
        Tạo embeddings (vector nhúng) cho danh sách các đoạn văn bản.
        """
        # TODO: Cài đặt logic chuyển các đoạn text thành vector embedding
        return [[] for _ in chunks]

    def embed_query(self, query: str) -> List[float]:
        """
        Tạo embedding (vector nhúng) cho một chuỗi truy vấn (query).
        """
        # TODO: Cài đặt logic chuyển chuỗi truy vấn thành vector
        return []
