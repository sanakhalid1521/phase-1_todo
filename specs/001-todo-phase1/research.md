# Research: Todo Application Phase I

## Design Decisions

### R1: Task ID Matching
- **Decision**: Users provide the first 8 characters of the task ID (UUID) for identification.
- **Rationale**: UUIDs are too long for convenient manual entry. The first 8 characters (hex) provide 2^32 combinations, which is more than sufficient for an in-memory application to avoid collisions.
- **Alternatives Considered**: Integer IDs. (Rejected to maintain consistency with the long-term plan for UUID-based cloud synchronization in Phase V).

### R2: Table Border & UI
- **Decision**: Use ASCII characters (`+`, `-`, `|`) for borders and native Python string formatting (`f-strings` with alignment) for columns.
- **Rationale**: Ensures maximum compatibility across heterogeneous terminal environments (Windows CMD, PowerShell, Bash).
- **Alternatives Considered**: Box-drawing characters (─, │). (Rejected as they can sometimes display incorrectly on older terminal configurations).

### R3: Status Icons
- **Decision**: Use Unicode symbols `○` (U+25CB) and `✓` (U+2713).
- **Rationale**: Modern terminals support these symbols, providing a more professional look than plain ASCII `[ ]` and `[x]`.
- **Alternatives Considered**: Plain ASCII `( )` and `(X)`. (Keep as fallback if encoding errors are detected).

### R4: Validation Logic
- **Decision**: Centralize validation in the `Task` dataclass `__post_init__` method and a dedicated `validator` utility.
- **Rationale**: Ensures that no invalid `Task` object can exist in the system, simplifying error handling in the `TodoService`.
- **Alternatives Considered**: Validating only in the CLI layer. (Rejected as it violates the separation of concerns and leads to logic duplication).

## Technical Unknowns Resolved

- **Python 3.13 Compatibility**: All standard library modules (`uuid`, `datetime`, `dataclasses`) are stable and compatible.
- **Memory Limits**: Python's `list` and `dict` can easily handle thousands of tasks without significant memory overhead for this use case.
- **Terminal Colors**: Confirmed ANSI escape codes `\033[92m` (Green) and `\033[91m` (Red) work in most modern terminals including Windows Terminal and VS Code.
