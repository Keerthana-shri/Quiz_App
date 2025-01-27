from sqlalchemy.orm import Session
from src.models.quiz_models import Quiz, Question
from src.schemas.quiz_schemas import QuizCreate, QuestionCreate

class QuizRepository:
    def create_quiz(self, db: Session, quiz: QuizCreate):
        db_quiz = Quiz(**quiz.dict())
        db.add(db_quiz)
        db.commit()
        db.refresh(db_quiz)
        return db_quiz

    def get_quiz_by_title(self, db: Session, title: str):
        return db.query(Quiz).filter(Quiz.title == title).first()

class QuestionRepository:
    def create_question(self, db: Session, question: QuestionCreate):
        db_question = Question(**question.dict())
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        return db_question

    def get_question_by_text_and_quiz(self, db: Session, text: str, quiz_id: int):
        return db.query(Question).filter(Question.text == text, Question.quiz_id == quiz_id).first()
