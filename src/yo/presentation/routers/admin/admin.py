from fastapi import APIRouter

from .auth import auth_router

admin_router = APIRouter(prefix="/admin")
admin_router.include_router(auth_router)
