from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.api.dependencies.deps import get_db
from backend.schemas.user_schema import UserCreate, UserResponse
from fastapi.security import OAuth2PasswordRequestForm
from backend.schemas.auth_schema import Token
from backend.services import auth_service, user_service

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Đăng ký người dùng mới.
    - Input: user (UserCreate), db (Session).
    - Output: Thông tin người dùng mới được tạo.
    """
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email đã được đăng ký")
    return user_service.create_user(db=db, user=user)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Đăng nhập và lấy mã thông báo (access token).
    - Input: login_data (OAuth2PasswordRequestForm), db (Session).
    - Output: Mã thông báo truy cập (JWT).
    """
    user = user_service.get_user_by_email(db, email=form_data.username)
    if not user or not auth_service.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai email hoặc mật khẩu",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}