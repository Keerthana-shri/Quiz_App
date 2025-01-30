from sqlalchemy.orm import Session
from src.schemas.quiz_schemas import QuizCreate, QuestionCreate, QuizUpdate, QuestionUpdate
from src.repository.quiz_repository import QuizRepository, QuestionRepository
import random
from src.models.quiz_models import Quiz, Question

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
    quiz = quiz_repo.get_quiz_by_id(db, question.quiz_id)
    if not quiz:
        return "QuizNotFound", None
    
    existing_question = question_repo.get_question_by_text_and_quiz(db, question.text, question.quiz_id)
    if existing_question:
        return "QuestionExists", None
    
    created_question = question_repo.create_question(db, question)
    return created_question, quiz

def get_question_service(db: Session, question_id: int):
    return question_repo.get_question_by_id(db, question_id)

def update_question_service(db: Session, question_id: int, question_update: QuestionUpdate):
    return question_repo.update_question(db, question_id, question_update)

def delete_question_service(db: Session, question_id: int):
    return question_repo.delete_question(db, question_id)

def get_random_questions(db: Session, quiz_id: int, limit: int = 5):
    questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
    return random.sample(questions, min(len(questions), limit))

def get_quizzes_by_category(db: Session, topic: str, difficulty: str):
    return db.query(Quiz).filter(Quiz.topic == topic, Quiz.difficulty == difficulty).all()