import json
import logging

from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

logger = logging.getLogger(__name__)


class Persona(BaseModel):
    __tablename__ = "personas"

    code = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    region = Column(String(100), nullable=False)
    niche = Column(String(100), nullable=False)
    business_context = Column(Text, nullable=True)
    difficulty = Column(String(50), nullable=False, default="medium")
    temperament = Column(String(100), nullable=True)
    budget_level = Column(String(50), nullable=True)
    urgency_level = Column(String(50), nullable=True)
    digital_literacy = Column(String(50), nullable=True)
    trust_level = Column(String(50), nullable=True)
    communication_style = Column(String(100), nullable=True)
    hidden_pain = Column(Text, nullable=True)
    objections_json = Column(Text, nullable=True)  # JSON-массив строк
    buy_conditions_json = Column(Text, nullable=True)  # JSON-массив строк
    fail_conditions_json = Column(Text, nullable=True)  # JSON-массив строк
    typical_phrases_json = Column(Text, nullable=True)  # JSON-массив строк
    system_prompt = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    tags_json = Column(Text, nullable=True)  # JSON-массив строк

    def get_objections(self):
        if not self.objections_json:
            return []
        try:
            return json.loads(self.objections_json)
        except Exception as e:
            logger.warning(f"Failed to parse objections_json: {e}")
            return []

    def get_buy_conditions(self):
        if not self.buy_conditions_json:
            return []
        try:
            return json.loads(self.buy_conditions_json)
        except Exception as e:
            logger.warning(f"Failed to parse buy_conditions_json: {e}")
            return []

    def get_fail_conditions(self):
        if not self.fail_conditions_json:
            return []
        try:
            return json.loads(self.fail_conditions_json)
        except Exception as e:
            logger.warning(f"Failed to parse fail_conditions_json: {e}")
            return []

    def get_typical_phrases(self):
        if not self.typical_phrases_json:
            return []
        try:
            return json.loads(self.typical_phrases_json)
        except Exception as e:
            logger.warning(f"Failed to parse typical_phrases_json: {e}")
            return []

    def get_tags(self):
        if not self.tags_json:
            return []
        try:
            return json.loads(self.tags_json)
        except Exception as e:
            logger.warning(f"Failed to parse tags_json: {e}")
            return []