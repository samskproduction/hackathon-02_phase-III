---
id: 1
title: Update Project Constitution
stage: constitution
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: alish
command: /sp.constitution
labels: [constitution, setup, hackathon]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
/sp.constitution

Project: Hackathon Phase 2 – Todo Full-Stack Web Application (Next.js + FastAPI + Neon DB)

Core principles:

Fully spec-driven and agentic development
Zero manual coding allowed – all implementation must be generated via Claude Code using Spec-Kit references
Modular architecture through agents and skills
Complete user isolation and data ownership enforcement
Strict adherence to the provided technology stack and monorepo structure

Key standards:

All features must be implemented exactly as defined in /specs folder
Every API endpoint must require valid JWT token and filter data by authenticated user\_id
Better Auth configured with JWT plugin and shared BETTER\_AUTH\_SECRET between frontend and backend
Database schema must match @specs/database/schema.md exactly (users table managed by Better Auth, tasks table with user\_id foreign key)
All references in prompts must use @specs/path/to/file.md format
Code structure must follow guidelines in root CLAUDE.md, frontend/CLAUDE.md, and backend/CLAUDE.md
Responsive, clean UI using Tailwind CSS and Next.js App Router (server components by default)

Constraints:

Technology stack locked: Next.js 16+ (App Router), FastAPI, SQLModel, Neon Serverless PostgreSQL, Better Auth (JWT), Tailwind CSS
Monorepo structure must exactly match the documented layout including .spec-kit/config.yaml
No external libraries beyond the specified stack
No direct database access from frontend – all operations via protected FastAPI endpoints
No session storage on backend – authentication must be stateless (JWT only)
All CRUD operations must enforce task ownership (user can only access their own tasks)

Success criteria:

Complete implementation of all 5 basic task CRUD operations + toggle completion as a multi-user web app
Successful user signup and login with Better Auth
JWT tokens issued on login and automatically attached to all API requests from frontend
FastAPI middleware correctly verifies JWT and extracts user\_id on every protected route
All database queries filtered by authenticated user\_id – zero data leakage between users
Responsive frontend with task list, create/edit forms, and authentication pages
Project runs locally with docker-compose up (or separately via npm run dev and uvicorn)
Entire implementation traceable to specs via Claude Code prompts using @specs references
Full agentic structure in place: Main Agent, Task Agent, Auth Agent, UI Agent with defined skills
All files and folders created exactly as per the monorepo specification structure

Final deliverables:

Fully structured monorepo with all specs, CLAUDE.md files, and .spec-kit config
Working full-stack application meeting all acceptance criteria
Clear history of spec-driven Claude Code prompts demonstrating zero manual coding
```

## Response snapshot

Updated the project constitution file at `.specify/memory/constitution.md` to reflect the core principles and guidelines for the Hackathon Phase 2 Todo Full-Stack Web Application project. The constitution now includes:

- Spec-driven development principles
- Technology stack adherence requirements
- Security & data isolation mandates
- Quality standards
- Architecture requirements
- Technical constraints
- Success criteria
- Governance guidelines

The constitution establishes the foundation for the entire project, ensuring all future development adheres to the specified requirements for a secure, multi-user todo application using Next.js, FastAPI, and Neon DB with JWT-based authentication.

## Outcome

- ✅ Impact: Created project constitution file establishing core principles and guidelines
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with comprehensive project guidelines
- 🔁 Next prompts: Will proceed with creating specs, plan, and tasks based on this constitution
- 🧠 Reflection: Constitution provides clear foundation for agentic development approach

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Create feature specifications based on constitution