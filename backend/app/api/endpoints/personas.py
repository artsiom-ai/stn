from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.persona import Persona

router = APIRouter()


@router.get("/personas")
def list_personas(db: Session = Depends(get_db)):
    personas = db.query(Persona).all()
    return [
        {
            "id": p.id,
            "code": p.code,
            "name": p.name,
            "role": p.role,
            "region": p.region,
            "niche": p.niche,
            "difficulty": p.difficulty,
            "tags": p.get_tags(),
        }
        for p in personas
    ]


@router.get("/personas/{persona_id}")
def get_persona(persona_id: int, db: Session = Depends(get_db)):
    persona = db.query(Persona).filter(Persona.id == persona_id).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona not found")

    return {
        "id": persona.id,
        "name": persona.name,
        "role": persona.role,
        "region": persona.region,
        "niche": persona.niche,
        "difficulty": persona.difficulty,
        "temperament": persona.temperament,
        "budget_level": persona.budget_level,
        "urgency_level": persona.urgency_level,
        "hidden_pain": persona.hidden_pain,
        "objections": persona.get_objections(),
        "buy_conditions": persona.get_buy_conditions(),
        "fail_conditions": persona.get_fail_conditions(),
    }