import json
import logging
from typing import Optional, Dict, Any, List

from app.llm.router import LLMRouter
from app.models.persona import Persona
from app.models.simulation import Simulation
from app.models.message import Message
from app.database import SessionLocal

logger = logging.getLogger(__name__)

# Лимиты сессии
MAX_MESSAGES_PER_SESSION = 100
MAX_USER_MESSAGES_PER_SESSION = 50


class SimulationService:
    def __init__(self):
        self.router = LLMRouter()

    def start_simulation(self, persona_id: int, scenario_id: Optional[int],
                         difficulty: str, db) -> dict:
        persona = db.query(Persona).filter(Persona.id == persona_id).first()
        if not persona:
            raise ValueError(f"Persona with id={persona_id} not found")

        sim = Simulation(
            persona_id=persona_id,
            scenario_id=scenario_id,
            difficulty=difficulty,
            status="active",
        )
        db.add(sim)
        db.commit()
        db.refresh(sim)

        opening = self._get_persona_reply(
            persona=persona,
            user_message=None,
            conversation_history=[],
            sim=sim,
        )

        sim.opened_message = opening
        sim.message_count = 1
        db.add(sim)

        db.add(Message(
            simulation_id=sim.id,
            sender="persona",
            content=opening,
        ))
        db.commit()

        return {
            "simulation_id": sim.id,
            "scenario": {
                "id": scenario_id,
                "persona_id": persona_id,
                "difficulty": difficulty,
            },
            "opening_message": opening,
        }

    def send_message(self, simulation_id: int, content: str, db) -> dict:
        sim = db.query(Simulation).filter(Simulation.id == simulation_id).first()
        if not sim:
            raise ValueError(f"Simulation with id={simulation_id} not found")
        if sim.status != "active":
            raise ValueError("Simulation is already finished")

        user_msgs = (
            db.query(Message)
            .filter(Message.simulation_id == simulation_id, Message.sender == "user")
            .count()
        )
        total_msgs = sim.message_count or 0

        if user_msgs >= MAX_USER_MESSAGES_PER_SESSION:
            return {
                "message_id": None,
                "persona_reply": "Сессия достигла лимита сообщений. Завершите симуляцию.",
                "status": "limited",
            }
        if total_msgs >= MAX_MESSAGES_PER_SESSION:
            return {
                "message_id": None,
                "persona_reply": "Сессия достигла лимита сообщений. Завершите симуляцию.",
                "status": "limited",
            }

        db.add(Message(
            simulation_id=simulation_id,
            sender="user",
            content=content,
        ))
        sim.message_count = total_msgs + 1
        db.add(sim)
        db.commit()

        history = self._get_conversation_history(db, simulation_id)
        persona = db.query(Persona).filter(Persona.id == sim.persona_id).first()

        persona_reply = self._get_persona_reply(
            persona=persona,
            user_message=content,
            conversation_history=history,
            sim=sim,
        )

        db.add(Message(
            simulation_id=simulation_id,
            sender="persona",
            content=persona_reply,
        ))
        sim.message_count = (sim.message_count or 0) + 1
        db.add(sim)
        db.commit()

        return {
            "message_id": sim.message_count,
            "persona_reply": persona_reply,
            "status": "active",
        }
    def finish_simulation(self, simulation_id: int, db) -> dict:
        sim = db.query(Simulation).filter(Simulation.id == simulation_id).first()
        if not sim:
            raise ValueError(f"Simulation with id={simulation_id} not found")
        sim.status = "finished"
        db.add(sim)
        db.commit()
        return {
            "simulation_id": sim.id,
            "status": "finished",
            "evaluation": {},
        }

    def _get_conversation_history(self, db, simulation_id: int) -> List[dict]:
        messages = (
            db.query(Message)
            .filter(Message.simulation_id == simulation_id)
            .order_by(Message.created_at)
            .all()
        )
        return [
            {"role": m.sender, "content": m.content}
            for m in messages
        ]

    def _get_persona_reply(self, persona: Persona, user_message: Optional[str],
                           conversation_history: List[dict], sim: Simulation) -> str:
        system_prompt = persona.system_prompt or self._default_system_prompt(persona)

        system_prompt += "\n\nОграничения:\n"
        system_prompt += "- Не подсказывай ученице правильные ответы.\n"
        system_prompt += "- Не соглашайся на покупку сразу, пока не будут выполнены условия покупки.\n"
        system_prompt += "- Отвечай кратко, по делу, в personnage.\n"
        system_prompt += "- Не выдумывай событий, которых не было в диалоге.\n"

        if user_message is None:
            prompt = "Начни диалог. Представься и спроси, чем можешь помочь."
        else:
            prompt = f"Ученица написала: \"{user_message}\"\nОтветь от лица персонажа."

        history_text = ""
        for h in conversation_history[-10:]:
            prefix = "Ученица" if h["role"] == "user" else "Ты"
            history_text += f"{prefix}: {h['content']}\n"

        full_prompt = f"{history_text}\n{prompt}" if history_text else prompt

        try:
            reply = self.router.complete(
                prompt=full_prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=500,
            )
            return reply.strip() if reply else "..."
        except Exception as e:
            logger.error(f"Persona LLM error: {e}")
            return "Извини, сейчас не могу ответить. Попробуй ещё раз."

    def _default_system_prompt(self, persona: Persona) -> str:
        return (
            f"Ты — {persona.name}, {persona.role} из региона {persona.region}. "
            f"Твоя ниша: {persona.niche}. Сложность: {persona.difficulty}. "
            f"Скрытый痛: {persona.hidden_pain or 'не указан'}. "
            f"Возражения: {', '.join(persona.get_objections())}. "
            f"Условия покупки: {', '.join(persona.get_buy_conditions())}. "
            f"Условия провала: {', '.join(persona.get_fail_conditions())}. "
            "Отвечай в роли этого персонажа."
        )