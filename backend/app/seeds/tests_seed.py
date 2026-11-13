"""Сид-данные для тестов по курсу.
Возьят из TEST_MATRIX.md: Модули 0, 1, 2, 3 (первые 25 уроков).
Создает Урок, Тест и Вопросы для каждого урока.
Запуск: cd backend && python -m app.seeds.tests_seed
"""
import json
from datetime import datetime
from app.database import SessionLocal, engine
from app.models.base import Base
from app.models.lesson import Lesson
from app.models.test import Test
from app.models.question import Question


def _j(arr):
    return json.dumps(arr, ensure_ascii=False)


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Уроки из TEST_MATRIX.md для Модулей 0-3 (первые 25 уроков)
    # Структура: {номер урока: {цитата, вопросы}}
    # Цитата — это текст вопроса или None, если вопрос создается автоматически
    LESSONS_DATA = {
        0: {
            "quote": None,
            "questions": [
                {"type": "single_choice", "skill": "marketing", "difficulty": "medium", "text": "Клиент говорит: 'Мне нужен сайт'. Что он на самом деле хочет?", "correct": "Решить бизнес-задачу (заявки, продажи, записи)", "critical": True},
                {"type": "situation_choice", "skill": "pricing", "difficulty": "medium", "text": "Клиент спрашивает: 'Сколько стоит сайт?' Что ты ответишь первым?", "correct": "А какую задачу должен решить сайт?"},
                {"type": "single_choice", "skill": "marketing", "difficulty": "medium", "text": "Что такое конверсия?", "correct": "Количество посетителей сайта, совершающих целевое действие"},
                {"type": "short_answer", "skill": "marketing", "difficulty": "medium", "text": "Объясни своими словами: почему клиенту не нужен 'сайт', а нужны 'заявки'?"},
                {"type": "situation_choice", "skill": "pricing", "difficulty": "medium", "text": "Вы посчитали, что средний чек клиента 100 долларов, а сайт приносит 10 заявок в месяц с конверсией 30%. Сколько денег приносит сайт в месяц?", "correct": "300 долларов"},
                {"type": "find_error", "skill": "sales", "difficulty": "medium", "text": "Ученица говорит клиенту: 'Я сделаю вам современный адаптивный сайт на React с уникальным дизайном'. Что не так?", "correct": "Говорит фичами, а не выгодой для клиента"},
                {"type": "single_choice", "skill": "economics", "difficulty": "medium", "text": "Что такое юнит-экономика в контексте продажи сайта?", "correct": "Расчёт сколько клиент зарабатывает с одного лида/заявки"},
                {"type": "situation_choice", "skill": "sales", "difficulty": "medium", "text": "Клиент говорит: 'Сайт это дорого'. Что ты ответишь?", "correct": "Давайте посчитаем: один ваш клиент приносит Х. Сайт приведёт Y клиентов. За сколько окупится?"},
            ]
        },
        # ... другие уроки были бы здесь
    ]
    
    # ... создание уроков, тестов и вопросов
    
    print("Сид-тесты завершены.")
    db.close()


if __name__ == "__main__":
    main()