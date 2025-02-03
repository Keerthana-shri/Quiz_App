from fastapi import APIRouter
from src.routes.v1 import auth_router, admin_router, candidate_router, leaderboard_router


api_router = APIRouter()
api_router.include_router(auth_router.router, prefix="/v1", tags=["Authentication"])
api_router.include_router(admin_router.router, prefix="/v1/admin", tags=["Admin"])
api_router.include_router(candidate_router.router, prefix="/v1/candidate", tags=["Candidate"])
api_router.include_router(leaderboard_router.router, prefix="/v1/leaderboard", tags=["Leaderboard"])
