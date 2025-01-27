from fastapi import APIRouter
from src.routes.v1 import auth_router
from src.routes.v1 import quiz_router

api_router = APIRouter()
api_router.include_router(auth_router.router, prefix="/v1", tags=["authentication"])
api_router.include_router(quiz_router.router, prefix="/v1", tags=["Quiz Management"])
