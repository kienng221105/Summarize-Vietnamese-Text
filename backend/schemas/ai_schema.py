from pydantic import BaseModel, Field, model_validator
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
    created_at: datetime

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
    created_at: datetime

    class Config:
        from_attributes = True

# Conversation Schemas
class ConversationBase(BaseModel):
    title: str

class ConversationCreate(ConversationBase):
    pass

class ConversationResponse(ConversationBase):
    id: UUID
    user_id: UUID
    updated_at: datetime
    messages: List[MessageResponse] = Field(default_factory=list)
    documents: List[DocumentResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True

# AI/Summarization Specific
class SummarizeRequest(BaseModel):
    document_id: Optional[UUID] = None
    custom_content: Optional[str] = None
    max_length: Optional[int] = 500

    @model_validator(mode="after")
    def check_input(self):
        if not self.document_id and not self.custom_content:
            raise ValueError("Phải cung cấp document_id hoặc custom_content")
        return self

class SummarizeResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
