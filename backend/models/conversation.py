from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from backend.database.base import Base
from sqlalchemy.orm import relationship

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id") ,nullable=False)
    title = Column(String, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    #relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation",cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="conversation",cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="conversation")