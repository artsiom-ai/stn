from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Message(BaseModel):
    __tablename__ = "messages"

    simulation_id = Column(Integer, ForeignKey("simulations.id"), nullable=False)
    sender = Column(String(20), nullable=False)  # "user" | "persona"
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    simulation = relationship("Simulation", back_populates="messages")