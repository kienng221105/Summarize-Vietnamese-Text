from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.api.dependencies.deps import get_db
from backend.schemas.ai_schema import ConversationResponse
from backend.schemas.history_schema import HistoryResponse
from backend.services import history_service
from backend.api.dependencies.deps import get_current_active_user
from backend.database.models import AppUser as User
from uuid import UUID

router = APIRouter()

@router.get("/conversations", response_model=List[ConversationResponse])
def list_conversations(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """
    Danh sách các cuộc hội thoại của người dùng hiện tại.
    """
    return history_service.get_user_conversations(db, current_user.id)

@router.delete("/conversations/{conversation_id}")
def delete_conv(conversation_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """
    Xóa một cuộc hội thoại của người dùng.
    """
    success = history_service.delete_conversation(db, conversation_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Không tìm thấy cuộc hội thoại")
    return {"message": "Đã xóa thành công"}