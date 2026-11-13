import json
import logging
from typing import Optional

from app.llm.router import LLMRouter
from app.models.lesson import Lesson
from app.models.test import Test
from app.models.question import Question
from app.database import SessionLocal

logger = logging.getLogger(__name__)


class TestGenerator:
    """Сервис генерации теста по теме урока через LLM."""

    def __init__(self):
        self.router = LLMRouter()

    def _load_prompt(self) -> str:
        try:
            with open("app/prompts/test_generation_prompt.txt", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            # Fallback: промпт inline, если файл не найден
            return """Ты — опытный методик по продажам. Составь тест из 5 вопросов (single_choice, 4 варианта) по теории урока.
Урок: {lesson_title}
Теория: {theory_markdown}
Верни строго JSON без markdown:
{"title": "...", "min_pass_score": 80, "questions": [{"question_text": "...", "options": ["A","B","C","D"], "correct_answer": "...", "explanation": "...", "order_index": 1}, ...]}"""

    def generate_test_for_lesson(self, lesson_id: int, db=None) -> dict:
        """
        Генерирует тест с 5 вопросами для указанного урока и сохраняет в БД.
        Возвращает словарь с id теста и списком вопросов (без правильных ответов для фронта).
        """
        close_db = False
        if db is None:
            db = SessionLocal()
            close_db = True

        try:
            lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
            if not lesson:
                raise ValueError(f"Lesson with id={lesson_id} not found")

            prompt_template = self._load_prompt()
            prompt = prompt_template.format(
                lesson_title=lesson.title,
                theory_markdown=lesson.theory_markdown or "Теория не описана",
            )

            # Вызываем LLM Router — он сам сделает фолбэк и ретраи при битом JSON
            result = self.router.complete_json(
                prompt=prompt,
                system_prompt="Ты generates тесты в формате JSON. Не добавляй текста вне JSON.",
                temperature=0.4,
                max_tokens=1500,
                max_retries=2,
            )

            # Валидация минимальной структуры
            title = result.get("title") or f"Тест для урока «{lesson.title}»"
            min_pass_score = int(result.get("min_pass_score", 80))
            questions_data = result.get("questions", [])
            if not questions_data or len(questions_data) < 3:
                raise ValueError("LLM вернул недостаточно вопросов")

            # Создаём тест
            test = Test(
                lesson_id=lesson_id,
                title=title,
                question_count=len(questions_data),
                min_pass_score=min_pass_score,
            )
            db.add(test)
            db.commit()
            db.refresh(test)

            # Создаём вопросы
            for q in questions_data:
                question = Question(
                    test_id=test.id,
                    question_text=q.get("question_text", ""),
                    question_type=q.get("question_type", "single_choice"),
                    options=json.dumps(q.get("options", []), ensure_ascii=False),
                    correct_answer=q.get("correct_answer", ""),
                    explanation=q.get("explanation", ""),
                    order_index=q.get("order_index", 0),
                )
                db.add(question)

            db.commit()

            # Возвращаем вопросы БЕЗ правильных ответов (для фронта)
            return {
                "test_id": test.id,
                "title": test.title,
                "question_count": test.question_count,
                "min_pass_score": test.min_pass_score,
                "questions": [
                    {
                        "id": q.id,
                        "question_text": q.question_text,
                        "options": q.get_options(),
                        "order_index": q.order_index,
                    }
                    for q in db.query(Question)
                    .filter(Question.test_id == test.id)
                    .order_by(Question.order_index)
                    .all()
                ],
            }

        except Exception as e:
            db.rollback()
            logger.error(f"Test generation failed for lesson {lesson_id}: {e}")
            raise
        finally:
            if close_db:
                db.close()