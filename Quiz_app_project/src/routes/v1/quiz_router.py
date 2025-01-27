from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.utils.dependencies import JWTBearer
from src.schemas.quiz_schemas import QuizCreate, QuizResponse, QuestionCreate
from src.services.quiz_services import create_quiz_service, create_question_service
from src.config.database import get_db

router = APIRouter()

@router.post("/quizzes/", dependencies=[Depends(JWTBearer())])
def create_quiz(quiz: QuizCreate, db: Session = Depends(get_db)):
    created_quiz = create_quiz_service(db, quiz)
    if created_quiz is None:
        raise HTTPException(status_code=400, detail="Quiz with this title already exists.")
    return {"message": f"The quiz for the provided title '{quiz.title}' is generated."}

@router.post("/questions/", dependencies=[Depends(JWTBearer())])
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    created_question = create_question_service(db, question)
    if created_question is None:
        raise HTTPException(status_code=400, detail="Question with this text and quiz association already exists.")
    return {"message": f"The question is added to the quiz with ID {question.quiz_id}."}
