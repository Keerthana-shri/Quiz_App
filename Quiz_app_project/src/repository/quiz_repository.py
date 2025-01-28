from sqlalchemy.orm import Session
from src.models.quiz_models import Quiz, Question
from src.schemas.quiz_schemas import QuizCreate, QuestionCreate, QuizUpdate, QuestionUpdate

class QuizRepository:
    def create_quiz(self, db: Session, quiz: QuizCreate):
        db_quiz = Quiz(**quiz.dict())
        db.add(db_quiz)
        db.commit()
        db.refresh(db_quiz)
        return db_quiz

    def get_quiz_by_title(self, db: Session, title: str):
        return db.query(Quiz).filter(Quiz.title == title).first()

    def get_quiz_by_id(self, db: Session, quiz_id: int):
        return db.query(Quiz).filter(Quiz.id == quiz_id).first()

    def update_quiz(self, db: Session, quiz_id: int, quiz_update: QuizUpdate):
        quiz = self.get_quiz_by_id(db, quiz_id)
        if not quiz:
            return None
        for key, value in quiz_update.dict(exclude_unset=True).items():
            setattr(quiz, key, value)
        db.commit()
        db.refresh(quiz)
        return quiz

    def delete_quiz(self, db: Session, quiz_id: int):
        quiz = self.get_quiz_by_id(db, quiz_id)
        if not quiz:
            return False
        db.delete(quiz)
        db.commit()
        return True

class QuestionRepository:
    def create_question(self, db: Session, question: QuestionCreate):
        db_question = Question(**question.dict())
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        return db_question

    def get_question_by_text_and_quiz(self, db: Session, text: str, quiz_id: int):
        return db.query(Question).filter(Question.text == text, Question.quiz_id == quiz_id).first()

    def get_question_by_id(self, db: Session, question_id: int):
        return db.query(Question).filter(Question.id == question_id).first()

    def update_question(self, db: Session, question_id: int, question_update: QuestionUpdate):
        question = self.get_question_by_id(db, question_id)
        if not question:
            return None
        for key, value in question_update.dict(exclude_unset=True).items():
            setattr(question, key, value)
        db.commit()
        db.refresh(question)
        return question

    def delete_question(self, db: Session, question_id: int):
        question = self.get_question_by_id(db, question_id)
        if not question:
            return False
        db.delete(question)
        db.commit()
        return True