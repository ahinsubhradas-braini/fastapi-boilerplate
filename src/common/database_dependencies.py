from typing import AsyncGenerator
from src.core.db.db_config import get_db
from sqlalchemy.ext.asyncio import AsyncSession

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with get_db() as session:
        yield session