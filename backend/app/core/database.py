from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Abstract Base class for SQLAlchemy ORM models
Base = declarative_base()

# Configure SQLAlchemy Engine
# Note: Connects to CockroachDB using postgresql+psycopg driver configuration
engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,  # Proactively inspects connection health before operations
    pool_size=20,
    max_overflow=10
)

# Async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields a database session lifecycle.
    Ensures rollback on request errors and database connection closing.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
