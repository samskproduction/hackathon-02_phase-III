---
id: "001"
title: "Fix Chat Endpoint Error"
stage: "general"
date_iso: "2026-02-06"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "none"
branch: "main"
user: "alish"
command: "restart backend"
labels: ["backend", "bug-fix", "database", "context-manager"]
spec: "null"
ticket: "null"
adr: "null"
pr: "null"
---

# Fix Chat Endpoint Error

## User Input
User reported that the chatbot was showing a "Request failed" error when saying "hello", even though both frontend and backend were running.

## Issue Identified
- Backend was running but chat endpoint was returning error: `'generator' object does not support the context manager protocol`
- Error occurred in `services/cohere_runner.py` when using `with get_session() as session:`
- The `get_session()` function was implemented as a generator but used as a context manager

## Solution Applied
Modified all instances in `services/cohere_runner.py` where `get_session()` was used with the `with` statement to properly handle the generator function by manually advancing the generator.

## Files Modified
- `backend/services/cohere_runner.py` - Fixed 5 instances of improper session handling

## Verification
- Backend restarted successfully
- Chat endpoint tested with: `curl -X POST http://localhost:8000/api/{user_id}/chat`
- Response returned successfully without the generator error

## Outcome
- Chatbot functionality restored
- No more "Request failed" errors when communicating with the chatbot
- Backend properly handles database sessions in the Cohere integration

## Test Results
```
curl -X POST http://localhost:8000/api/f07171d4-c13a-43cf-82e8-8846a4a51d04/chat \
-H "Authorization: Bearer <token>" \
-H "Content-Type: application/json" \
-d '{"message":"hello"}'

Response: {"conversation_id":"55c046eb-8240-481a-a3b5-66c80a28640e","response":"Hello! I'm your AI assistant...","tool_calls":[]}
```