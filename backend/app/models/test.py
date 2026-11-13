from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Test(BaseModel):
    __tablename__ = "tests"

    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    title = Column(String(255), nullable=False)
    question_count = Column(Integer, default=0)
    min_pass_score = Column(Integer, default=80)

    lesson = relationship("Lesson", back_populates="tests")
    questions = relationship("Question", back_populates="test")