from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from src.config.database import get_db
from src.models.quiz_models import QuizAttempt
from src.models.quiz_models import User
from src.schemas.quiz_schemas import LeaderboardResponse
from typing import List

router = APIRouter()

@router.get("/leaderboard", response_model=List[LeaderboardResponse])
def get_leaderboard(db: Session = Depends(get_db)):
    subquery = db.query(
        QuizAttempt.candidate_id,
        QuizAttempt.quiz_id,
        func.max(QuizAttempt.score).label('best_score')
    ).group_by(QuizAttempt.candidate_id, QuizAttempt.quiz_id).subquery()

    leaderboard = db.query(
        subquery.c.candidate_id,
        User.username,
        func.sum(subquery.c.best_score).label('total_score')
    ).join(User, User.id == subquery.c.candidate_id) \
     .group_by(subquery.c.candidate_id, User.username) \
     .order_by(desc('total_score')).limit(10).all()

    if not leaderboard:
        raise HTTPException(status_code=404, detail="No leaderboard data found.")
    return leaderboard
