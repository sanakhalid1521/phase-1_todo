"""User database model using SQLModel."""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone
import uuid


class User(SQLModel, table=True):
    """User entity for authentication and task ownership."""

    __tablename__ = "users"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        description="Unique user identifier (UUID)"
    )
    email: str = Field(
        unique=True,
        index=True,
        description="User email address (validated format)"
    )
    password_hash: str = Field(
        description="Bcrypt hashed password (12 rounds)"
    )
    name: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Optional display name"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Account creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Last profile update timestamp"
    )
