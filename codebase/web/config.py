import os

API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", 8000))
API_BASE_URL = os.getenv("API_BASE_URL", f"http://{API_HOST}:{API_PORT}/api/v1")

APP_TITLE = "VLearn AI Quiz Generator"
APP_SUBTITLE = "Hệ thống AI Tạo & Kiểm Tra Kiến Thức Cuối Buổi Học dành cho Sinh Viên & Giảng Viên"
