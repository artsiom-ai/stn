import logging
from typing import Optional, Dict, Any, List

from app.models.skill import Skill
from app.models.mistake import Mistake
from app.models.evaluation import Evaluation
from app.models.test_attempt import TestAttempt
from app.database import SessionLocal

logger = logging.getLogger(__name__)

DEFAULT_SKILLS = [
    {
        "name": "Холодные продажи и контакт",
        "description": "Работа с холодным контактом, установление контакта, первый звонок",
        "level": 0.0,
    },
    {
        "name": "Работа с возражениями",
        "description": "Ответы на возражения клиента, препятствия к сделке",
        "level": 0.0,
    },
    {
        "name": "Презентация и закрытие",
        "description": "Презентация продукта, движение к сделке, закрытие",
        "level": 0.0,
    },
    {
        "name": "Базовая техническая грамотность",
        "description": "Понимание сайтов, ботов, автоматизации, CRM",
        "level": 0.0,
    },
    {
        "name": "Маркетинг и дизайн",
        "description": "Понимание маркетинга, дизайна, визуала",
        "level": 0.0,
    },
]


class ProgressService:
    def __init__(self, db=None):
        self.db = db
        self._close_db = False

    def _ensure_db(self):
        if self.db is None:
            self.db = SessionLocal()
            self._close_db = True

    def _close_db_if_needed(self):
        if self._close_db and self.db:
            self.db.close()
            self.db = None
            self._close_db = False

    def _init_default_skills(self):
        existing = self.db.query(Skill).all()
        existing_names = {s.name for s in existing}
        for skill_data in DEFAULT_SKILLS:
            if skill_data["name"] not in existing_names:
                skill = Skill(**skill_data)
                self.db.add(skill)
        self.db.commit()

    def calculate_progress(self) -> dict:
        self._ensure_db()
        try:
            self._init_default_skills()
            skills = self.db.query(Skill).all()

            mistakes = self.db.query(Mistake).all()
            evaluations = self.db.query(Evaluation).all()
            test_attempts = self.db.query(TestAttempt).all()

            skill_levels = {s.name: s.level for s in skills}
            skill_mentions = {s.name: 0 for s in skills}

            for m in mistakes:
                skill_name = m.skill
                if skill_name in skill_levels:
                    skill_levels[skill_name] = max(0, skill_levels[skill_name] - 5)
                    skill_mentions[skill_name] += 1

            for e in evaluations:
                if e.total_score >= 80:
                    for name in skill_levels:
                        skill_levels[name] = min(100, skill_levels[name] + 2)

            for ta in test_attempts:
                if ta.passed:
                    for name in skill_levels:
                        skill_levels[name] = min(100, skill_levels[name] + 1)

            for s in skills:
                s.level = skill_levels.get(s.name, s.level)
                self.db.add(s)
            self.db.commit()

            if skills:
                weak_skill = min(skills, key=lambda s: s.level)
                weak_skill_name = weak_skill.name
                weak_skill_level = weak_skill.level
            else:
                weak_skill_name = ""
                weak_skill_level = 0.0

            mistake_counts: Dict[str, int] = {}
            latest_mistake = None
            for m in mistakes:
                key = f"{m.skill}:{m.mistake_type}"
                mistake_counts[key] = mistake_counts.get(key, 0) + 1
                if latest_mistake is None or m.created_at > latest_mistake.created_at:
                    latest_mistake = m

            frequent_mistake = ""
            if mistake_counts:
                most_common = max(mistake_counts, key=mistake_counts.get)
                frequent_mistake = most_common

            if weak_skill_name:
                recommended_training = {
                    "skill": weak_skill_name,
                    "level": weak_skill_level,
                    "action": f"Потренируйте навык «{weak_skill_name}» — пройдите симуляцию с персонажем.",
                }
            else:
                recommended_training = {
                    "skill": "",
                    "level": 0.0,
                    "action": "Начните с любого урока, чтобы собрать первую статистику.",
                }

            return {
                "skills": [
                    {
                        "name": s.name,
                        "level": round(s.level, 1),
                        "description": s.description,
                    }
                    for s in skills
                ],
                "weak_skill": weak_skill_name,
                "frequent_mistake": frequent_mistake,
                "recommended_training": recommended_training,
            }
        finally:
            self._close_db_if_needed()

    def get_all_mistakes(self) -> List[dict]:
        self._ensure_db()
        try:
            mistakes = self.db.query(Mistake).all()
            return [
                {
                    "skill": m.skill,
                    "mistake_type": m.mistake_type,
                    "description": m.description,
                    "occurrences": 1,
                    "last_seen_at": m.created_at.isoformat() if m.created_at else None,
                }
                for m in mistakes
            ]
        finally:
            self._close_db_if_needed()