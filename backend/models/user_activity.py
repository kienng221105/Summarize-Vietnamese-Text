from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from backend.database.base import Base
from sqlalchemy.orm import relationship

class UserActivity(Base):
    __tablename__ = "user_activities"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    action = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    resource_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime, nullable=False)
    
    #relationships
    user = relationship("User", back_populates="user_activities")