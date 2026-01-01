"""Database connection and session management."""
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import asyncpg
from dotenv import load_dotenv
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Database connection string from .env
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Convert to async URL for asyncpg (remove sslmode from URL, add separately)
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("?sslmode=require", "")

# Create async engine for SQLModel
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    connect_args={"ssl": "require"}
)


async def init_db() -> None:
    """Initialize database tables."""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session dependency."""
    async with AsyncSession(async_engine) as session:
        try:
            yield session
        finally:
            await session.close()


async def test_connection() -> bool:
    """Test database connection using raw asyncpg."""
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        version = await conn.fetchval("SELECT version()")
        await conn.close()
        print("[OK] Database connected successfully!")
        print(f"    PostgreSQL Version: {version}")
        return True
    except Exception as e:
        print(f"[FAIL] Database connection failed: {e}")
        return False


@asynccontextmanager
async def get_db_connection() -> AsyncGenerator[asyncpg.Connection, None]:
    """Get raw asyncpg connection for direct queries."""
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()
