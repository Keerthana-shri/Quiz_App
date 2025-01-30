from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.quiz_schemas import QuizResponse
from src.services.quiz_services import get_quiz_service, get_random_questions, get_quizzes_by_category
from src.config.database import get_db
from src.utils.dependencies import get_current_candidate

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