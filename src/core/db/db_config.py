# Import python core libary dependices
from typing import AsyncGenerator

# Imports from project or 3rd party libary dependices
from fastapi.concurrency import asynccontextmanager
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

# Database URL from settings
SQLALCHEMY_DATABASE_URL = settings.database_url

# Create the async database engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)

# Create a configured "AsyncSession" class
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Create a Base class for our models to inherit from
DbBase = declarative_base()

class DbAdmin:
    @staticmethod
    async def create_db_tables():
        print("Creating database tables from lifespan.")
        # Import models to register them with DbBase
        from src.apps.v1.users.models import user
        async with engine.begin() as conn:
            await conn.run_sync(DbBase.metadata.create_all)

    @staticmethod
    async def close():
        await engine.dispose()

# Get a database session (async generator)
# Async context manager for dependency injection
@asynccontextmanager
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()