---
id: 1
title: "Update Phase III Constitution"
stage: constitution
date_iso: 2026-02-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: "/sp.constitution"
labels: ["constitution", "phase-iii", "ai-chatbot"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
---

# Constitution Update: Phase III AI Todo Chatbot Integration

## Original Prompt

Project: Phase III – AI Todo Chatbot Integration into Existing Full-Stack Todo Application

Core principles:

Full agentic, spec-driven development with zero manual coding – all implementation via Claude Code + Spec-Kit references

Seamless integration into the existing Phase II backend (FastAPI + Neon PostgreSQL + Better Auth + JWT) without breaking any current functionality

Stateless architecture for scalability: conversation state persisted only in database (conversations + messages tables)

Natural language chatbot that fully controls task management (add, list, complete, delete, update) and provides user profile information (id, email, name, createdAt)

Use Cohere API as the primary LLM backend for agent reasoning, tool calling, and response generation (instead of OpenAI)

Adapt OpenAI Agents SDK patterns and code structure to work with Cohere API (use Cohere's tool-calling capabilities, structured outputs, and chat completions)

MCP (Model Context Protocol) tools remain the standardized interface for agent-tool interaction – expose all task and user operations as MCP-compatible tools

Secure: All chat operations protected by JWT (user_id from token), strict task/user isolation, no data leakage

Friendly, contextual, and multilingual responses (English + Urdu support when relevant) with action confirmations and graceful error handling

Key standards:

Chat endpoint: POST /api/{user_id}/chat (accepts conversation_id optional, message required) – returns conversation_id, response, tool_calls

MCP Tools must exactly match spec: add_task, list_tasks, complete_task, delete_task, update_task + new get_user_profile

All tools require user_id (from JWT) and enforce ownership

Conversation history fetched from DB on every request, user/assistant messages stored after processing

Agent behavior: Understand natural language intents (e.g., "Add task buy milk", "Show pending tasks", "Mera profile batao", "Mark task 4 complete", "Delete the old one")

Use Cohere API key via environment variable COHERE_API_KEY

Cohere model: Use latest suitable model (e.g., command-r-plus or command-r) with tool calling enabled

Pydantic models for strict request/response validation

Error handling: Return helpful messages for task not found, invalid input, auth failure (401)

All queries filtered by authenticated user_id from JWT middleware (reuse existing get_current_user)

Swagger docs updated to include /api/{user_id}/chat endpoint

Frontend: Integrate OpenAI ChatKit (or compatible Cohere-compatible chat UI) in existing Next.js app – call backend /api/{user_id}/chat

Domain allowlist: Prepare for OpenAI ChatKit hosted mode (even if using Cohere backend) – document setup in README

Constraints:

Existing Phase II stack locked: FastAPI, SQLModel, Neon PostgreSQL, Better Auth + JWT

LLM switch: Use Cohere API exclusively (no OpenAI calls) – adapt OpenAI Agents SDK patterns to Cohere's chat/tool-calling API

No new external libraries beyond Cohere SDK (cohere-python) and Official MCP SDK

Environment variables: Add COHERE_API_KEY; reuse BETTER_AUTH_SECRET, NEON_DB_URL

Stateless server: No in-memory session – all state in DB

Public auth routes (signup/signin) remain unchanged; chat endpoint fully protected

No real-time (WebSockets) – single-turn stateless requests

No advanced features like multi-agent swarms, voice, or image generation (keep to text-based task management + profile)

Timeline: Integrate without disrupting Phase II task CRUD UI/API

Success criteria:

Chatbot fully manages tasks via natural language: add, list (with filters), complete, delete, update – with friendly confirmations

User profile queries work: "Mera email kya hai?" → returns id, email, name, createdAt

Conversation context preserved across requests via DB persistence – resumes after server restart

All operations secure: JWT required, user_id enforced, no cross-user access

Agent uses Cohere for reasoning/tool selection – successful tool calls visible in response (tool_calls array)

Endpoint returns correct response format: {conversation_id, response, tool_calls}

Full integration: Existing frontend can add ChatKit UI tab/page calling backend chat endpoint

Judges confirm: "Seamless Phase III upgrade – agentic, secure, scalable, Cohere-powered, fully spec-driven"

Zero regressions in Phase II functionality (task CRUD, auth)

Runs locally with docker-compose (frontend + backend + Neon)

Final deliverables:

Updated monorepo: New specs in /specs/agents/ and /specs/skills/ for chatbot, MCP tools, Cohere integration

Backend additions: /api/{user_id}/chat endpoint, Cohere agent runner, MCP tools implementation

DB schema extensions: Conversation and Message tables

Frontend: ChatKit integration in Next.js (new page/route) with JWT attachment

README updates: Setup Cohere API key, domain allowlist for ChatKit, full run instructions

Complete traceable history of spec-driven Claude Code prompts (@specs references) demonstrating agentic workflow

Working end-to-end: Natural language chat controls entire Todo app + user info

This constitution ensures a production-grade, Cohere-powered AI chatbot that perfectly extends the existing full-stack Todo app – secure, scalable, and impressively agentic. Every detail is covered for hackathon excellence.

## Response Summary

Updated the project constitution file at `.specify/memory/constitution.md` to reflect the requirements for Phase III - AI Todo Chatbot Integration. The new constitution maintains the core principles of spec-driven development while adding specific requirements for:

- Full agentic, spec-driven development with zero manual coding
- Seamless integration with existing Phase II backend
- Stateless architecture with database persistence
- Cohere API as primary LLM backend
- MCP tools standard interface
- Secure operations with user isolation
- Natural language processing and multilingual support

The version was incremented from 1.0.0 to 2.0.0 to reflect the major update from Phase II to Phase III requirements.

## Outcome

Successfully updated the constitution file to reflect Phase III requirements for AI Todo Chatbot Integration, maintaining all essential governance structures while incorporating new technical requirements for Cohere API integration, chatbot functionality, and enhanced security measures.