from sqlalchemy.orm import Session
from src.schemas.quiz_schemas import QuizCreate, QuestionCreate
from src.repository.quiz_repository import QuizRepository, QuestionRepository

quiz_repo = QuizRepository()
question_repo = QuestionRepository()

def create_quiz_service(db: Session, quiz: QuizCreate):
    existing_quiz = quiz_repo.get_quiz_by_title(db, quiz.title)
    if existing_quiz:
        return None
    return quiz_repo.create_quiz(db, quiz)

def create_question_service(db: Session, question: QuestionCreate):
    existing_question = question_repo.get_question_by_text_and_quiz(db, question.text, question.quiz_id)
    if existing_question:
        return None
    return question_repo.create_question(db, question)
