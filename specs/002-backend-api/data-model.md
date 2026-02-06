# Data Model: Backend API for Todo Application

## Key Entities

### User
**Representation**: Registered user (managed by Better Auth, referenced by user_id in tasks)
**Fields**:
- id: str (unique identifier from Better Auth system)
- email: str (user's email address)
- created_at: datetime (timestamp when user account was created)
- updated_at: datetime (timestamp when user data was last updated)

### Task
**Representation**: Individual todo item with properties (id, user_id, title, description, completed, created_at, updated_at, due_date, priority)
**Fields**:
- id: int (auto-incrementing primary key)
- user_id: str (foreign key linking to the owning user from JWT)
- title: str (task title, 1-200 characters, required)
- description: str | None (optional detailed description)
- is_completed: bool (completion status, default: false)
- created_at: datetime (timestamp when task was created)
- updated_at: datetime (timestamp when task was last updated)
- due_date: datetime | None (optional deadline for the task)
- priority: str ("low" | "medium" | "high" | "urgent", default: "medium")

## State Transitions

### Task State Transitions
- **Created** → **Active** → **Completed** → **Edited** → **Active** (or Completed if edited to completed)
- **Deleted**: Active/Completed → **Pending Deletion** → **Deleted**

## Validation Rules

### Task Validation
- Title must be 1-200 characters
- Title cannot be empty or only whitespace
- Priority must be one of the allowed values: "low", "medium", "high", "urgent"
- user_id must match authenticated user from JWT token (enforced by backend)

### User Validation
- user_id must be a valid string format from Better Auth system
- All operations must be tied to authenticated user_id

## Relationships
- User "has many" Tasks (one-to-many relationship)
- Tasks belong to a single User (via user_id foreign key)
- All queries must filter by user_id to enforce data isolation

## Database Schema
```
users table (managed by Better Auth):
- id (primary key)
- email
- created_at
- updated_at

tasks table:
- id (primary key, auto-incrementing)
- user_id (foreign key referencing users.id)
- title (string, not null)
- description (text, nullable)
- is_completed (boolean, default false)
- created_at (datetime, default current timestamp)
- updated_at (datetime, default current timestamp, auto-update)
- due_date (datetime, nullable)
- priority (string enum, default 'medium')
- FOREIGN KEY (user_id) REFERENCES users(id)
- INDEX ON user_id
- INDEX ON is_completed
```

## Query Patterns
- GET /api/tasks (filter by user_id and optionally by is_completed status)
- GET /api/tasks/{id} (filter by user_id and specific task id)
- GET /api/tasks (with status query param for filtering)