from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.api.dependencies.deps import get_db
from backend.schemas.user_schema import UserResponse
from backend.api.dependencies.deps import get_current_admin_user
from backend.database.models import AppUser as User

router = APIRouter()

@router.get("/users", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin_user)):
    """
    Danh sách toàn bộ người dùng (Dành cho Admin).
    """
    return db.query(User).all()

@router.get("/logs")
def get_logs(db: Session = Depends(get_db), current_admin: User = Depends(get_current_admin_user)):
    """
    Xem nhật ký hệ thống (Dành cho Admin).
    """
    return {"logs": "Hệ thống chưa có chức năng này"}
