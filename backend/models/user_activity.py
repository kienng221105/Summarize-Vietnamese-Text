from sqlalchemy import Column, String, DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4
from backend.database.base import Base

class UserActivity(Base):
    __tablename__ = "user_activities"
    __table_args__ = {'extend_existing': True}
    id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    action = Column(String, nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())