from fastapi import APIRouter
from src.endpoints.v1.users import view as users_view

api_v1_router = APIRouter()
api_v1_router.include_router(users_view.router, prefix="/users", tags=["users"])