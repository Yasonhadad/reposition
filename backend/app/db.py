import os
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# אם תרצו, אפשר לקרוא את ה-URL מ-ENV:
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:yossi@postgres:5432/postgres"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def init_db() -> None:
    """יוצר את כל הטבלאות בהתחלת האפליקציה"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    """משתמש כ־dependency ב-FastAPI כדי לקבל סשן"""
    async with AsyncSessionLocal() as session:
        yield session
