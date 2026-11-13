from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.services.simulation_service import SimulationService

router = APIRouter()


@router.post("/simulations/start")
def start_simulation(payload: dict, db: Session = Depends(get_db)):
    """
    Запуск сессии симуляции с ИИ-клиентом.
    Body: { "persona_id": int, "scenario_id": int|null, "difficulty": str }
    """
    persona_id = payload.get("persona_id")
    scenario_id = payload.get("scenario_id")
    difficulty = payload.get("difficulty", "medium")

    if persona_id is None:
        raise HTTPException(status_code=400, detail="persona_id is required")

    service = SimulationService()
    try:
        return service.start_simulation(
            persona_id=persona_id,
            scenario_id=scenario_id,
            difficulty=difficulty,
            db=db,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/simulations/{simulation_id}/messages")
def send_message(
    request: Request,
    simulation_id: int,
    payload: dict,
    db: Session = Depends(get_db),
):
    """
    Отправить сообщение ученицы и получить ответ персонажа.
    Body: { "content": str }
    """
    content = payload.get("content", "").strip()
    if not content:
        raise HTTPException(status_code=400, detail="content is required")

    if len(content) > settings.MAX_MESSAGE_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Сообщение слишком длинное. Максимум {settings.MAX_MESSAGE_LENGTH} символов.",
        )

    service = SimulationService()
    try:
        return service.send_message(
            simulation_id=simulation_id,
            content=content,
            db=db,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/simulations/{simulation_id}/finish")
def finish_simulation(simulation_id: int, db: Session = Depends(get_db)):
    """Завершить сессию симуляции."""
    service = SimulationService()
    try:
        return service.finish_simulation(simulation_id=simulation_id, db=db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))