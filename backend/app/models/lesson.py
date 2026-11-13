from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Lesson(BaseModel):
    __tablename__ = "lessons"

    module_code = Column(String(100), nullable=False)
    module_title = Column(String(255), nullable=False)
    lesson_code = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    short_description = Column(Text, nullable=False)
    theory_markdown = Column(Text, nullable=True)
    difficulty = Column(String(50), nullable=False, default="medium")
    has_test = Column(Boolean, default=True)
    has_simulation = Column(Boolean, default=True)

    tests = relationship("Test", back_populates="lesson")
    scenarios = relationship("SimulationScenario", back_populates="lesson")