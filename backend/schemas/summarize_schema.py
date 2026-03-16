from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional

# Message Schemas
class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    conversation_id: UUID

class MessageResponse(MessageBase):
    id: UUID
    conversation_id: UUID
    create_at: datetime

    class Config:
        from_attributes = True

# Document Schemas
class DocumentBase(BaseModel):
    filename: str
    file_type: str

class DocumentResponse(DocumentBase):
    id: UUID
    conversation_id: UUID
    vector_collection_id: str
    chunk_count: int
    embedding_model: str
    create_at: datetime

    class Config:
        from_attributes = True

# Conversation Schemas
class ConversationBase(BaseModel):
    title: str

class ConversationCreate(ConversationBase):
    user_id: UUID

class ConversationResponse(ConversationBase):
    id: UUID
    user_id: UUID
    update_at: datetime
    messages: List[MessageResponse] = []
    documents: List[DocumentResponse] = []

    class Config:
        from_attributes = True

# AI/Summarization Specific
class SummarizeRequest(BaseModel):
    document_id: Optional[UUID] = None
    custom_content: Optional[str] = None
    max_length: Optional[int] = 500

class SummarizeResponse(BaseModel):
    summary: str
    original_id: Optional[UUID] = None
