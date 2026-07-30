# Personal Reflection – Hà Tấn Phong

## Vai trò và đóng góp

Trong dự án, tôi phụ trách phần xây dựng hệ thống tạo câu hỏi trắc nghiệm từ tài liệu học tập. Các công việc chính bao gồm:

* Xây dựng lớp Provider để kết nối OpenRouter API.
* Đọc và xử lý tài liệu đầu vào từ các file Markdown và PDF.
* Chuẩn hóa kết quả trả về (difficulty, type, answer key, hint, explanation) để tương thích với UI.
* Kiểm thử với nhiều bộ tài liệu nhằm đánh giá chất lượng câu hỏi sinh ra.

## Điều học được

Thông qua dự án, tôi hiểu rõ hơn quy trình phát triển một ứng dụng sử dụng Large Language Model.

Một số kiến thức và kỹ năng tôi tích lũy được:

* Thiết kế prompt để mô hình tạo đầu ra có cấu trúc ổn định.
* Xử lý dữ liệu đầu vào từ nhiều định dạng tài liệu khác nhau.
* Kiểm soát đầu ra bằng JSON schema và hậu xử lý dữ liệu.
* Quản lý token, chi phí và giới hạn của API.
* Tổ chức mã nguồn theo hướng dễ bảo trì và mở rộng.

## Khó khăn

Việc sử dụng toàn bộ tài liệu lớn cũng gặp giới hạn về token. Tôi phải giới hạn kích thước dữ liệu đầu vào và tối ưu prompt để cân bằng giữa chất lượng câu hỏi và chi phí sử dụng API.

## Điều sẽ cải thiện

Nếu có thêm thời gian, tôi muốn phát triển hệ thống theo các hướng sau:

* Tích hợp RAG để chỉ truy xuất những đoạn tài liệu liên quan thay vì gửi toàn bộ nội dung.
* Hỗ trợ nhiều loại câu hỏi hơn như điền khuyết, tự luận và ghép nối.
* Đánh giá chất lượng câu hỏi bằng bộ tiêu chí và tập dữ liệu kiểm thử tự động.
* Cho phép sinh câu hỏi theo từng chương hoặc từng chủ đề thay vì toàn bộ tài liệu.

## Kết luận

Dự án giúp tôi có trải nghiệm thực tế trong việc xây dựng một ứng dụng AI hoàn chỉnh, từ xử lý dữ liệu, thiết kế prompt, tích hợp mô hình cho đến đánh giá kết quả. Đây cũng là cơ hội để tôi hiểu rõ hơn các giới hạn của mô hình ngôn ngữ và cách xây dựng hệ thống ổn định, dễ mở rộng trong thực tế.
