from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from backend.database.base import Base

class Rating(Base):
    __tablename__ = "ratings"
    __table_args__ = {'extend_existing': True}
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    conversation_id = Column(PG_UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False, unique=True)
    rating = Column(Integer, nullable=False)
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    user = relationship("AppUser", back_populates="ratings")
    conversation = relationship("Conversation", back_populates="rating")