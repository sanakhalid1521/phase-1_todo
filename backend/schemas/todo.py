"""Todo Pydantic schemas for API request/response."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    """Schema for creating a new todo."""

    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=5, max_length=500)


class TodoUpdate(BaseModel):
    """Schema for updating an existing todo."""

    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, min_length=5, max_length=500)
    completed: Optional[bool] = Field(None)


class TodoResponse(BaseModel):
    """Schema for todo response."""

    id: str
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TodoListResponse(BaseModel):
    """Schema for list of todos response."""

    todos: list[TodoResponse]
    total: int
    completed: int
    pending: int
