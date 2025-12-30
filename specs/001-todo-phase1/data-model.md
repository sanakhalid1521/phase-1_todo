# Data Model: Todo Application Phase I

## Entity: Task

Represents a single todo item stored in the system.

### Fields

| Field | Type | Required | Constraints / Validation |
|-------|------|----------|--------------------------|
| `id` | UUID | Yes | Auto-generated (UUIDv4) |
| `title` | string | Yes | Length: 3 to 100 characters |
| `description` | string | Yes | Length: 5 to 500 characters |
| `completed` | boolean | Yes | Default: False |
| `created_at` | datetime | Yes | Read-only; set on creation |
| `updated_at` | datetime | Yes | Updated on every modification |

### State Transitions

1. **Pending** (Default): `completed = False`
2. **Completed**: `completed = True`
3. **Toggle**: State can be switched between Pending and Completed at any time.

### Validation Rules

- **ID**: Must be a valid UUID object.
- **Title**: Stripped of whitespace. Error if length < 3 or > 100.
- **Description**: Stripped of whitespace. Error if length < 5 or > 500.
- **Dates**: `updated_at` must always be >= `created_at`.
