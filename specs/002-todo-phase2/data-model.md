# Data Model: Todo Application Phase II

**Feature**: Phase 2 - Full-stack web application
**Date**: 2025-12-31
**Database**: PostgreSQL (Neon Serverless)
**ORM**: SQLModel

## Entity Relationship Diagram

```mermaid
erDiagram
    User ||--o{ Task : owns
    User {
        string id PK "UUID"
        string email UK "validated email"
        string password_hash "bcrypt hash"
        timestamp created_at
        timestamp updated_at
    }
    Task {
        int id PK "auto-increment"
        string user_id FK "UUID -> User.id"
        string title "3-100 chars"
        text description "optional, max 500"
        boolean completed "default false"
        timestamp created_at
        timestamp updated_at
    }
```

## User Entity

### SQLModel Definition

**File**: `backend/app/models/user.py`

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class User(SQLModel, table=True):
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
        default_factory=datetime.utcnow,
        description="Account creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last profile update timestamp"
    )
```

### Field Specifications

| Field | Type | Constraints | Validation | Description |
|-------|------|-------------|------------|-------------|
| id | string | UUID format | Auto-generated | Primary key, immutable |
| email | string | max 255, unique | RFC 5322 email format | Login identifier |
| password_hash | string | bcrypt output | Auto-hashed | Never store plaintext |
| name | string | optional, max 100 | Strip whitespace | Display name |
| created_at | timestamp | UTC | Auto-set | Immutable creation time |
| updated_at | timestamp | UTC | Auto-update | Modified on changes |

### Database Indexes

```sql
-- Primary key (auto-created on id)
CREATE INDEX idx_users_email ON users (email);
```

## Task Entity

### SQLModel Definition

**File**: `backend/app/models/task.py`

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Auto-increment task ID"
    )
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        description="Owning user UUID"
    )
    title: str = Field(
        max_length=100,
        description="Task title (3-100 characters)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Optional task details"
    )
    completed: bool = Field(
        default=False,
        description="Task completion status"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Task creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last modification timestamp"
    )
```

### Field Specifications

| Field | Type | Constraints | Validation | Description |
|-------|------|-------------|------------|-------------|
| id | int | auto-increment | Auto-generated | Primary key |
| user_id | string | FK to users.id | Must exist | Owner reference |
| title | string | 3-100 chars | Trim whitespace | Task summary |
| description | text | optional, max 500 | Strip whitespace | Details |
| completed | boolean | default false | Toggleable | Status flag |
| created_at | timestamp | UTC | Auto-set | Immutable |
| updated_at | timestamp | UTC | Auto-update | Modified on changes |

### Database Indexes

```sql
-- Foreign key index (auto-created by SQLModel)
CREATE INDEX idx_tasks_user_id ON tasks (user_id);
-- Composite for user task queries
CREATE INDEX idx_tasks_user_completed ON tasks (user_id, completed);
```

## Relationships

### User → Tasks (One-to-Many)

```python
from typing import LIST
from sqlmodel import Relationship

class User(SQLModel, table=True):
    # ... fields from above ...
    tasks: list["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    # ... fields from above ...
    user: User = Relationship(back_populates="tasks")
```

**Cascade Behavior**:
- `delete` cascade: Deleting a user should delete all their tasks
- SQLModel does not auto-cascade; handle in service layer

```python
# In UserService.delete()
async def delete_user(user_id: str):
    # Delete all user tasks first
    await Task.filter(user_id=user_id).delete()
    # Then delete user
    await User.filter(id=user_id).delete()
```

## Pydantic Schemas (Request/Response)

**File**: `backend/app/schemas/task.py`

### TaskCreate

```python
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str | None = Field(None, max_length=500)
```

### TaskUpdate

```python
from pydantic import BaseModel

class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=100)
    description: str | None = Field(None, max_length=500)
    completed: bool | None = None
```

### TaskResponse

```python
from datetime import datetime

class TaskResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### UserCreate

```python
from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
```

### UserResponse

```python
from datetime import datetime

class UserResponse(BaseModel):
    id: str
    email: str
    name: str | None
    created_at: datetime

    class Config:
        from_attributes = True
```

### AuthResponse

```python
class AuthResponse(BaseModel):
    token: str
    user: UserResponse
```

## Database Initialization

### Create Tables (SQLModel)

**File**: `backend/app/database.py`

```python
from sqlmodel import create_engine
from app.models.user import User
from app.models.task import Task

DATABASE_URL = "postgresql://user:pass@host.neon.tech/db?sslmode=require"
engine = create_engine(DATABASE_URL)

def create_tables():
    SQLModel.metadata.create_all(engine)
```

### Alembic Migration (Optional)

**File**: `backend/alembic/versions/001_initial.py`

```python
"""Initial migration

Revision ID: 001
Revises:
Create Date: 2025-12-31
"""

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('name', sa.String(100)),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )

    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(100), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('completed', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False),
    )

    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'])

def downgrade():
    op.drop_index('idx_tasks_user_id', table_name='tasks')
    op.drop_index('idx_users_email', table_name='users')
    op.drop_table('tasks')
    op.drop_table('users')
```

## Validation Rules Summary

### Input Validation (Frontend)

| Field | Min | Max | Pattern |
|-------|-----|-----|---------|
| email | - | 255 | RFC 5322 email |
| password | 8 | 128 | Any characters |
| title | 3 | 100 | Trim whitespace |
| description | 0 | 500 | Trim whitespace |

### Database Constraints

| Constraint | Target | Behavior |
|------------|--------|----------|
| UNIQUE | users.email | Reject duplicate signup |
| NOT NULL | users.id, email, password_hash | Always required |
| NOT NULL | tasks.user_id, title, completed | Always required |
| FK | tasks.user_id -> users.id | Referential integrity |
