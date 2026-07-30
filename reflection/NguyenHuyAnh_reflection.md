# Reflection cá nhân — Nguyễn Huy Anh

## Vai trò và đóng góp

Trong dự án **Auto-Quiz Generator**, tôi phụ trách toàn bộ việc phát triển **Giao diện người dùng (UI) và API Backend** thuộc thư mục `codebase/web/`. Các công việc chính của tôi bao gồm:

* **Xây dựng ứng dụng Web tương tác (`app.py` & `ui_components.py`):** Thiết kế giao diện cho phép học viên dễ dàng chọn bài giảng hoặc tải lên Slide (PDF) và Transcript (TXT/PDF), tùy chỉnh số lượng câu hỏi và độ khó.
* **Xây dựng luồng trải nghiệm Quiz:** Phát triển giao diện trắc nghiệm trực quan với các tính năng làm bài, đếm giờ, chọn đáp án, hiển thị kết quả chấm điểm tức thì, kèm phần giải thích chi tiết và trích dẫn nguồn (Citation) từ slide/transcript.
* **Tích hợp API Backend (`api_server.py`):** Kết nối giao diện người dùng với mô hình AI (Provider), xử lý bất đồng bộ, truyền nhận dữ liệu JSON schema và quản lý trạng thái phiên làm việc (Session State).
* **Xử lý dữ liệu thử nghiệm & Mock Data (`mock_data.py`):** Chuẩn bị dữ liệu mẫu các bài giảng để hỗ trợ quá trình test UI nhanh chóng khi không gọi API thật.

## Điều học được

Thực hiện dự án này giúp tôi nâng cao nhiều kỹ năng về lập trình giao diện sản phẩm AI:

* **Tối ưu trải nghiệm người dùng AI (AI UX):** Học cách hiển thị trạng thái chờ (Loading / Progress Bar) và thông báo minh bạch cho người dùng khi AI mất vài phút để đọc bài giảng và sinh câu hỏi.
* **Quản lý trạng thái tương tác phức tạp (Session State):** Xử lý luồng chuyển màn hình từ lúc upload tài liệu ➔ sinh quiz ➔ làm bài ➔ nộp bài & xem kết quả mà không làm mất dữ liệu người dùng khi re-render UI.
* **Chuẩn hóa dữ liệu JSON cho Frontend:** Hiểu tầm quan trọng của việc bắt buộc AI trả về đúng JSON Schema để giao diện render danh sách đáp án, đáp án đúng và trích dẫn nguồn một cách mượt mà, không bị crash lỗi giao diện.

## Khó khăn

* **Độ trễ API (Latency):** Do mô hình AI phải xử lý đồng thời cả tệp Slide PDF lớn và bản ghi Transcript dài, thời gian sinh câu hỏi còn khá lâu. Việc giữ chân người dùng trong lúc chờ đợi đòi hỏi giao diện phải phản hồi trạng thái minh bạch.
* **Đồng bộ hóa dữ liệu trích dẫn (Citation UI):** Việc hiển thị nguồn trích dẫn từ Slide số mấy hay đoạn Transcript nào đòi hỏi phải bóc tách dữ liệu chính xác từ AI và hiển thị sao cho trực quan, không làm rối mắt học viên.

## Điều sẽ cải thiện

Nếu có thêm thời gian phát triển sản phẩm, tôi sẽ tập trung vào các điểm sau:

* **Tối ưu tốc độ & Streaming UI:** Tích hợp Streaming API để hiển thị từng câu hỏi ngay khi AI vừa sinh xong thay vì phải chờ sinh xong toàn bộ 10 câu mới hiển thị.
* **Lưu trữ lịch sử & Caching:** Tích hợp cơ sở dữ liệu (SQLite/PostgreSQL) để lưu bộ Quiz đã sinh, giúp học viên quay lại ôn tập mà không cần gọi lại AI.
* **Tương thích thiết bị di động (Mobile Responsive):** Cải thiện giao diện UI để học viên có thể tiện lợi ôn bài và làm Quiz ngay trên điện thoại di động.

## Kết luận

Dự án là một trải nghiệm tuyệt vời giúp tôi gắn kết kiến thức phát triển Web/API với các công nghệ AI Agent tiên tiến. Việc đưa một ý tưởng AI Spec thành một sản phẩm có giao diện bấm được, làm bài thật và nhận phản hồi thực tế từ người dùng giúp tôi hiểu sâu sắc hơn về quy trình phát triển sản phẩm AI hoàn chỉnh.
