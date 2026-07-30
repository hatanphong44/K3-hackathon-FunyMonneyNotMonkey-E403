# VLearn AI Quiz Generator — Web Component (Streamlit + FastAPI)

Ứng dụng Web AI Tạo & Kiểm Tra Kiến Thức Cuối Buổi Học dành cho Sinh viên và Giảng viên trong hệ thống VLearn.

---

## 🏗️ Cấu Trúc Thư Mục `web/`

```text
web/
├── app.py              # Streamlit Frontend UI chính
├── api_server.py       # FastAPI Backend RESTful API Server
├── config.py           # Thiết lập kết nối API & Cấu hình ứng dụng
├── mock_data.py        # Dữ liệu bài giảng mẫu & Engine sinh quiz AI
├── ui_components.py   # Style CSS giao diện modern & UI Helpers
├── requirements.txt    # Các thư viện Python cần thiết
└── README.md           # Hướng dẫn chạy ứng dụng
```

---

## 🚀 Hướng Dẫn Khởi Chạy Ứng Dụng

### 1. Cài đặt các thư viện phụ thuộc (nếu chưa cài)
```bash
pip install -r web/requirements.txt
```

### 2. Khởi chạy FastAPI Backend Server
Mở một cửa sổ terminal và chạy lệnh:
```bash
python web/api_server.py
```
*Server sẽ lắng nghe tại: `http://127.0.0.1:8000`. Bạn có thể truy cập API Docs Swagger tại `http://127.0.0.1:8000/docs`.*

### 3. Khởi chạy Streamlit Frontend UI
Mở một cửa sổ terminal mới và chạy lệnh:
```bash
streamlit run web/app.py
```
*Giao diện trang web sẽ tự động mở trên trình duyệt tại `http://localhost:8501`.*

---

## ✨ Các Tính Năng Nổi Bật

1. **👨‍🏫 Giảng viên / TA Dashboard**:
   - Chọn bài giảng sẵn có hoặc tải lên/nhập nội dung slide tóm tắt.
   - Tùy chỉnh số lượng câu hỏi, độ khó (Dễ / Trung bình / Nâng cao), và dạng câu hỏi (Trắc nghiệm 4 lựa chọn, Đúng/Sai, Trả lời ngắn).
   - Đánh giá câu hỏi theo taxonomy mức độ tư duy (Nhận biết, Thông hiểu, Vận dụng, Phân tích).
   - Xuất bộ câu hỏi ra file Markdown (.md) hoặc JSON (.json) chỉ với 1 click.

2. **🎓 Sinh viên View**:
   - Làm bài test trực quan cuối buổi học.
   - Hệ thống gợi ý thông minh (AI Hint) hỗ trợ khi học viên gặp khó khăn.
   - Chấm điểm ngay lập tức (Instant Evaluation) kèm giải thích đáp án chi tiết và trích dẫn kiến thức bài học.

3. **📊 Thống kê Lỗ hổng Kiến thức (Class Knowledge Gap Matrix)**:
   - Thống kê tỷ lệ hoàn thành bài làm, điểm trung bình của lớp.
   - Nhận diện các chủ đề học viên hay làm sai nhất kèm theo khuyến nghị hành động cụ thể cho Giảng viên/TA trong buổi tiếp theo.

4. **⚡ Lớp Dự Phòng Thông Minh (Sandbox Fallback)**:
   - Streamlit UI được tích hợp cơ chế tự động chuyển sang Engine AI nội bộ nếu FastAPI server chưa được khởi chạy, đảm bảo trang web luôn hoạt động trơn tru không gián đoạn!
