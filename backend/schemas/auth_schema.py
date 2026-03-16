from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[EmailStr] = None
    user_id: Optional[UUID] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
