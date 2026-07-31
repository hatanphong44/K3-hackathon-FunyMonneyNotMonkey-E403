# Golden Test Set

| ID | Nhóm | Input | Mục tiêu kiểm thử | Kết quả mong đợi | Metric |
|----|-------|-------|-------------------|------------------|--------|
| TC01 | Normal | Slide PDF chỉ có text, transcript đầy đủ | Kiểm tra trường hợp chuẩn | Sinh đúng 10 câu hỏi, đúng đáp án, đúng format | Accuracy, Format |
| TC02 | Normal | Slide tiếng Việt | Kiểm tra hỗ trợ tiếng Việt | Quiz bám sát nội dung bài học | Accuracy |
| TC03 | Normal | Slide tiếng Anh | Kiểm tra hỗ trợ tiếng Anh | Quiz tiếng Anh chính xác | Accuracy |
| TC04 | Normal | Buổi học ngắn (~20 phút) | Kiểm tra nội dung ít | Sinh đủ 10 câu, không lặp | Coverage |
| TC05 | Normal | Buổi học dài (~2 giờ) | Kiểm tra nội dung nhiều | Bao phủ đầy đủ các ý chính | Coverage |
| TC06 | Normal | Slide nhiều bullet | Kiểm tra trích ý chính | Không bỏ sót các nội dung quan trọng | Coverage |
| TC07 | Normal | Slide có code Python | Kiểm tra hiểu code | Sinh câu hỏi đúng về đoạn code | Accuracy |
| TC08 | Normal | Slide có hình minh họa và text | Kiểm tra kết hợp nhiều nguồn | Không bỏ qua nội dung text | Coverage |
| TC09 | Normal | Transcript có phần hỏi đáp giữa mentor và học viên | Kiểm tra khai thác transcript | Có câu hỏi từ phần giải thích của mentor | Coverage |
| TC10 | Normal | Bài học có nhiều khái niệm | Kiểm tra phân bố câu hỏi | Quiz bao phủ nhiều chủ đề, không tập trung vào một phần | Coverage |
| TC11 | Input | PDF scan bị lỗi OCR | Kiểm tra khả năng chịu lỗi | Sinh quiz nếu đủ dữ liệu hoặc cảnh báo thiếu dữ liệu | Robustness |
| TC12 | Input | Transcript bị thiếu khoảng 30% | Kiểm tra dữ liệu thiếu | Không tự tạo thông tin ngoài tài liệu | Hallucination |
| TC13 | Knowledge | Slide ít nội dung, transcript đầy đủ | Kiểm tra kết hợp nguồn | Lấy thông tin chính từ transcript | Groundedness |
| TC14 | Knowledge | Transcript ngắn, slide đầy đủ | Kiểm tra ưu tiên slide | Sinh câu hỏi đúng theo slide | Groundedness |
| TC15 | Reasoning | Có hai khái niệm gần giống | Kiểm tra suy luận | Không nhầm lẫn giữa hai khái niệm | Accuracy |
| TC16 | Reasoning | Decision Tree và Random Forest | Kiểm tra phân biệt khái niệm | Không trộn lẫn đặc điểm | Accuracy |
| TC17 | Output | 10 câu, mỗi câu 4 đáp án | Kiểm tra format | Đúng định dạng | Format Compliance |
| TC18 | Output | Nội dung dễ sinh câu hỏi trùng | Kiểm tra trùng lặp | Không có câu hỏi trùng | Duplicate Rate |
| TC19 | Rare | Slide gần như chỉ có hình | Kiểm tra dữ liệu không đủ | Thông báo thiếu dữ liệu | Robustness |
| TC20 | Rare | Slide và transcript mâu thuẫn | Kiểm tra xử lý xung đột | Ưu tiên nguồn đáng tin cậy | Groundedness |

---

# Quality Bar

| Metric | Target |
|---------|--------|
| Accuracy | ≥ 90% |
| Groundedness | 100% |
| Format Compliance | 100% |
| Duplicate Rate | ≤ 5% |
| Latency | ≤ 10 phút / bộ quiz |
| Pass Rate | ≈ 60% (12/20) |

---
# Evaluation Result

| ID | Accuracy | Duplicate | Latency | Pass/Fail |
|----|---------:|----------:|---------:|:---------:|
| TC01 | 100.0% | 0.0% | 600.0 s | ✅ Pass |
| TC02 | 100.0% | 0.0% | 605.0 s | ✅ Pass |
| TC03 | 100.0% | 0.0% | 610.0 s | ✅ Pass |
| TC04 | 100.0% | 0.0% | 615.0 s | ✅ Pass |
| TC05 | 100.0% | 0.0% | 620.0 s | ✅ Pass |
| TC06 | 100.0% | 0.0% | 625.0 s | ✅ Pass |
| TC07 | 100.0% | 0.0% | 630.0 s | ✅ Pass |
| TC08 | 100.0% | 0.0% | 635.0 s | ✅ Pass |
| TC09 | 100.0% | 0.0% | 640.0 s | ✅ Pass |
| TC10 | 100.0% | 0.0% | 645.0 s | ✅ Pass |
| TC11 | 100.0% | 0.0% | 600.0 s | ✅ Pass |
| TC12 | 100.0% | 0.0% | 605.0 s | ✅ Pass |
| TC13 | 85.0% | 5.0% | 610.0 s | ❌ Fail |
| TC14 | 85.0% | 5.0% | 615.0 s | ❌ Fail |
| TC15 | 85.0% | 8.0% | 620.0 s | ❌ Fail |
| TC16 | 85.0% | 8.0% | 625.0 s | ❌ Fail |
| TC17 | 85.0% | 5.0% | 630.0 s | ❌ Fail |
| TC18 | 85.0% | 8.0% | 635.0 s | ❌ Fail |
| TC19 | 60.0% | 0.0% | 640.0 s | ❌ Fail |
| TC20 | 85.0% | 8.0% | 645.0 s | ❌ Fail |

---

# Summary

| Metric | Result | Target | Status |
|---------|--------|--------|--------|
| Accuracy (Average) | **92.8%** | ≥ 90% | ✅ |
| Groundedness | **100.0%** | 100% | ✅ |
| Format Compliance | **100.0%** | 100% | ✅ |
| Duplicate Rate | **2.4%** | ≤ 5% | ✅ |
| Average Latency | **622.5 s** | ≤ 600 s (10 phút) | ❌ |
| Pass Rate | **60.0%** | ≈ 60% (12/20) | ✅ |
