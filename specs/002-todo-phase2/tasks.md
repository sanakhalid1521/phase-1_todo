---
description: "Task list for Todo Application Phase II"
---

# Tasks: Todo Application Phase II

**Input**: Design documents from `specs/002-todo-phase2/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/, research.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and monorepo structure

- [X] T001 Create monorepo directories per plan.md: `frontend/`, `backend/`
- [X] T002 [P] Initialize Next.js frontend with TypeScript, TailwindCSS in `frontend/`
- [X] T003 [P] Initialize FastAPI backend with UV in `backend/`
- [X] T004 Create `.env.example` at repository root with all required variables
- [X] T005 [P] Create root `docker-compose.yml` for local development (optional)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story

**CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [X] T006 Install backend dependencies: fastapi, uvicorn, sqlmodel, pydantic, python-jose, passlib, bcrypt, asyncpg
- [X] T007 Create `backend/app/__init__.py`
- [X] T008 Create `backend/app/models/__init__.py`
- [X] T009 Create `backend/app/schemas/__init__.py`
- [X] T010 Create `backend/app/routers/__init__.py`
- [X] T011 Create `backend/app/core/__init__.py`
- [X] T012 [P] Implement `backend/app/core/config.py` with environment variable loading
- [X] T013 [P] Implement `backend/app/core/security.py` with JWT decode and password hashing utilities
- [X] T014 [P] Create `backend/app/database.py` with SQLModel engine and table creation

### Frontend Foundation

- [X] T015 Install frontend dependencies: better-auth, react-hook-form, clsx, tailwind-merge, lucide-react
- [X] T016 Create `frontend/app/(auth)/` route group directory
- [X] T017 Create `frontend/app/tasks/` directory
- [X] T018 Create `frontend/components/` directory
- [X] T019 Create `frontend/services/` directory
- [X] T020 Create `frontend/schemas/` directory
- [X] T021 Create `frontend/lib/` directory
- [X] T022 [P] Implement `frontend/lib/auth.ts` with Better Auth configuration
- [X] T023 [P] Create `frontend/services/api.ts` with ApiClient class per contracts/api-types.ts

### Database Models (Foundational - required by all stories)

- [X] T024 Create `backend/app/models/user.py` with User SQLModel entity
- [X] T025 Create `backend/app/models/task.py` with Task SQLModel entity
- [X] T026 [P] Create `backend/app/schemas/user.py` with UserCreate, UserResponse, AuthResponse Pydantic models
- [X] T027 [P] Create `backend/app/schemas/task.py` with TaskCreate, TaskUpdate, TaskResponse Pydantic models

### Backend App Entry

- [X] T028 Create `backend/app/main.py` with FastAPI app, CORS middleware, and include routers

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Sign Up (Priority: P1) 🎯 MVP

**Goal**: Allow new users to register with email and password

**Independent Test**: Navigate to /signup, enter valid email/password, verify redirect to /tasks with account created

### Backend Auth Endpoints

- [X] T029 [US1] Create `backend/app/routers/auth.py`
- [X] T030 [US1] Implement `POST /api/auth/signup` endpoint in `backend/app/routers/auth.py`
- [X] T031 [US1] Implement password hashing with bcrypt (12 rounds) in signup handler
- [X] T032 [US1] Implement User creation in database with unique email validation
- [X] T033 [US1] Implement JWT token generation on successful signup
- [X] T034 [US1] Return 409 Conflict if email already registered

### Frontend Signup Page

- [X] T035 [US1] Create `frontend/app/(auth)/signup/page.tsx`
- [X] T036 [US1] Implement signup form with email/password fields and validation
- [X] T037 [US1] Connect form to auth service API call
- [X] T038 [US1] Handle success: store JWT, redirect to /tasks
- [X] T039 [US1] Handle error: display "Email already registered" or validation errors

**Checkpoint**: User can sign up and is redirected to tasks page

---

## Phase 4: User Story 2 - Sign In (Priority: P1)

**Goal**: Allow returning users to authenticate with email and password

**Independent Test**: Navigate to /signin, enter valid credentials, verify redirect to /tasks with JWT token

### Backend Auth Endpoints (continued)

- [X] T040 [US2] Implement `POST /api/auth/signin` endpoint in `backend/app/routers/auth.py`
- [X] T041 [US2] Implement email lookup and password verification
- [X] T042 [US2] Return JWT token on successful authentication
- [X] T043 [US2] Return 401 Unauthorized for invalid credentials

### Frontend Signin Page

- [X] T044 [US2] Create `frontend/app/(auth)/signin/page.tsx`
- [X] T045 [US2] Implement signin form with email/password fields and validation
- [X] T046 [US2] Connect form to auth service API call
- [X] T047 [US2] Handle success: store JWT, redirect to /tasks
- [X] T048 [US2] Handle error: display "Invalid email or password"

### Shared Auth Utilities

- [X] T049 [P] [US1, US2] Implement JWT verification dependency in `backend/app/core/security.py`
- [X] T050 [P] [US1, US2] Create `GET /api/auth/me` endpoint for current user retrieval

**Checkpoint**: User can sign in and is redirected to tasks page

---

## Phase 5: User Story 3 - Sign Out (Priority: P1)

**Goal**: Allow logged-in users to securely log out

**Independent Test**: Click logout button, verify redirect to /signin and session cleared

### Frontend Signout

- [X] T051 [US3] Implement logout action in `frontend/lib/auth.ts`
- [X] T052 [US3] Clear JWT from storage on logout
- [X] T053 [US3] Redirect to /signin after logout

### Navbar Component (for logout button)

- [X] T054 [US3] Create `frontend/components/Navbar.tsx` with logo and logout button
- [X] T055 [US3] Display user email in navbar when logged in

**Checkpoint**: Logout clears session and redirects to signin

---

## Phase 6: User Story 5 - View Tasks + User Story 4 - Add Task (Priority: P1)

**Goal**: Display all user tasks and allow creating new tasks

**Independent Test**: On /tasks page, see empty state "No tasks yet" initially, add task, verify it appears in list

### Backend Task Endpoints (list and create)

- [X] T056 [US5, US4] Create `backend/app/routers/tasks.py`
- [X] T057 [US5] Implement `GET /api/{user_id}/tasks` endpoint
- [X] T058 [US5] Add JWT verification and user_id authorization check
- [X] T059 [US5] Query tasks filtered by user_id
- [X] T060 [US4] Implement `POST /api/{user_id}/tasks` endpoint
- [X] T061 [US4] Validate title (3-100 chars), optional description (max 500)
- [X] T062 [US4] Create task linked to user_id from JWT

### Frontend Tasks Page Layout

- [X] T063 [US5, US4] Create `frontend/app/tasks/page.tsx`
- [X] T064 [US5, US4] Create `frontend/app/tasks/layout.tsx` with Navbar integration
- [X] T065 [US5, US4] Implement task list component in `frontend/components/TaskList.tsx`
- [X] T066 [US5, US4] Display empty state: "No tasks yet. Create your first task!"
- [X] T067 [US5, US4] Fetch and display user's tasks on page load

### Frontend Add Task

- [X] T068 [US4] Create `frontend/components/TaskForm.tsx` with title/description fields
- [X] T069 [US4] Add title validation (3-100 chars) and error display
- [X] T070 [US4] Implement create task API call and list update on success

**Checkpoint**: User can view tasks list and add new tasks

---

## Phase 7: User Story 8 - Toggle Complete (Priority: P1)

**Goal**: Allow users to mark tasks complete or incomplete

**Independent Test**: Click checkbox on task, verify status changes between complete/incomplete

### Backend Toggle Endpoint

- [X] T071 [US8] Implement `PATCH /api/{user_id}/tasks/{task_id}/toggle` endpoint
- [X] T072 [US8] Toggle completed boolean field
- [X] T073 [US8] Return updated task with new completed status

### Frontend Toggle

- [X] T074 [US8] Add checkbox component to each task in `TaskList.tsx`
- [X] T075 [US8] Implement toggle API call on checkbox click
- [X] T076 [US8] Update task list UI to reflect completion status change

**Checkpoint**: User can toggle task completion status

---

## Phase 8: User Story 6 - Update Task (Priority: P2)

**Goal**: Allow users to edit task details

**Independent Test**: Click edit, modify title, verify change is saved and displayed

### Backend Update Endpoint

- [X] T077 [US6] Implement `GET /api/{user_id}/tasks/{task_id}` endpoint for single task
- [X] T078 [US6] Implement `PUT /api/{user_id}/tasks/{task_id}` endpoint
- [X] T079 [US6] Validate and update title (3-100 chars), description (max 500)

### Frontend Update Task

- [X] T080 [US6] Create edit mode in `TaskList.tsx` or separate `TaskItem.tsx` component
- [X] T081 [US6] Add edit button to each task
- [X] T082 [US6] Show inline edit form when edit clicked
- [X] T083 [US6] Implement update API call and list refresh on save
- [X] T084 [US6] Cancel edit without saving

**Checkpoint**: User can edit task details

---

## Phase 9: User Story 7 - Delete Task (Priority: P2)

**Goal**: Allow users to remove tasks with confirmation

**Independent Test**: Click delete, confirm, verify task is removed from list

### Backend Delete Endpoint

- [X] T085 [US7] Implement `DELETE /api/{user_id}/tasks/{task_id}` endpoint
- [X] T086 [US7] Return 204 on successful deletion

### Frontend Delete Task

- [X] T087 [US7] Add delete button to each task
- [X] T088 [US7] Implement confirmation dialog before delete
- [X] T089 [US7] Call delete API on confirmation
- [X] T090 [US7] Remove task from list UI on success

**Checkpoint**: User can delete tasks with confirmation

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements affecting multiple user stories

### Error Handling

- [ ] T091 [P] Implement consistent error response format in `backend/app/main.py`
- [ ] T092 [P] Add network error handling in `frontend/services/api.ts`
- [ ] T093 [P] Add toast notifications for success/error feedback in frontend

### UX Improvements

- [ ] T094 [P] Add loading states to forms and API calls
- [ ] T095 [P] Add responsive design for mobile in `frontend/app/globals.css`
- [ ] T096 [P] Implement redirect to /signin for unauthenticated /tasks access

### Authentication Hardening

- [ ] T097 [P] Handle JWT expiry gracefully (redirect to signin)
- [ ] T098 [P] Add CORS configuration per plan.md security section

### Documentation

- [ ] T099 [P] Create `README.md` with setup and usage instructions
- [ ] T100 Run full `quickstart.md` validation checklist

**Checkpoint**: All user stories functional with polished UX

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phases 3-9)**: All depend on Foundational completion
- **Polish (Phase 10)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 Sign Up**: Can start after Foundational - No dependencies on other stories
- **US2 Sign In**: Can start after Foundational - No dependencies on other stories
- **US3 Sign Out**: Depends on US1 or US2 completion (needs auth flow)
- **US4 Add Task**: Depends on US1 or US2 completion (needs auth)
- **US5 View Tasks**: Depends on US1 or US2 completion (needs auth)
- **US6 Update Task**: Depends on US4/US5 (needs task display first)
- **US7 Delete Task**: Depends on US4/US5 (needs task display first)
- **US8 Toggle Complete**: Depends on US4/US5 (needs task display first)

### Recommended Execution Order

1. Setup + Foundational (critical path)
2. US1 Sign Up (enables authentication)
3. US2 Sign In (complements signup)
4. US3 Sign Out (quick after auth flow)
5. US4 + US5 (task CRUD - core value)
6. US8 Toggle Complete (quick add-on)
7. US6 Update Task (P2)
8. US7 Delete Task (P2)
9. Polish

---

## Parallel Opportunities

Within Foundational:
- T012, T013, T014 (backend core) can run in parallel
- T022, T023 (frontend auth/api) can run in parallel
- T026, T027 (schemas) can run in parallel

Within User Stories:
- US1 and US2 can run in parallel after Foundational (different files)
- US4 and US5 are bundled (same page) but components can parallelize
- US6 and US7 can run in parallel (separate endpoints)
- US8 can run in parallel with US6/US7

---

## Implementation Strategy

### MVP First (US1-US5, US8)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: Sign Up
4. Complete Phase 4: Sign In
5. Complete Phase 5: Sign Out
6. Complete Phase 6: View + Add Tasks
7. Complete Phase 7: Toggle Complete
8. **STOP and VALIDATE**: Full authentication and basic task CRUD working
9. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 → Sign up works
3. Add US2 → Sign in works
4. Add US3 → Sign out works
5. Add US4 + US5 → Task list and create work (MVP complete!)
6. Add US8 → Toggle works
7. Add US6 → Update works
8. Add US7 → Delete works
9. Polish → Production ready

### Parallel Team Strategy

Once Foundational is done:
- Developer A: US1 Sign Up + US2 Sign In + US3 Sign Out (auth flow)
- Developer B: US4 Add Task + US5 View Tasks + US8 Toggle (task core)
- Developer C: US6 Update + US7 Delete (task actions)
