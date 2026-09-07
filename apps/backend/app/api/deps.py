"""FastAPI dependency injection utilities."""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session

# Re-export for route dependency injection
get_db = get_db_session
