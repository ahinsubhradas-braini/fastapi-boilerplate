from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.core.config import settings

# Database URL from settings
SQLALCHEMY_DATABASE_URL = settings.database_url

print(f"Database URL: {SQLALCHEMY_DATABASE_URL}")

# Create the async database engine
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=True
)

# Create a configured "AsyncSession" class
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# Create a Base class for our models to inherit from
DbBase = declarative_base()

class DbAdmin:
    @staticmethod
    async def create_db_tables():
        print("Creating database tables...")
        # Import models to register them with DbBase
        from src.apps.v1.users.models import user
        async with engine.begin() as conn:
            await conn.run_sync(DbBase.metadata.create_all)

    @staticmethod
    async def close():
        await engine.dispose()

# Get a database session (async generator)
async def get_db():
    async with SessionLocal() as session:
        yield session