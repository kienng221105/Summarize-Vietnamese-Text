def extract_text_from_pdf(filepath: str) -> str:
    """
    Rút trích chữ (text) từ file PDF.
    """
    # TODO: Cài đặt trích xuất văn bản dùng thư viện pdfplumber
    return ""

def extract_text_from_docx(filepath: str) -> str:
    """
    Rút trích chữ (text) từ file DOCX.
    """
    # TODO: Cài đặt trích xuất văn bản từ file Word DOCX
    return ""

def extract_text_from_txt(filepath: str) -> str:
    """
    Đọc chữ trực tiếp từ file TXT.
    """
    # TODO: Tối ưu hóa việc xử lý encoding cho TXT
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def process_file(filepath: str, file_type: str) -> str:
    """
    Điều hướng file tới hàm xử lý tương ứng dựa trên định dạng file.
    """
    if file_type == 'application/pdf':
        return extract_text_from_pdf(filepath)
    elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return extract_text_from_docx(filepath)
    elif file_type == 'text/plain':
        return extract_text_from_txt(filepath)
    else:
        raise ValueError(f"Không hỗ trợ định dạng file: {file_type}")
