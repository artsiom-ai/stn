from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Simulation(BaseModel):
    __tablename__ = "simulations"

    persona_id = Column(Integer, nullable=False)  # пока без FK, чтобы избежать cyclic import
    scenario_id = Column(Integer, nullable=True)
    difficulty = Column(String(50), nullable=False, default="medium")
    status = Column(String(50), nullable=False, default="active")  # active, finished
    opened_message = Column(String, nullable=True)  # первое сообщение от персонажа
    message_count = Column(Integer, default=0)  # сколько сообщений всего в сессии

    messages = relationship("Message", back_populates="simulation")