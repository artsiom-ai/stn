from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.database import engine

router = APIRouter()


@router.get("/health")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "degraded", "database": "disconnected", "detail": str(e)}


@router.get("/health/db")
def health_db():
    """Проверяет реальное соединение с базой данных.
    Выполняет SELECT 1 и возвращает статус."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except OperationalError as e:
        return {"status": "degraded", "database": "disconnected", "detail": str(e)}
    except Exception as e:
        return {"status": "error", "database": "unknown", "detail": str(e)}