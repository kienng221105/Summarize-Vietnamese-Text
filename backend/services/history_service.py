from sqlalchemy.orm import Session, joinedload
from backend.database.models import Conversation, UserActivity
from uuid import UUID

def get_user_conversations(db: Session, user_id: UUID):
    """
    Lấy danh sách các cuộc hội thoại của một người dùng.
    - Input: db (Session), user_id (UUID).
    - Output: Danh sách các đối tượng Conversation.
    """
    return db.query(Conversation).options(
        joinedload(Conversation.messages),
        joinedload(Conversation.documents)
    ).filter(Conversation.user_id == user_id).all()

def get_user_activities(db: Session, user_id: UUID):
    """
    Lấy lịch sử hoạt động của người dùng.
    - Input: db (Session), user_id (UUID).
    - Output: Danh sách các đối tượng UserActivity.
    """
    return db.query(UserActivity).filter(UserActivity.user_id == user_id).all()

def delete_conversation(db: Session, conversation_id: UUID, user_id: UUID):
    """
    Xóa một cuộc hội thoại.
    - Input: db (Session), conversation_id (UUID), user_id (UUID).
    - Output: True nếu xóa thành công.
    """
    db_conv = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.user_id == user_id).first()
    if db_conv:
        db.delete(db_conv)
        db.commit()
        return True
    return False
