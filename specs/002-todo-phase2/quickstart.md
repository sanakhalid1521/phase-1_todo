# Quickstart: Todo Application Phase II

**Feature**: Phase 2 - Full-stack web application
**Date**: 2025-12-31

## Prerequisites

- Node.js 20+ and npm
- Python 3.13+
- UV (Python package manager)
- PostgreSQL database (Neon Serverless)

## Setup Steps

### 1. Clone and Navigate

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Setup Backend

```bash
# Create and activate virtual environment with UV
uv venv .venv
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows

# Initialize backend project
cd backend
uv init --name backend
uv add fastapi uvicorn sqlmodel pydantic python-jose passlib bcrypt

# Create environment file
cp .env.example .env
# Edit .env with your database URL and secrets
```

**Backend .env**:
```bash
DATABASE_URL=postgresql://user:pass@host.neon.tech/db?sslmode=require
BETTER_AUTH_SECRET=your-32-character-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
CORS_ORIGINS=http://localhost:3000
```

### 3. Setup Frontend

```bash
# Navigate to frontend directory (from root)
cd frontend

# Initialize Next.js project
npx create-next-app@latest . \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*" \
  --use-npm \
  --no-git

# Install additional dependencies
npm install better-auth react-hook-form clsx tailwind-merge lucide-react

# Create environment file
cp .env.example .env.local
```

**Frontend .env.local**:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=same-as-backend-secret
BETTER_AUTH_URL=http://localhost:3000
```

### 4. Database Setup (Neon)

1. Create account at [neon.tech](https://neon.tech)
2. Create new project "todo-app"
3. Get connection string from dashboard
4. Add to backend/.env as DATABASE_URL

### 5. Initialize Database Tables

**File**: `backend/app/database.py`

```python
from sqlmodel import create_engine
from app.models.user import User
from app.models.task import Task

DATABASE_URL = "postgresql://..."
engine = create_engine(DATABASE_URL)

def create_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()
```

Run:
```bash
cd backend
python -m app.database
```

### 6. Start Development Servers

**Terminal 1 - Backend**:
```bash
cd backend
source ../.venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

### 7. Verify Setup

1. Open http://localhost:3000
2. Navigate to /signup
3. Create account with valid email (8+ chars password)
4. Verify redirect to /tasks
5. Add a task
6. Verify task appears in list

## Project Structure

```
./
├── frontend/                 # Next.js 16+ application
│   ├── app/
│   │   ├── (auth)/          # Auth pages (signin, signup)
│   │   │   ├── signin/
│   │   │   └── signup/
│   │   ├── tasks/           # Task management
│   │   │   └── page.tsx
│   │   ├── layout.tsx       # Root layout
│   │   └── page.tsx         # Home (redirect to tasks)
│   ├── components/          # Reusable components
│   │   ├── TaskList.tsx
│   │   ├── TaskForm.tsx
│   │   └── Navbar.tsx
│   ├── services/            # API client
│   │   └── api.ts
│   ├── schemas/             # TypeScript types
│   │   └── index.ts
│   ├── lib/                 # Utilities
│   │   └── auth.ts
│   └── .env.local
│
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── models/          # SQLModel entities
│   │   │   ├── user.py
│   │   │   └── task.py
│   │   ├── routers/         # API endpoints
│   │   │   ├── auth.py
│   │   │   └── tasks.py
│   │   ├── schemas/         # Pydantic models
│   │   │   ├── user.py
│   │   │   └── task.py
│   │   ├── core/            # Config, security
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── main.py          # FastAPI entry
│   │   └── database.py      # DB connection
│   ├── .env
│   └── pyproject.toml
│
├── .env.example             # Root env template
├── docker-compose.yml       # Optional Docker setup
└── README.md
```

## Environment Variables

### Root (.env.example)

```bash
# Shared secrets (must match across frontend/backend)
BETTER_AUTH_SECRET=your-secure-random-string
```

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=same-as-root-secret
BETTER_AUTH_URL=http://localhost:3000
```

### Backend (.env)

```bash
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=same-as-root-secret
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
CORS_ORIGINS=http://localhost:3000
```

## Common Issues

### Connection Refused (Backend)

```bash
# Check if backend is running
curl http://localhost:8000/health

# Verify port in use
lsof -i :8000
```

### CORS Errors

Ensure CORS_ORIGINS in backend/.env matches your frontend URL:
- Development: `http://localhost:3000`
- Production: `https://your-domain.com`

### Database Connection Failed

1. Verify DATABASE_URL is correct
2. Check Neon dashboard for connection issues
3. Ensure SSL is required for Neon: `?sslmode=require`

### Module Not Found

```bash
# Backend: Reinstall dependencies
cd backend
uv sync

# Frontend: Clear node_modules
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Testing Checklist

After setup, verify:

- [ ] Backend runs on http://localhost:8000
- [ ] Frontend runs on http://localhost:3000
- [ ] Signup page loads and accepts valid input
- [ ] Signin works with created account
- [ ] Tasks list shows after login
- [ ] Can create new task
- [ ] Can toggle task completion
- [ ] Can delete task
- [ ] Logout redirects to signin

## Deployment

### Frontend (Vercel)

1. Connect GitHub repository to Vercel
2. Add environment variables in Vercel dashboard
3. Deploy from `002-phase2-web` branch
4. Configure custom domain (optional)

### Backend (Vercel Serverless)

1. Create `api/` directory with `main.py` entry
2. Add Vercel configuration
3. Deploy from same branch
4. Set environment variables

### Database (Neon)

- Already serverless; no deployment needed
- Monitor connection limits in Neon dashboard
