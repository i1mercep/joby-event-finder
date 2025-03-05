from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import get_settings

settings = get_settings()
engine = create_async_engine(settings.database_url)
SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession]:
    """Get an asynchronous SQLAlchemy session from the engine."""
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


SessionDep = Annotated[AsyncSession, Depends(get_session)]
