from sqlalchemy import Column, String, DateTime, Boolean, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from backend.database.base import Base

class AppUser(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    conversations = relationship("Conversation", back_populates="user")
    ratings = relationship("Rating", back_populates="user")