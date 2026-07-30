"""
FastAPI Backend Server for VLearn AI Quiz Generator.
Provides RESTful APIs for quiz generation, grading, analytics, and export.
"""

import sys
import os
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from web.mock_data import SAMPLE_LECTURES, generate_quiz_from_content

app = FastAPI(
    title="VLearn AI Quiz Generator API",
    description="FastAPI Backend cho Hệ Thống Tạo & Kiểm Tra Kiến Thức Cuối Buổi Học",
    version="1.0.0"
)

# Enable CORS for Streamlit / external frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateQuizRequest(BaseModel):
    lecture_id: Optional[str] = Field(None, description="ID bài giảng mẫu (e.g. lec-01)")
    custom_title: Optional[str] = Field("Bài giảng tùy chỉnh", description="Tiêu đề bài giảng")
    custom_content: Optional[str] = Field(None, description="Nội dung bài giảng / Slide / Transcript")
    num_questions: int = Field(5, ge=1, le=15, description="Số lượng câu hỏi cần tạo")
    difficulty: str = Field("Trung bình", description="Độ khó: Dễ, Trung bình, Nâng cao")
    question_types: List[str] = Field(["multiple_choice", "true_false"], description="Các dạng câu hỏi")


class GenerateStudentQuizRequest(BaseModel):
    """Yêu cầu sinh một đề mới từ toàn bộ tài liệu trong Data_Import."""

    difficulty: str = Field("Trung bình", description="Độ khó: Dễ, Trung bình, Nâng cao")


class StudentAnswersRequest(BaseModel):
    quiz_id: str = "quiz-default"
    answers: Dict[str, Any] = Field(..., description="Mapping câu hỏi -> câu trả lời của sinh viên")
    questions_data: List[Dict[str, Any]] = Field(..., description="Danh sách câu hỏi trong đề thi")


class ExportQuizRequest(BaseModel):
    quiz_data: Dict[str, Any]
    format: str = Field("markdown", description="markdown | json | text")


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "VLearn AI Quiz Generator API",
        "version": "1.0.0",
        "documentation": "/docs"
    }


@app.get("/api/v1/health")
def health_check():
    return {"status": "ok", "message": "FastAPI service running smoothly"}


@app.get("/api/v1/lectures")
def list_lectures():
    """Lấy danh sách các bài giảng & tài liệu sẵn có."""
    return {"status": "success", "lectures": SAMPLE_LECTURES}


@app.post("/api/v1/generate-quiz")
def generate_quiz(req: GenerateQuizRequest):
    """
    Tạo bộ câu hỏi quiz kiểm tra kiến thức dựa trên nội dung bài giảng.
    """
    content = ""
    title = req.custom_title or "Bài giảng"

    if req.lecture_id:
        lecture = next((l for l in SAMPLE_LECTURES if l["id"] == req.lecture_id), None)
        if lecture:
            title = lecture["title"]
            content = lecture["summary"] + "\n" + "\n".join(lecture["key_points"])

    if req.custom_content:
        content = req.custom_content + "\n" + content

    if not content.strip():
        content = "Bài giảng tổng quan về kiến thức lập trình AI, quy trình RAG, prompt engineering và đánh giá mô hình."

    quiz = generate_quiz_from_content(
        content=content,
        lecture_title=title,
        num_questions=req.num_questions,
        difficulty=req.difficulty,
        question_types=req.question_types
    )

    return {
        "status": "success",
        "quiz": quiz
    }


@app.post("/api/v1/generate-student-quiz")
def generate_student_quiz(req: GenerateStudentQuizRequest):
    """Tạo một đề mới bằng OpenRouter provider trong Model/Provider.py.

    Frontend lưu kết quả trong session, vì vậy endpoint này chỉ được gọi lần đầu hoặc khi sinh viên chủ động yêu cầu tạo lại đề.
    """
    try:
        from Model.Provider import OpenRouterProvider

        provider = OpenRouterProvider()
        quiz = provider.generate_quiz(num_questions=20, difficulty=req.difficulty)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Không thể tạo đề từ AI provider: {exc}") from exc

    return {"status": "success", "quiz": quiz}


@app.post("/api/v1/evaluate-quiz")
def evaluate_quiz(req: StudentAnswersRequest):
    """
    Chấm điểm bài làm của sinh viên, tính % kết quả và cung cấp giải thích chi tiết.
    """
    total = len(req.questions_data)
    if total == 0:
        raise HTTPException(status_code=400, detail="Danh sách câu hỏi rỗng")

    correct_count = 0
    evaluations = []

    for q in req.questions_data:
        q_id = q.get("id")
        user_ans = req.answers.get(q_id)
        is_correct = False

        if q.get("type") in ["multiple_choice", "true_false"]:
            correct_idx = q.get("correct")
            if user_ans is not None and int(user_ans) == correct_idx:
                is_correct = True
                correct_count += 1
        else:
            # Short answer evaluation logic
            user_str = str(user_ans or "").strip().lower()
            if len(user_str) > 5:
                is_correct = True
                correct_count += 1

        evaluations.append({
            "question_id": q_id,
            "question": q.get("question"),
            "user_answer": user_ans,
            "correct_answer": q.get("correct") if q.get("type") != "short_answer" else q.get("answer_key"),
            "is_correct": is_correct,
            "explanation": q.get("explanation"),
            "hint": q.get("hint")
        })

    score = round((correct_count / total) * 10, 1)
    percentage = round((correct_count / total) * 100, 1)

    return {
        "status": "success",
        "score": score,
        "percentage": percentage,
        "correct_count": correct_count,
        "total_questions": total,
        "feedback": "Xuất sắc! Bạn đã nắm vững các kiến thức cốt lõi." if percentage >= 80 else "Khá tốt! Hãy ôn lại các câu trả lời chưa đúng.",
        "details": evaluations
    }


@app.get("/api/v1/analytics/class-gaps")
def get_class_gaps():
    """
    Trả về dữ liệu thống kê lỗ hổng kiến thức toàn lớp cho Giảng viên.
    """
    return {
        "status": "success",
        "total_students_tested": 42,
        "average_score": 7.8,
        "completion_rate": "95%",
        "knowledge_gaps": [
            {
                "topic": "Xử lý tình huống 'Ngoài Thẩm Quyền'",
                "error_rate": "42%",
                "status": "Cần củng cố",
                "recommendation": "Dành 10 phút đầu buổi tiếp theo nhắc lại taxonomy từ chối của AI Tutor."
            },
            {
                "topic": "Phân biệt Temperature & Sampling",
                "error_rate": "28%",
                "status": "Trung bình",
                "recommendation": "Cung cấp bài tập thực hành chỉnh parameter trên VLearn Playground."
            },
            {
                "topic": "Vector Search & Cosine Similarity",
                "error_rate": "14%",
                "status": "Nắm tốt",
                "recommendation": "Tiếp tục duy trì bài tập thực hành code RAG."
            }
        ]
    }


@app.post("/api/v1/export-quiz")
def export_quiz(req: ExportQuizRequest):
    """
    Xuất bộ câu hỏi ra định dạng Markdown / JSON.
    """
    quiz = req.quiz_data
    fmt = req.format.lower()

    if fmt == "json":
        import json
        return {"status": "success", "content": json.dumps(quiz, ensure_ascii=False, indent=2), "format": "json"}

    # Markdown export default
    md_lines = [
        f"# {quiz.get('title', 'Bộ Đề Kiểm Tra')}",
        f"- **Số câu hỏi**: {quiz.get('total_questions')}",
        f"- **Độ khó**: {quiz.get('difficulty')}",
        f"- **Thời gian ước tính**: {quiz.get('estimated_minutes')} phút",
        "---",
        ""
    ]

    for idx, q in enumerate(quiz.get("questions", []), 1):
        md_lines.append(f"### Câu {idx}: {q.get('question')}")
        md_lines.append(f"*Mức độ tư duy*: `{q.get('tax_level', 'Thông hiểu')}` | *Độ khó*: `{q.get('difficulty', 'Trung bình')}`\n")
        
        if q.get("type") in ["multiple_choice", "true_false"]:
            opts = q.get("options", [])
            for opt_idx, opt in enumerate(opts):
                prefix = "[x]" if opt_idx == q.get("correct") else "[ ]"
                md_lines.append(f"- {prefix} {chr(65+opt_idx)}. {opt}")
        else:
            md_lines.append(f"- **Đáp án mẫu**: {q.get('answer_key')}")
            
        md_lines.append(f"\n> **Giải thích**: {q.get('explanation')}")
        md_lines.append(f"> **Gợi ý (Hint)**: {q.get('hint')}\n")

    return {
        "status": "success",
        "content": "\n".join(md_lines),
        "format": "markdown"
    }


if __name__ == "__main__":
    import uvicorn
    from web.config import API_HOST, API_PORT
    uvicorn.run(app, host=API_HOST, port=API_PORT)
