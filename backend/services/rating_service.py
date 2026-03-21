from sqlalchemy.orm import Session
from backend.database.models import Rating
from backend.schemas.rating_schema import RatingCreate
from uuid import UUID, uuid4

def create_rating(db: Session, user_id: UUID, rating_data: RatingCreate):
    """
    Lưu phản hồi và đánh giá của người dùng.
    - Input: db (Session), user_id (UUID), rating_data (RatingCreate).
    - Output: Đối tượng Rating mới được tạo.
    """
    try:
        print(f"Creating rating for user {user_id}, conv {rating_data.conversation_id}")
        db_rating = Rating(
            id=uuid4(),
            user_id=user_id,
            conversation_id=rating_data.conversation_id,
            rating=rating_data.rating,
            feedback=rating_data.feedback
        )
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        print(f"Rating created: {db_rating.id}")
        return db_rating
    except Exception as e:
        import traceback
        from fastapi import HTTPException
        from sqlalchemy.exc import IntegrityError
        
        db.rollback()
        if isinstance(e, IntegrityError):
            raise HTTPException(status_code=400, detail="Bạn đã đánh giá cuộc hội thoại này hoặc cuộc hội thoại không tồn tại.")
            
        error_msg = f"LỖI ĐÁNH GIÁ: {e}\n{traceback.format_exc()}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

def get_rating(db: Session, conversation_id: UUID):
    """
    Lấy thông tin đánh giá của một cuộc hội thoại.
    - Input: db (Session), conversation_id (UUID).
    - Output: Đối tượng Rating hoặc None.
    """
    return db.query(Rating).filter(Rating.conversation_id == conversation_id).first()
