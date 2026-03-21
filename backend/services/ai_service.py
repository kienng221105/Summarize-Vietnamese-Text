from sqlalchemy.orm import Session
from backend.database.models import Message, Conversation
from backend.schemas.ai_schema import SummarizeRequest
from uuid import UUID, uuid4

def create_conversation(db: Session, user_id: UUID, title: str):
    """
    Tạo một cuộc hội thoại mới.
    - Input: db (Session), user_id (UUID), title (str).
    - Output: Đối tượng Conversation mới được tạo.
    """
    db_conversation = Conversation(
        id=uuid4(),
        user_id=user_id,
        title=title
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation

def create_message(db: Session, conversation_id: UUID, content: str):
    """
    Lưu tin nhắn mới vào cuộc hội thoại.
    - Input: db (Session), conversation_id (UUID), content (str).
    - Output: Đối tượng Message mới được tạo.
    """
    db_message = Message(
        id=uuid4(),
        conversation_id=conversation_id,
        content=content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages(db: Session, conversation_id: UUID):
    """
    Lấy toàn bộ tin nhắn trong một cuộc hội thoại.
    - Input: db (Session), conversation_id (UUID).
    - Output: Danh sách các đối tượng Message.
    """
    return db.query(Message).filter(Message.conversation_id == conversation_id).all()
