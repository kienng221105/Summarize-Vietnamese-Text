from sqlalchemy import Column, String, DateTime, Integer, Text, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4
from backend.database.base import Base

class SystemLog(Base):
    __tablename__ = "system_logs"
    __table_args__ = {'extend_existing': True}
    id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    endpoint = Column(String, nullable=False)
    method = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
    response_time = Column(Integer, nullable=True) # ms
    user_id = Column(PG_UUID(as_uuid=True), nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
