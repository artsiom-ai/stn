from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.progress_service import ProgressService

router = APIRouter()


@router.get("/progress")
def get_progress(db: Session = Depends(get_db)):
    """Возвращает навыки, слабое место, частую ошибку и рекомендацию дня."""
    service = ProgressService(db=db)
    return service.calculate_progress()


@router.get("/mistakes")
def get_mistakes(db: Session = Depends(get_db)):
    """Возвращает журнал ошибок."""
    service = ProgressService(db=db)
    return service.get_all_mistakes()