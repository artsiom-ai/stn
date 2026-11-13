import json
import logging
from typing import Optional, Dict, Any, List

from app.llm.router import LLMRouter
from app.models.persona import Persona
from app.models.simulation import Simulation
from app.models.message import Message
from app.models.evaluation import Evaluation
from app.models.mistake import Mistake
from app.database import SessionLocal

logger = logging.getLogger(__name__)


class JudgeService:
    def __init__(self):
        self.router = LLMRouter()

    def _load_prompt(self) -> str:
        try:
            with open("app/prompts/judge_prompt.txt", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return "Проанализируй диалог и верни JSON с оценкой: total_score, rubric, strengths, weaknesses, recommendations, mistakes."

    def evaluate_simulation(self, simulation_id: int, db) -> dict:
        sim = db.query(Simulation).filter(Simulation.id == simulation_id).first()
        if not sim:
            raise ValueError(f"Simulation with id={simulation_id} not found")
        if sim.status != "finished":
            raise ValueError("Simulation is not finished yet")

        existing = db.query(Evaluation).filter(Evaluation.simulation_id == simulation_id).first()
        if existing:
            return self._evaluation_to_dict(existing, db)

        persona = db.query(Persona).filter(Persona.id == sim.persona_id).first()
        if not persona:
            raise ValueError(f"Persona with id={sim.persona_id} not found")

        messages = (
            db.query(Message)
            .filter(Message.simulation_id == simulation_id)
            .order_by(Message.created_at)
            .all()
        )

        dialog_lines = []
        for m in messages:
            role_label = "Ученица" if m.sender == "user" else "Клиент"
            dialog_lines.append(f"{role_label}: {m.content}")
        dialog_transcript = "\n".join(dialog_lines)

        prompt_template = self._load_prompt()
        prompt = prompt_template.format(
            dialog_transcript=dialog_transcript,
            persona_name=persona.name,
            persona_role=persona.role,
            persona_niche=persona.niche,
            persona_difficulty=sim.difficulty,
            hidden_pain=persona.hidden_pain or "не указано",
            objections=", ".join(persona.get_objections()),
            buy_conditions=", ".join(persona.get_buy_conditions()),
            fail_conditions=", ".join(persona.get_fail_conditions()),
        )

        try:
            result = self.router.complete_json(
                prompt=prompt,
                system_prompt="Ты — опытный наставник по продажам. Анализируй диалог и возвращай строго JSON. Не выдумывай событий.",
                temperature=0.3,
                max_tokens=2000,
                max_retries=2,
            )
        except Exception as e:
            logger.error(f"Judge LLM failed: {e}")
            raise ValueError(f"Не удалось получить оценку от судии: {e}")
        total_score = int(result.get("total_score", 0))
        rubric = result.get("rubric", {})
        strengths = result.get("strengths", [])
        weaknesses = result.get("weaknesses", [])
        recommendations = result.get("recommendations", [])
        mistakes_data = result.get("mistakes", [])

        evaluation = Evaluation(
            simulation_id=simulation_id,
            total_score=total_score,
            rubric_json=json.dumps(rubric, ensure_ascii=False),
            judge_summary=f"Итоговая оценка: {total_score}/100",
            strengths=json.dumps(strengths, ensure_ascii=False),
            weaknesses=json.dumps(weaknesses, ensure_ascii=False),
            recommendations=json.dumps(recommendations, ensure_ascii=False),
        )
        db.add(evaluation)
        db.commit()
        db.refresh(evaluation)

        for m in mistakes_data:
            mistake = Mistake(
                simulation_id=simulation_id,
                skill=m.get("skill", "общее"),
                mistake_type=m.get("mistake_type", "ошибка"),
                description=m.get("description", ""),
                recommendation=m.get("recommendation", ""),
            )
            db.add(mistake)

        db.commit()

        return self._evaluation_to_dict(evaluation, db)

    def get_evaluation(self, simulation_id: int, db) -> Optional[dict]:
        evaluation = db.query(Evaluation).filter(Evaluation.simulation_id == simulation_id).first()
        if not evaluation:
            return None
        return self._evaluation_to_dict(evaluation, db)

    def get_mistakes(self, simulation_id: int, db) -> List[dict]:
        mistakes = (
            db.query(Mistake)
            .filter(Mistake.simulation_id == simulation_id)
            .all()
        )
        return [
            {
                "skill": m.skill,
                "mistake_type": m.mistake_type,
                "description": m.description,
                "occurrences": 1,
                "last_seen_at": m.created_at.isoformat() if m.created_at else None,
                "recommendation": m.recommendation,
            }
            for m in mistakes
        ]

    def _evaluation_to_dict(self, evaluation: Evaluation, db) -> dict:
        mistakes = self.get_mistakes(evaluation.simulation_id, db)
        return {
            "simulation_id": evaluation.simulation_id,
            "total_score": evaluation.total_score,
            "rubric": evaluation.get_rubric(),
            "judge_summary": evaluation.judge_summary,
            "strengths": evaluation.get_strengths(),
            "weaknesses": evaluation.get_weaknesses(),
            "recommendations": evaluation.get_recommendations(),
            "mistakes": mistakes,
        }