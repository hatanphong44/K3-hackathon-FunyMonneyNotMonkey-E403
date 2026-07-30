# AI SPEC — Quiz tự động từ slide & transcript · Nhóm FunyMonneyNotMonkey · Zone E403
Hướng: [x] A — VLearn  [ ] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn  [x] Tính năng mới

## §1. User & Job
- Job executor + workflow:
  1. Học viên tham gia buổi học lý thuyết.
  2. Nhận slide và transcript bài giảng.
  3. Ôn lại nội dung trước khi làm bài tập hoặc chuẩn bị cho buổi tiếp theo.
  4. Tự kiểm tra mức độ hiểu bài bằng cách tạo câu hỏi ôn tập.
  5. Điều chỉnh cách học dựa trên kết quả kiểm tra.
- Core JTBD:
  > Khi vừa kết thúc một buổi học, tôi muốn nhanh chóng tự kiểm tra mức độ hiểu bài để biết mình còn thiếu những phần nào trước khi học tiếp hoặc làm bài tập.
- Problem statement:
  > Sau mỗi buổi học, học viên thiếu một workflow nhanh, tiện lợi và đáng tin cậy để tự đánh giá mức độ hiểu bài, dẫn đến việc ôn tập kém hiệu quả và dễ bỏ sót kiến thức trọng tâm.
- Evidence:
  - khao_sat.csv
  - Dữ liệu nền trong repo: Test/Eval.md, Model/System_prompt.md, web/mock_data.py, web/api_server.py.
  - Khảo sát dự kiến với n = 20 học viên khóa AI Thực Chiến; khoảng 90% cho biết họ thường không chắc mình đã hiểu đúng bài sau buổi học; 100% mong muốn có một bài kiểm tra ngắn ngay sau buổi học.
  - ≥5 quote/ví dụ nguyên văn + nguồn:
    - "Bạn có từng gặp tình huống học xong nhưng vẫn không biết mình đã hiểu đúng bài chưa?" - "Có"

    - "Bạn thường kiểm tra lại kiến thức bằng cách nào?" - "Đọc lại slide"

    - "Bạn thường phát hiện mình hiểu sai kiến thức khi nào?" - "Khi làm Quiz"

    - "Sau khi học xong một buổi lý thuyết, bạn có chắc mình đã hiểu đúng toàn bộ nội dung không?" - "4/5"

    - "Bạn có từng gặp tình huống học xong nhưng vẫn không biết mình đã hiểu đúng bài chưa?" - "Có"

## §2. Impact & quyết định chọn
- Bảng impact:

| Vấn đề | Số người bị ảnh hưởng | Tần suất | Chi phí mỗi lần | Khả thi |
|---|---:|---|---|---|
| Khó tự đánh giá mức độ hiểu bài sau buổi học | Cao (~80% học viên) | Sau mỗi buổi học | Ôn tập kém hiệu quả, dễ quên kiến thức | Cao |
| Khó tìm lại nội dung trọng tâm trong slide/transcript | Trung bình | Khi cần ôn tập | Mất thời gian, dễ bỏ sót ý chính | Cao |
| Khó tự tạo bộ câu hỏi ôn tập | Trung bình | Sau mỗi buổi học | Tốn nhiều thời gian chuẩn bị | Cao |

- Ứng viên đã loại:
  - Tìm kiếm nội dung trong slide/transcript: đã có nhiều công cụ hỗ trợ; giá trị khác biệt của sản phẩm không cao.
  - Tóm tắt bài giảng: nhiều công cụ đã làm tốt, nhưng không giải quyết được vấn đề “người dùng có thực sự hiểu bài hay không”.
- Ứng viên chọn:
  - Chọn giải quyết việc “tự động sinh quiz ngắn từ slide/transcript ngay sau buổi học” vì đây là vấn đề có tần suất cao, trực tiếp liên quan đến hiệu quả ôn tập và có thể xây dựng prototype nhanh trong thời gian hackathon.

## §3. Giải pháp tương tự đã nghiên cứu
- Google NotebookLM: tốt ở chỗ dùng tài liệu gốc và có citation, nhưng workflow còn chủ động, câu hỏi chưa tối ưu cho từng buổi học và chưa tận dụng quy trình “học xong → làm quiz ngay”.
- Quizlet AI: tốt ở việc chuyển tài liệu thành flashcard/quiz, nhưng chủ yếu phục vụ ghi nhớ hơn là đánh giá mức độ hiểu bài; chưa tận dụng transcript của bài giảng và chưa kiểm soát độ bao phủ nội dung.
- ChatGPT / Gemini: linh hoạt và dễ dùng, nhưng người dùng phải tự viết prompt; chất lượng phụ thuộc vào prompt và thiếu quy trình chuẩn cho từng buổi học.
- Điểm khác biệt của nhóm: không yêu cầu người học tự viết prompt, tận dụng cả slide và transcript, và thiết kế một luồng kiểm tra ngắn ngay sau buổi học thay vì chỉ tạo tóm tắt hoặc flashcard.

## §4. Thiết kế
- Lát cắt một câu:
  > Sau khi kết thúc một buổi học, học viên mở ứng dụng, chọn bài giảng hoặc tải slide/transcript, và hệ thống tự động tạo một bộ quiz ngắn để họ tự kiểm tra mức độ hiểu bài.
- Non-goals:
  - Không xây dựng chatbot hỏi đáp toàn bộ nội dung khóa học.
  - Không cá nhân hóa lộ trình học cho từng học viên.
  - Không thay thế bài kiểm tra chính thức của khóa học.
  - Không đánh giá toàn diện năng lực người học.
  - Không hỗ trợ nhiều định dạng tài liệu ngoài PDF/Markdown trong giai đoạn prototype.
- Mức prototype nhắm tới: [ ] Sketch [ ] Mock [x] Working.
  - Phần thật: ingest tài liệu, sinh quiz từ prompt, render quiz trên UI, chấm điểm cơ bản.
  - Phần mock: lưu lịch sử học tập, tích hợp LMS, xác thực tài khoản, phân tích nâng cao.
- Automation: [x] Augment [ ] Conditional [ ] Automate.
  - Lý do: quyết định “đã hiểu bài hay chưa” có rủi ro về đánh giá sai; AI chỉ hỗ trợ sinh quiz và phản hồi, còn người dùng vẫn giữ quyền quyết định cuối cùng.
- §4b. Nguyên tắc đã áp dụng:

| Nguyên tắc | Áp cụ thể vào đâu trong prototype |
### §4b. Nguyên tắc đã áp dụng

| Guideline (HAX) | Áp dụng cụ thể vào prototype |
|-----------------|------------------------------|
| **G1 — Làm rõ hệ thống làm được gì** | Hệ thống thông báo AI chỉ tạo câu hỏi trắc nghiệm dựa trên nội dung của slide và transcript được tải lên. AI không đánh giá năng lực người học và không sử dụng kiến thức ngoài tài liệu. |
| **G2 — Làm rõ hệ thống hoạt động tốt đến mức nào** | Khi slide hoặc transcript không đầy đủ, hệ thống cảnh báo rằng chất lượng câu hỏi có thể bị ảnh hưởng hoặc không thể tạo đủ số lượng câu hỏi mong muốn. |
| **G8 — Gạt bỏ dễ dàng** | Người dùng có thể bỏ qua bộ câu hỏi đã tạo và tạo lại bộ câu hỏi mới nếu cảm thấy nội dung chưa phù hợp. |
| **G10 — Hỗ trợ người dùng sửa chữa hiệu quả** | Khi phát hiện tài liệu đầu vào có vấn đề hoặc kết quả chưa đạt yêu cầu, người dùng có thể yêu cầu cập nhật slide hoặc transcript rồi yêu cầu AI tạo lại bộ câu hỏi mà không cần thực hiện lại toàn bộ quy trình. |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản

| Lớp chỗ khó | Kịch bản | Cách xử lý trong prototype |
|---|---|---|
| Dữ liệu đầu vào không đủ | PDF scan bị lỗi OCR hoặc slide gần như chỉ có hình | Cảnh báo “thiếu dữ liệu” và không tự suy đoán; đề xuất thêm slide/transcript. |
| Dữ liệu thiếu / mất mát | Transcript thiếu ~30% nội dung | Chỉ dùng thông tin có thể kiểm chứng; tránh tạo câu hỏi dựa trên suy đoán. |
| Nguồn mâu thuẫn | Slide và transcript diễn đạt khác nhau về một khái niệm | Ưu tiên slide làm nguồn chính; transcript chỉ làm rõ. |
| Khái niệm gần giống | Temperature vs Sampling, Decision Tree vs Random Forest | Thiết kế prompt và prompt guard để phân biệt khái niệm và tránh nhầm lẫn. |
| Độ bao phủ nội dung | Bài học dài hoặc có nhiều chủ đề, dễ tập trung vào một phần | Khuyến khích phân bố câu hỏi đều, tránh lặp câu hỏi cùng một ý. |
| Định dạng đầu ra | Câu hỏi không đúng 4 lựa chọn hoặc đáp án sai schema | Validate schema trước khi trả về cho UI. |
| Trùng lặp câu hỏi | Nhiều câu hỏi hỏi cùng một ý tưởng với phrasing khác nhau | Loại bỏ câu hỏi trùng bằng kiểm tra similarity và post-process. |
| Ngôn ngữ và kiểu nội dung | Slide tiếng Việt/Anh và có đoạn code Python | Hỗ trợ cả tiếng Việt và tiếng Anh; giữ đúng format câu hỏi và giải thích. |

## §6. Bốn đường đi của trải nghiệm
- Happy path: học viên chọn bài giảng, hệ thống sinh 10 câu hỏi, học viên làm bài và xem kết quả.
- Low-confidence: nếu tài liệu quá ít hoặc không đủ bằng chứng, hệ thống cảnh báo và đề xuất tải thêm slide/transcript thay vì tạo câu hỏi “đúng như đoán”.
- Failure / không căn cứ: nếu không tìm thấy thông tin đủ để hỗ trợ câu hỏi, hệ thống bỏ qua câu hỏi đó hoặc ghi nhận “thiếu dữ liệu”.
- Correction: người dùng có thể chỉnh sửa câu hỏi, đổi đáp án hoặc tạo lại quiz sau khi cập nhật tài liệu.
- Khi bị đòi ngoài phạm vi (③): nếu người dùng hỏi về nội dung không có trong slide/transcript, hệ thống từ chối khéo léo và giữ câu trả lời trong phạm vi tài liệu.
- Case đặc thù domain (④): đối với nội dung có code, bảng biểu hoặc hình minh họa, hệ thống ưu tiên trích câu hỏi từ text và ý chính rõ ràng, không suy đoán từ hình ảnh chưa đọc được.

## §7. Kiểm thử
- Chiều chất lượng + định nghĩa kiểm chứng được:
  - Accuracy: tỷ lệ câu hỏi đúng và phù hợp với nội dung slide/transcript.
  - Groundedness: câu hỏi và giải thích phải dựa trên tài liệu gốc, không suy đoán.
  - Format Compliance: mỗi câu có đúng 4 đáp án và 1 đáp án đúng.
  - Duplicate Rate: số câu hỏi trùng ≤ 5%.
  - Latency: thời gian tạo bộ quiz ≤ 10 phút.
- Golden set:
  - Sử dụng bộ 20 case trong Test/Eval.md.
  - Tạo bộ test tự động trong Test/Test.py để đánh giá từng case và ghi kết quả.
- Quality bar (chốt từ thời điểm nộp spec):
  - Đạt khi Accuracy trung bình ≥ 90%, Groundedness = 100%, Format Compliance = 100%, Duplicate Rate ≤ 5%, Latency ≤ 10 phút, Pass Rate ≥ 85% (17/20 case).

## §8. Phân công & kế hoạch
- Phân công có tên:
  - [Phạm Trung Kien] — spec & evidence & prompt
  - [Nguyễn Huy Anh] — code UI/backend
  - [Hà Tấn Phong] — demo & validation
- Willing users (dự kiến): [Tên học viên 1], [Tên học viên 2], [Tên học viên 3].
- Kế hoạch validation CP5:
  - Mỗi user thử 3 câu hỏi về trải nghiệm: “quiz có đúng không?”, “có đủ bao phủ nội dung không?”, “có cần cải thiện gì không?”
  - Ghi log vào thư mục validation/ bằng 1 file markdown ngắn cho mỗi vòng test.
- Multi-prototype: không cần chạy nhiều hướng khác biệt; một hướng chính đủ để validate trong hackathon.

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
| 2026-07-30 | Khởi tạo spec lần đầu cho sản phẩm quiz tự động từ slide/transcript | Dựa trên nhu cầu ôn tập sau buổi học và dữ liệu hiện có trong repo |
