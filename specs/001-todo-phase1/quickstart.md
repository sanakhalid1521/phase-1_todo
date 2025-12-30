# Quickstart: Todo Application Phase I

## Prerequisites

- **Python**: 3.13 or higher
- **System**: Any OS with a standard terminal supporting UTF-8 and ANSI colors
- **Package Manager**: [uv](https://github.com/astral-sh/uv) (Recommended)

## Setup & Execution

1. **Clone the repository** (if not already local).
2. **Navigate to the project root**:
   ```bash
   cd "E:\quarter-4\Hackathon-II\phase-1 todo"
   ```
3. **Run the application**:
   ```bash
   uv run src/main.py
   ```

## Basic Usage

- **Add Task**: Choice `1`. Follow the sequential prompts for Title and Description.
- **List Tasks**: Choice `2`. View the table of all tasks and the status summary.
- **Update Task**: Choice `3`. Provide the first 8 characters of a task ID.
- **Delete Task**: Choice `4`. Provide ID and confirm with `y`.
- **Toggle Status**: Choice `5`. Provide ID to switch between incomplete and complete.
- **Exit**: Choice `6`.

## Development

All source code is located in `src/`.
- `models.py`: Task data structures
- `services.py`: Business logic
- `utils.py`: Display and validation helpers
- `main.py`: Entry point
