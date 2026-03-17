from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class HistoryResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    summary: str
    created_at: datetime

    class Config:
        from_attributes = True