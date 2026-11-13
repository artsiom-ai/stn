from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.lesson import Lesson
from app.models.test import Test

router = APIRouter()


@router.get("/lessons")
def list_lessons(db: Session = Depends(get_db)):
    lessons = db.query(Lesson).all()
    return [
        {
            "id": l.id,
            "module_code": l.module_code,
            "module_title": l.module_title,
            "lesson_code": l.lesson_code,
            "title": l.title,
            "short_description": l.short_description,
            "difficulty": l.difficulty,
            "is_completed": False,
            "has_test": l.has_test,
            "has_simulation": l.has_simulation,
        }
        for l in lessons
    ]


@router.get("/lessons/{lesson_id}")
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    test = db.query(Test).filter(Test.lesson_id == lesson_id).first()

    return {
        "id": lesson.id,
        "title": lesson.title,
        "theory_markdown": lesson.theory_markdown or "",
        "skills": [],
        "test": (
            {
                "id": test.id,
                "question_count": test.question_count,
                "min_pass_score": test.min_pass_score,
            }
            if test
            else None
        ),
        "simulation_scenarios": [],
    }