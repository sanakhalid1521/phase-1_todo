---
id: 0023
title: Task Update Logic and Sidebar Context
stage: green
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-phase1
branch: 001-todo-phase1
user: local
command: none
labels: ["crud", "state-management", "ui-ux", "sidebar"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/app/tasks/page.tsx
tests:
  - Verified Update Sidebar pre-fills with task data
  - Verified Apply Changes correctly modifies existing tasks
  - Verified Create mode still works independently
---

## Prompt

added task mai jo eye ka icon he os o update ka kaam kary os ko bhi sahi karo

## Response snapshot

Upgraded the Task Management logic to support full editing capabilities:
1. **Update Connection**: Replaced the placeholder Eye icon with an `Edit3` icon and connected it to a new `handleEditClick` function.
2. **Context-Aware Sidebar**: The task sidebar now intelligently switches between **"New Directive"** and **"Update Directive"** based on the user's action.
3. **Pre-filled Forms**: When clicking edit, the sidebar automatically pre-fills with the existing task's title, description, and deadline.
4. **Dynamic Actions**: The primary button text changes from "Save Directive" to "Apply Changes" when in update mode.
5. **State Logic**: Refactored the `saveTask` function to handle both inserting new records and mapping updates to existing ones based on `editingTaskId`.

## Outcome

- ✅ Impact: Full CRUD (Create, Read, Update, Delete) capability now works seamlessly in the frontend.
- 🧪 Tests: Confirmed modal state resets correctly after dismissal/save.
- 📁 Files: Updated `frontend/app/tasks/page.tsx`.
- 🧠 Reflection: Reusing the same sidebar for both Create and Update reduces code duplication and provides a consistent mental model for the user.
---
id: 230744-48f5-9be4-8f4b00235b31
---
