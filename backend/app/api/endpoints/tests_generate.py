from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.test_generator import TestGenerator

router = APIRouter()


@router.post("/tests/generate/{lesson_id}")
def generate_test(lesson_id: int, db: Session = Depends(get_db)):
    """
    Генерирует тест с 5 вопросами по теме урока через LLM.
    Сохраняет тест и вопросы в БД. Возвращает тест без правильных ответов.
    """
    generator = TestGenerator()
    try:
        return generator.generate_test_for_lesson(lesson_id, db=db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации теста: {e}")