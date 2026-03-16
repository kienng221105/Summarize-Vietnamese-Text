from sqlalchemy import Column, Text , DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from backend.database.base import Base
from sqlalchemy.orm import relationship

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    conversation_id = Column(UUID(as_uuid=True),ForeignKey("conversations.id") ,nullable=False)
    content = Column(Text, nullable=False)
    create_at = Column(DateTime, nullable=False)
    
    #relationships
    conversation = relationship("Conversation", back_populates="messages")