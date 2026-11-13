"""Скрипт для ручного сида тестовых уроков и тестов.
Запуск: cd backend && python seed_data.py
"""
import json
from app.database import SessionLocal, engine
from app.models.base import Base
from app.models.lesson import Lesson
from app.models.test import Test
from app.models.question import Question


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Проверяем, не засеяны ли уже данные
    if db.query(Lesson).first():
        print("Данные уже засеяны, пропускаем.")
        db.close()
        return

    # Урок 1
    lesson1 = Lesson(
        module_code="sales_basics",
        module_title="Основы продаж",
        lesson_code="cold_intro",
        title="Холодное знакомство и первый контакт",
        short_description="Как правильно начать разговор с потенциальным клиентом по продаже сайтов и ботов.",
        theory_markdown="# Холодное знакомство\n\nГлавное правило — не продавать с первых слов. Сначала установите контакт, задайте вопросы о бизнесе клиента, выявите боль.",
        difficulty="easy",
        has_test=True,
        has_simulation=True,
    )
    db.add(lesson1)
    db.commit()
    db.refresh(lesson1)

    test1 = Test(
        lesson_id=lesson1.id,
        title="Тест: холодное знакомство",
        question_count=3,
        min_pass_score=80,
    )
    db.add(test1)
    db.commit()
    db.refresh(test1)

    q1 = Question(
        test_id=test1.id,
        type="single_choice",
        skill="sales",
        difficulty="easy",
        question_text="Что НЕ рекомендуется делать в первом сообщении холодного контакта?",
        options_json=json.dumps([
            "Рассказать о своем опыте и кейсах",
            "Сразу предложить купить сайт за 50 000 рублей",
            "Задать вопрос о текущем сайте клиента",
            "Предложить бесплатный аудит",
        ], ensure_ascii=False),
        correct_answer="Сразу предложить купить сайт за 50 000 рублей",
        explanation="Сначала нужно выявить потребность клиента, а не продавать с первой фразы.",
        is_critical=False,
        order_index=1,
    )
    q2 = Question(
        test_id=test1.id,
        type="single_choice",
        skill="sales",
        difficulty="easy",
        question_text="Какой тон общения лучше выбрать при холодном звонке?",
        options_json=json.dumps([
            "Агрессивный и настойчивый",
            "Вежливый, дружелюбный, заинтересованный",
            "Сухой и формальный",
        ], ensure_ascii=False),
        correct_answer="Вежливый, дружелюбный, заинтересованный",
        explanation="Клиент должен почувствовать комфорт, а не давление.",
        is_critical=False,
        order_index=2,
    )
    q3 = Question(
        test_id=test1.id,
        type="single_choice",
        skill="sales",
        difficulty="easy",
        question_text="Сколько времени ideally отводить на первую часть холодного звонка (установление контакта)?",
        options_json=json.dumps([
            "1-2 минуты",
            "15-20 минут",
            "Весь звонок",
        ], ensure_ascii=False),
        correct_answer="1-2 минуты",
        explanation="Контакт устанавливается быстро, затем переходим к выявлению потребностей.",
        is_critical=False,
        order_index=3,
    )
    db.add_all([q1, q2, q3])
    db.commit()

    print(f"Создан урок id={lesson1.id}, тест id={test1.id}, 3 вопроса.")
    db.close()


if __name__ == "__main__":
    main()