from email.mime import text
from collections import Counter 
import os
import json
import re
import PyPDF2
import docx

class TextPreprocessingPipeline:
    def __init__(self):
        # Bạn có thể thêm các cấu hình khởi tạo ở đây nếu cần
        pass

    # ================= 1. BƯỚC TRÍCH XUẤT (EXTRACTION) =================
    def _read_txt(self, file_path):
        """Đọc file .txt"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _read_pdf(self, file_path):
        """Đọc file .pdf"""
        text = ""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text

    def _read_docx(self, file_path):
        """Đọc file .docx"""
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text

    def extract_text(self, file_path):
        """Hàm phân loại file và gọi đúng hàm đọc tương ứng"""
        ext = os.path.splitext(file_path)[1].lower()
        try:
            if ext == '.txt':
                return self._read_txt(file_path)
            elif ext == '.pdf':
                return self._read_pdf(file_path)
            elif ext in ['.doc', '.docx']:
                return self._read_docx(file_path)
            else:
                print(f"[Cảnh báo] Bỏ qua file {file_path}: Định dạng {ext} chưa được hỗ trợ.")
                return None
        except Exception as e:
            print(f"[Lỗi] Không thể đọc file {file_path}. Lỗi: {e}")
            return None

    # ================= 2. BƯỚC LÀM SẠCH (CLEANING) =================
    # ================= 2. BƯỚC LÀM SẠCH (CLEANING) TỔNG QUÁT =================
   # ================= 2. BƯỚC LÀM SẠCH (CLEANING) TỔNG QUÁT =================
    def clean_text(self, raw_text):
        if not raw_text:
            return ""
        
        text = raw_text

        # 1. Chuẩn hóa khoảng trắng
        text = re.sub(r'[ \t]+', ' ', text)

        # 2. XÓA SỐ TRANG DÍNH LIỀN (Giải quyết vấn đề 1/18Phương...)
        # Pattern này tìm: [Số]/[Số] theo sau là một chữ cái (không cần khoảng trắng)
        # và xóa cụm số đó đi.
        text = re.sub(r'\d+\s*/\s*\d+', '', text)
        
        # Bổ sung: Xóa các số thứ tự đứng đầu dòng dính liền (nếu có dạng 1.Nội dung)
        # text = re.sub(r'(?m)^\d+\.', '', text) 

        # 3. XÓA CÁC ĐỊNH DẠNG SỐ TRANG PHỔ BIẾN KHÁC
        text = re.sub(r'(?i)\b(Trang|Page)\s*:?\s*\d+(\s*(/|of)\s*\d+)?\b', '', text)
        text = re.sub(r'(?m)^\s*[-[|]\s*\d+\s*[-\]|]\s*$', '', text)
        text = re.sub(r'(?im)^\s*\d+\s*$', '', text)

        # 4. XÓA URL
        text = re.sub(r'http[s]?://\S+|www\.\S+', '', text)

        # 5. TỰ ĐỘNG XÓA HEADER/FOOTER LẶP LẠI (Dòng cố định)
        lines = text.split('\n')
        
        # Chuẩn hóa để nhận diện mẫu lặp lại (Ví dụ: "Khoa Toán - Cơ - Tin học" xuất hiện nhiều lần)
        def normalize_line(line):
            return re.sub(r'\d+', '[NUM]', line.strip())
        
        line_counts = Counter(normalize_line(line) for line in lines if len(line.strip()) > 0)
        
        suspected_patterns = {
            pattern for pattern, count in line_counts.items() 
            if count >= 2 and len(pattern) < 150 # Hạ ngưỡng xuống 2 để bắt chặt hơn
        }

        cleaned_lines = []
        for line in lines:
            stripped_line = line.strip()
            if not stripped_line:
                continue
                
            norm_pattern = normalize_line(stripped_line)
            if norm_pattern not in suspected_patterns:
                cleaned_lines.append(stripped_line)

        text = '\n'.join(cleaned_lines)

        # 6. FIX XUỐNG DÒNG SAI (Nối các câu bị ngắt đoạn)
        # Bắt các chữ cái tiếng Việt viết thường ở đầu dòng để nối vào dòng trước
        lowercase_vn = r'[a-zàáảãạâầấẩẫậăằắẳẵặeèéẻẽẹêềếểễệiìíỉĩịoòóỏõọôồốổỗộơờớởỡợuùúủũụưừứửữựyỳýỷỹỵđ]'
        text = re.sub(rf'(?<![.!?:;])\n(?={lowercase_vn})', ' ', text)

        # 7. DỌN DẸP CUỐI CÙNG
        text = re.sub(r'\n\s*\n', '\n', text)

        return text.strip()
    # ================= 3. CHẠY PIPELINE (EXECUTE) =================
    def process_files(self, file_paths, output_json="data_cleaned.json"):
        """Chạy toàn bộ pipeline cho một danh sách các file và lưu ra JSON"""
        results = []
        
        for file_path in file_paths:
            print(f"Đang xử lý: {file_path} ...")
            
            # Bước 1: Trích xuất Text
            raw_text = self.extract_text(file_path)
            
            if raw_text is not None:
                # Bước 2: Làm sạch Text
                cleaned_text = self.clean_text(raw_text)
                
                # Lưu vào danh sách kết quả
                results.append({
                    "file_name": os.path.basename(file_path),
                    "file_extension": os.path.splitext(file_path)[1].lower(),
                    "cleaned_data": cleaned_text
                })
                print(f"  -> Xong: {os.path.basename(file_path)}")

        # Bước 3: Xuất ra file JSON
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
            
        print(f"\n[Thành công] Toàn bộ dữ liệu sạch đã được lưu vào file: {output_json}")


# ================= CÁCH SỬ DỤNG (TESTING) =================
if __name__ == "__main__":
    # Khởi tạo Pipeline
    pipeline = TextPreprocessingPipeline()
    
    # DANH SÁCH 3 FILE BẠN MUỐN TEST (Thay đổi đường dẫn cho đúng với máy của bạn)
    # Ví dụ nếu file để cùng thư mục với script code này:
    files_to_test = [
        "t0.txt",
        "104.-KHMTTT-chuẩn-04.11.2023.docx",
        "5-presentation.pdf"
    ]
    
    # Kiểm tra xem file có tồn tại không trước khi chạy
    valid_files = [f for f in files_to_test if os.path.exists(f)]
    
    if not valid_files:
        print("Vui lòng đặt 3 file vào cùng thư mục với script này hoặc trỏ đúng đường dẫn!")
    else:
        # Chạy pipeline và xuất ra JSON
        pipeline.process_files(valid_files, output_json="data_cleaned.json")
        