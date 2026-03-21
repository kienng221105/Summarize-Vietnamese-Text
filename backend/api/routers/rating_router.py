from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.api.dependencies.deps import get_db
from backend.schemas.rating_schema import RatingCreate, RatingResponse
from backend.services import rating_service
from backend.api.dependencies.deps import get_current_active_user
from backend.database.models import AppUser as User
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=RatingResponse)
def rate(rating_data: RatingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """
    Gửi đánh giá cho một đoạn tóm tắt.
    """
    return rating_service.create_rating(db, current_user.id, rating_data)

@router.get("/conversation/{conversation_id}", response_model=RatingResponse)
def get_rate(conversation_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """
    Lấy nội dung đánh giá của cuộc hội thoại.
    """
    rating = rating_service.get_rating(db, conversation_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Không tìm thấy đánh giá")
    return rating
