# Research: Backend API Implementation

## Decision Log

### JWT Verification Approach
**Decision**: Use PyJWT with shared BETTER_AUTH_SECRET for token verification
**Rationale**: Direct integration with Better Auth's frontend-issued tokens, lightweight, standard approach for FastAPI applications
**Alternatives considered**:
- OAuth2 with password flow (more complex, unnecessary for this integration)
- Custom token scheme (would break compatibility with Better Auth)

### Database Connection Pooling
**Decision**: Use SQLModel's built-in connection pooling with Neon Serverless PostgreSQL
**Rationale**: Efficient resource management for serverless environment, proper handling of connection limits
**Alternatives considered**:
- Raw SQLAlchemy (would lose SQLModel benefits)
- Connection string without pooling (inefficient for concurrent requests)

### Authentication Middleware Approach
**Decision**: FastAPI dependency with Depends for JWT verification (use Depends with reusable get_current_user dependency)
**Rationale**: Clean integration with FastAPI's dependency injection system, reusable across endpoints, cleaner and more reusable
**Alternatives considered**:
- Decorator approach (less idiomatic for FastAPI)
- Manual verification in each route (repetitive and error-prone)
- Manual extraction (harder to reuse)

### Database Session Management
**Decision**: Session per request via dependency (instead of global)
**Rationale**: Best practice for FastAPI + SQLModel, ensures proper resource management per request
**Alternatives considered**:
- Global session (poor resource management, potential race conditions)
- Manual session management (error-prone, inconsistent)

### Environment Loading
**Decision**: Use python-dotenv (instead of pydantic-settings)
**Rationale**: Simple, matches provided .env example, lightweight solution
**Alternatives considered**:
- pydantic-settings (more complex, heavier)

### CORS Configuration
**Decision**: Specific origin with credentials support (instead of wildcard)
**Rationale**: More secure approach that works well with Better Auth cookies if any
**Alternatives considered**:
- Wildcard (*) (less secure)

### JWT Library
**Decision**: pyjwt (instead of authlib)
**Rationale**: Lightweight, widely used, sufficient for verification requirements
**Alternatives considered**:
- authlib (heavier, more complex for this use case)

### Table Creation
**Decision**: SQLModel create_all on startup (instead of manual migrations)
**Rationale**: Acceptable for hackathon project, Neon handles schema management
**Alternatives considered**:
- Manual migrations (overkill for hackathon)
- Alembic migrations (too complex for this scope)

### API Prefix
**Decision**: /api (instead of root)
**Rationale**: Clean separation of concerns, matches specification
**Alternatives considered**:
- Root path (would mix API and other routes)

### Response Models
**Decision**: Separate Pydantic models for TaskCreate, TaskUpdate, TaskResponse
**Rationale**: Better validation and documentation, follows FastAPI best practices
**Alternatives considered**:
- Single model (less flexible, worse validation)

### Error Handling Strategy
**Decision**: Use FastAPI's HTTPException with standardized error responses
**Rationale**: Consistent with FastAPI patterns, clear status codes for frontend integration
**Alternatives considered**:
- Custom exception handlers (more complex, unnecessary)
- Generic error responses (not informative enough)

### Database Indexing Strategy
**Decision**: Create indexes on user_id and completed fields for efficient queries
**Rationale**: Optimizes the most common query patterns (filtering by user and completion status)
**Alternatives considered**:
- No indexes (poor performance)
- Excessive indexing (unnecessary overhead)