---
id: 1
title: Create Backend API Spec
stage: spec
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: backend-api
branch: 002-backend-api
user: alish
command: /sp.specify
labels: [spec, backend, api, fastapi]
links:
  spec: specs/002-backend-api/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-backend-api/spec.md
tests:
 - none
---

## Prompt

```
/sp.specify
Backend Specification for Hackathon Phase 2 Todo Full-Stack Web Application Target audience: Hackathon judges evaluating secure, scalable backend architecture, spec-driven implementation, and seamless full-stack integration; end-users relying on reliable task persistence and user isolation in a multi-user Todo app Focus: Develop a robust, secure FastAPI backend with SQLModel ORM for Neon Serverless PostgreSQL, implementing all RESTful API endpoints for task CRUD operations, JWT-based authentication verification integrated with Better Auth from the frontend, and full enforcement of user data isolation, ensuring perfect interoperability with the Next.js frontend via shared JWT secrets and environment variables Success criteria:

All 6 RESTful endpoints fully implemented as specified in @specs/api/rest-endpoints.md (GET /api/tasks, POST /api/tasks, GET /api/tasks/{id}, PUT /api/tasks/{id}, DELETE /api/tasks/{id}, PATCH /api/tasks/{id}/complete) JWT middleware correctly verifies tokens on every protected route using the shared BETTER\_AUTH\_SECRET, extracts user\_id, and enforces task ownership (401 Unauthorized for invalid/missing tokens) Database schema exactly matches @specs/database/schema.md: 'users' table (managed by Better Auth integration) and 'tasks' table with user\_id foreign key, indexes for user\_id and completed SQLModel used for all ORM operations: models in models.py, database connection in db.py via NEON\_DB\_URL env var User isolation enforced: All queries filter by authenticated user\_id from JWT; no data leakage between users Query parameters supported: For GET /api/tasks – status ("all"/"pending"/"completed"), sort ("created"/"title"/"due\_date" if extended) Error handling: Use HTTPException for validation errors (e.g., missing title), 404 for non-existent tasks, 403 for unauthorized task access Pydantic models for request/response validation on all endpoints Backend runs independently with uvicorn main:app --reload and integrates via docker-compose.yml Seamless frontend integration: API calls from frontend's /lib/api.ts succeed with JWT headers; auth flow from Better Auth issues verifiable tokens Environment variables loaded correctly: BETTER\_AUTH\_SECRET for JWT, NEON\_DB\_URL for DB connection (use provided example values for setup) Performance optimizations: Efficient queries with indexes; connection pooling for Neon DB Entire backend generated via Claude Code using references to @specs/features/task-crud.md, @specs/features/authentication.md, @specs/agents/task-agent.md, @specs/agents/auth-agent.md, @specs/skills/task-skills.md, @specs/skills/auth-skills.md Judges confirm: "Secure, efficient, and perfectly integrated – no vulnerabilities, full spec compliance"

Constraints:

Technology locked: FastAPI (Python), SQLModel (ORM), Neon Serverless PostgreSQL, PyJWT or equivalent for token verification (no additional installs beyond stack) No manual coding: All generation via Spec-Kit and Claude Code prompts referencing specs Authentication: FastAPI middleware for JWT verification; integrate with Better Auth's frontend-issued tokens using shared BETTER\_AUTH\_SECRET env var Structure: Follow backend/CLAUDE.md guidelines exactly (main.py entry, models.py, routes/ folder for handlers, db.py for connection) Environment variables: Use .env file with BETTER\_AUTH\_SECRET=secret, BETTER\_AUTH\_URL=http://localhost:3000, NEON\_DB\_URL=postgresql://neonpg\_5xMPfhq9XgaS@ep-bitter-cloud-adk6f8ds-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require\&channel\_binding=require (load via dotenv or similar) Stateless auth: No shared DB sessions; JWT for verification only API base: All routes under /api/ (e.g., /api/tasks); CORS enabled for frontend origin Database: Neon-specific connection string; handle migrations implicitly via SQLModel (create\_all on startup if needed) Exclude frontend generation in this spec (assume frontend is complete; focus on backend and integration points) Timeline: Complete backend before full-stack testing; ensure integration succeeds without modifications to frontend

Not building:

Frontend UI or Next.js components (handled in separate frontend spec) Better Auth library itself (use as-is for frontend; backend only verifies JWTs) Advanced database features like full-text search, pagination beyond basic filtering, or real-time updates (WebSockets) Custom authentication beyond JWT (no OAuth, no email verification) Testing frameworks or CI/CD pipelines (focus on core backend logic) Deployment configurations (e.g., Heroku, Vercel – local docker-compose only) Phase 3 chatbot or MCP tools (keep to Phase 2 basics)

Final note: The backend must be rock-solid, secure, and integrate flawlessly with the frontend – every endpoint should handle real-world scenarios like concurrent requests, invalid inputs, and token expiry. Use the provided .env example to ensure immediate testability, and reference all specs precisely in Claude prompts for traceable, agentic development. This will make the full-stack app production-grade in security and performance.
```

## Response snapshot

Created a comprehensive specification for the Backend API component of the Todo Application. The specification includes:

- Four user stories covering task management, JWT authentication, database operations, and performance/scalability
- 13 functional requirements covering authentication, data isolation, CRUD operations, validation, and error handling
- Key entities (User, Task, JWT Token, Database Connection)
- Seven measurable success criteria with specific performance and security targets

The specification ensures that the backend will be secure, performant, and fully integrated with the frontend while maintaining strict data isolation between users.

## Outcome

- ✅ Impact: Created complete backend API specification with security and data isolation requirements
- 🧪 Tests: none
- 📁 Files: Created specs/002-backend-api/spec.md with comprehensive requirements
- 🔁 Next prompts: Ready to proceed with backend API implementation
- 🧠 Reflection: Specification provides clear foundation for secure backend development

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with backend API implementation based on spec