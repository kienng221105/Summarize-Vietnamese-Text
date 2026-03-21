from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class RatingCreate(BaseModel):
    conversation_id: UUID
    rating: int = Field(ge=1, le=5)
    feedback: Optional[str] = None


class RatingResponse(BaseModel):
    id: UUID
    user_id: UUID
    conversation_id: UUID
    rating: int
    feedback: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True