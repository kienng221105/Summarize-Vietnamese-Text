from uuid import UUID

def process_document_task(document_id: UUID, filepath: str):
    """
    Tác vụ chạy ngầm để lấy văn bản từ file tài liệu và đẩy vào worker nhúng vector.
    """
    # TODO: Đọc file dùng file_loader, cập nhật trạng thái CSDL, và gọi embedding_worker
    pass
