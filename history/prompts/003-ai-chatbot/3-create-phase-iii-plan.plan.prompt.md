---
id: 3
title: "Create Phase III Plan"
stage: plan
date_iso: 2026-02-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: 003-ai-chatbot
branch: main
user: user
command: "/sp.plan Implementation Plan for Phase III – AI Todo Chatbot (Cohere-Powered Integration)"
labels: ["plan", "ai-chatbot", "cohere", "implementation"]
links:
  spec: "../003-ai-chatbot/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/003-ai-chatbot/plan.md"
  - "specs/003-ai-chatbot/research.md"
  - "specs/003-ai-chatbot/data-model.md"
  - "specs/003-ai-chatbot/quickstart.md"
  - "specs/003-ai-chatbot/contracts/chatbot-api.yaml"
tests_yaml: []
---

# Implementation Plan Creation: Phase III AI Chatbot Integration

## Original Prompt

Implementation Plan for Phase III – AI Todo Chatbot (Cohere-Powered Integration)

Create:

Updated backend architecture diagram showing how Cohere + custom agent runner fits into existing FastAPI server

New database schema extensions (Conversation and Message models) with relationships to users

MCP-compatible tool definitions in Cohere format (JSON schema for tool calling)

Custom Cohere Runner class / function that mimics OpenAI Agents SDK behavior (chat → tool call detection → execution → final response)

Chat endpoint logic flow: auth → load history → call Cohere → execute tools → save messages → return response

Frontend chatbot UI integration plan: floating icon, modal/chat window, message streaming simulation, typing indicator

Environment variable & security checklist (COHERE_API_KEY, domain allowlist prep)

Error & fallback strategy document (tool failure, rate limit, invalid JWT)

Decisions needing documentation:

Cohere model choice: command-r-plus (better reasoning/tool use) vs command-r (faster, cheaper) → Choose command-r-plus for best tool-calling accuracy in hackathon demo

Tool calling implementation: Use Cohere native tool calling vs force JSON mode → Native tool calling (more reliable, supports parallel calls)

Chat UI technology: Hosted OpenAI ChatKit vs custom React + Tailwind component → Hybrid: Try hosted ChatKit first (configure domain allowlist), fallback to custom lightweight modal if setup fails

Floating icon style: Circular FAB vs chat bubble icon → Modern circular FAB with subtle pulse animation on new messages (inspired by WhatsApp/Telegram)

Message history limit: Unlimited vs truncate after N messages → Truncate to last 20 messages per conversation (prevents token blowup)

Tool execution order: Sequential vs parallel when multiple tools called → Parallel execution when possible (Cohere supports it)

Response streaming: Full response vs simulate typing → Simulate typing effect in frontend (no real streaming from Cohere in basic setup)

Conversation naming: Auto-generate from first message vs manual → Auto-generate short title from first user message

Testing strategy (validation against success criteria):

Natural language task commands: Test 10+ variations ("Add task buy milk", "Show all tasks", "Mark task 3 done", "Delete the first one", "Change task 2 to call mom")

Profile queries: "Mera email kya hai?", "Who am I logged in as?", "Mera naam batao" → correct data returned

Context preservation: Send 5 messages, restart backend, continue same conversation_id → history intact

Security: Try accessing chat without JWT → 401; try task operations for wrong user_id → 403 or no data

Tool calls visibility: Check response.tool_calls array shows correct tools invoked

UI integration: Floating icon appears only when logged in; chat window opens/closes smoothly; messages display correctly

Multilingual: Test Urdu commands ("Ek task add karo grocery khareedne ka") → understood and executed

Edge cases: Empty message, very long input, task not found, duplicate task title, rate limit simulation

End-to-end: Signup → login → open chat → manage tasks → see updates in main task list UI

Technical details:

Use spec-concurrent approach: Implement backend chatbot logic first, then frontend UI, iterate with @specs references

Cohere integration: cohere.Client with api_key from env, tools defined as list of dicts (name, description, parameters schema)

Custom runner: Function that takes history + new message → calls cohere.chat() → if tool_calls → execute via existing FastAPI route logic or direct DB calls → feed results back → final response

DB: Use SQLModel to define Conversation(user_id, id, title?, created_at) and Message(conversation_id, role, content, created_at)

Frontend: Add /components/ChatbotIcon.tsx, /components/ChatWindow.tsx; use existing api.ts to call /api/{user_id}/chat

JWT: Reuse get_current_user dependency → pass user_id to tools automatically

Organize by phases:

Foundation
→ Add COHERE_API_KEY to .env
→ Extend DB schema: Conversation + Message models
→ Create tools list in Cohere-compatible format (add_task, list_tasks, ..., get_user_profile)

Backend – Chat Endpoint & Agent Runner
→ Implement POST /api/{user_id}/chat (protected)
→ Build custom CohereRunner: load history, call Cohere, handle tool calls, save messages
→ Integrate existing task & user logic as tool executors

MCP Tools Implementation
→ Code each tool function (add_task → DB insert, list_tasks → query with filter, etc.)
→ Ensure every tool enforces user_id ownership

Frontend – Chatbot UI
→ Add floating chatbot icon (visible only logged-in)
→ Create chat modal/window with message list, input, send button
→ Implement message sending to backend + display responses
→ Add typing indicator + auto-scroll

Polish & Optimizations
→ Friendly response formatting (action confirmations, emojis)
→ Error handling in UI (connection lost, invalid response)
→ Dark mode consistency with main app
→ Performance: Limit history sent to Cohere (last 15–20 messages)

Final Integration & Review
→ Full end-to-end testing: chat controls tasks → main UI reflects changes
→ Verify no regressions in Phase II CRUD
→ Document domain allowlist setup for ChatKit (if used)
→ Judges-ready demo flow: login → chat → manage tasks conversationally

This plan ensures a clean, powerful, Cohere-powered AI chatbot that feels like a natural 2026 upgrade to your existing premium Todo app – fully integrated, secure, delightful, and spec-driven from start to finish.

## Response Summary

Created a comprehensive implementation plan for the Phase III AI Todo Chatbot Integration including:

- Technical context and architecture overview
- Research summary with key decisions made (Cohere model choice, UI technology, etc.)
- Data model specifications for Conversation and Message entities
- Quickstart guide for setting up the feature
- API contracts in OpenAPI format for the chatbot endpoints
- Proper file structure organization in the specs directory

The plan follows the spec-driven development approach and integrates the Cohere-powered chatbot into the existing Phase II application while maintaining all security and architectural requirements.

## Outcome

Successfully created the complete implementation plan for Phase III at specs/003-ai-chatbot/plan.md with accompanying research, data model, quickstart guide, and API contracts. The plan addresses all the requirements specified in the original prompt including Cohere integration, database schema extensions, tool definitions, and frontend integration planning.