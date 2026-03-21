from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from backend.core.config import settings

password_hasher = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password: str) -> str:
    """
    Mã hóa mật khẩu người dùng.
    - Input: password (str) - Mật khẩu thô.
    - Output: chuỗi mật khẩu đã được mã hóa (str).
    """
    return password_hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Kiểm tra mật khẩu thô có khớp với mật khẩu đã mã hóa hay không.
    - Input: plain_password (str), hashed_password (str).
    - Output: True nếu khớp, ngược lại False (bool).
    """
    try:
        return password_hasher.verify(plain_password, hashed_password)
    except Exception:
        return False
    
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Tạo mã thông báo truy cập (JWT access token).
    - Input: data (dict) - Dữ liệu cần mã hóa, expires_delta (timedelta, optional).
    - Output: Chuỗi token JWT (str).
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    if "sub" not in to_encode:
        to_encode["sub"] = data.get("sub", "")
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY.get_secret_value(), algorithm=settings.algorithm)
    return encoded_jwt

def verify_access_token(token: str) -> Optional[dict]:
    """
    Xác thực và giải mã token JWT.
    - Input: token (str).
    - Output: Payload của token nếu hợp lệ, ngược lại None (Optional[dict]).
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY.get_secret_value(), algorithms=[settings.algorithm], options = {"require": ["exp", "sub"]})
        return payload
    except jwt.PyJWTError:
        return None
