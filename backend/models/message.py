from sqlalchemy import Column, DateTime, Boolean, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from backend.database.base import Base

class Message(Base):
    __tablename__ = "messages"
    __table_args__ = {'extend_existing': True}
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    conversation_id = Column(PG_UUID(as_uuid=True),ForeignKey("conversations.id") ,nullable=False)
    content = Column(Text, nullable=False)
    is_user = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    conversation = relationship("Conversation", back_populates="messages")