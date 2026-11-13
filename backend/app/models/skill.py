from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from app.models.base import BaseModel


class Skill(BaseModel):
    __tablename__ = "skills"

    name = Column(String(100), unique=True, index=True, nullable=False)
    level = Column(Float, nullable=False, default=0.0)  # 0-100
    description = Column(String(255), nullable=True)
    attempts_count = Column(Integer, default=0)
    last_activity_at = Column(DateTime(timezone=True), nullable=True)
    trend = Column(String(20), nullable=True)  # "improving", "stable", "declining"