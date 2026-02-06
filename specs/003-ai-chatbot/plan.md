# Implementation Plan: Phase III – AI Todo Chatbot (Cohere-Powered Integration)

**Branch**: `003-ai-chatbot` | **Date**: 2026-02-06 | **Spec**: [specs/003-ai-chatbot/spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-ai-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Integration of a Cohere-powered AI chatbot into the existing Todo application that enables natural language task management and profile queries. The solution includes a custom Cohere agent runner, MCP-compatible tools, floating chat UI, and persistent conversation storage, all while maintaining existing Phase II functionality.

## Technical Context

**Language/Version**: Python 3.11, TypeScript/JavaScript, Next.js 16+
**Primary Dependencies**: FastAPI, Cohere Python SDK, SQLModel, Better Auth, Tailwind CSS
**Storage**: Neon PostgreSQL (existing), new Conversation and Message tables
**Testing**: pytest for backend, Jest/Cypress for frontend
**Target Platform**: Web application (frontend + backend)
**Project Type**: Web (frontend and backend components)
**Performance Goals**: Sub-3 second response times for chat interactions, 90% success rate for natural language commands
**Constraints**: Stateless architecture, JWT-authenticated endpoints, existing Phase II functionality preserved
**Scale/Scope**: Single-user conversations, persistent across sessions

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Full agentic, spec-driven development with zero manual coding - following Claude Code + Spec-Kit approach
- ✅ Seamless integration with existing Phase II backend - leveraging existing FastAPI + Neon PostgreSQL + Better Auth + JWT
- ✅ Stateless architecture with database persistence - conversation state stored in database only
- ✅ Cohere API as primary LLM backend - using Cohere instead of OpenAI as specified
- ✅ MCP tools standard interface - implementing tools in Cohere-compatible format
- ✅ Secure operations with user isolation - all operations protected by JWT with user_id enforcement
- ✅ Natural language processing with multilingual support - English + Urdu support as specified

## Project Structure

### Documentation (this feature)

```text
specs/003-ai-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── conversation.py      # New: Conversation model
│   │   ├── message.py          # New: Message model
│   │   └── user.py             # Existing: User model
│   ├── services/
│   │   ├── __init__.py
│   │   ├── cohere_runner.py    # New: Custom Cohere agent runner
│   │   ├── mcp_tools.py        # New: MCP-compatible tools for Cohere
│   │   └── auth.py             # Existing: Authentication service
│   ├── api/
│   │   ├── __init__.py
│   │   ├── chat.py            # New: Chat API endpoints
│   │   └── tasks.py           # Existing: Task API endpoints
│   └── main.py                # Existing: Main application entry point
└── tests/
    └── integration/

frontend/
├── src/
│   ├── components/
│   │   ├── __init__.tsx
│   │   ├── ChatbotIcon.tsx    # New: Floating chat icon component
│   │   ├── ChatWindow.tsx     # New: Chat interface component
│   │   └── TaskList.tsx       # Existing: Task list component
│   ├── pages/
│   │   ├── dashboard.tsx      # Existing: Dashboard page
│   │   └── index.tsx          # Existing: Home page
│   └── services/
│       ├── api.ts             # Existing: API service
│       └── auth.ts            # Existing: Authentication service
└── tests/
    └── components/
```

**Structure Decision**: Following the existing web application structure with frontend and backend components. New chatbot functionality is integrated into the existing monorepo while maintaining clear separation of concerns. Backend adds new models, services, and API endpoints for chat functionality. Frontend adds new components for the chat interface while preserving existing UI.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [None] | [No violations identified] | [All constitutional requirements met] |