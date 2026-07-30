"""
VLearn AI Quiz Generator - Streamlit Main Application
Enhanced version with Instructor Edit Mode, Student Quiz Selection, Unanswered Question Warnings,
Role Protection, and Student/Instructor Knowledge Gap Dashboards.
"""

import sys
import os
import streamlit as st
import requests
import json
from typing import Dict, Any, List, Callable

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from config import APP_TITLE, APP_SUBTITLE, API_BASE_URL
from mock_data import SAMPLE_LECTURES, generate_quiz_from_content
from ui_components import render_header, inject_custom_css, render_metric_box

# Streamlit Page Config
st.set_page_config(
    page_title="VLearn AI Quiz Generator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Helper class with fallback
class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def check_health(self) -> bool:
        try:
            r = requests.get(f"{self.base_url}/health", timeout=1.5)
            return r.status_code == 200
        except Exception:
            return False

    def get_lectures(self) -> List[Dict[str, Any]]:
        try:
            r = requests.get(f"{self.base_url}/lectures", timeout=2.0)
            if r.status_code == 200:
                return r.json().get("lectures", SAMPLE_LECTURES)
        except Exception:
            pass
        return SAMPLE_LECTURES

    def generate_quiz(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            r = requests.post(f"{self.base_url}/generate-quiz", json=payload, timeout=3.0)
            if r.status_code == 200:
                return r.json().get("quiz")
        except Exception:
            pass
        # Fallback to local generator
        content = payload.get("custom_content") or ""
        lecture_id = payload.get("lecture_id")
        title = payload.get("custom_title", "Bài giảng")
        if lecture_id:
            lecture = next((l for l in SAMPLE_LECTURES if l["id"] == lecture_id), None)
            if lecture:
                title = lecture["title"]
                content = lecture["summary"] + "\n" + "\n".join(lecture["key_points"])
        return generate_quiz_from_content(
            content=content or "Bài giảng tổng quan AI",
            lecture_title=title,
            num_questions=payload.get("num_questions", 5),
            difficulty=payload.get("difficulty", "Trung bình"),
            question_types=payload.get("question_types", ["multiple_choice", "true_false"])
        )

    def generate_student_quiz(self, difficulty: str = "Trung bình", data_dir: str | None = None, progress_callback: Callable[[str], None] | None = None) -> Dict[str, Any]:
        """Get a fresh 20-question quiz from Model/Provider.py via FastAPI.

        If FastAPI is not running, the same provider is invoked locally. There
        is deliberately no mock-data fallback for this student flow.
        """
        backend_error = ""
        try:
            payload = {"difficulty": difficulty}
            if data_dir:
                payload["data_dir"] = str(data_dir)
            if progress_callback:
                try:
                    progress_callback("Dispatching request to FastAPI backend...")
                except Exception:
                    pass
            response = requests.post(
                f"{self.base_url}/generate-student-quiz",
                json=payload,
                timeout=10.0,
            )
            if response.status_code == 200:
                quiz = response.json().get("quiz")
                if quiz and quiz.get("questions"):
                    return quiz
            try:
                backend_error = response.json().get("detail", "Lỗi không xác định")
            except ValueError:
                backend_error = f"HTTP {response.status_code}"
        except requests.RequestException as exc:
            backend_error = "Không kết nối được FastAPI backend"

            try:
                from Model.Provider import OpenRouterProvider

                return OpenRouterProvider().generate_quiz(num_questions=20, difficulty=difficulty, data_dir=data_dir or None, progress_callback=progress_callback)
            except Exception as exc:
                raise RuntimeError(
                    f"{backend_error}. Provider cục bộ cũng không thể tạo đề: {exc}"
                ) from exc

    def evaluate_quiz(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            r = requests.post(f"{self.base_url}/evaluate-quiz", json=payload, timeout=3.0)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        
        # Local evaluation fallback
        questions = payload.get("questions_data", [])
        answers = payload.get("answers", {})
        correct_count = 0
        evals = []
        for q in questions:
            q_id = q.get("id")
            user_ans = answers.get(q_id)
            is_correct = False
            if q.get("type") in ["multiple_choice", "true_false"]:
                if user_ans is not None and int(user_ans) == q.get("correct"):
                    is_correct = True
                    correct_count += 1
            else:
                if user_ans and len(str(user_ans).strip()) > 3:
                    is_correct = True
                    correct_count += 1

            evals.append({
                "question_id": q_id,
                "question": q.get("question"),
                "user_answer": user_ans,
                "correct_answer": q.get("correct") if q.get("type") != "short_answer" else q.get("answer_key"),
                "is_correct": is_correct,
                "explanation": q.get("explanation"),
                "hint": q.get("hint")
            })

        total = max(len(questions), 1)
        score = round((correct_count / total) * 10, 1)
        return {
            "status": "success",
            "score": score,
            "percentage": round((correct_count / total) * 100, 1),
            "correct_count": correct_count,
            "total_questions": total,
            "feedback": "Xuất sắc! Bạn đã nắm chắc kiến thức." if score >= 8.0 else "Khá tốt! Hãy ôn lại các câu trả lời chưa đúng.",
            "details": evals
        }

    def get_class_gaps(self) -> Dict[str, Any]:
        try:
            r = requests.get(f"{self.base_url}/analytics/class-gaps", timeout=2.0)
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return {
            "total_students_tested": 42,
            "average_score": 7.8,
            "completion_rate": "95%",
            "knowledge_gaps": [
                {"topic": "Xử lý tình huống Ngoài Thẩm Quyền", "error_rate": "42%", "status": "Cần củng cố", "recommendation": "Nhắc lại taxonomy từ chối của AI Tutor"},
                {"topic": "Phân biệt Temperature & Sampling", "error_rate": "28%", "status": "Trung bình", "recommendation": "Cho bài tập chỉnh parameter trên VLearn Playground"},
                {"topic": "Vector Search & Cosine Similarity", "error_rate": "14%", "status": "Nắm tốt", "recommendation": "Tiếp tục duy trì thực hành RAG"}
            ]
        }

    def export_quiz(self, quiz_data: Dict[str, Any], fmt: str = "markdown") -> str:
        try:
            r = requests.post(f"{self.base_url}/export-quiz", json={"quiz_data": quiz_data, "format": fmt}, timeout=3.0)
            if r.status_code == 200:
                return r.json().get("content", "")
        except Exception:
            pass
        
        # Local format fallback
        if fmt == "json":
            return json.dumps(quiz_data, ensure_ascii=False, indent=2)
        lines = [f"# {quiz_data.get('title', 'Bộ Đề Kiểm Tra')}\n"]
        for idx, q in enumerate(quiz_data.get("questions", []), 1):
            lines.append(f"### Câu {idx}: {q.get('question')}")
            for opt_idx, opt in enumerate(q.get("options", [])):
                lines.append(f"- {'[x]' if opt_idx == q.get('correct') else '[ ]'} {chr(65+opt_idx)}. {opt}")
            lines.append(f"> Giải thích: {q.get('explanation')}\n")
        return "\n".join(lines)


# Initialize API client
api = APIClient(API_BASE_URL)
api_online = api.check_health()

# Initialize Session State
if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = generate_quiz_from_content(
        content=SAMPLE_LECTURES[0]["summary"] + "\n" + "\n".join(SAMPLE_LECTURES[0]["key_points"]),
        lecture_title=SAMPLE_LECTURES[0]["title"],
        num_questions=4,
        difficulty="Trung bình"
    )

if "student_results" not in st.session_state:
    st.session_state.student_results = None

if "is_instructor_authenticated" not in st.session_state:
    st.session_state.is_instructor_authenticated = False

if "shuffle_version" not in st.session_state:
    st.session_state.shuffle_version = 0

if "active_student_quiz" not in st.session_state:
    st.session_state.active_student_quiz = None

if "student_quiz_version" not in st.session_state:
    st.session_state.student_quiz_version = 0

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/isometric-folders/100/brain.png", width=64)
st.sidebar.title("⚡ VLearn EduQuiz")
st.sidebar.caption("Sản phẩm AI cho Khóa Học AI Thực Chiến")

st.sidebar.markdown("---")
mode = st.sidebar.radio(
    "📌 Chọn Vai Trò / Chức Năng:",
    [
        "🎓 Sinh viên: Làm Bài Kiểm Tra",
        "👨‍🏫 Giảng viên: Tạo & Tinh Chỉnh Quiz",
        "📊 Thống Kê & Lỗ Hổng Kiến Thức",
        "⚙️ Hệ Thống & FastAPI Status"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔒 Khóa Quyền Giảng Viên")
if st.session_state.is_instructor_authenticated:
    st.sidebar.success("✅ Đã xác thực Giảng viên")
    if st.sidebar.button("🔒 Đăng Xuất Giảng Viên"):
        st.session_state.is_instructor_authenticated = False
        st.rerun()
else:
    st.sidebar.info("Mã PIN mặc định Giảng viên: `1234`")

# Render Top Header
def create_student_shuffled_quiz(master_quiz: Dict[str, Any]) -> Dict[str, Any]:
    """Generates a student-specific randomized quiz variant (shuffled questions and shuffled choices)."""
    import copy
    import random
    quiz_copy = copy.deepcopy(master_quiz)
    questions = list(quiz_copy.get("questions", []))
    random.shuffle(questions)
    
    for q_idx, q in enumerate(questions):
        q["id"] = f"student-q-{q_idx+1}"
        if q.get("type") == "multiple_choice":
            orig_opts = list(q.get("options", []))
            orig_corr = q.get("correct", 0)
            if 0 <= orig_corr < len(orig_opts):
                indexed = list(enumerate(orig_opts))
                random.shuffle(indexed)
                new_opts = [o for _, o in indexed]
                new_corr = next(new_i for new_i, (orig_i, _) in enumerate(indexed) if orig_i == orig_corr)
                q["options"] = new_opts
                q["correct"] = new_corr
                
    quiz_copy["questions"] = questions
    return quiz_copy


# ==========================================
# MODE 1: GIẢNG VIÊN - TẠO & TINH CHỈNH QUIZ
# ==========================================
if mode == "👨‍🏫 Giảng viên: Tạo & Tinh Chỉnh Quiz":
    # Role Protection Passcode Check
    if not st.session_state.is_instructor_authenticated:
        st.warning("🔒 Chức năng này dành riêng cho Giảng viên / TA. Vui lòng nhập mã PIN để xác thực.")
        pin_input = st.text_input("🔑 Nhập mã PIN Giảng viên:", type="password", placeholder="Nhập 1234...")
        if st.button("🔓 Xác Nhận Mã PIN", type="primary"):
            if pin_input == "1234":
                st.session_state.is_instructor_authenticated = True
                st.success("✅ Xác thực Giảng viên thành công!")
                st.rerun()
            else:
                st.error("❌ Mã PIN không chính xác! Vui lòng thử lại (Gợi ý: 1234).")
        st.stop()

    st.subheader("🛠️ Công Cụ Sinh & Tinh Chỉnh Đề Thi Tự Động Cho Giảng Viên")
    
    col_input, col_config = st.columns([3, 2])
    
    with col_input:
        st.markdown("#### 1. Chọn hoặc Nhập Nội Dung Bài Giảng")
        lecture_option = st.selectbox(
            "📚 Chọn bài giảng có sẵn trong Kho VLearn Pack:",
            options=["-- Nhập bài giảng tùy chỉnh --"] + [l["title"] for l in SAMPLE_LECTURES]
        )
        
        custom_content = ""
        custom_title = ""
        if lecture_option == "-- Nhập bài giảng tùy chỉnh --":
            custom_title = st.text_input("📝 Tiêu đề bài học / Chủ đề:", value="Bài 04: Kiến Trúc Microservices & API Design")
            custom_content = st.text_area(
                "📄 Nhập Tóm tắt Slide / Nội dung giảng dạy / Ghi chú:",
                value="""Bài giảng hướng dẫn thiết kế RESTful API chuẩn OpenAPI specification. Thảo luận các nguyên lý cơ bản: Stateless, Resource-based routing, HTTP methods (GET, POST, PUT, DELETE), và cách xử lý mã lỗi HTTP Status Codes (200 OK, 400 Bad Request, 401 Unauthorized, 404 Not Found, 500 Internal Server Error). Nhấn mạnh tầm quan trọng của API Rate Limiting và JWT Authentication.""",
                height=180
            )
        else:
            selected_lec = next(l for l in SAMPLE_LECTURES if l["title"] == lecture_option)
            st.info(f"**Tóm tắt**: {selected_lec['summary']}")
            custom_title = selected_lec["title"]

    with col_config:
        st.markdown("#### 2. Cấu Hình Thông Số Đề Thi")
        num_q = st.slider("🎯 Số lượng câu hỏi:", min_value=3, max_value=12, value=5)
        difficulty = st.select_slider("🎚️ Độ khó đề thi:", options=["Dễ", "Trung bình", "Nâng cao"], value="Trung bình")
        
        q_types = st.multiselect(
            "📋 Dạng câu hỏi mong muốn:",
            options=["multiple_choice", "true_false", "short_answer"],
            default=["multiple_choice", "true_false"],
            format_func=lambda x: {"multiple_choice": "Trắc nghiệm 4 đáp án", "true_false": "Đúng / Sai", "short_answer": "Trả lời ngắn"}[x]
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        btn_generate = st.button("✨ 🚀 AI Sinh Bộ Câu Hỏi", type="primary", use_container_width=True)

    if btn_generate:
        with st.spinner("🤖 AI đang phân tích bài giảng và tổng hợp bộ câu hỏi..."):
            lec_id = None
            if lecture_option != "-- Nhập bài giảng tùy chỉnh --":
                lec_id = next(l["id"] for l in SAMPLE_LECTURES if l["title"] == lecture_option)
            
            payload = {
                "lecture_id": lec_id,
                "custom_title": custom_title,
                "custom_content": custom_content,
                "num_questions": num_q,
                "difficulty": difficulty,
                "question_types": q_types if q_types else ["multiple_choice", "true_false"]
            }
            
            quiz_result = api.generate_quiz(payload)
            st.session_state.current_quiz = quiz_result
            st.success("✅ Đã sinh bộ câu hỏi thành công!")

    # Display Generated Quiz Preview & Instructor Edit Mode
    if st.session_state.current_quiz:
        st.markdown("---")
        quiz = st.session_state.current_quiz
        
        st.markdown(f"### 📋 Bộ Đề Hiện Tại: **{quiz.get('title')}**")
        
        # Metric summary row
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            render_metric_box("Tổng số câu", f"{quiz.get('total_questions')} câu", "Tự động phân bổ")
        with m2:
            render_metric_box("Độ khó", f"{quiz.get('difficulty')}", "Phù hợp sinh viên")
        with m3:
            render_metric_box("Thời gian", f"~{quiz.get('estimated_minutes')} phút", "Kiểm tra nhanh")
        with m4:
            render_metric_box("Đánh giá AI", "Chuẩn Taxonomy", "4 Lớp chỗ khó")

        tab_view, tab_edit = st.tabs(["👁️ Xem Trước Bộ Đề", "✏️ Tinh Chỉnh / Chỉnh Sửa Câu Hỏi"])
        
        with tab_view:
            st.markdown("#### 📝 Danh Sách Câu Hỏi Hướng Cho Học Viên")
            for idx, q in enumerate(quiz.get("questions", []), 1):
                with st.expander(f"Câu {idx}: {q.get('question')} [{q.get('tax_level', 'Thông hiểu')}]", expanded=True):
                    st.write(f"**Loại câu hỏi**: `{q.get('type')}` | **Mức độ tư duy**: `{q.get('tax_level')}`")
                    
                    if q.get("type") in ["multiple_choice", "true_false"]:
                        opts = q.get("options", [])
                        for opt_i, opt in enumerate(opts):
                            is_correct = (opt_i == q.get("correct"))
                            st.markdown(f"{'✅ **[Đáp án Đúng]**' if is_correct else '⚪'} **{chr(65+opt_i)}.** {opt}")
                    else:
                        st.write(f"**Đáp án mẫu**: {q.get('answer_key')}")
                    
                    st.markdown(f"""
                    <div class="explanation-box">
                        💡 <b>Giải thích chi tiết:</b> {q.get('explanation')}
                    </div>
                    <div class="hint-box">
                        🔑 <b>Gợi ý (Hint cho Sinh viên):</b> {q.get('hint')}
                    </div>
                    """, unsafe_allow_html=True)

        with tab_edit:
            st.markdown("#### ✏️ Studio Tinh Chỉnh Đề Thi Cho Giảng Viên")
            st.caption("Chọn từng câu hỏi bên dưới để chỉnh sửa nội dung, lựa chọn đáp án và giải thích.")
            
            questions_list = quiz.get("questions", [])
            if not questions_list:
                st.info("Chưa có câu hỏi nào trong đề thi.")
            else:
                q_tabs = st.tabs([f"❓ Câu {i+1}" for i in range(len(questions_list))])
                edited_questions = list(questions_list)
                
                for idx, (q_tab, q) in enumerate(zip(q_tabs, questions_list)):
                    with q_tab:
                        with st.container(border=True):
                            st.markdown(f"##### 📌 Đang chỉnh sửa Câu {idx+1} — Dạng: `{q.get('type')}` | Taxonomy: `{q.get('tax_level', 'Thông hiểu')}`")
                            
                            c_left, c_right = st.columns([3, 2])
                            
                            with c_left:
                                st.markdown("**1. Nội dung câu hỏi & Gợi ý:**")
                                e_q_text = st.text_area(
                                    f"Nội dung câu hỏi {idx+1}:",
                                    value=q.get("question"),
                                    height=90,
                                    key=f"edit_q_{idx}_v{st.session_state.shuffle_version}"
                                )
                                
                                explanation = st.text_area(
                                    f"Giải thích đáp án chi tiết:",
                                    value=q.get("explanation", ""),
                                    height=90,
                                    key=f"edit_exp_{idx}_v{st.session_state.shuffle_version}"
                                )
                                
                                hint = st.text_input(
                                    f"Gợi ý (Hint cho sinh viên):",
                                    value=q.get("hint", ""),
                                    key=f"edit_hint_{idx}_v{st.session_state.shuffle_version}"
                                )
                            
                            with c_right:
                                st.markdown("**2. Các lựa chọn & Đáp án đúng:**")
                                edited_q = dict(q)
                                edited_q["question"] = e_q_text
                                edited_q["explanation"] = explanation
                                edited_q["hint"] = hint
                                
                                if q.get("type") in ["multiple_choice", "true_false"]:
                                    opts = q.get("options", [])
                                    new_opts = []
                                    for opt_i, opt in enumerate(opts):
                                        new_opt = st.text_area(
                                            f"Lựa chọn {chr(65+opt_i)}:",
                                            value=opt,
                                            height=68,
                                            key=f"edit_opt_{idx}_{opt_i}_v{st.session_state.shuffle_version}"
                                        )
                                        new_opts.append(new_opt)
                                    
                                    edited_q["options"] = new_opts
                                    
                                    correct_idx = st.selectbox(
                                        f"🎯 Chọn đáp án đúng:",
                                        options=list(range(len(new_opts))),
                                        index=min(q.get("correct", 0), max(0, len(new_opts)-1)),
                                        format_func=lambda x: f"Đáp án đúng: {chr(65+x)}. {new_opts[x][:60]}...",
                                        key=f"edit_correct_{idx}_v{st.session_state.shuffle_version}"
                                    )
                                    edited_q["correct"] = correct_idx
                                else:
                                    ans_key = st.text_input(
                                        f"Đáp án mẫu:",
                                        value=q.get("answer_key", ""),
                                        key=f"edit_key_{idx}_v{st.session_state.shuffle_version}"
                                    )
                                    edited_q["answer_key"] = ans_key
                                
                                edited_questions[idx] = edited_q

                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("💾 Lưu Tất Cả Thay Đổi Đề Thi", type="primary", use_container_width=True):
                    st.session_state.current_quiz["questions"] = edited_questions
                    st.success("✅ Đã cập nhật và lưu thay đổi cho toàn bộ đề thi!")
                    st.rerun()

        # Export Actions
        st.markdown("---")
        st.markdown("#### 📥 Xuất Bộ Đề Thi & Chia Sẻ")
        ex1, ex2, ex3 = st.columns(3)
        with ex1:
            md_content = api.export_quiz(quiz, "markdown")
            st.download_button(
                "📥 Tải Về File Markdown (.md)",
                data=md_content,
                file_name="vlearn_quiz.md",
                mime="text/markdown",
                use_container_width=True
            )
        with ex2:
            json_content = api.export_quiz(quiz, "json")
            st.download_button(
                "📥 Tải Về JSON Data (.json)",
                data=json_content,
                file_name="vlearn_quiz.json",
                mime="application/json",
                use_container_width=True
            )
        with ex3:
            if st.button("📋 Sao Chép Đề Bài Markdown", use_container_width=True):
                st.code(md_content, language="markdown")
                st.toast("Đã chuẩn bị Markdown text! Bạn có thể copy bên trên.", icon="📋")


# ==========================================
# MODE 2: SINH VIÊN - KIỂM TRA CUỐI BUỔI
# ==========================================
elif mode == "🎓 Sinh viên: Làm Bài Kiểm Tra":
    st.subheader("🎓 Trải Nghiệm Kiểm Tra Kiến Thức Cuối Buổi Học dành cho Sinh Viên")
    st.caption("Đề được AI Provider tạo từ tài liệu trong Data_Import và giữ nguyên trong phiên làm bài.")

    col_source, col_regenerate = st.columns([3, 1])
    with col_source:
        st.markdown("#### 📚 Đề kiểm tra từ AI Provider")
        st.caption("Lần đầu mở trang, hệ thống tạo một đề 20 câu. Không tạo lại khi trang tự chạy lại.")

        # Day selector: choose which Data_Import subfolder to use as source materials
        data_import_root = os.path.join(PROJECT_ROOT, "Data_Import")
        day_options = []
        try:
            if os.path.isdir(data_import_root):
                day_options = [d for d in sorted(os.listdir(data_import_root)) if os.path.isdir(os.path.join(data_import_root, d))]
        except Exception:
            day_options = []

        if not day_options:
            day_options = ["."]

        selected_day = st.selectbox("📅 Chọn ngày nguồn dữ liệu (Data_Import/<Ngày>):", options=day_options, index=0)
        # Keep selection in session so regenerations use same day
        st.session_state.selected_data_day = selected_day

    if st.session_state.active_student_quiz is None:
        with st.spinner("🤖 AI đang tạo đề từ tài liệu bài học..."):
            try:
                sel_day = st.session_state.get("selected_data_day")
                if sel_day and sel_day != ".":
                    data_dir_path = os.path.join(PROJECT_ROOT, "Data_Import", sel_day)
                else:
                    data_dir_path = os.path.join(PROJECT_ROOT, "Data_Import")

                # prepare debug placeholder and storage
                if "provider_debug" not in st.session_state:
                    st.session_state.provider_debug = []
                debug_placeholder = st.empty()

                def _progress(msg: str) -> None:
                    st.session_state.provider_debug.append(msg)
                    try:
                        debug_placeholder.text("\n".join(st.session_state.provider_debug))
                    except Exception:
                        pass

                # show initial debug area before blocking call
                debug_placeholder.text("Preparing to generate quiz...\n")
                st.session_state.active_student_quiz = api.generate_student_quiz(data_dir=data_dir_path, progress_callback=_progress)
                st.session_state.student_quiz_version += 1
            except RuntimeError as exc:
                st.error(f"Không thể tạo đề AI: {exc}")
                st.stop()

    with col_regenerate:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🎲 Tạo Đề Mới", use_container_width=True):
            with st.spinner("🤖 AI đang tạo đề mới..."):
                try:
                    sel_day = st.session_state.get("selected_data_day")
                    if sel_day and sel_day != ".":
                        data_dir_path = os.path.join(PROJECT_ROOT, "Data_Import", sel_day)
                    else:
                        data_dir_path = os.path.join(PROJECT_ROOT, "Data_Import")

                    if "provider_debug" not in st.session_state:
                        st.session_state.provider_debug = []
                    debug_placeholder = st.empty()

                    def _progress(msg: str) -> None:
                        st.session_state.provider_debug.append(msg)
                        try:
                            debug_placeholder.text("\n".join(st.session_state.provider_debug))
                        except Exception:
                            pass

                    st.session_state.active_student_quiz = api.generate_student_quiz(data_dir=data_dir_path, progress_callback=_progress)
                    st.session_state.student_results = None
                    st.session_state.student_quiz_version += 1
                except RuntimeError as exc:
                    st.error(f"Không thể tạo đề AI: {exc}")
                else:
                    st.toast("🎲 AI đã tạo một đề hoàn toàn mới!", icon="🎲")
                    st.rerun()

    active_quiz = st.session_state.active_student_quiz

    if not active_quiz:
        st.warning("Chưa có bài test nào được chọn!")
    else:
        # High contrast card styling for quiz description
        st.markdown(f"""
        <div class="glass-card" style="background:#ffffff !important; color:#0f172a !important; border:1px solid #cbd5e1; border-radius:14px; padding:1.4rem; margin-bottom:1.2rem;">
            <h3 style="margin-top:0; color:#1e1b4b !important; font-weight:800;">📌 {active_quiz.get('title')}</h3>
            <p style="font-size:0.95rem; color:#334155 !important;">⏱️ Thời gian khuyến nghị: <b style="color:#1e1b4b !important;">{active_quiz.get('estimated_minutes')} phút</b> | 📊 Tổng câu hỏi: <b style="color:#1e1b4b !important;">{active_quiz.get('total_questions')} câu</b> | 🎚️ Độ khó: <b style="color:#1e1b4b !important;">{active_quiz.get('difficulty')}</b></p>
            <p style="font-size:0.9rem; color:#475569 !important;">⚠️ <i style="color:#475569 !important;">Lưu ý: Bạn cần chọn đầy đủ đáp án cho tất cả các câu hỏi trước khi nhấn nút Nộp Bài.</i></p>
        </div>
        """, unsafe_allow_html=True)
        
        user_answers = {}
        
        with st.form("student_quiz_form"):
            for idx, q in enumerate(active_quiz.get("questions", []), 1):
                st.markdown(f"#### Câu {idx}: {q.get('question')}")
                
                # Expandable Hint
                with st.expander("💡 Xem Gợi ý (AI Hint)"):
                    st.info(q.get("hint", "Hãy nhớ lại nội dung chính trong bài giảng."))
                
                if q.get("type") in ["multiple_choice", "true_false"]:
                    opts = q.get("options", [])
                    # Set index=None so NO option is pre-selected by default!
                    choice = st.radio(
                        f"Lựa chọn của bạn cho câu {idx}:",
                        options=list(range(len(opts))),
                        index=None,
                        format_func=lambda x: f"{chr(65+x)}. {opts[x]}",
                        key=f"student_radio_q_{q.get('id')}_{idx}_v{st.session_state.student_quiz_version}"
                    )
                    user_answers[q.get("id")] = choice
                else:
                    text_ans = st.text_input(
                        f"Trả lời ngắn cho câu {idx}:",
                        key=f"student_text_q_{q.get('id')}_{idx}_v{st.session_state.student_quiz_version}",
                        placeholder="Nhập câu trả lời của bạn tại đây..."
                    )
                    user_answers[q.get("id")] = text_ans.strip() if text_ans else None
                
                st.markdown("<br>", unsafe_allow_html=True)

            submit_quiz = st.form_submit_button("📩 Nộp Bài & Xem Kết Quả Chấm Điểm", type="primary", use_container_width=True)

        if submit_quiz:
            # Check for unanswered questions
            unanswered = []
            for idx, q in enumerate(active_quiz.get("questions", []), 1):
                ans = user_answers.get(q.get("id"))
                if ans is None or (isinstance(ans, str) and not ans.strip()):
                    unanswered.append(f"Câu {idx}")

            if unanswered:
                st.error(f"⚠️ **Cảnh báo chưa hoàn thành!** Bạn chưa chọn đáp án hoặc chưa trả lời cho các câu: **{', '.join(unanswered)}**. Vui lòng hoàn thành tất cả các câu hỏi trước khi nộp bài!")
            else:
                with st.spinner("🤖 AI đang chấm điểm và tạo giải thích bài làm cho bạn..."):
                    eval_payload = {
                        "quiz_id": "quiz-session-student",
                        "answers": user_answers,
                        "questions_data": active_quiz.get("questions", [])
                    }
                    res = api.evaluate_quiz(eval_payload)
                    st.session_state.student_results = res

        # Display Student Results
        if st.session_state.student_results:
            st.markdown("---")
            res = st.session_state.student_results
            
            st.markdown("### 🏆 Kết Quả Đánh Giá Bài Làm Của Bạn")
            
            rc1, rc2, rc3 = st.columns(3)
            with rc1:
                render_metric_box("Điểm Số", f"{res.get('score')} / 10", res.get("feedback"))
            with rc2:
                render_metric_box("Tỷ lệ đúng", f"{res.get('percentage')}%", f"{res.get('correct_count')}/{res.get('total_questions')} câu đúng")
            with rc3:
                render_metric_box("Trạng Thái", "Xuất sắc" if res.get('score') >= 8 else ("Đạt" if res.get('score') >= 5 else "Cần Ôn Tập"), "Ghi nhận VLearn")

            st.markdown("#### 🔍 Chi Tiết Đáp Án & Trích Dẫn Giải Thích")
            for idx, item in enumerate(res.get("details", []), 1):
                is_correct = item.get("is_correct")
                border_color = "#22c55e" if is_correct else "#ef4444"
                badge_str = "✅ ĐÚNG" if is_correct else "❌ CHƯA ĐÚNG"
                
                st.markdown(f"""
                <div style="border-left: 4px solid {border_color}; padding: 1rem 1.2rem; background: #ffffff !important; color: #0f172a !important; border-radius: 0 10px 10px 0; margin-bottom: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.04); border: 1px solid #cbd5e1;">
                    <div style="font-weight: 700; color: #1e1b4b !important; font-size: 1.05rem;">Câu {idx}: {item.get('question')}</div>
                    <div style="margin-top: 0.4rem; font-size: 0.9rem; color: #334155 !important;">
                        <b style="color: #0f172a !important;">Trạng thái:</b> <span style="color:{border_color} !important; font-weight:700;">{badge_str}</span>
                    </div>
                    <div style="margin-top: 0.4rem; font-size: 0.9rem; color: #334155 !important;">
                        <b style="color: #0f172a !important;">Giải thích đáp án:</b> <span style="color: #334155 !important;">{item.get('explanation')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)


# ==========================================
# MODE 3: THỐNG KÊ & LỖ HỔNG KIẾN THỨC (HỌC VIÊN + GIẢNG VIÊN)
# ==========================================
elif mode == "📊 Thống Kê & Lỗ Hổng Kiến Thức":
    st.subheader("📊 Báo Cáo & Phân Tích Lỗ Hổng Kiến Thức")
    st.caption("Cung cấp góc nhìn phân tích lỗ hổng kiến thức cho cả Học viên và Giảng viên.")
    
    tab_student_gap, tab_class_gap = st.tabs([
        "🎓 Góc Học Viên: Lỗ Hổng Kiến Thức Cá Nhân",
        "👨‍🏫 Góc Giảng Viên: Ma Trận Lỗ Hổng Cả Lớp"
    ])
    
    with tab_student_gap:
        st.markdown("### 🎓 Bản Đồ Lỗ Hổng Kiến Thức Cá Nhân Của Bạn")
        
        if st.session_state.student_results:
            res = st.session_state.student_results
            st.info(f"Kết quả bài kiểm tra gần nhất: **{res.get('score')} / 10** ({res.get('correct_count')}/{res.get('total_questions')} câu đúng)")
            
            wrong_items = [d for d in res.get("details", []) if not d.get("is_correct")]
            
            if wrong_items:
                st.warning(f"⚠️ Bạn có {len(wrong_items)} câu chưa trả lời chính xác. Dưới đây là các chủ đề bạn cần củng cố lại:")
                for item in wrong_items:
                    st.markdown(f"""
                    <div class="glass-card" style="border-left: 5px solid #ef4444; background:#ffffff !important; color:#0f172a !important; padding:1.2rem; margin-bottom:1rem; border:1px solid #cbd5e1; border-radius:10px;">
                        <h4 style="margin:0; color:#1e1b4b !important; font-weight:700;">📌 Câu hỏi chưa đúng: {item.get('question')}</h4>
                        <p style="margin-top:0.5rem; font-size:0.95rem; color:#334155 !important;"><b style="color:#1e1b4b !important;">Lời khuyên từ AI Tutor:</b> {item.get('explanation')}</p>
                        <p style="font-size:0.85rem; color:#475569 !important;"><b style="color:#475569 !important;">Gợi ý ôn tập:</b> {item.get('hint')}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("🎉 Xuất sắc! Bạn không có lỗ hổng kiến thức nào trong bài test vừa rồi. Hãy tiếp tục duy trì phong độ!")
        else:
            st.info("💡 Bạn chưa hoàn thành bài test nào trong phiên học này. Hãy sang tab **🎓 Sinh viên: Làm Bài Kiểm Tra** để thực hiện bài test và nhận bản phân tích cá nhân!")
            
            st.markdown("#### 📌 Ví Dụ Minh Họa Bản Đồ Lỗ Hổng Cá Nhân:")
            m_s1, m_s2 = st.columns(2)
            with m_s1:
                render_metric_box("Chủ đề vững chắc", "Prompting & CoT", "Tỷ lệ làm đúng 100%")
            with m_s2:
                render_metric_box("Chủ đề cần củng cố", "Temperature Tuning", "Tỷ lệ đúng 50% - Cần đọc lại Bài 01")

    with tab_class_gap:
        st.markdown("### 👨‍🏫 Ma Trận Lỗ Hổng Kiến Thức Tổng Hợp Toàn Lớp (Class Knowledge Gap Matrix)")
        st.caption("Tổng hợp dữ liệu bài làm cuối buổi để giúp Giảng viên/TA chuẩn bị nội dung củng cố cho buổi tiếp theo.")
        
        gaps_data = api.get_class_gaps()
        
        a1, a2, a3 = st.columns(3)
        with a1:
            render_metric_box("Tổng Học Viên Đã Làm", f"{gaps_data.get('total_students_tested')} HV", "Tham gia test cuối buổi")
        with a2:
            render_metric_box("Điểm Trung Bình Lớp", f"{gaps_data.get('average_score')} / 10", "Chất lượng chung")
        with a3:
            render_metric_box("Tỷ Lệ Hoàn Thành", f"{gaps_data.get('completion_rate')}", "Tham gia tích cực")

        st.markdown("---")
        st.markdown("### ⚠️ Các Chủ Đề Học Viên Hay Làm Sai Nhất")
        
        for gap in gaps_data.get("knowledge_gaps", []):
            color = "#ef4444" if "Cần củng cố" in gap.get("status") else ("#f59e0b" if "Trung bình" in gap.get("status") else "#22c55e")
            st.markdown(f"""
            <div class="glass-card" style="border-left: 5px solid {color}; background:#ffffff !important; color:#0f172a !important; padding:1.2rem; margin-bottom:1rem; border:1px solid #cbd5e1; border-radius:10px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h4 style="margin:0; color:#1e1b4b !important; font-weight:700;">📌 Chủ đề: {gap.get('topic')}</h4>
                    <span class="badge" style="background:{color}22; color:{color} !important; font-weight:700;">Tỷ lệ sai: {gap.get('error_rate')}</span>
                </div>
                <p style="margin-top:0.6rem; color:#334155 !important;"><b style="color:#1e1b4b !important;">Khuyến nghị cho Giảng viên:</b> {gap.get('recommendation')}</p>
            </div>
            """, unsafe_allow_html=True)


# ==========================================
# MODE 4: FASTAPI STATUS & CONFIG
# ==========================================
elif mode == "⚙️ Hệ Thống & FastAPI Status":
    st.subheader("⚙️ Trạng Thái Hệ Thống & Kết Nối Backend FastAPI")
    
    st.markdown(f"**URL Backend API Configuration**: `{API_BASE_URL}`")
    
    if api_online:
        st.success("🟢 FastAPI Backend Server đang hoạt động bình thường trên cổng 8000!")
    else:
        st.warning("🟡 FastAPI Server hiện đang offline. Ứng dụng Streamlit đang tự động sử dụng Engine AI Sandbox nội bộ để phục vụ bạn liền mạch.")

    st.markdown("### 🛠️ Các Endpoint RESTful API Khả Dụng")
    endpoints = [
        {"method": "GET", "path": "/api/v1/health", "desc": "Kiểm tra sức khỏe dịch vụ API"},
        {"method": "GET", "path": "/api/v1/lectures", "desc": "Lấy danh sách các bài giảng mẫu"},
        {"method": "POST", "path": "/api/v1/generate-quiz", "desc": "Sinh bộ câu hỏi từ nội dung bài giảng & thông số"},
        {"method": "POST", "path": "/api/v1/evaluate-quiz", "desc": "Chấm điểm và giải thích bài làm của sinh viên"},
        {"method": "GET", "path": "/api/v1/analytics/class-gaps", "desc": "Báo cáo phân tích lỗ hổng kiến thức toàn lớp"},
        {"method": "POST", "path": "/api/v1/export-quiz", "desc": "Xuất bộ đề thi định dạng Markdown / JSON"}
    ]
    st.table(endpoints)

    if st.button("🔄 Kiểm Tra Lại Kết Nối FastAPI"):
        st.rerun()
