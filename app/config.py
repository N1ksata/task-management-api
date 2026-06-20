"""Application configuration management"""

from pydantic_settings import BaseSettings
from functools import lru_cache
import os
import sys


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # Database
    database_url: str = "postgresql://user:password@localhost:5432/task_management_db"

    # JWT
    secret_key: str = "your-super-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # API
    app_name: str = "Task Management API"
    app_version: str = "1.0.0"
    debug: bool = True

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings"""
    s = Settings()

    # When running under pytest prefer an in-memory SQLite DB so tests don't
    # require a running PostgreSQL instance. Detect pytest by presence of the
    # 'pytest' module in sys.modules or the PYTEST_CURRENT_TEST env var.
    if "pytest" in sys.modules or os.environ.get("PYTEST_CURRENT_TEST"):
        s.database_url = "sqlite+aiosqlite:///:memory:"

    return s
