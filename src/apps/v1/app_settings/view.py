# src/apps/v1/app_settings/routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.common.database_dependencies import get_async_session
from src.apps.v1.app_settings.service import AppSettingsService

router = APIRouter(prefix="/app-settings", tags=["app-settings"])

@router.post("/create")
async def create_app_settings(db: AsyncSession = Depends(get_async_session)):
    await AppSettingsService.create_app_settings(db)
    return {"message": "Application settings created"}