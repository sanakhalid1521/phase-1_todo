---
id: "0001"
title: "Phase 2 Planning"
stage: "plan"
date: "2025-12-31"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "todo-phase2"
branch: "001-todo-phase1"
user: "Human"
command: "/sp.plan (with architecture specs)"
labels: [backend,frontend,architecture,authentication]
links:
  spec: "specs/002-todo-phase2/spec.md"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - "specs/002-todo-phase2/plan.md"
  - "specs/002-todo-phase2/research.md"
  - "specs/002-todo-phase2/data-model.md"
  - "specs/002-todo-phase2/quickstart.md"
  - "specs/002-todo-phase2/contracts/openapi.yaml"
  - "specs/002-todo-phase2/contracts/api-types.ts"
tests: []
---

## Prompt

Create a comprehensive technical implementation plan for Phase II using the following architecture:

TECHNOLOGY STACK:

Frontend:
- Next.js 16+ with App Router
- React 19+
- TypeScript
- TailwindCSS for styling
- Better Auth for authentication

Backend:
- Python 3.13+
- FastAPI framework
- SQLModel ORM
- Pydantic for validation
- python-jose for JWT
- passlib with bcrypt for password hashing
- UV for package management

Database:
- Neon Serverless PostgreSQL
- Alembic for migrations (optional)

Development Tools:
- Claude Code with Spec-Kit Plus
- Git for version control

ARCHITECTURE DESIGN:

1. MONOREPO STRUCTURE:

Root level:
- /frontend - Next.js application
- /backend - FastAPI application
- /CLAUDE.md - Root instructions
- /.env.example - Environment variables template
- /docker-compose.yml - Local development setup (optional)
- /README.md - Setup instructions

Frontend structure:
frontend/
├── app/
│   ├── (auth)/
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── task_service.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py
│   ├── database.py
│   └── main.py
├── CLAUDE.md
├── pyproject.toml
└── .env.example

2. DATABASE MODELS (SQLModel):

User Model (backend/app/models/user.py):
```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

Task Model (backend/app/models/task.py):
```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

3. AUTHENTICATION IMPLEMENTATION:

Better Auth Setup (Frontend):
- Install: npm install better-auth
- Configure JWT plugin
- Setup email/password provider
- Configure session expiration
- Export auth client

JWT Verification (Backend):
- Extract token from Authorization header
- Verify token signature using BETTER_AUTH_SECRET
- Decode payload to get user_id and email
- Create dependency for protected routes
- Return 401 Unauthorized if invalid

4. API IMPLEMENTATION:

Authentication Router (backend/app/routers/auth.py):
Endpoints:
- POST /api/auth/signup
- POST /api/auth/signin
- GET /api/auth/me (protected)

Tasks Router (backend/app/routers/tasks.py):
All endpoints require JWT authentication.

- GET /api/{user_id}/tasks
- POST /api/{user_id}/tasks
- GET /api/{user_id}/tasks/{task_id}
- PUT /api/{user_id}/tasks/{task_id}
- PATCH /api/{user_id}/tasks/{task_id}/toggle
- DELETE /api/{user_id}/tasks/{task_id}

5. FRONTEND PAGES:

- /signup: Email/password form, validation, redirect to tasks on success
- /signin: Email/password form, validation, redirect to tasks on success
- /tasks: Task list, add task form, edit/delete actions, logout button
- Empty state: "No tasks yet. Create your first task!"
- Confirmation dialog for delete
- Navbar: Logo, user email, logout button

6. ENVIRONMENT VARIABLES:

Frontend (.env.local):
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-here
BETTER_AUTH_URL=http://localhost:3000

Backend (.env):
DATABASE_URL=postgresql://user:pass@host/db
BETTER_AUTH_SECRET=same-as-frontend-secret
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
CORS_ORIGINS=http://localhost:3000

7. SECURITY IMPLEMENTATION:

Password Hashing:
- Use passlib with bcrypt
- Rounds: 12 (good balance of security and performance)

JWT Tokens:
- Use python-jose for encoding/decoding
- Algorithm: HS256
- Include: user_id, email, exp (expiration)
- Expiration: 7 days

CORS:
- Allow only frontend origin
- Allow credentials (cookies)
- Methods: GET, POST, PUT, PATCH, DELETE

Input Validation:
- Pydantic schemas for request validation
- SQLModel constraints for database
- Frontend validation with react-hook-form (optional)

8. ERROR HANDLING:

Backend:
- HTTPException for API errors
- Custom error messages
- Proper status codes (400, 401, 404, 500)
- Error logging

Frontend:
- Try-catch for API calls
- Toast notifications for errors
- Inline form validation errors
- Fallback UI for errors

9. DEVELOPMENT WORKFLOW:

Setup:
1. Clone repository
2. Install dependencies (frontend: npm install, backend: uv sync)
3. Create .env files with required variables
4. Setup Neon database
5. Run migrations (if using Alembic)
6. Start backend: uvicorn app.main:app --reload
7. Start frontend: npm run dev

Database Setup:
1. Create Neon project
2. Get connection string
3. Add to backend .env
4. Create tables (SQLModel.metadata.create_all)

10. TESTING STRATEGY:

Manual Testing Checklist:
- [ ] User can sign up with valid email/password
- [ ] User cannot sign up with existing email
- [ ] User can sign in with correct credentials
- [ ] User cannot sign in with wrong password
- [ ] User is redirected to signin if not authenticated
- [ ] Logged-in user can create task
- [ ] Tasks are saved to database
- [ ] User sees only their own tasks
- [ ] User can update task title
- [ ] User can update task description
- [ ] User can delete task with confirmation
- [ ] User can toggle task completion
- [ ] User can log out
- [ ] JWT token expires after 7 days
- [ ] Responsive design works on mobile

11. DEPLOYMENT PLAN:

Frontend (Vercel):
- Connect GitHub repository
- Set environment variables
- Deploy from 002-phase2-web branch
- Custom domain (optional)

Backend (Vercel/Railway/Render):
- Connect GitHub repository
- Set environment variables
- Deploy from same branch
- Get API URL for frontend

Database (Neon):
- Already serverless, no deployment needed
- Connection string from Neon dashboard

12. IMPLEMENTATION SEQUENCE:

Phase 1: Setup (Day 1)
- Create monorepo structure
- Initialize frontend (Next.js)
- Initialize backend (FastAPI)
- Setup database connection
- Create SQLModel models

Phase 2: Authentication (Day 2-3)
- Implement Better Auth (frontend)
- Implement JWT verification (backend)
- Create auth endpoints (signup, signin)
- Create auth pages (frontend)
- Test authentication flow

Phase 3: Task CRUD (Day 4-5)
- Create task endpoints (backend)
- Create task components (frontend)
- Implement create task
- Implement list tasks
- Test with multiple users

Phase 4: Task Actions (Day 6)
- Implement update task
- Implement delete task
- Implement toggle complete
- Add confirmations and validations

Phase 5: Polish & Deploy (Day 7)
- Responsive design refinement
- Error handling improvements
- Deploy to Vercel
- Final testing

This plan provides a complete roadmap for implementing Phase II while maintaining clean architecture and security best practices.

## Response snapshot

Created comprehensive plan artifacts for Phase 2 full-stack web application:

1. **plan.md** - Technical architecture with monorepo structure, technology stack details (Next.js 16+, FastAPI, SQLModel, Better Auth), constitution check, API contract summary, and phased implementation timeline (7 days).

2. **research.md** - Best practices for Better Auth integration, SQLModel ORM patterns, Neon PostgreSQL setup, JWT implementation, password hashing with bcrypt (12 rounds), and CORS configuration.

3. **data-model.md** - Entity definitions for User (UUID id, email, password_hash, created_at, updated_at) and Task (integer id, user_id FK, title, description, completed, timestamps) with Pydantic schemas and validation rules.

4. **quickstart.md** - Development setup guide with commands for both frontend (npm) and backend (uv), environment configuration, database setup, and common troubleshooting.

5. **contracts/openapi.yaml** - OpenAPI 3.1.0 specification with auth endpoints (/api/auth/signup, /api/auth/signin, /api/auth/me) and task endpoints (CRUD scoped by user_id).

6. **contracts/api-types.ts** - TypeScript API client types and ApiClient class with type-safe methods for all endpoints.

## Outcome

- ✅ Impact: Full implementation blueprint created for Phase 2 web application
- 📁 Files: 6 artifacts created in specs/002-todo-phase2/
- 🔁 Next prompts: /sp.tasks to generate implementation tasks
- 🧠 Reflection: User provided comprehensive architecture specs; planning focused on extracting and organizing into Spec-Kit Plus templates with research consolidation.
