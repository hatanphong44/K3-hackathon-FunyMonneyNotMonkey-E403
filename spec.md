## §1. User & Job

### User

- **Primary user:** Học viên tham gia khóa học AI Thực Chiến.
- **Bối cảnh:** Sau mỗi buổi học lý thuyết, học viên nhận được slide và transcript của bài giảng. Trước khi làm bài tập hoặc tham gia buổi học tiếp theo, họ cần ôn lại kiến thức và kiểm tra xem mình đã hiểu bài đến đâu.

### Job executor + workflow

**Workflow hiện tại**

1. Tham gia buổi học lý thuyết.
2. Nhận slide buổi học.
3. Đọc lại tài liệu hoặc xem lại ghi chú.
4. Tự ghi nhớ các kiến thức quan trọng.
5. Làm bài tập hoặc chuẩn bị cho buổi học tiếp theo.

**Pain points**

- Không biết mình đã thực sự hiểu bài hay chưa.
- Khó xác định nội dung nào là kiến thức trọng tâm cần ghi nhớ.
- Việc tự tạo câu hỏi để ôn tập mất nhiều thời gian.
- Thiếu động lực ôn tập vì không có cách tự đánh giá nhanh sau mỗi buổi học.

### Core JTBD

> Khi hoàn thành một buổi học lý thuyết, tôi muốn nhanh chóng tự kiểm tra mức độ hiểu bài để biết mình còn thiếu những kiến thức nào trước khi học tiếp hoặc làm bài tập.

### Problem Statement

> Sau mỗi buổi học lý thuyết, học viên chưa có một cách nhanh chóng và thuận tiện để tự đánh giá mức độ hiểu bài, dẫn đến việc ôn tập kém hiệu quả và dễ bỏ sót các kiến thức quan trọng trước khi làm bài tập hoặc tham gia buổi học tiếp theo.

### Evidence

**Khảo sát (dự kiến)**

- Đối tượng khảo sát: Học viên khóa AI Thực Chiến.
- Số lượng mẫu (n): 20
- 90%  học viên học xong chưa hiểu bài.
- 100% học viên mong muốn có một bài kiểm tra ngắn ngay sau mỗi buổi học.(chọn mức 3 trở lên)

**Quotes**

> "Bạn có từng gặp tình huống học xong nhưng vẫn không biết mình đã hiểu đúng bài chưa?" - "Có"

> "Bạn thường kiểm tra lại kiến thức bằng cách nào?" - "Đọc lại slide"

> "Bạn thường phát hiện mình hiểu sai kiến thức khi nào?" - "Khi làm Quiz"

> "Sau khi học xong một buổi lý thuyết, bạn có chắc mình đã hiểu đúng toàn bộ nội dung không?" - "4/5"

> "Bạn có từng gặp tình huống học xong nhưng vẫn không biết mình đã hiểu đúng bài chưa?" - "Có"

## §2. Impact & quyết định chọngit add .

### Bảng đánh giá các vấn đề

| Vấn đề | Số người bị ảnh hưởng | Tần suất | Chi phí mỗi lần | Khả thi |
|--------|----------------------|----------|-----------------|----------|
| Khó tự đánh giá mức độ hiểu bài sau buổi học | Cao | Sau mỗi buổi học | Ôn tập kém hiệu quả, dễ quên kiến thức | Cao |
| Khó tìm lại nội dung trong slide và transcript | Trung bình | Khi cần ôn tập hoặc làm bài | Mất thời gian tìm kiếm thông tin | Cao |
| Khó tạo bộ câu hỏi để ôn tập | Trung bình | Sau mỗi buổi học | Mất nhiều thời gian chuẩn bị câu hỏi | Cao |

### Ứng viên đã loại

#### 1. Tìm kiếm nội dung trong slide và transcript

- **Lý do loại:** Đã có nhiều công cụ hỗ trợ tìm kiếm hoặc hỏi đáp trên tài liệu (NotebookLM, ChatGPT, Gemini...). Giá trị khác biệt của sản phẩm không cao.

#### 2. Tóm tắt bài giảng

- **Lý do loại:** Nhiều mô hình AI hiện nay đã thực hiện tốt việc tóm tắt tài liệu. Người dùng vẫn chưa biết mình đã hiểu bài hay chưa sau khi đọc bản tóm tắt.

### Ứng viên được chọn

**Vấn đề được chọn:** Học viên khó tự đánh giá mức độ hiểu bài sau mỗi buổi học lý thuyết.

**Lý do lựa chọn**

- Xảy ra sau hầu hết các buổi học.
- Ảnh hưởng trực tiếp đến hiệu quả ôn tập và khả năng hoàn thành bài tập.
- Có thể giải quyết bằng một prototype đơn giản: tạo bộ câu hỏi trắc nghiệm từ slide và transcript để người học tự kiểm tra kiến thức.
- Dễ đánh giá chất lượng thông qua tỷ lệ câu hỏi đúng, mức độ bao phủ nội dung và phản hồi của người dùng.


## §3. Giải pháp tương tự đã nghiên cứu

### 1. Google NotebookLM

**Flow**

- Người dùng tải slide hoặc tài liệu lên NotebookLM.
- Đặt câu hỏi về nội dung tài liệu.
- AI trả lời dựa trên tài liệu và có thể tạo Study Guide hoặc Quiz.

**Đáng học**

- Chỉ sử dụng thông tin trong tài liệu đã tải lên.
- Có khả năng tạo câu hỏi ôn tập và study guide tự động.
- Dẫn nguồn (citation) giúp người học kiểm tra lại kiến thức.

**Đáng né**

- Người dùng phải chủ động yêu cầu tạo quiz.
- Câu hỏi còn khá tổng quát, chưa tối ưu cho từng buổi học.
- Chưa có workflow "học xong → làm quiz ngay".

**Điểm khác biệt của nhóm**

- Tự động sinh quiz ngay sau mỗi buổi học.
- Tập trung vào nội dung của từng bài giảng trong khóa học.
- Thiết kế để người học kiểm tra kiến thức ngay sau khi học, thay vì phải chủ động yêu cầu AI.

---

### 2. Quizlet AI

**Flow**

- Người dùng tải tài liệu hoặc nhập ghi chú.
- AI tạo Flashcards và câu hỏi luyện tập.
- Người học làm quiz và xem kết quả.

**Đáng học**

- Chuyển tài liệu thành câu hỏi nhanh.
- Có nhiều chế độ luyện tập giúp tăng khả năng ghi nhớ.
- Giao diện đơn giản, dễ sử dụng.

**Đáng né**

- Chủ yếu phục vụ học từ vựng hoặc ghi nhớ.
- Chưa tận dụng transcript của bài giảng.
- Không đánh giá mức độ bao phủ kiến thức của toàn bộ bài học.

**Điểm khác biệt của nhóm**

- Sử dụng đồng thời slide và transcript để tạo câu hỏi.
- Hướng đến việc kiểm tra mức độ hiểu bài thay vì chỉ ghi nhớ thông tin.

---

### 3. ChatGPT / Gemini

**Flow**

- Người dùng tải slide hoặc transcript.
- Viết prompt yêu cầu AI tạo câu hỏi trắc nghiệm.
- AI sinh bộ câu hỏi theo yêu cầu.

**Đáng học**

- Chất lượng câu hỏi tốt nếu prompt rõ ràng.
- Linh hoạt, có thể điều chỉnh số lượng và mức độ khó.
- Hỗ trợ nhiều định dạng câu hỏi.

**Đáng né**

- Người dùng phải tự viết prompt.
- Chất lượng phụ thuộc vào cách đặt yêu cầu.
- Không có quy trình cố định cho việc ôn tập sau mỗi buổi học.

**Điểm khác biệt của nhóm**

- Không yêu cầu người học viết prompt.
- Tự động tạo bộ câu hỏi theo một quy trình thống nhất.
- Tập trung giải quyết bài toán ôn tập sau mỗi buổi học lý thuyết của khóa AI Thực Chiến.

## §4. Thiết kế

### Lát cắt

**Học viên sau khi hoàn thành một buổi học lý thuyết tải slide và transcript lên hệ thống, AI tự động tạo bộ câu hỏi trắc nghiệm để học viên tự kiểm tra mức độ hiểu bài.**

---

### Non-goals

Prototype **không** hướng tới các chức năng sau:

- Không xây dựng chatbot hỏi đáp toàn bộ nội dung khóa học.
- Không cá nhân hóa lộ trình học cho từng học viên.
- Không thay thế bài kiểm tra chính thức của khóa học.
- Không đánh giá toàn diện năng lực người học.
- Không hỗ trợ nhiều định dạng tài liệu ngoài PDF (giai đoạn prototype).

---

### Mức prototype nhắm tới

- [ ] Sketch
- [x] Mock
- [ ] Working

**Phần hoạt động thật**

- Upload slide PDF.
- Upload transcript PDF hoặc TXT.
- AI tạo bộ câu hỏi trắc nghiệm.
- Hiển thị câu hỏi và đáp án cho người dùng.

**Phần mock**

- Không lưu lịch sử học tập.
- Không tích hợp với hệ thống LMS.
- Không có tài khoản người dùng.

---

### Automation

- [x] Augment
- [ ] Conditional
- [ ] Automate

**Lý do**

Việc đánh giá mức độ hiểu bài là quyết định có ảnh hưởng trực tiếp đến quá trình học của người dùng. AI chỉ đóng vai trò hỗ trợ tạo câu hỏi để người học tự kiểm tra, thay vì tự động kết luận người học đã hiểu hay chưa. Người dùng vẫn là người quyết định kết quả cuối cùng.

---

### §4b. Nguyên tắc đã áp dụng

| Nguyên tắc | Áp dụng trong prototype |
|------------|-------------------------|
| Transparency | Hiển thị nguồn dữ liệu được sử dụng (slide và transcript) để người dùng biết AI tạo câu hỏi dựa trên tài liệu nào. |
| Support, don't replace | AI hỗ trợ tạo câu hỏi ôn tập, không thay thế việc học hoặc đánh giá chính thức. |
| Error Recovery | Người dùng có thể tạo lại bộ câu hỏi nếu kết quả chưa phù hợp hoặc sau khi cập nhật tài liệu. |