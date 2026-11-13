import json
import logging

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

logger = logging.getLogger(__name__)

VALID_QUESTION_TYPES = [
    "single_choice",
    "multiple_choice",
    "situation_choice",
    "find_error",
    "reorder_steps",
    "short_answer",
    "rewrite_text",
    "explain_simple",
]


class Question(BaseModel):
    __tablename__ = "questions"

    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    type = Column(String(50), nullable=False, default="single_choice")
    skill = Column(String(100), nullable=True)
    difficulty = Column(String(50), nullable=True, default="medium")
    question_text = Column(Text, nullable=False)
    options_json = Column(Text, nullable=True)  # JSON-массив вариантов
    correct_answer = Column(Text, nullable=False)  # JSON или строка
    explanation = Column(Text, nullable=True)
    is_critical = Column(Boolean, default=False)
    order_index = Column(Integer, default=0)

    test = relationship("Test", back_populates="questions")

    def get_options(self):
        if not self.options_json:
            return []
        try:
            return json.loads(self.options_json)
        except Exception as e:
            logger.warning(f"Failed to parse options_json: {e}")
            return []

    def get_correct_answer(self):
        try:
            return json.loads(self.correct_answer)
        except Exception:
            return self.correct_answer