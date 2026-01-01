# Implementation Plan: Todo Application Phase II

**Branch**: `002-todo-phase2` | **Date**: 2025-12-31 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-todo-phase2/spec.md`

## Summary

Transform the console-based Todo Application (Phase I) into a full-stack multi-user web application with persistent storage. The system will feature a Next.js 16+ frontend with Better Auth authentication, a FastAPI Python backend with SQLModel/PostgreSQL, and JWT-based stateless authentication for secure multi-user task management.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript 5.x (frontend)
**Primary Dependencies**: FastAPI, SQLModel, Pydantic, python-jose, passlib/bcrypt (backend); Next.js 16+, React 19+, TailwindCSS, Better Auth (frontend)
**Storage**: Neon Serverless PostgreSQL with SQLModel ORM
**Testing**: Manual testing checklist; pytest available for backend
**Target Platform**: Web browser (responsive desktop/mobile)
**Project Type**: Monorepo with separate frontend/backend applications
**Performance Goals**: Task list loads <1s (SC-002); Sign up/in <5s (SC-001)
**Constraints**: JWT token expiration 7 days; CORS restricted to frontend origin; Password bcrypt rounds=12
**Scale/Scope**: Individual users with personal task lists; no team sharing in Phase 2

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **I. Development Philosophy**: Spec complete with 8 user stories, acceptance scenarios, and edge cases
- [x] **I. Development Philosophy**: Aligns with Progressive Enhancement - web migration of Phase I console features
- [x] **II. Code Quality**: Monorepo structure allows SOLID separation; TypeScript + Python type hints planned
- [x] **II. Code Quality**: Type Safety via TypeScript (frontend) and Pydantic/SQLModel (backend); docstrings planned
- [x] **III. User Experience**: Clear feedback via toast notifications; validation errors inline; empty states defined
- [x] **IV. Security & Privacy**: JWT authentication, bcrypt password hashing, CORS restrictions, user_id data isolation
- [x] **Phase I Constraint**: (N/A - Phase II) Uses external dependencies as designed

## Project Structure

### Documentation (this feature)

```text
specs/002-todo-phase2/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
./
├── frontend/            # Next.js 16+ application
│   ├── app/
│   │   ├── (auth)/      # Auth route group (signin, signup pages)
│   │   │   ├── signin/
│   │   │   └── signup/
│   │   ├── tasks/       # Tasks page (list, add, edit, delete)
│   │   ├── api/         # API routes for backend communication
│   │   └── layout.tsx   # Root layout with providers
│   ├── components/      # Reusable UI components
│   ├── services/        # API client services
│   ├── schemas/         # TypeScript interfaces
│   └── lib/             # Utilities and config
│
├── backend/             # FastAPI application
│   ├── app/
│   │   ├── models/      # SQLModel entities (User, Task)
│   │   ├── routers/     # API route handlers (auth, tasks)
│   │   ├── core/        # Config, security, dependencies
│   │   ├── schemas/     # Pydantic request/response models
│   │   └── main.py      # FastAPI application entry
│   └── tests/           # Backend tests
│
├── .env.example         # Environment template
├── docker-compose.yml   # Local development (optional)
└── README.md            # Setup instructions
```

**Structure Decision**: Monorepo with `/frontend` (Next.js) and `/backend` (FastAPI) as sibling directories at repository root, enabling independent deployment while sharing environment configuration.

## Technology Stack Details

### Frontend Specifications

| Category | Technology | Rationale |
|----------|------------|-----------|
| Framework | Next.js 16+ with App Router | Server-side rendering, file-based routing, React 19+ compatibility |
| Language | TypeScript | Type safety for API contracts and components |
| Styling | TailwindCSS | Utility-first, responsive design support |
| Authentication | Better Auth | JWT plugin, email/password provider, session management |
| State Management | React hooks + Context | Simple state for auth and task data |
| Form Handling | react-hook-form (optional) | Client-side validation |

### Backend Specifications

| Category | Technology | Rationale |
|----------|------------|-----------|
| Framework | FastAPI | Python 3.13+, async support, auto OpenAPI docs |
| ORM | SQLModel | Pydantic + SQLAlchemy unified; type-safe DB operations |
| Validation | Pydantic | Request/response validation with detailed errors |
| JWT | python-jose | JWT encoding/decoding, HS256 algorithm |
| Password Hashing | passlib + bcrypt | Industry-standard, 12 rounds |
| Package Management | UV | Fast Python package manager |

### Database Specifications

| Category | Technology | Rationale |
|----------|------------|-----------|
| Database | Neon Serverless PostgreSQL | Serverless, auto-scaling, connection pooling |
| Migrations | SQLModel.metadata (optional Alembic) | Auto-create tables from models |
| Connection | asyncpg + SQLModel | Async database driver |

## Architecture Decisions

### AD-001: Monorepo Structure

**Decision**: Separate `/frontend` and `/backend` directories at root level

**Alternatives Considered**:
- Single repo per service (rejected: fragments codebase)
- Backend-as-API-within-Next.js (rejected: Python backend requires separate process)

**Rationale**: Clear separation of concerns; independent deployment options; different technology stacks per component.

### AD-002: JWT-Based Authentication

**Decision**: Stateless JWT tokens with Better Auth on frontend, python-jose verification on backend

**Alternatives Considered**:
- Session-based with cookies (rejected: requires distributed session store)
- OAuth only (rejected: email/password required per spec)

**Rationale**: Stateless scales horizontally; JWT works across deployment units; Better Auth provides mature JWT implementation.

### AD-003: User-ID Scoped Tasks

**Decision**: All task endpoints require `{user_id}` path parameter matching JWT user_id

**Alternatives Considered**:
- Task endpoint auto-uses JWT user_id (rejected: explicit user_id allows URL verification)
- User extracts own tasks server-side only (rejected: no client-side filtering audit)

**Rationale**: Defense in depth - backend verifies user_id matches token; prevents any cross-user access.

## API Contract Summary

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | Create new user account |
| POST | `/api/auth/signin` | Authenticate and return JWT |
| GET | `/api/auth/me` | Get current user info (protected) |

### Task Endpoints (all protected, scoped by user_id)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all user's tasks |
| POST | `/api/{user_id}/tasks` | Create new task |
| GET | `/api/{user_id}/tasks/{task_id}` | Get single task |
| PUT | `/api/{user_id}/tasks/{task_id}` | Update task |
| PATCH | `/api/{user_id}/tasks/{task_id}/toggle` | Toggle completion |
| DELETE | `/api/{user_id}/tasks/{task_id}` | Delete task |

## Security Implementation

### Password Hashing
- Algorithm: bcrypt
- Rounds: 12
- Library: passlib with bcrypt

### JWT Tokens
- Algorithm: HS256
- Payload: user_id, email, exp (7 days)
- Library: python-jose

### CORS Configuration
- Origin: Restricted to frontend URL only
- Credentials: Enabled (cookies for auth token)
- Methods: GET, POST, PUT, PATCH, DELETE

### Input Validation
- Backend: Pydantic schemas with email format, password length (8+), title length (3-100)
- Database: SQLModel field constraints
- Frontend: Form validation with Better Auth

## Deployment Architecture

### Frontend Deployment (Vercel)
- Platform: Vercel
- Branch: `002-phase2-web`
- Environment: NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL

### Backend Deployment (Vercel/Railway/Render)
- Platform: Vercel (Serverless Functions) or Railway/Render
- Branch: Same as frontend
- Environment: DATABASE_URL, BETTER_AUTH_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_DAYS, CORS_ORIGINS

### Database (Neon)
- Already serverless; no deployment needed
- Connection pooling configured for serverless functions

## Complexity Tracking

> No Constitution Check violations requiring justification.

## Implementation Phases

### Phase 1: Setup (Day 1)
- Create monorepo directories
- Initialize Next.js frontend with TypeScript and TailwindCSS
- Initialize FastAPI backend with UV
- Setup Neon PostgreSQL connection
- Create SQLModel User and Task models

### Phase 2: Authentication (Day 2-3)
- Implement Better Auth on frontend
- Create backend auth endpoints (signup, signin, me)
- Implement JWT verification on backend
- Create signup and signin pages
- Test authentication flow

### Phase 3: Task CRUD (Day 4-5)
- Create backend task endpoints (all CRUD)
- Create frontend task components
- Implement task list, create, view
- Test with multiple users for isolation

### Phase 4: Task Actions (Day 6)
- Implement update task
- Implement delete task with confirmation
- Implement toggle completion
- Add validations and error handling

### Phase 5: Polish & Deploy (Day 7)
- Responsive design refinement
- Error handling improvements
- Deploy to Vercel + backend platform
- Final testing against acceptance criteria

## Generated Artifacts

- [x] `plan.md` - This file
- [ ] `research.md` - Best practices and integration patterns
- [ ] `data-model.md` - Entity definitions and relationships
- [ ] `quickstart.md` - Development setup guide
- [ ] `contracts/` - OpenAPI specification directory
