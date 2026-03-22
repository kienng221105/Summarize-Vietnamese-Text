import re

def sanitize_text(text: str) -> str:
    """
    Làm sạch văn bản (loại bỏ khoảng trắng thừa, các ký tự lạ).
    """
    # TODO: Cải thiện logic làm sạch văn bản nếu cần
    return re.sub(r'\s+', ' ', text).strip()

def count_tokens(text: str) -> int:
    """
    Đếm số lượng token trong văn bản (ước tính thô).
    """
    # TODO: Cài đặt logic đếm token chính xác cho từng loại mô hình
    return len(text.split())

def is_text_too_short(text: str, min_words: int = 20) -> bool:
    """
    Kiểm tra xem văn bản có quá ngắn để cần tóm tắt hay không.
    Mặc định: dưới 20 từ thì không cần tóm tắt.
    """
    cleaned_text = sanitize_text(text)
    return len(cleaned_text.split()) < min_words
