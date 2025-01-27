from fastapi import APIRouter
from src.routes.v1 import auth_router

api_router = APIRouter()
api_router.include_router(auth_router.router, prefix="/v1", tags=["authentication"])
