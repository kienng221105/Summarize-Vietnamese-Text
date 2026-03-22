from uuid import UUID

def embed_document_task(document_id: UUID, text: str):
    """
    Tác vụ chạy ngầm để cắt văn bản và nhúng vector vào CSDL (ChromaDB).
    """
    # TODO: Nối với pipeline RAG để cắt (chunk) và nhúng (embed), sau đó cập nhật CSDL
    pass
