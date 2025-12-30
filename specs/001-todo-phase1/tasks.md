---
description: "Task list for Todo Application Phase I"
---

# Tasks: Todo Application Phase I

**Input**: Design documents from `specs/001-todo-phase1/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and modular structure

- [X] T001 Create project directories `src/` and `src/__init__.py`
- [ ] T002 Initialize `uv` environment and project configuration in `pyproject.toml`
- [X] T003 [P] Create empty shell files: `src/main.py`, `src/models.py`, `src/services.py`, `src/utils.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data structures and service skeleton

- [X] T004 Create `Task` dataclass with `__post_init__` validation in `src/models.py`
- [X] T005 Implement `TodoService` class with in-memory storage (list) in `src/services.py`
- [X] T006 [P] Create `print_error` and `print_success` color helpers in `src/utils.py`
- [X] T007 [P] Create `clear_screen` utility in `src/utils.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add Tasks (Priority: P1) 🎯 MVP

**Goal**: Allow users to add new tasks with title and description

- [X] T008 [US1] Implement `TodoService.add_task` method in `src/services.py`
- [X] T009 [P] [US1] Add `validate_title` and `validate_description` in `src/utils.py`
- [X] T010 [US1] Implement `handle_add_task` UI logic (sequential prompts) in `src/main.py`

**Independent Test**: Run app, select "Add Task", provide valid inputs, verify success message and ID.

---

## Phase 4: User Story 2 - View Tasks (Priority: P1)

**Goal**: Display all tasks in a formatted table with a summary

- [X] T011 [US2] Implement `TodoService.get_all_tasks` and summary calculation in `src/services.py`
- [X] T012 [P] [US2] Implement `format_task_table` with ASCII borders and icons in `src/utils.py`
- [X] T013 [US2] Implement `handle_list_tasks` UI logic in `src/main.py`

**Independent Test**: Add 2 tasks, select "List Tasks", verify table layout and summary counts.

---

## Phase 5: User Story 5 - Mark Complete/Incomplete (Priority: P1)

**Goal**: Toggle the completion status of a task by ID

- [X] T014 [US5] Implement `TodoService.toggle_task_status` in `src/services.py`
- [X] T015 [US5] Implement `handle_toggle_complete` UI logic in `src/main.py`

**Independent Test**: Select "Mark Task Complete", provide a valid ID, verify status change to ✓ in the list.

---

## Phase 6: User Story 3 - Update Tasks (Priority: P2)

**Goal**: Correct or detail existing tasks by ID

- [X] T016 [US3] Implement `TodoService.update_task` in `src/services.py`
- [X] T017 [US3] Implement `handle_update_task` UI logic in `src/main.py`

**Independent Test**: Select "Update Task", provide ID, change title, verify updated title in the list.

---

## Phase 7: User Story 4 - Delete Tasks (Priority: P2)

**Goal**: Remove tasks with confirmation

- [X] T018 [US4] Implement `TodoService.delete_task` in `src/services.py`
- [X] T019 [P] [US4] Add `get_confirmation` utility (y/n) in `src/utils.py`
- [X] T020 [US4] Implement `handle_delete_task` UI logic in `src/main.py`

**Independent Test**: Select "Delete Task", provide ID, confirm 'y', verify task is removed.

---

## Phase 8: Polish & Menu Integration

**Purpose**: Finalize the user experience

- [X] T021 Implement `main()` menu loop with option mapping in `src/main.py`
- [X] T022 [P] add docstrings and type hints to all public functions in `src/`
- [ ] T023 Run full `quickstart.md` validation checklist

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on T001-T003
- **User Stories (Phases 3-7)**: All depend on Phase 2 completion
- **Polish (Phase 8)**: Depends on all stories being functional

### User Story Dependencies
- **All User Stories (US1-US5)**: Independent of each other at the service level but should be implemented in priority order (P1 -> P2).

---

## Parallel Opportunities

- T003, T006, T007 (Infrastructure shells and side-effects)
- T012 (Formatting logic) and T014 (Toggle logic) if worked on by different agents
- T019 (Confirmation helper) while implementing other P2 stories

---

## Implementation Strategy: MVP First

1. Complete Setup and Foundational phases.
2. Implement **User Story 1** (Add) and **User Story 2** (View).
3. **VALIDATE**: Ensure a user can add a task and see it. This is the core MVP.
4. Proceed to Toggle (US5), then P2 stories.
5. Finalize the main loop.
