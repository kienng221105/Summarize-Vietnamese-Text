from fastapi import UploadFile
from sqlalchemy.orm import Session
from uuid import UUID
import os

class DocumentService:
    def __init__(self, db: Session):
        self.db = db
        self.upload_dir = os.path.join(os.path.dirname(__file__), "../../data/uploads")

    def upload_document(self, file: UploadFile, user_id: UUID) -> dict:
        """
        Xử lý file tải lên, lưu vào thư mục data/uploads và tạo bản ghi trong CSDL.
        """
        # TODO: Cài đặt luồng lưu file và gửi tác vụ cho worker
        return {"status": "success", "message": "Đã tải file lên (tạm thời)."}

    def get_document_status(self, document_id: UUID) -> dict:
        """
        Trích xuất trạng thái xử lý của một tài liệu.
        """
        # TODO: Truy vấn CSDL để xem trạng thái tài liệu
        return {"status": "completed"}
