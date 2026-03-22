from typing import List

class TextChunker:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str) -> List[str]:
        """
        Chia văn bản thành các đoạn (chunk) nhỏ hơn để nhúng vector.
        """
        # TODO: Cài đặt logic cắt văn bản (RecursiveCharacterTextSplitter)
        return [text]
