"""Database configuration and session management"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import get_settings

settings = get_settings()

# Create async engine
engine = create_async_engine(
    settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.debug,
    future=True,
)

# Create async session factory
async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, future=True
)

# Base class for all models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """Get database session dependency"""
    async with async_session() as session:
        yield session
