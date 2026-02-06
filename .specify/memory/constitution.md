<!--
SYNC IMPACT REPORT:
Version change: 1.0.0 → 2.0.0
Modified principles: All principles updated from Phase II to Phase III requirements
Added sections: New core principles for AI Chatbot Integration, Cohere API usage, MCP tools
Removed sections: Phase II specific principles
Templates requiring updates: ✅ Updated constitution template
Follow-up TODOs: None
-->

# Project Constitution: Hackathon Phase III – AI Todo Chatbot Integration into Existing Full-Stack Todo Application

## Core Principles

### I. Full Agentic, Spec-Driven Development
All implementation must follow specifications defined in the `/specs` folder with zero manual coding - all code generated via Claude Code using Spec-Kit references. Every feature and requirement must be traceable to specifications, ensuring consistent and predictable development outcomes. Maintain complete adherence to full agentic, spec-driven development with zero manual coding – all implementation via Claude Code + Spec-Kit references.

### II. Seamless Integration with Existing Backend
Adhere strictly to seamless integration into the existing Phase II backend (FastAPI + Neon PostgreSQL + Better Auth + JWT) without breaking any current functionality. Maintain the existing technology stack: Next.js 16+ (App Router) for frontend, FastAPI and SQLModel for backend, Neon Serverless PostgreSQL for database, and Better Auth with JWT plugin for authentication. The architecture follows a monorepo structure with modular agents to ensure consistency and maintainability.

### III. Stateless Architecture with Database Persistence
Implement stateless architecture for scalability where conversation state is persisted only in database (conversations + messages tables). Implement complete user data isolation where users can only access their own tasks and conversations. All API endpoints require valid JWT tokens, database queries must be filtered by authenticated user_id, and maintain stateless authentication with no server-side session storage to prevent data leakage between users.

### IV. Cohere API as Primary LLM Backend
Use Cohere API as the primary LLM backend for agent reasoning, tool calling, and response generation (instead of OpenAI). Adapt OpenAI Agents SDK patterns and code structure to work with Cohere API (use Cohere's tool-calling capabilities, structured outputs, and chat completions). Pydantic models for strict request/response validation and use Cohere API key via environment variable COHERE_API_KEY.

### V. MCP Tools Standard Interface
MCP (Model Context Protocol) tools remain the standardized interface for agent-tool interaction – expose all task and user operations as MCP-compatible tools. MCP Tools must exactly match spec: add_task, list_tasks, complete_task, delete_task, update_task + new get_user_profile. All tools require user_id (from JWT) and enforce ownership. All queries filtered by authenticated user_id from JWT middleware (reuse existing get_current_user).

### VI. Secure Operations and User Isolation
All chat operations protected by JWT (user_id from token), strict task/user isolation, no data leakage. Implement complete user data isolation where users can only access their own tasks. All API endpoints require valid JWT tokens, database queries must be filtered by authenticated user_id, and maintain stateless authentication with no server-side session storage to prevent data leakage between users.

### VII. Natural Language Processing and Multilingual Support
Natural language chatbot that fully controls task management (add, list, complete, delete, update) and provides user profile information (id, email, name, createdAt). Friendly, contextual, and multilingual responses (English + Urdu support when relevant) with action confirmations and graceful error handling. Agent behavior: Understand natural language intents (e.g., "Add task buy milk", "Show pending tasks", "Mera profile batao", "Mark task 4 complete", "Delete the old one").

## Technical Constraints

Non-negotiable requirements include Better Auth configured with JWT plugin and shared BETTER_AUTH_SECRET, Cohere API key via environment variable COHERE_API_KEY, database schema that matches specifications exactly, and all CRUD operations that enforce task ownership. The frontend must communicate with backend only through protected API endpoints, with no external libraries beyond the specified stack (Cohere SDK) and existing stack, no direct database access from frontend, and no session storage on backend. The monorepo structure must match the documented layout. Existing Phase II stack locked: FastAPI, SQLModel, Neon PostgreSQL, Better Auth + JWT. LLM switch: Use Cohere API exclusively (no OpenAI calls) – adapt OpenAI Agents SDK patterns to Cohere's chat/tool-calling API. Stateless server: No in-memory session – all state in DB. Public auth routes (signup/signin) remain unchanged; chat endpoint fully protected. No real-time (WebSockets) – single-turn stateless requests. No advanced features like multi-agent swarms, voice, or image generation (keep to text-based task management + profile).

Chat endpoint: POST /api/{user_id}/chat (accepts conversation_id optional, message required) – returns conversation_id, response, tool_calls. All tools require user_id (from JWT) and enforce ownership. Conversation history fetched from DB on every request, user/assistant messages stored after processing. Environment variables: Add COHERE_API_KEY; reuse BETTER_AUTH_SECRET, NEON_DB_URL. Cohere model: Use latest suitable model (e.g., command-r-plus or command-r) with tool calling enabled. Error handling: Return helpful messages for task not found, invalid input, auth failure (401). Swagger docs updated to include /api/{user_id}/chat endpoint.

## Success Criteria

Functional requirements include complete implementation of natural language chatbot that fully manages tasks via natural language: add, list (with filters), complete, delete, update – with friendly confirmations. User profile queries work: "Mera email kya hai?" → returns id, email, name, createdAt. Successful user signup and login with Better Auth, JWT tokens issued on login and automatically attached to API requests, FastAPI middleware correctly verifying JWT and extracting user_id, and all database queries filtered by authenticated user_id with zero data leakage. Agent uses Cohere for reasoning/tool selection – successful tool calls visible in response (tool_calls array). Endpoint returns correct response format: {conversation_id, response, tool_calls}. Conversation context preserved across requests via DB persistence – resumes after server restart.

Non-functional requirements encompass responsive frontend with task list, create/edit forms, chat interface, and authentication pages, application running locally with docker-compose up, entire implementation traceable to specs via Claude Code prompts, and full agentic structure with properly defined agents and skills. Full integration: Existing frontend can add ChatKit UI tab/page calling backend chat endpoint.

Delivery requirements demand a fully structured monorepo with all specs and configuration, working full-stack application meeting all acceptance criteria, clear history of spec-driven Claude Code prompts, and zero manual coding with all implementation generated via Claude Code. Judges confirm: "Seamless Phase III upgrade – agentic, secure, scalable, Cohere-powered, fully spec-driven". Zero regressions in Phase II functionality (task CRUD, auth). Runs locally with docker-compose (frontend + backend + Neon).

## Governance
This constitution supersedes all other development practices. All implementation must adhere to these principles, and any deviations require formal documentation and approval. Code reviews must verify compliance with all constitutional requirements, and complexity must be justified against these foundational principles. Use the defined spec-kit tools for runtime development guidance. This constitution supersedes all other development practices. All implementation must adhere to these principles, and any deviations require formal documentation and approval. Code reviews must verify compliance with all constitutional requirements, and complexity must be justified against these foundational principles. Use the defined spec-kit tools for runtime development guidance.

**Version**: 2.0.0 | **Ratified**: 2026-02-05 | **Last Amended**: 2026-02-06
