from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.quiz_schemas import QuizCreate, QuizResponse, QuizUpdate, QuestionCreate, QuestionResponse, QuestionUpdate, QuestionOptionSchema
from src.services.quiz_services import (
    create_quiz_service, create_question_service, get_quiz_service,
    update_quiz_service, delete_quiz_service, get_question_service,
    update_question_service, delete_question_service, get_random_questions, get_quizzes_by_category
)
from src.config.database import get_db

router = APIRouter()

@router.get("/quizzes/category")
def fetch_quizzes_by_category(topic: str, difficulty: str, db: Session = Depends(get_db)):
    quizzes = get_quizzes_by_category(db, topic, difficulty)
    if not quizzes:
        raise HTTPException(status_code=404, detail="Quiz with this category is not found.")
    return quizzes

@router.get("/quizzes/{quiz_id}/random-questions")
def fetch_random_questions(quiz_id: int, page: int = 1, page_size: int = 5, db: Session = Depends(get_db)):
    return get_random_questions(db, quiz_id, page, page_size)

@router.get("/quizzes/{quiz_id}", response_model=QuizResponse)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = get_quiz_service(db, quiz_id)
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found.")
    return quiz

@router.post("/quizzes/")
def create_quiz(quiz: QuizCreate, db: Session = Depends(get_db)):
    created_quiz = create_quiz_service(db, quiz)
    if created_quiz is None:
        raise HTTPException(status_code=400, detail="Quiz with this title already exists.")
    return {"message": f"Quiz '{created_quiz.title}' with id {created_quiz.id} created successfully."}

@router.put("/quizzes/{quiz_id}", response_model=QuizResponse)
def update_quiz(quiz_id: int, quiz_update: QuizUpdate, db: Session = Depends(get_db)):
    updated_quiz = update_quiz_service(db, quiz_id, quiz_update)
    if updated_quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found.")
    return {"message": "Quiz updated successfully."}

@router.delete("/quizzes/{quiz_id}")
def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    deleted = delete_quiz_service(db, quiz_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Quiz not found.")
    return {"message": "Quiz deleted successfully."}

@router.post("/questions/")
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    created_question, quiz = create_question_service(db, question)
    if created_question == "QuizNotFound":
        raise HTTPException(status_code=404, detail=f"Quiz with id {question.quiz_id} doesn't exist")
    elif created_question == "QuestionExists":
        raise HTTPException(status_code=400, detail="Question with this text and quiz association already exists.")
    
    return {"message": "Question created successfully."}

@router.get("/questions/{question_id}", response_model=QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = get_question_service(db, question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found.")
    return question

@router.put("/questions/{question_id}")
def update_question(question_id: int, question_update: QuestionUpdate, db: Session = Depends(get_db)):
    updated_question = update_question_service(db, question_id, question_update)
    if updated_question is None:
        raise HTTPException(status_code=404, detail="Question not found.")
    return {"message": "Question updated successfully."}


@router.delete("/questions/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    deleted = delete_question_service(db, question_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Question not found.")
    return {"message": "Question deleted successfully."}