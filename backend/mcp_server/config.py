"""
MCP Server Configuration

Provides database connection management and configuration settings
for the MCP server.
"""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# Use FastAPI settings system instead of reading env vars directly
# This ensures DATABASE_URL is loaded from .env file consistently
from src.config import get_settings

settings = get_settings()

# Get DATABASE_URL from FastAPI settings (already validated and converted to asyncpg)
DATABASE_URL = settings.database_url

# Create async engine with connection pooling
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL query logging during development
    future=True,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before using them
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_database_session() -> AsyncIterator[AsyncSession]:
    """
    Dependency for getting database sessions.

    Usage:
        async for session in get_database_session():
            # Use session for database operations
            result = await session.execute(query)

    The session is automatically closed after use.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_database():
    """
    Initialize database schema (if needed).

    Note: In production, use Alembic migrations instead.
    This function is here for reference/testing purposes.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_database():
    """
    Close database connections.
    Call this during server shutdown.
    """
    await engine.dispose()
