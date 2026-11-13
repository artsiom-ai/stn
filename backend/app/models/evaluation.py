from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Evaluation(BaseModel):
    __tablename__ = "evaluations"

    simulation_id = Column(Integer, ForeignKey("simulations.id"), nullable=False)
    total_score = Column(Integer, nullable=False, default=0)  # 0-100
    rubric_json = Column(Text, nullable=True)  # JSON с разбором по критериям
    judge_summary = Column(Text, nullable=True)  # текстовый разбор судьи
    strengths = Column(Text, nullable=True)  # JSON-массив сильных сторон
    weaknesses = Column(Text, nullable=True)  # JSON-массив слабых сторон
    recommendations = Column(Text, nullable=True)  # JSON-массив рекомендаций

    import json

    def get_rubric(self):
        if not self.rubric_json:
            return {}
        try:
            return json.loads(self.rubric_json)
        except Exception:
            return {}

    def get_strengths(self):
        if not self.strengths:
            return []
        try:
            return json.loads(self.strengths)
        except Exception:
            return []

    def get_weaknesses(self):
        if not self.weaknesses:
            return []
        try:
            return json.loads(self.weaknesses)
        except Exception:
            return []

    def get_recommendations(self):
        if not self.recommendations:
            return []
        try:
            return json.loads(self.recommendations)
        except Exception:
            return []