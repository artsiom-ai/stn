import json

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class TestAttempt(BaseModel):
    __tablename__ = "test_attempts"

    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    user_id = Column(Integer, nullable=True)  # пока без жёсткой привязки к пользователю
    score = Column(Integer, default=0)
    passed = Column(Boolean, default=False)
    wrong_question_ids = Column(Text, nullable=True)  # JSON-массив id вопросов
    explanations = Column(Text, nullable=True)  # JSON-массив с разборами

    test = relationship("Test")

    def get_wrong_question_ids(self):
        if not self.wrong_question_ids:
            return []
        try:
            return json.loads(self.wrong_question_ids)
        except Exception:
            return []

    def get_explanations(self):
        if not self.explanations:
            return []
        try:
            return json.loads(self.explanations)
        except Exception:
            return []