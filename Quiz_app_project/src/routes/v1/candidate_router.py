from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List
from src.schemas.quiz_schemas import QuizCandidateResponse, QuizAttemptBaseResponse, QuizAttemptDetailedResponse
from src.services.quiz_services import create_quiz_attempt_service, get_quizzes_by_category, get_quiz_service, get_quiz_attempts_by_candidate_service, get_random_questions, calculate_score_for_attempt
from src.config.database import get_db
from src.utils.dependencies import get_current_candidate
from src.models.auth_models import User 

router = APIRouter()

@router.get("/quizzes/category", response_model=List[QuizCandidateResponse], dependencies=[Depends(get_current_candidate)])
def fetch_quizzes_by_category(topic: str, difficulty: str, db: Session = Depends(get_db), current_candidate: User = Depends(get_current_candidate)):
    quizzes = get_quizzes_by_category(db, topic, difficulty, is_admin=False)
    if not quizzes:
        raise HTTPException(status_code=404, detail="Quiz with this category is not found.")
    return quizzes

@router.get("/quizzes/{quiz_id}/random-questions", response_model=QuizCandidateResponse, dependencies=[Depends(get_current_candidate)])
def fetch_random_questions(quiz_id: int, page: int = 1, page_size: int = 5, db: Session = Depends(get_db)):
    return get_random_questions(db, quiz_id, page, page_size)

@router.get("/quizzes/{quiz_id}", response_model=QuizCandidateResponse, dependencies=[Depends(get_current_candidate)])
def get_quiz(quiz_id: int, db: Session = Depends(get_db), current_candidate: User = Depends(get_current_candidate)):
    quiz = get_quiz_service(db, quiz_id, is_admin=False)
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found.")
    return quiz

@router.post("/quizzes/{quiz_id}/attempt", response_model=QuizAttemptBaseResponse, dependencies=[Depends(get_current_candidate)])
def attempt_quiz(quiz_id: int, answers: dict = Body(..., example={"question_id_1": "answer_1", "question_id_2": "answer_2"}), db: Session = Depends(get_db), current_candidate: User = Depends(get_current_candidate)):
    result, attempt = create_quiz_attempt_service(db, current_candidate.id, quiz_id, answers)
    if result == "IncompleteAttempt":
        raise HTTPException(status_code=400, detail="Attempt is incomplete. Please answer all questions before submitting.")
    return attempt

@router.post("/attempts/{attempt_id}/calculate-score", response_model=QuizAttemptDetailedResponse, dependencies=[Depends(get_current_candidate)])
def calculate_score(attempt_id: int, db: Session = Depends(get_db), current_candidate: User = Depends(get_current_candidate)):
    attempt = calculate_score_for_attempt(db, attempt_id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found.")
    return attempt

@router.get("/candidates/{candidate_id}/attempts", response_model=List[QuizAttemptDetailedResponse], dependencies=[Depends(get_current_candidate)])
def get_quiz_attempts(candidate_id: int, db: Session = Depends(get_db), current_candidate: User = Depends(get_current_candidate)):
    if candidate_id != current_candidate.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this candidate's attempts")
    return get_quiz_attempts_by_candidate_service(db, candidate_id)
