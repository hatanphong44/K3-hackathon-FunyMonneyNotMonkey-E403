# Reflection cá nhân

## Vai trò và đóng góp

Trong dự án này, tôi phụ trách ba công việc chính là thiết kế **system prompt**, thu thập và tổng hợp **dữ liệu khảo sát người dùng**, đồng thời viết và hoàn thiện **spec.md**. Tôi xây dựng các ràng buộc để AI chỉ sử dụng thông tin trong slide và transcript khi tạo câu hỏi, đồng thời điều chỉnh prompt qua nhiều lần thử nghiệm để cải thiện chất lượng đầu ra.

Ngoài ra, tôi tổng hợp kết quả khảo sát để xây dựng phần **Evidence** và **Impact**, xác định phạm vi sản phẩm, các tiêu chí đánh giá, Golden Test Set và Quality Bar trong tài liệu đặc tả. Những công việc này giúp kết nối giữa nhu cầu của người dùng và giải pháp kỹ thuật mà nhóm xây dựng.

## Điều học được

Qua dự án, tôi nhận ra rằng phát triển một sản phẩm AI không chỉ là gọi API của mô hình ngôn ngữ mà còn cần bắt đầu từ việc tìm hiểu nhu cầu thực tế của người dùng. Việc xác định đúng bài toán, thu thập bằng chứng và xây dựng tiêu chí đánh giá rõ ràng quan trọng không kém việc xây dựng mô hình hay viết code.

Tôi cũng học được cách thiết kế một system prompt hiệu quả hơn. Một prompt tốt không chỉ mô tả yêu cầu mà còn phải có các ràng buộc để hạn chế mô hình tạo thông tin ngoài tài liệu và đảm bảo đầu ra có định dạng ổn định. Bên cạnh đó, việc xây dựng Golden Test Set giúp tôi hiểu tầm quan trọng của kiểm thử có hệ thống thay vì chỉ đánh giá bằng một vài ví dụ.

## Khó khăn

Khó khăn lớn nhất của tôi là thiết kế prompt để AI tạo ra các câu hỏi vừa chính xác, vừa bao phủ được nội dung bài học mà không sinh thêm thông tin ngoài slide và transcript. Với những buổi học có nhiều khái niệm tương tự hoặc transcript dài, mô hình đôi khi vẫn tạo ra những câu hỏi chưa thực sự phù hợp.

Ngoài ra, việc sử dụng API miễn phí khiến thời gian xử lý khá lâu khi phải đọc toàn bộ slide và transcript của một buổi học. Điều này buộc nhóm phải cân nhắc giữa tốc độ và chất lượng trong phạm vi của prototype.

## Điều sẽ cải thiện

Nếu có thêm thời gian, tôi sẽ tiếp tục tối ưu system prompt để tăng độ bao phủ nội dung, giảm câu hỏi trùng lặp và cải thiện chất lượng đáp án. Tôi cũng muốn nghiên cứu thêm các phương pháp tiền xử lý tài liệu để giảm thời gian sinh quiz và nâng cao trải nghiệm của người dùng.

Bên cạnh đó, tôi muốn mở rộng quá trình validation với nhiều học viên và mentor hơn để thu thập thêm phản hồi thực tế, từ đó tiếp tục cải thiện sản phẩm theo đúng nhu cầu của người dùng.

## Kết luận

Dự án giúp tôi hiểu rõ hơn toàn bộ quy trình phát triển một sản phẩm AI, từ khảo sát người dùng, xác định bài toán, thiết kế giải pháp, xây dựng system prompt cho đến kiểm thử và đánh giá chất lượng. Đây là một trải nghiệm thực tế giúp tôi rèn luyện cả tư duy AI Product và kỹ năng làm việc với các mô hình ngôn ngữ, đồng thời mang lại nhiều kinh nghiệm hữu ích cho các dự án AI trong tương lai.