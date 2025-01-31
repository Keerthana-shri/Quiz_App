from sqlalchemy.orm import Session
from src.schemas.quiz_schemas import QuizCreate, QuestionCreate, QuizUpdate, QuestionUpdate
from src.repository.quiz_repository import QuizRepository, QuestionRepository, QuizAttemptRepository
import random
from src.models.quiz_models import Quiz, Question, QuestionOption

quiz_repo = QuizRepository()
question_repo = QuestionRepository()
quiz_attempt_repo = QuizAttemptRepository()

def create_quiz_service(db: Session, quiz: QuizCreate):
    existing_quiz = quiz_repo.get_quiz_by_title(db, quiz.title)
    if existing_quiz:
        return None
    return quiz_repo.create_quiz(db, quiz)

def get_quiz_service(db: Session, quiz_id: int):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        return None
    
    # Load questions associated with the quiz
    questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
    quiz.questions = questions
    return quiz

def get_quizzes_by_category(db: Session, topic: str, difficulty: str):
    quizzes = db.query(Quiz).filter(Quiz.topic == topic, Quiz.difficulty == difficulty).all()
    
    if not quizzes:
        return None
    
    for quiz in quizzes:
        # Load all questions related to this quiz
        quiz.questions = db.query(Question).filter(Question.quiz_id == quiz.id).all()
    
    return quizzes

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

def update_question_service(db: Session, question_id: int, question_update: QuestionUpdate):
    question = question_repo.get_question_by_id(db, question_id)
    if not question:
        return None
    
    for key, value in question_update.dict(exclude_unset=True).items():
        if key == "options":
            db.query(QuestionOption).filter(QuestionOption.question_id == question_id).delete()
            for option in value:
                is_correct = option["is_correct"] if 'is_correct' in option else (option["option_text"] == question_update.correct_answer)
                db_option = QuestionOption(
                    option_text=option["option_text"],
                    is_correct=is_correct,
                    question_id=question_id
                )
                db.add(db_option)
        else:
            setattr(question, key, value)
    
    db.commit()
    db.refresh(question)
    return question

def get_question_service(db: Session, question_id: int):
    return question_repo.get_question_by_id(db, question_id)

def delete_question_service(db: Session, question_id: int):
    return question_repo.delete_question(db, question_id)

def get_random_questions(db: Session, quiz_id: int, page: int = 1, page_size: int = 5):
    questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
    random_questions = random.sample(questions, min(len(questions), page * page_size))
    
    # Paginate the random questions
    start = (page - 1) * page_size
    end = start + page_size
    paginated_questions = random_questions[start:end]
    
    # Assign sequential numbers to the questions
    for idx, question in enumerate(paginated_questions, start=1):
        question.id = idx
    
    return paginated_questions

def calculate_score(db: Session, quiz_id: int, answers: dict):
    questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
    score = 0
    for question in questions:
        if question.id in answers and question.correct_answer == answers[question.id]:
            score += 1
    return score / len(questions) * 100

def create_quiz_attempt_service(db: Session, candidate_id: int, quiz_id: int, answers: dict):
    score = calculate_score(db, quiz_id, answers)
    return quiz_attempt_repo.create_quiz_attempt(db, candidate_id, quiz_id, score)

def get_quiz_attempts_by_candidate_service(db: Session, candidate_id: int):
    return quiz_attempt_repo.get_quiz_attempts_by_candidate(db, candidate_id)