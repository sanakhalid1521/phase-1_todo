# Research: Todo Application Phase II

**Feature**: Phase 2 - Full-stack web application
**Date**: 2025-12-31
**Tech Stack**: Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth

## Technology Decisions

### Better Auth Integration with FastAPI Backend

**Decision**: Use Better Auth on frontend with custom JWT backend verification

**Rationale**:
- Better Auth provides mature JWT plugin with email/password provider
- Frontend handles all auth UI flows
- Backend verifies JWT tokens using shared secret
- Stateless design enables horizontal scaling

**Implementation Pattern**:
```python
# Backend JWT verification
from jose import jwt, JWTError

async def get_current_user(authorization: str = None):
    token = authorization.replace("Bearer ", "")
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id: str = payload.get("sub")
    return user_id
```

**Reference**: Better Auth JWT plugin documentation

### SQLModel for Python ORM

**Decision**: Use SQLModel as ORM layer

**Rationale**:
- Unified Pydantic + SQLAlchemy (SQLModel)
- Type hints work with Pydantic validation
- Auto-generates tables from models
- Async support via SQLModel with asyncpg

**Model Pattern**:
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    tasks: list["Task"] = Relationship(back_populates="user")
```

**Reference**: SQLModel documentation - https://sqlmodel.tiangolo.com/

### Neon Serverless PostgreSQL

**Decision**: Use Neon for PostgreSQL hosting

**Rationale**:
- Serverless connection pooling
- Auto-scales with usage
- Direct PostgreSQL protocol support
- Compatible with SQLModel/SQLAlchemy

**Connection Pattern**:
```python
from sqlmodel import create_engine
DATABASE_URL = "postgresql://user:pass@host.neon.tech/db?sslmode=require"
engine = create_engine(DATABASE_URL, echo=True)
```

**Note**: For serverless functions, use Neon branch endpoints or connection pooling to avoid connection limits.

### FastAPI with UV

**Decision**: Use FastAPI framework with UV package management

**Rationale**:
- Native async support for PostgreSQL
- Auto OpenAPI documentation
- UV is 10-100x faster than pip
- Python 3.13+ support

**Setup**:
```bash
uv init backend
cd backend
uv add fastapi uvicorn sqlmodel pydantic python-jose passlib bcrypt
```

## Security Patterns

### JWT Implementation

**Token Structure**:
```python
# Payload
{
    "sub": user_id,  # UUID string
    "email": user_email,
    "exp": datetime.utcnow() + timedelta(days=7)
}
```

**Verification Flow**:
1. Frontend stores JWT (Better Auth manages this)
2. API requests include `Authorization: Bearer <token>`
3. Backend extracts and verifies token signature
4. Backend extracts user_id for data scoping

**Best Practices**:
- Use HS256 algorithm
- Include expiration (exp claim)
- Store only non-sensitive data in token
- Verify user_id in token matches requested resource

### Password Hashing

**Implementation**:
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

**Bcrypt Rounds**: 12 (balance of security and performance)

### CORS Configuration

**Backend Setup**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Frontend Architecture

### Next.js 16 App Router

**Directory Structure**:
```
frontend/
├── app/
│   ├── (auth)/
│   │   ├── signin/
│   │   │   └── page.tsx
│   │   └── signup/
│   │       └── page.tsx
│   ├── tasks/
│   │   └── page.tsx
│   └── layout.tsx
├── components/
│   ├── TaskList.tsx
│   ├── TaskForm.tsx
│   └── Navbar.tsx
└── lib/
    └── auth.ts
```

**Key Patterns**:
- Server Components for initial data fetch
- Client Components for interactive elements
- Server Actions for form submissions (optional)
- API routes for backend communication

### Better Auth Setup

**Configuration**:
```typescript
import { betterAuth } from "better-auth"

export const auth = betterAuth({
  database: "postgresql://...",
  emailAndPassword: {
    enabled: true
  },
  plugins: [jwt()],
  advanced: {
    cookiePrefix: "todo-app"
  }
})
```

## API Design Patterns

### RESTful Endpoints

**Pattern**: User-scoped resources
```
GET    /api/{user_id}/tasks          # List tasks
POST   /api/{user_id}/tasks          # Create task
GET    /api/{user_id}/tasks/{id}     # Get task
PUT    /api/{user_id}/tasks/{id}     # Update task
PATCH  /api/{user_id}/tasks/{id}/toggle  # Toggle complete
DELETE /api/{user_id}/tasks/{id}     # Delete task
```

**Authorization Check**:
```python
async def get_user_tasks(user_id: str, current_user_id: str):
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return await db.get_tasks(user_id)
```

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Status Codes**:
- 400: Validation error
- 401: Unauthorized (no/invalid token)
- 403: Forbidden (not your resource)
- 404: Not found
- 500: Server error

## Environment Configuration

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-32-character-secret-key
BETTER_AUTH_URL=http://localhost:3000
```

### Backend (.env)
```
DATABASE_URL=postgresql://user:pass@host.neon.tech/db?sslmode=require
BETTER_AUTH_SECRET=same-as-frontend-secret
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
CORS_ORIGINS=http://localhost:3000
```

## Testing Strategy

### Manual Testing Checklist

**Authentication**:
- [ ] Sign up with valid email/password
- [ ] Sign up rejects duplicate email
- [ ] Sign up rejects invalid email format
- [ ] Sign in with correct credentials
- [ ] Sign in rejects wrong password
- [ ] Logout clears session
- [ ] Protected endpoints reject invalid token

**Task Operations**:
- [ ] Create task with valid input
- [ ] Create task rejects short title
- [ ] List shows only user's tasks
- [ ] Update task modifies data
- [ ] Delete removes task
- [ ] Toggle changes completion status
- [ ] Empty state shows "No tasks yet"

**Security**:
- [ ] User cannot access another user's tasks
- [ ] JWT expiration works
- [ ] CORS blocks unauthorized origins

## Deployment Considerations

### Vercel (Frontend)
- Automatic deployments from main branch
- Environment variables in Vercel dashboard
- Serverless function timeout: 10s (adjust if needed)

### Serverless Backend on Vercel
- Use `@fastapi/fastapi` adapter
- Connection pooling critical for serverless
- Consider using Neon branch endpoints

### Alternative Backend Platforms
- Railway: Simple deployment, includes PostgreSQL option
- Render: Direct deployment, good free tier
- Fly.io: Edge deployment, more control

## References

1. FastAPI Documentation - https://fastapi.tiangolo.com/
2. SQLModel Documentation - https://sqlmodel.tiangolo.com/
3. Better Auth Documentation - https://www.better-auth.com/
4. Next.js Documentation - https://nextjs.org/docs
5. Neon Serverless PostgreSQL - https://neon.tech/docs
6. python-jose JWT - https://python-jose.readthedocs.io/
7. passlib bcrypt - https://passlib.readthedocs.io/
