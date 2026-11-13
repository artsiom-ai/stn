from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.judge_service import JudgeService

router = APIRouter()


@router.post("/simulations/{simulation_id}/evaluate")
def evaluate_simulation(simulation_id: int, db: Session = Depends(get_db)):
    """Запустить ИИ-судью над завершённой сессией и получить оценку."""
    service = JudgeService()
    try:
        return service.evaluate_simulation(simulation_id=simulation_id, db=db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/simulations/{simulation_id}/evaluation")
def get_evaluation(simulation_id: int, db: Session = Depends(get_db)):
    """Получить сохранённую оценку симуляции."""
    service = JudgeService()
    result = service.get_evaluation(simulation_id=simulation_id, db=db)
    if not result:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return result


@router.get("/simulations/{simulation_id}/mistakes")
def get_mistakes(simulation_id: int, db: Session = Depends(get_db)):
    """Получить список ошибок ученицы по симуляции."""
    service = JudgeService()
    return service.get_mistakes(simulation_id=simulation_id, db=db)