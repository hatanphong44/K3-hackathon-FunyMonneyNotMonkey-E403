"""Tạo quiz từ toàn bộ tài liệu Markdown/PDF trong thư mục ``Data_Import``.

Chạy trực tiếp để debug:
    python Model/Provider.py
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Callable

from openai import OpenAI

try:
    from dotenv import load_dotenv
except ImportError:  # python-dotenv là tùy chọn khi chạy trong môi trường đã có biến môi trường
    load_dotenv = None

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = PROJECT_ROOT / "Data_Import"
SYSTEM_PROMPT_PATH = Path(__file__).resolve().parent / "System_prompt.md"
MAX_SOURCE_CHARS = 100_000
MAX_OUTPUT_TOKENS = 6_000


class OpenRouterProvider:
    """Gọi OpenRouter để tạo quiz đúng schema mà giao diện hiện đang dùng."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "openrouter/free",
    ) -> None:
        if load_dotenv:
            load_dotenv(PROJECT_ROOT / ".env")

        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("Thiếu OPENROUTER_API_KEY. Hãy đặt biến môi trường hoặc thêm vào .env.")

        self.model = model
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1",
        )

    @staticmethod
    def _read_markdown(path: Path) -> str:
        return path.read_text(encoding="utf-8", errors="replace")

    @staticmethod
    def _read_pdf(path: Path) -> str:
        if PdfReader is None:
            raise RuntimeError("Chưa cài pypdf. Chạy: pip install pypdf")

        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    @staticmethod
    def _load_system_prompt() -> str:
        """Đọc instruction chuẩn cho quiz từ file để tránh hard-code prompt."""
        if not SYSTEM_PROMPT_PATH.is_file():
            raise FileNotFoundError(f"Không tìm thấy system prompt: {SYSTEM_PROMPT_PATH}")
        return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8", errors="replace").strip()

    def load_data_import(self, data_dir: str | Path = DEFAULT_DATA_DIR) -> tuple[str, list[str]]:
        """Đọc tất cả file ``.md`` và ``.pdf`` phía dưới Data_Import."""
        data_path = Path(data_dir)
        if not data_path.is_dir():
            raise FileNotFoundError(f"Không tìm thấy thư mục dữ liệu: {data_path}")

        sections: list[str] = []
        source_files: list[str] = []
        for path in sorted(data_path.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in {".md", ".pdf"}:
                continue

            try:
                text = self._read_markdown(path) if path.suffix.lower() == ".md" else self._read_pdf(path)
            except Exception as exc:
                print(f"[WARN] Không đọc được {path.name}: {exc}")
                continue

            text = text.strip()
            if text:
                relative_path = str(path.relative_to(PROJECT_ROOT))
                source_files.append(relative_path)
                source_kind = "LECTURE SLIDES (PRIMARY SOURCE)" if path.suffix.lower() == ".pdf" else "LECTURE TRANSCRIPT (SUPPORTING SOURCE)"
                sections.append(f"\n--- {source_kind}: {relative_path} ---\n{text}")

        if not sections:
            raise ValueError("Không tìm thấy nội dung đọc được từ file .md hoặc .pdf trong Data_Import.")

        content = "\n".join(sections)
        if len(content) > MAX_SOURCE_CHARS:
            print(f"[WARN] Nội dung quá dài, chỉ dùng {MAX_SOURCE_CHARS:,} ký tự đầu để tạo quiz.")
            content = content[:MAX_SOURCE_CHARS]
        return content, source_files

    @staticmethod
    def _parse_json(response_text: str) -> dict[str, Any]:
        """Lấy JSON kể cả khi model vô tình bọc trong markdown code fence."""
        cleaned = response_text.strip()
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned, flags=re.IGNORECASE)
        try:
            result = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Model không trả về JSON hợp lệ: {exc}\nRaw response:\n{response_text}") from exc
        if not isinstance(result, dict) or not isinstance(result.get("questions"), list):
            raise ValueError("JSON từ model không đúng schema: thiếu object 'questions'.")
        return result

    def generate_quiz(
        self,
        num_questions: int = 20,
        difficulty: str = "Trung bình",
        data_dir: str | Path = DEFAULT_DATA_DIR,
        progress_callback: Callable[[str], None] | None = None,
    ) -> dict[str, Any]:
        """Tạo quiz từ các file .md/.pdf và trả về JSON theo format hiện tại."""
        if num_questions != 20:
            raise ValueError("System_prompt.md yêu cầu tạo chính xác 20 câu hỏi.")

        if progress_callback:
            try:
                progress_callback("Loading data files from Data_Import...")
            except Exception:
                pass

        content, source_files = self.load_data_import(data_dir)
        if progress_callback:
            try:
                progress_callback(f"Loaded {len(source_files)} source file(s): {', '.join(source_files) if source_files else 'none'}")
            except Exception:
                pass
        system_prompt = self._load_system_prompt()
        if progress_callback:
            try:
                progress_callback("Building prompt for model...")
            except Exception:
                pass

        prompt = f"""Generate the quiz using the system instructions. The requested difficulty is '{difficulty}'.

    The materials below include both lecture slides and lecture transcripts. Their labels are intentional: slides are the primary source; transcripts may only clarify the slides. Return only the JSON format defined in the system prompt.

    LECTURE MATERIALS:
    {content}"""

        if progress_callback:
            try:
                progress_callback(f"Calling model API ({self.model})...")
            except Exception:
                pass

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            # OpenRouter mặc định có thể reserve 16,384 tokens, vượt số credit
            # còn lại dù đề 5 câu chỉ cần khoảng 1-2k tokens.
            max_tokens=MAX_OUTPUT_TOKENS,
            response_format={"type": "json_object"},
        )
        if progress_callback:
            try:
                progress_callback("Model returned response, parsing JSON...")
            except Exception:
                pass

        response_text = response.choices[0].message.content or ""
        quiz = self._parse_json(response_text)
        # Giữ tương thích với UI hiện tại: system prompt chỉ sinh multiple choice,
        # còn UI cần type/taxonomy/hint để hiển thị và chấm bài.
        quiz["difficulty"] = difficulty
        for question in quiz["questions"]:
            question["type"] = "multiple_choice"
            question["difficulty"] = difficulty
            question.setdefault("tax_level", "Thông hiểu")
            question.setdefault("hint", "Đọc lại phần slide liên quan đến câu hỏi.")
            options = question.get("options", [])
            correct = question.get("correct")
            if isinstance(correct, int) and 0 <= correct < len(options):
                question.setdefault("answer_key", options[correct])
        quiz["source_files"] = source_files  # Metadata debug; UI có thể bỏ qua field này.
        return quiz


if __name__ == "__main__":
    provider = OpenRouterProvider()
    quiz = provider.generate_quiz()
    print(json.dumps(quiz, ensure_ascii=False, indent=2))
