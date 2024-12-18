from fastapi import APIRouter

from .auth import auth_router

user_router = APIRouter()
user_router.include_router(auth_router)
