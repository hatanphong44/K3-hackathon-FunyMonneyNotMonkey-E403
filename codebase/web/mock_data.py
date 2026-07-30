"""
Mock data and dynamic quiz generation engine for VLearn AI Quiz Generator.
Provides lecture presets, custom content parsing, and rule-based AI quiz synthesis.
"""

import re
import random
from typing import List, Dict, Any

SAMPLE_LECTURES = [
    {
        "id": "lec-01",
        "title": "Bài 01: Tổng quan về Prompt Engineering & LLM Architecture",
        "topic": "Prompt Engineering",
        "summary": "Bài giảng giới thiệu nguyên lý hoạt động của Large Language Models (LLM), kỹ thuật Zero-shot, Few-shot prompting, Chain of Thought (CoT), và các phương pháp phòng chống Hallucination (ảo giác AI). Thảo luận vai trò của Temperature và System Prompt.",
        "key_points": [
            "LLM dự đoán token tiếp theo dựa trên xác suất.",
            "Few-shot prompting cung cấp ví dụ mẫu giúp mô hình định hình format output.",
            "Chain-of-Thought khuyến khích mô hình suy luận theo từng bước nhỏ.",
            "Temperature cao (e.g. 0.8) tăng sự sáng tạo, Temperature thấp (e.g. 0.1) tăng tính chính xác."
        ]
    },
    {
        "id": "lec-02",
        "title": "Bài 02: Kỹ thuật Retrieval-Augmented Generation (RAG) & Vector Database",
        "topic": "RAG & Vector DB",
        "summary": "Phân tích kiến trúc RAG nâng cao: Chunking strategy, Text Embeddings, Similarity Metrics (Cosine, Dot Product), Vector Database (Pinecone, Qdrant, Chroma), Re-ranking và Citation Tracing trong AI Tutor.",
        "key_points": [
            "RAG giúp kết hợp tri thức riêng tư/mới nhất mà không cần fine-tune mô hình.",
            "Chunking với overlap giúp giữ ngữ cảnh nguyên vẹn giữa các đoạn văn.",
            "Cosine Similarity đo góc giữa 2 vector chỉ hướng ngữ nghĩa.",
            "Re-ranking (Cross-Encoder) cải thiện thứ tự kết quả tìm kiếm trước khi đưa vào LLM."
        ]
    },
    {
        "id": "lec-03",
        "title": "Bài 03: Đánh giá Mô hình (Evaluation) & Guardrails trong AI Sản Phẩm",
        "topic": "AI Evaluation & Safety",
        "summary": "Quy trình kiểm thử sản phẩm AI: LLM-as-a-Judge, Ragas Framework, Faithfulness, Answer Relevance, Context Precision, và triển khai Guardrails ngăn chặn Prompt Injection.",
        "key_points": [
            "Faithfulness đo lường mức độ trung thực của câu trả lời so với tài liệu gốc.",
            "LLM-as-a-Judge dùng mô hình mạnh để chấm điểm tự động các câu trả lời ngắn.",
            "Prompt Injection là nguy cơ bảo mật hàng đầu với ứng dụng LLM.",
            "Taxonomy chỗ khó gồm: Nguồn sự thật, Mơ hồ thiếu thông tin, Thẩm quyền và Đặc thù Domain."
        ]
    }
]

# Question Templates database for realistic synthesis
QUESTION_TEMPLATES = [
    {
        "type": "multiple_choice",
        "tax_level": "Nhận biết",
        "question": "Khái niệm chính được đề cập trong bài giảng là gì?",
        "options": [
            "Tối ưu hóa thời gian tính toán của mô hình",
            "Ứng dụng và nguyên lý hoạt động của giải pháp AI trong thực tế",
            "Thay thế hoàn toàn con người bằng tự động hóa",
            "Chỉ áp dụng cho bài toán phân loại hình ảnh"
        ],
        "correct": 1,
        "explanation": "Nội dung bài giảng tập trung vào ứng dụng, kỹ thuật cốt lõi và nguyên lý vận hành của AI trong thực tiễn.",
        "hint": "Hãy chú ý đến các điểm tổng quan được nhấn mạnh ở đầu bài học."
    },
    {
        "type": "multiple_choice",
        "tax_level": "Thông hiểu",
        "question": "Theo tài liệu bài giảng, ưu điểm vượt trội của phương pháp được thảo luận là gì?",
        "options": [
            "Không tốn chi phí phần cứng",
            "Cải thiện độ chính xác và khả năng truy vết trích dẫn nguồn tri thức",
            "Loại bỏ 100% rủi ro ảo giác AI",
            "Không yêu cầu dữ liệu đầu vào"
        ],
        "correct": 1,
        "explanation": "Phương pháp này giúp mô hình đưa ra câu trả lời dựa trên trích dẫn căn cứ và nguồn sự thật rõ ràng.",
        "hint": "Xem xét yếu tố kiểm soát Nguồn sự thật (Source of Truth)."
    },
    {
        "type": "true_false",
        "tax_level": "Thông hiểu",
        "question": "Đúng hay Sai: Việc thiết lập tham số temperature tiệm cận 0 sẽ làm tăng tính biến thiên và sáng tạo của câu trả lời?",
        "options": ["Đúng", "Sai"],
        "correct": 1,
        "explanation": "Sai. Temperature gần 0 làm mô hình hội tụ vào đáp án có xác suất cao nhất, giúp tăng tính nhất quán và chính xác chứ không làm tăng tính ngẫu nhiên sáng tạo.",
        "hint": "Nhớ lại quy tắc: Temperature càng cao -> Càng sáng tạo; Temperature càng thấp -> Càng chính xác."
    },
    {
        "type": "multiple_choice",
        "tax_level": "Vận dụng",
        "question": "Khi hệ thống gặp tình huống sinh viên hỏi câu hỏi ngoài phạm vi bài giảng, giải pháp hợp lý nhất là gì?",
        "options": [
            "Bịa ra thông tin để trả lời cho đầy đủ",
            "Từ chối khéo léo, giải thích phạm vi chuyên môn và gợi ý giảng viên/TA hỗ trợ",
            "Bỏ qua câu hỏi và không phản hồi",
            "Thay đổi chủ đề câu hỏi sang nội dung khác"
        ],
        "correct": 1,
        "explanation": "Xử lý tình huống Ngoài phạm vi / Thẩm quyền cần từ chối minh bạch và định hướng kênh hỗ trợ thích hợp.",
        "hint": "Xem quy tắc xử lý trường hợp 'Ngoài phạm vi / thẩm quyền' trong thiết kế AI Tutor."
    },
    {
        "type": "short_answer",
        "tax_level": "Phân tích",
        "question": "Nêu 2 chỉ số quan trọng để đánh giá chất lượng câu trả lời của AI Tutor dựa trên tài liệu bài giảng?",
        "answer_key": "Faithfulness (Độ trung thực) và Context Relevance / Answer Relevance (Độ liên quan context)",
        "explanation": "Faithfulness đảm bảo AI không bịa thông tin so với context; Answer Relevance đảm bảo AI trả lời đúng trọng tâm câu hỏi.",
        "hint": "Hai chỉ số này thuộc khung đánh giá Ragas."
    }
]

def generate_quiz_from_content(
    content: str,
    lecture_title: str = "Bài giảng custom",
    num_questions: int = 5,
    difficulty: str = "Trung bình",
    question_types: List[str] = None
) -> Dict[str, Any]:
    """
    Generates a structured quiz object based on input text and configuration.
    """
    if not question_types:
        question_types = ["multiple_choice", "true_false", "short_answer"]

    lines = [line.strip() for line in content.split("\n") if line.strip()]
    keywords = re.findall(r'\b[A-Za-z0-9ĐđÀ-ỹ]{4,}\b', content)
    unique_keywords = list(set(keywords))[:10]

    questions = []

    # Generate custom dynamic questions based on text extracted key lines
    for i in range(num_questions):
        q_type = question_types[i % len(question_types)]

        if i < len(lines) and len(lines[i]) > 15:
            topic_snippet = lines[i][:90] + ("..." if len(lines[i]) > 90 else "")
        elif unique_keywords:
            kw = unique_keywords[i % len(unique_keywords)]
            topic_snippet = f"chủ đề quan trọng liên quan đến '{kw}'"
        else:
            topic_snippet = "nội dung kiến thức cốt lõi trong bài giảng"

        if q_type == "multiple_choice":
            raw_opts = [
                f"Là thành phần cốt lõi giúp hệ thống vận hành chính xác và duy trì tính nhất quán.",
                f"Là khái niệm chỉ áp dụng trong lý thuyết, không có giá trị thực tiễn.",
                f"Là kỹ thuật cũ đã bị thay thế hoàn toàn bởi các công nghệ hiện đại khác.",
                f"Là tham số cố định không thể điều chỉnh trong mô hình."
            ]
            indexed = list(enumerate(raw_opts))
            random.shuffle(indexed)
            shuffled_opts = [opt for _, opt in indexed]
            correct_idx = next(new_i for new_i, (orig_i, _) in enumerate(indexed) if orig_i == 0)
            correct_letter = chr(65 + correct_idx)
            
            q_obj = {
                "id": f"q-{i+1}",
                "type": "multiple_choice",
                "difficulty": difficulty,
                "tax_level": random.choice(["Nhận biết", "Thông hiểu", "Vận dụng"]),
                "question": f"Câu {i+1}: Dựa trên bài giảng, phát biểu nào sau đây đúng nhất về {topic_snippet}?",
                "options": shuffled_opts,
                "correct": correct_idx,
                "explanation": f"Đáp án {correct_letter} đúng. Bài giảng nhấn mạnh tầm quan trọng của {topic_snippet} đối với hiệu quả tổng thể.",
                "hint": f"Hãy tìm các từ khóa chính liên quan đến '{unique_keywords[i % len(unique_keywords)] if unique_keywords else 'kiến thức'}' trong tài liệu."
            }
        elif q_type == "true_false":
            is_true = (i % 2 == 0)
            q_obj = {
                "id": f"q-{i+1}",
                "type": "true_false",
                "difficulty": difficulty,
                "tax_level": "Thông hiểu",
                "question": f"Câu {i+1}: Phát biểu: '{topic_snippet}' đóng vai trò nền tảng trong quy trình học tập cuối buổi.",
                "options": ["Đúng", "Sai"],
                "correct": 0 if is_true else 1,
                "explanation": f"Khẳng định này là {'Đúng' if is_true else 'Sai'} theo nội dung phân tích trong bài giảng.",
                "hint": "Đối chiếu phát biểu với phần tóm tắt lý thuyết chính của buổi học."
            }
        else:
            q_obj = {
                "id": f"q-{i+1}",
                "type": "short_answer",
                "difficulty": difficulty,
                "tax_level": "Phân tích",
                "question": f"Câu {i+1}: Tóm tắt ngắn gọn (1-2 câu) ý nghĩa của {topic_snippet} đối với bài học hôm nay?",
                "answer_key": f"Giúp hiểu rõ nguyên lý, nắm bắt Nguồn sự thật và áp dụng vào bài tập thực hành.",
                "explanation": "Câu trả lời cần thể hiện được mối liên hệ giữa lý thuyết và ứng dụng thực tiễn.",
                "hint": "Nêu 2 từ khóa quan trọng nhất mà giảng viên đã nhấn mạnh."
            }

        questions.append(q_obj)

    return {
        "title": f"Quiz Đánh Giá Cuối Buổi: {lecture_title}",
        "total_questions": len(questions),
        "difficulty": difficulty,
        "estimated_minutes": len(questions) * 2,
        "questions": questions
    }
