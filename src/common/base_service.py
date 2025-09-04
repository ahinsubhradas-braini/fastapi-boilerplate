# core/services/base_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.core.db.db_config import get_db

class BaseService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db