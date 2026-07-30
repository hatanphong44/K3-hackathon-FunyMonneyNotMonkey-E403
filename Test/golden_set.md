# Golden Set

## TC01
- Nhóm: Normal
- Input: Slide PDF chỉ có text, transcript đầy đủ
- Mục tiêu kiểm thử: Kiểm tra trường hợp chuẩn
- Kết quả mong đợi: Sinh đúng 10 câu hỏi, đúng đáp án, đúng format
- Metric: Accuracy, Format
- Keywords: prompt engineering, few-shot prompting, chain-of-thought, hallucination

## TC02
- Nhóm: Normal
- Input: Slide tiếng Việt
- Mục tiêu kiểm thử: Kiểm tra hỗ trợ tiếng Việt
- Kết quả mong đợi: Quiz bám sát nội dung bài học
- Metric: Accuracy
- Keywords: tiếng Việt, bài học, nội dung

## TC03
- Nhóm: Normal
- Input: Slide tiếng Anh
- Mục tiêu kiểm thử: Kiểm tra hỗ trợ tiếng Anh
- Kết quả mong đợi: Quiz tiếng Anh chính xác
- Metric: Accuracy
- Keywords: tiếng Anh, evaluation, guardrails

## TC04
- Nhóm: Normal
- Input: Buổi học ngắn (~20 phút)
- Mục tiêu kiểm thử: Kiểm tra nội dung ít
- Kết quả mong đợi: Sinh đủ 10 câu, không lặp
- Metric: Coverage
- Keywords: prompt, temperature, system prompt

## TC05
- Nhóm: Normal
- Input: Buổi học dài (~2 giờ)
- Mục tiêu kiểm thử: Kiểm tra nội dung nhiều
- Kết quả mong đợi: Bao phủ đầy đủ các ý chính
- Metric: Coverage
- Keywords: architecture, retrieval, evaluation, safety

## TC06
- Nhóm: Normal
- Input: Slide nhiều bullet
- Mục tiêu kiểm thử: Kiểm tra trích ý chính
- Kết quả mong đợi: Không bỏ sót các nội dung quan trọng
- Metric: Coverage
- Keywords: retrieval, re-ranking, citation tracing

## TC07
- Nhóm: Normal
- Input: Slide có code Python
- Mục tiêu kiểm thử: Kiểm tra hiểu code
- Kết quả mong đợi: Sinh câu hỏi đúng về đoạn code
- Metric: Accuracy
- Keywords: Python, prompt template, JSON output

## TC08
- Nhóm: Normal
- Input: Slide có hình minh họa và text
- Mục tiêu kiểm thử: Kiểm tra kết hợp nhiều nguồn
- Kết quả mong đợi: Không bỏ qua nội dung text
- Metric: Coverage
- Keywords: RAG, architecture, data flow

## TC09
- Nhóm: Normal
- Input: Transcript có phần hỏi đáp giữa mentor và học viên
- Mục tiêu kiểm thử: Kiểm tra khai thác transcript
- Kết quả mong đợi: Có câu hỏi từ phần giải thích của mentor
- Metric: Coverage
- Keywords: prompt injection, taxonomy, mentor

## TC10
- Nhóm: Normal
- Input: Bài học có nhiều khái niệm
- Mục tiêu kiểm thử: Kiểm tra phân bố câu hỏi
- Kết quả mong đợi: Quiz bao phủ nhiều chủ đề, không tập trung vào một phần
- Metric: Coverage
- Keywords: prompt, retrieval, embedding, cosine similarity

## TC11
- Nhóm: Input
- Input: PDF scan bị lỗi OCR
- Mục tiêu kiểm thử: Kiểm tra khả năng chịu lỗi
- Kết quả mong đợi: Sinh quiz nếu đủ dữ liệu hoặc cảnh báo thiếu dữ liệu
- Metric: Robustness
- Keywords: OCR, scan, dữ liệu thiếu

## TC12
- Nhóm: Input
- Input: Transcript bị thiếu khoảng 30%
- Mục tiêu kiểm thử: Kiểm tra dữ liệu thiếu
- Kết quả mong đợi: Không tự tạo thông tin ngoài tài liệu
- Metric: Hallucination
- Keywords: transcript, thiếu nội dung, groundedness

## TC13
- Nhóm: Knowledge
- Input: Slide ít nội dung, transcript đầy đủ
- Mục tiêu kiểm thử: Kiểm tra kết hợp nguồn
- Kết quả mong đợi: Lấy thông tin chính từ transcript
- Metric: Groundedness
- Keywords: transcript, evaluation, faithfulness

## TC14
- Nhóm: Knowledge
- Input: Transcript ngắn, slide đầy đủ
- Mục tiêu kiểm thử: Kiểm tra ưu tiên slide
- Kết quả mong đợi: Sinh câu hỏi đúng theo slide
- Metric: Groundedness
- Keywords: slide, RAG, vector database

## TC15
- Nhóm: Reasoning
- Input: Có hai khái niệm gần giống
- Mục tiêu kiểm thử: Kiểm tra suy luận
- Kết quả mong đợi: Không nhầm lẫn giữa hai khái niệm
- Metric: Accuracy
- Keywords: temperature, sampling

## TC16
- Nhóm: Reasoning
- Input: Decision Tree và Random Forest
- Mục tiêu kiểm thử: Kiểm tra phân biệt khái niệm
- Kết quả mong đợi: Không trộn lẫn đặc điểm
- Metric: Accuracy
- Keywords: decision tree, random forest

## TC17
- Nhóm: Output
- Input: 10 câu, mỗi câu 4 đáp án
- Mục tiêu kiểm thử: Kiểm tra format
- Kết quả mong đợi: Đúng định dạng
- Metric: Format Compliance
- Keywords: format, options, answer key

## TC18
- Nhóm: Output
- Input: Nội dung dễ sinh câu hỏi trùng
- Mục tiêu kiểm thử: Kiểm tra trùng lặp
- Kết quả mong đợi: Không có câu hỏi trùng
- Metric: Duplicate Rate
- Keywords: duplicate, repeated questions

## TC19
- Nhóm: Rare
- Input: Slide gần như chỉ có hình
- Mục tiêu kiểm thử: Kiểm tra dữ liệu không đủ
- Kết quả mong đợi: Thông báo thiếu dữ liệu
- Metric: Robustness
- Keywords: hình ảnh, thiếu text, thiếu dữ liệu

## TC20
- Nhóm: Rare
- Input: Slide và transcript mâu thuẫn
- Mục tiêu kiểm thử: Kiểm tra xử lý xung đột
- Kết quả mong đợi: Ưu tiên nguồn đáng tin cậy
- Metric: Groundedness
- Keywords: conflict, faithfulness, answer relevance
