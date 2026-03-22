import traceback
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.api.dependencies.deps import get_db
from backend.schemas.ai_schema import SummarizeRequest, SummarizeResponse, MessageResponse
from backend.services import ai_service as summarize_service
from backend.api.dependencies.deps import get_current_active_user
from backend.database.models import AppUser as User
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=SummarizeResponse)
def post_summarize(request: SummarizeRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    print(f"DEBUG START: post_summarize. User: {current_user.email}")
    print(f"DEBUG: Request Data: {request}")
    
    # 1. Tạo cuộc hội thoại mới
    try:
        print("DEBUG: Gọi hàm tạo cuộc hội thoại")
        conv = summarize_service.create_conversation(db, current_user.id, "Tóm tắt văn bản")
        print(f"DEBUG: Tạo cuộc hội thoại thành công. ID: {conv.id}")
    except Exception as e:
        print(f"DEBUG: Lỗi khi tạo cuộc hội thoại: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        raise e
    
    # 2. Tạo tin nhắn người dùng
    try:
        print("DEBUG: Chuẩn bị nội dung tóm tắt")
        from backend.utils.helpers import is_text_too_short
        
        # Nếu người dùng gửi text trực tiếp và đoạn text đó quá ngắn
        if request.custom_content and is_text_too_short(request.custom_content):
            print("DEBUG: Văn bản quá ngắn, trả về nguyên bản (bypass AI).")
            summary_content = request.custom_content
        else:
            summary_content = "Kết quả tóm tắt giả lập cho: " + (request.custom_content[:50] if request.custom_content else "tài liệu")
        print(f"DEBUG: Gọi hàm tạo tin nhắn")
        msg = summarize_service.create_message(db, conv.id, summary_content)
        print(f"DEBUG: Tạo tin nhắn thành công. ID: {msg.id}")
    except Exception as e:
        print(f"DEBUG: Lỗi khi tạo tin nhắn: {type(e).__name__}: {str(e)}")
        traceback.print_exc()
        raise e
    
    print("DEBUG: Trả về kết quả.")
    return {
        "id": msg.id,
        "conversation_id": conv.id,
        "content": msg.content,
        "created_at": msg.created_at
    }

@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
def get_history(conversation_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """
    Lấy lịch sử tin nhắn trong một cuộc hội thoại.
    """
    return summarize_service.get_messages(db, conversation_id)