from sqlalchemy.orm import Session
from src.schemas.quiz_schemas import QuizCreate, QuestionCreate, QuizUpdate, QuestionUpdate
from src.repository.quiz_repository import QuizRepository, QuestionRepository

quiz_repo = QuizRepository()
question_repo = QuestionRepository()

def create_quiz_service(db: Session, quiz: QuizCreate):
    existing_quiz = quiz_repo.get_quiz_by_title(db, quiz.title)
    if existing_quiz:
        return None
    return quiz_repo.create_quiz(db, quiz)

def get_quiz_service(db: Session, quiz_id: int):
    return quiz_repo.get_quiz_by_id(db, quiz_id)

def update_quiz_service(db: Session, quiz_id: int, quiz_update: QuizUpdate):
    return quiz_repo.update_quiz(db, quiz_id, quiz_update)

def delete_quiz_service(db: Session, quiz_id: int):
    return quiz_repo.delete_quiz(db, quiz_id)

def create_question_service(db: Session, question: QuestionCreate):
    existing_question = question_repo.get_question_by_text_and_quiz(db, question.text, question.quiz_id)
    if existing_question:
        return None
    return question_repo.create_question(db, question)

def get_question_service(db: Session, question_id: int):
    return question_repo.get_question_by_id(db, question_id)

def update_question_service(db: Session, question_id: int, question_update: QuestionUpdate):
    return question_repo.update_question(db, question_id, question_update)

def delete_question_service(db: Session, question_id: int):
    return question_repo.delete_question(db, question_id)
