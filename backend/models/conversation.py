from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from backend.database.base import Base

class Conversation(Base):
    __tablename__ = "conversations"
    __table_args__ = {'extend_existing': True}
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id") ,nullable=False)
    title = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    user = relationship("AppUser", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="conversation", cascade="all, delete-orphan")
    rating = relationship("Rating", back_populates="conversation", cascade="all, delete-orphan", uselist=False)