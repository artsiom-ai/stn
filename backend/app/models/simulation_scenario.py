from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class SimulationScenario(BaseModel):
    __tablename__ = "simulation_scenarios"

    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)
    goal = Column(Text, nullable=True)
    difficulty = Column(String(50), nullable=False, default="medium")
    channel = Column(String(50), nullable=True)  # "cold_call", "chat", "email"
    status = Column(String(50), nullable=False, default="active")
    start_message = Column(Text, nullable=True)
    fail_conditions = Column(Text, nullable=True)  # JSON
    success_conditions = Column(Text, nullable=True)  # JSON
    message_limit = Column(Integer, default=20)  # лимит сообщений в сессии

    lesson = relationship("Lesson", back_populates="scenarios")