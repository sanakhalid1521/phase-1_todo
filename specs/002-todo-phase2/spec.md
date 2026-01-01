# Feature Specification: Todo Application Phase II

**Feature Branch**: `002-todo-phase2`
**Created**: 2025-12-31
**Status**: Draft
**Input**: Build Phase II: Transform the console app into a full-stack multi-user web application with persistent storage.

## Clarifications

### Session 2025-12-31

- Q: Out-of-scope features → A: No social features, team sharing, or email notifications in Phase 2

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Sign Up (Priority: P1)

As a new user, I want to sign up with email and password.

**Why this priority**: Essential for multi-user support and secure access.

**Independent Test**: Can be tested by navigating to /signup, entering valid email/password, and verifying redirect to tasks page.

**Acceptance Scenarios**:

1. **Given** the signup page, **When** I enter a valid email and password (8+ chars), **Then** my account is created with hashed password and I am redirected to the tasks page.
2. **Given** the signup page, **When** I enter an invalid email, **Then** I should see "Invalid email format".
3. **Given** the signup page, **When** I enter an email that already exists, **Then** I should see "Email already registered".

---

### User Story 2 - Sign In (Priority: P1)

As a returning user, I want to sign in with my credentials.

**Why this priority**: Core requirement for user authentication and data security.

**Independent Test**: Can be tested by navigating to /signin, entering valid credentials, and verifying redirect to tasks page with JWT token.

**Acceptance Scenarios**:

1. **Given** the signin page, **When** I enter correct email and password, **Then** I should see a success message and be redirected to /tasks.
2. **Given** the signin page, **When** I enter incorrect password, **Then** I should see "Invalid email or password".

---

### User Story 3 - Sign Out (Priority: P1)

As a logged-in user, I want to log out securely.

**Why this priority**: Security requirement for session management.

**Independent Test**: Can be tested by clicking logout and verifying redirect to signin page.

**Acceptance Scenarios**:

1. **Given** I am logged in, **When** I click logout, **Then** the session is cleared and I am redirected to /signin.

---

### User Story 4 - Add Task (Web) (Priority: P1)

As a logged-in user, I want to add new tasks via a web form.

**Why this priority**: Core feature migration from Phase I.

**Independent Test**: Can be tested by clicking "Add Task", entering title/description, and verifying the task appears in the list.

**Acceptance Scenarios**:

1. **Given** I am on the tasks page, **When** I click "Add Task" and enter a valid title (3-100 chars) and optional description, **Then** the task is created and appears in the list.
2. **Given** I am on the tasks page, **When** I enter a title with less than 3 characters, **Then** I should see a validation error.

---

### User Story 5 - View Tasks (Web) (Priority: P1)

As a logged-in user, I want to view all my tasks in a web interface.

**Why this priority**: Core feature migration from Phase I.

**Independent Test**: Can be tested by verifying the tasks are displayed as cards/table with correct information.

**Acceptance Scenarios**:

1. **Given** I have tasks, **When** I visit /tasks, **Then** I should see all my tasks with title, status, and created date.
2. **Given** I have no tasks, **When** I visit /tasks, **Then** I should see "No tasks yet. Create your first task!".

---

### User Story 6 - Update Task (Web) (Priority: P2)

As a logged-in user, I want to update task details.

**Why this priority**: Core feature migration from Phase I.

**Independent Test**: Can be tested by clicking edit, modifying title, and verifying the change.

**Acceptance Scenarios**:

1. **Given** a task exists, **When** I click "Edit" and modify the title, **Then** the task should be updated and show the new title.

---

### User Story 7 - Delete Task (Web) (Priority: P2)

As a logged-in user, I want to delete tasks.

**Why this priority**: Core feature migration from Phase I.

**Independent Test**: Can be tested by clicking delete, confirming, and verifying the task is removed.

**Acceptance Scenarios**:

1. **Given** a task exists, **When** I click "Delete" and confirm, **Then** the task should be removed from the list.

---

### User Story 8 - Toggle Complete (Web) (Priority: P1)

As a logged-in user, I want to mark tasks complete/incomplete.

**Why this priority**: Core feature migration from Phase I.

**Independent Test**: Can be tested by clicking the checkbox and verifying the status changes.

**Acceptance Scenarios**:

1. **Given** a task is pending, **When** I click the checkbox, **Then** the status should change to complete.

---

### Edge Cases

- **Network Errors**: Show "Unable to connect. Please try again."
- **Unauthorized Access**: Redirect to /signin if no valid token.
- **Duplicate Emails**: Prevent signup with existing email.
- **Session Expiry**: Handle JWT expiry gracefully.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide signup page at `/signup` with email and password fields.
- **FR-002**: System MUST provide signin page at `/signin` with email and password fields.
- **FR-003**: System MUST hash passwords using bcrypt (rounds: 12).
- **FR-004**: System MUST issue JWT tokens on successful login/signup.
- **FR-005**: System MUST validate JWT tokens on every API request.
- **FR-006**: System MUST filter tasks by `user_id` to ensure data isolation.
- **FR-007**: System MUST provide CRUD endpoints for tasks (`/api/tasks`).
- **FR-008**: System MUST use PostgreSQL for persistent storage.

### Key Entities

- **User**: `id` (UUID), `email` (string), `password_hash` (string), `created_at` (timestamp).
- **Task**: `id` (integer), `user_id` (UUID), `title` (string), `description` (text), `completed` (boolean), `created_at` (timestamp).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can sign up and login successfully in under 5 seconds.
- **SC-002**: Task list loads in under 1 second.
- **SC-003**: 100% of unauthorized requests are rejected.
- **SC-004**: Users can only see and modify their own tasks.
- **SC-005**: Data persists across browser sessions (PostgreSQL).
