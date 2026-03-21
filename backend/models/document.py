from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from backend.database.base import Base

class Document(Base):
    __tablename__ = "documents"
    __table_args__ = {'extend_existing': True}
    id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    conversation_id = Column(PG_UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    vector_collection_id = Column(String, nullable=True)
    chunk_count = Column(Integer, default=0)
    embedding_model = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())

    conversation = relationship("Conversation", back_populates="documents")