"""Database configuration and session management"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import get_settings

# Do not create the engine at import time. Create lazily when a session is requested.
_engine = None
_async_session = None

settings = get_settings()

# Base class for all models (safe to create at import time)
Base = declarative_base()


def _get_database_url() -> str:
    """Return the database URL to use for engine creation.

    Keep default behavior (Postgres) but allow tests to override the dependency
    before an engine is created. This prevents attempts to connect to Postgres
    during test collection/import time.
    """
    db_url = settings.database_url
    # If a postgres URL is used, SQLAlchemy async driver expects the async driver
    if db_url.startswith("postgresql://"):
        return db_url.replace("postgresql://", "postgresql+asyncpg://")
    return db_url


def get_engine():
    """Create and cache an async engine on first use."""
    global _engine
    if _engine is None:
        _engine = create_async_engine(_get_database_url(), echo=settings.debug, future=True)
    return _engine


def get_sessionmaker():
    """Create and cache an async sessionmaker bound to the engine."""
    global _async_session
    if _async_session is None:
        _async_session = async_sessionmaker(get_engine(), class_=AsyncSession, expire_on_commit=False, future=True)
    return _async_session


async def get_db() -> AsyncSession:
    """Get database session dependency (created lazily)."""
    async_session = get_sessionmaker()
    async with async_session() as session:
        yield session
