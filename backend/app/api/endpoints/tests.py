import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.test import Test
from app.models.question import Question
from app.models.test_attempt import TestAttempt

router = APIRouter()


@router.get("/tests/{test_id}")
def get_test(test_id: int, db: Session = Depends(get_db)):
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    questions = (
        db.query(Question)
        .filter(Question.test_id == test_id)
        .order_by(Question.order_index)
        .all()
    )

    return {
        "id": test.id,
        "lesson_id": test.lesson_id,
        "title": test.title,
        "questions": [
            {
                "id": q.id,
                "question_text": q.question_text,
                "type": q.type,
                "options": q.get_options(),
                "order_index": q.order_index,
            }
            for q in questions
        ],
    }


@router.post("/tests/{test_id}/attempt")
def submit_test_attempt(test_id: int, payload: dict, db: Session = Depends(get_db)):
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    answers = payload.get("answers", [])
    questions = (
        db.query(Question)
        .filter(Question.test_id == test_id)
        .all()
    )
    question_map = {q.id: q for q in questions}

    wrong_question_ids = []
    explanations = []
    score = 0

    for answer in answers:
        qid = answer.get("question_id")
        selected = answer.get("selected_answer", "")
        q = question_map.get(qid)
        if not q:
            continue
        if str(selected).strip().lower() == str(q.correct_answer).strip().lower():
            score += 1
        else:
            wrong_question_ids.append(qid)
            explanations.append(
                {
                    "question_id": qid,
                    "correct_answer": q.correct_answer,
                    "explanation": q.explanation or "",
                }
            )

    total = len(questions)
    passed = (score / total * 100) >= test.min_pass_score if total > 0 else False

    attempt = TestAttempt(
        test_id=test_id,
        score=score,
        passed=passed,
        wrong_question_ids=json.dumps(wrong_question_ids, ensure_ascii=False),
        explanations=json.dumps(explanations, ensure_ascii=False),
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return {
        "attempt_id": attempt.id,
        "score": score,
        "passed": passed,
        "wrong_question_ids": wrong_question_ids,
        "explanations": explanations,
    }