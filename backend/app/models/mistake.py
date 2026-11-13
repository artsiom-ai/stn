from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.models.base import BaseModel


class Mistake(BaseModel):
    __tablename__ = "mistakes"

    simulation_id = Column(Integer, nullable=False)
    skill = Column(String(100), nullable=False)  # навык, в котором ошибка
    mistake_type = Column(String(100), nullable=False)  # тип ошибки
    description = Column(Text, nullable=False)  # описание ошибки
    occurred_at_message = Column(Integer, nullable=True)  # номер сообщения, где произошла
    recommendation = Column(Text, nullable=True)  # что тренировать