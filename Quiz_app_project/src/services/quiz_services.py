from sqlalchemy.orm import Session
from src.schemas.quiz_schemas import QuizCreate, QuestionCreate, QuizUpdate, QuestionUpdate, QuizResponse, QuizCandidateResponse, QuizAttemptBaseResponse, QuizAttemptDetailedResponse
from src.repository.quiz_repository import QuizRepository, QuestionRepository, QuizAttemptRepository
import random
from src.models.quiz_models import Quiz, Question, QuestionOption, QuizAttempt
from datetime import datetime

quiz_repo = QuizRepository()
question_repo = QuestionRepository()
quiz_attempt_repo = QuizAttemptRepository()

def create_quiz_service(db: Session, quiz: QuizCreate):
    existing_quiz = quiz_repo.get_quiz_by_title(db, quiz.title)
    if existing_quiz:
        return None
    return quiz_repo.create_quiz(db, quiz)

def get_quiz_service(db: Session, quiz_id: int, is_admin: bool):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        return None
    
    questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
    quiz.questions = questions
    
    if is_admin:
        return QuizResponse.from_orm(quiz)
    else:
        return QuizCandidateResponse.from_orm(quiz)

def get_quizzes_by_category(db: Session, topic: str, difficulty: str, is_admin: bool):
    quizzes = db.query(Quiz).filter(Quiz.topic == topic, Quiz.difficulty == difficulty).all()
    
    if not quizzes:
        return None
    
    for quiz in quizzes:
        quiz.questions = db.query(Question).filter(Question.quiz_id == quiz.id).all()
    
    if is_admin:
        return [QuizResponse.from_orm(quiz) for quiz in quizzes]
    else:
        return [QuizCandidateResponse.from_orm(quiz) for quiz in quizzes]

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
                db_option = QuestionOption(
                    option_text=option["option_text"],
                    is_correct=option.get("is_correct", False),
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
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        return None
    
    questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
    random_questions = random.sample(questions, min(len(questions), page * page_size))
    
    start = (page - 1) * page_size
    end = start + page_size
    paginated_questions = random_questions[start:end]
    
    candidate_questions = []
    for question in paginated_questions:
        candidate_question = {
            "text": question.text,
            "question_type": question.question_type,
            "image_url": question.image_url,
            "options": [{"option_text": option.option_text} for option in question.options],
            "quiz_id": question.quiz_id
        }
        candidate_questions.append(candidate_question)
    
    return {
        "id": quiz.id,
        "title": quiz.title,
        "topic": quiz.topic,
        "difficulty": quiz.difficulty,
        "timer": quiz.timer,
        "questions": candidate_questions
    }

def create_quiz_attempt_service(db: Session, candidate_id: int, quiz_id: int, answers: dict):
    # Fetch all questions for the quiz
    questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
    question_ids = {str(question.id) for question in questions}
    
    # Check if all questions are answered
    if not question_ids.issubset(answers.keys()):
        return "IncompleteAttempt", None
    
    attempt_number = db.query(QuizAttempt).filter(QuizAttempt.candidate_id == candidate_id, QuizAttempt.quiz_id == quiz_id).count() + 1
    quiz_attempt = QuizAttempt(
        candidate_id=candidate_id,
        quiz_id=quiz_id,
        attempt_number=attempt_number,
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow(),
        answers=answers
    )
    db.add(quiz_attempt)
    db.commit()
    db.refresh(quiz_attempt)
    return "Success", QuizAttemptBaseResponse.from_orm(quiz_attempt)

def calculate_score_for_attempt(db: Session, attempt_id: int):
    attempt = db.query(QuizAttempt).filter(QuizAttempt.id == attempt_id).first()
    if not attempt:
        return None
    
    answers = attempt.answers  # Assuming answers are stored in the attempt
    questions = db.query(Question).filter(Question.quiz_id == attempt.quiz_id).all()
    score = 0
    correct_answers = 0
    wrong_answers = 0
    for question in questions:
        if str(question.id) in answers and question.correct_answer.strip().lower() == answers[str(question.id)].strip().lower():
            score += 1
            correct_answers += 1
        else:
            wrong_answers += 1
    total_questions = len(questions)
    score_percentage = (score / total_questions) * 100
    
    # Update the attempt with the calculated score
    attempt.score = score_percentage
    attempt.correct_answers = correct_answers
    attempt.wrong_answers = wrong_answers
    db.commit()
    db.refresh(attempt)
    
    return QuizAttemptDetailedResponse.from_orm(attempt)

def get_quiz_attempts_by_candidate_service(db: Session, candidate_id: int):
    attempts = quiz_attempt_repo.get_quiz_attempts_by_candidate(db, candidate_id)
    return [QuizAttemptDetailedResponse.from_orm(attempt) for attempt in attempts]
