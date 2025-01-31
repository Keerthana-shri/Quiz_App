from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.schemas.quiz_schemas import QuizResponse, QuizAttemptCreate, QuizAttemptResponse
from src.services.quiz_services import create_quiz_attempt_service, get_quizzes_by_category,get_quiz_service, get_quiz_attempts_by_candidate_service, get_random_questions
from src.config.database import get_db
from src.utils.dependencies import get_current_candidate
from src.models.auth_models import User 

router = APIRouter()

@router.get("/quizzes/category", dependencies=[Depends(get_current_candidate)])
def fetch_quizzes_by_category(topic: str, difficulty: str, db: Session = Depends(get_db)):
    quizzes = get_quizzes_by_category(db, topic, difficulty)
    if not quizzes:
        raise HTTPException(status_code=404, detail="Quiz with this category is not found.")
    return quizzes

@router.get("/quizzes/{quiz_id}/random-questions", dependencies=[Depends(get_current_candidate)])
def fetch_random_questions(quiz_id: int, page: int = 1, page_size: int = 5, db: Session = Depends(get_db)):
    return get_random_questions(db, quiz_id, page, page_size)

@router.get("/quizzes/{quiz_id}", response_model=QuizResponse, dependencies=[Depends(get_current_candidate)])
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = get_quiz_service(db, quiz_id)
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found.")
    return quiz

@router.post("/quizzes/{quiz_id}/attempt", response_model=QuizAttemptResponse, dependencies=[Depends(get_current_candidate)])
def attempt_quiz(quiz_id: int, answers: dict, db: Session = Depends(get_db), current_candidate: User = Depends(get_current_candidate)):
    quiz_attempt = create_quiz_attempt_service(db, current_candidate.id, quiz_id, answers)
    return quiz_attempt

@router.get("/candidates/{candidate_id}/attempts", response_model=List[QuizAttemptResponse], dependencies=[Depends(get_current_candidate)])
def get_quiz_attempts(candidate_id: int, db: Session = Depends(get_db), current_candidate: User = Depends(get_current_candidate)):
    if candidate_id != current_candidate.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this candidate's attempts")
    return get_quiz_attempts_by_candidate_service(db, candidate_id)