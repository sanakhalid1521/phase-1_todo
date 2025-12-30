<!--
  Sync Impact Report:
  - Version change: [NONE] → 1.0.0
  - List of modified principles:
    - [PRINCIPLE_1_NAME] → I. Development Philosophy
    - [PRINCIPLE_2_NAME] → II. Code Quality Standards
    - [PRINCIPLE_3_NAME] → III. User Experience (UX)
    - [PRINCIPLE_4_NAME] → IV. Security & Privacy
  - Added sections:
    - Phase I Implementation (Console Application)
    - Development Standards & Structure
  - Removed sections: N/A (Initial ratification)
  - Templates requiring updates:
    - .specify/templates/plan-template.md: ✅ Updated "Constitution Check" gates
    - .specify/templates/spec-template.md: ✅ Aligned with core principles
    - .specify/templates/tasks-template.md: ✅ Aligned with phase-based progression
  - Follow-up TODOs: N/A
-->

# Todo Application Constitution

## Core Principles

### I. Development Philosophy
**Spec-Driven Development (SDD):** All features MUST be specified before implementation.
**AI-First Approach:** Claude Code generates all code; humans focus on refining specifications until the code output is correct. Never write code manually.
**Progressive Enhancement:** Each phase MUST build upon the prior phase, maintaining architectural integrity through all 5 phases (Phase I: Console to Phase V: Cloud).
**Reusable Intelligence:** Proactively create subagents and agent skills to codify common patterns and automate repetitive architectural tasks.

### II. Code Quality Standards
**Clean Code:** Code MUST be readable, maintainable, and self-documenting.
**SOLID Principles:** Adhere strictly to Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion.
**Type Safety:** Mandatory type hints for Python; TypeScript MUST be used for all frontend phases.
**DRY & KISS:** "Don't Repeat Yourself" and "Keep It Simple, Stupid" are the default modes of operation.
**Testing:** Minimum 80% code coverage is REQUIRED for the service layer and business logic.
**Documentation:** Maintain a clear README and API documentation; inline comments are reserved ONLY for complex logic that cannot be made self-evident.

### III. User Experience (UX)
**Intuitiveness:** Interfaces MUST be designed for a minimal learning curve.
**Feedback Loop:** Clear success and error messages MUST be provided for every user action.
**Resilience:** Graceful error handling is mandatory; the system MUST never crash and MUST always provide a path to recovery.
**Performance:** UIs MUST be responsive, and APIs MUST deliver fast, optimized responses.
**Accessibility:** Use semantic HTML and appropriate ARIA labels in all web-based phases.

### IV. Security & Privacy
**Authentication:** Use secure industry-standard methods (e.g., bcrypt/argon2 for hashing, JWT for tokens).
**Validation:** All inputs MUST be validated at the system boundary.
**Protection:** SQL injection prevention (via ORMs or parameterized queries) and XSS prevention (via output sanitization) are non-negotiable.
**Secret Management:** Never hardcode secrets or tokens; use environment variables and `.env` files exclusively.

## Phase I Implementation (Console Application)
**Environment:** Python 3.13+ using the `uv` package manager.
**Storage:** Initial implementation uses in-memory Python lists; no external database dependencies are permitted in Phase I.
**Dependencies:** Use the Python Standard Library exclusively; avoid external third-party dependencies unless absolutely necessary for infrastructure.
**Architecture:** Maintain a modular structure with strictly separated models, services, and UI layers.

## Development Standards & Structure
**Directory Layout (src/):**
- `main.py`: Entry point and CLI interface orchestration.
- `models.py`: Data models (e.g., Task dataclass).
- `services.py`: Core business logic (e.g., TodoService).
- `utils.py`: Shared helper functions.

**Implementation Rules:**
- Type hints are MANDATORY on all functions and variables.
- Docstrings are REQUIRED for all public classes, methods, and functions.
- All code changes MUST be small, testable, and reference specific code blocks.

## Governance
**Supremacy:** This constitution supersedes all individual implementation preferences. All development actions and architectural planning MUST be verified against these principles.
**Amendments:** Amendments require a version bump and documented rationale in the PHR.
**Compliance:** The "Constitution Check" in implementation plans is the primary gate for ensuring adherence.
**Versioning:** MAJOR for removals/redefinitions; MINOR for new principles/expanded guidance; PATCH for clarifications.

**Version**: 1.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2025-12-30
