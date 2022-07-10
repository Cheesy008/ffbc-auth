from fastapi import APIRouter

from src.routes.auth import auth_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
