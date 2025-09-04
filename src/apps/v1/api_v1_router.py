from fastapi import APIRouter
from src.apps.v1.users import view as users_view
from src.apps.v1.app_settings import view as app_settings_view

api_v1_router = APIRouter()
api_v1_router.include_router(users_view.router, prefix="/users", tags=["users"])
api_v1_router.include_router(app_settings_view.router, prefix="/app-settings", tags=["app-settings"])