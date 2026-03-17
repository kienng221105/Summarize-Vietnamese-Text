from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from backend.database.base import Base
from sqlalchemy.orm import relationship

class Document(Base):
    __tablename__ = "documents"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    vector_collection_id = Column(String, nullable=False)
    chunk_count = Column(Integer, nullable=False)
    embedding_model = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    #relationships
    conversation = relationship("Conversation", back_populates="documents")