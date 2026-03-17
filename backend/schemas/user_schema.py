from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    role: Optional[str] = "user"
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    isactive: Optional[bool] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
