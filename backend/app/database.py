"""Database connection and table creation."""

from sqlmodel import create_engine, SQLModel
from app.core.config import settings

# Create SQLModel engine - use SQLite for local dev
# For PostgreSQL, use: postgresql://user:pass@host/db
engine = create_engine(settings.DATABASE_URL, echo=True)


def create_tables():
    """Create all database tables from SQLModel metadata."""
    SQLModel.metadata.create_all(engine)


def get_engine():
    """Get the database engine."""
    return engine
