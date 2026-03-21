from sqlalchemy.orm import Session
from uuid import uuid4
from backend.database.models import AppUser as User
from backend.schemas.user_schema import UserCreate
from backend.services.auth_service import hash_password

def get_user_by_email(db: Session, email: str):
    """
    Tìm kiếm người dùng trong cơ sở dữ liệu theo email.
    - Input: db (Session), email (str).
    - Output: Đối tượng User hoặc None.
    """
    return db.query(User).filter(User.email == email).first()

def get_user(db: Session, user_id: str):
    """
    Tìm kiếm người dùng trong cơ sở dữ liệu theo ID.
    - Input: db (Session), user_id (str).
    - Output: Đối tượng User hoặc None.
    """
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    """
    Tạo người dùng mới trong cơ sở dữ liệu.
    - Input: db (Session), user (UserCreate).
    - Output: Đối tượng User đã được tạo.
    """
    try:
        db_user = User(
            id=uuid4(),
            email=user.email,
            password_hash=hash_password(user.password),
            role=user.role,
            is_active=user.is_active
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        import traceback
        from fastapi import HTTPException
        error_msg = f"LỖI NGƯỜI DÙNG: {e}\n{traceback.format_exc()}"
        print(error_msg)
        db.rollback()
        raise HTTPException(status_code=500, detail=error_msg)
