# Tasks: Phase III – AI Todo Chatbot (Cohere-Powered Integration)

## Feature Overview
Integrating a Cohere-powered AI chatbot into the existing Todo application that enables natural language task management and profile queries. The solution includes a custom Cohere agent runner, MCP-compatible tools, floating chat UI, and persistent conversation storage, all while maintaining existing Phase II functionality.

## Phase 1: Setup and Environment Configuration

- [X] T001 Add COHERE_API_KEY to backend/.env and backend/.env.example
- [X] T002 Install Cohere Python SDK dependency in requirements.txt
- [X] T003 Create backend/models/conversation.py with SQLModel
- [X] T004 Create backend/models/message.py with SQLModel
- [ ] T005 Update database migration files to include new Conversation and Message tables
- [X] T006 Create frontend/components/ChatbotIcon.tsx component skeleton
- [X] T007 Create frontend/components/ChatWindow.tsx component skeleton

## Phase 2: Foundational Components

- [X] T008 Implement Conversation model with all required fields in backend/models/conversation.py
- [X] T009 Implement Message model with all required fields in backend/models/message.py
- [X] T010 Create database initialization for Conversation and Message tables in backend/db_init.py
- [X] T011 Set up Cohere client in backend/services/cohere_client.py
- [X] T012 Create backend/services/mcp_tools.py with full implementation
- [X] T013 Create backend/services/cohere_runner.py with full implementation
- [X] T014 Create backend/api/chat.py with full implementation
- [X] T015 Add JWT auth dependency import to chat endpoint
- [X] T016 Use existing task model and database functions for tool usage in backend/services/mcp_tools.py

## Phase 3: [US1] User Accesses Chat Interface

**Goal**: Enable authenticated users to access the chat interface through a floating icon

**Independent Test Criteria**:
- When an authenticated user visits the app, they should see a floating chat icon
- When clicking the icon, a chat window should appear
- When clicking outside the window, it should close

**Tasks**:
- [X] T017 [P] [US1] Implement ChatbotIcon component with conditional rendering (show only when logged in) in frontend/components/ChatbotIcon.tsx
- [X] T018 [P] [US1] Add CSS animations for floating chat icon in frontend/components/ChatbotIcon.tsx
- [X] T019 [P] [US1] Implement ChatWindow component with open/close functionality in frontend/components/ChatWindow.tsx
- [X] T020 [US1] Integrate ChatbotIcon into main dashboard layout in frontend/app/dashboard/page.tsx
- [X] T021 [US1] Add proper positioning (bottom-right) for chat icon in frontend/components/ChatbotIcon.tsx
- [X] T022 [US1] Implement dark/light mode support for chat components in frontend/components/ChatWindow.tsx
- [X] T023 [US1] Add responsive design to chat window for mobile/desktop in frontend/components/ChatWindow.tsx

## Phase 4: [US2] Natural Language Task Management

**Goal**: Enable users to create, list, update, and delete tasks using natural language commands

**Independent Test Criteria**:
- When user types "Add task: Buy groceries", chatbot should create the task and confirm
- When user types "Show pending tasks", chatbot should list pending tasks
- When user types "Complete task 1", chatbot should mark task as completed
- When user types "Delete task 1", chatbot should remove the task

**Tasks**:
- [X] T024 [P] [US2] Implement add_task MCP tool function in backend/services/mcp_tools.py
- [X] T025 [P] [US2] Implement list_tasks MCP tool function in backend/services/mcp_tools.py
- [X] T026 [P] [US2] Implement complete_task MCP tool function in backend/services/mcp_tools.py
- [X] T027 [P] [US2] Implement delete_task MCP tool function in backend/services/mcp_tools.py
- [X] T028 [P] [US2] Implement update_task MCP tool function in backend/services/mcp_tools.py
- [X] T029 [US2] Add proper user_id validation to all tool functions in backend/services/mcp_tools.py
- [X] T030 [US2] Create Cohere-compatible tool schemas for all task operations in backend/services/mcp_tools.py
- [X] T031 [US2] Integrate Cohere runner with task tools in backend/services/cohere_runner.py
- [X] T032 [US2] Test tool calling with sample natural language inputs in backend/services/cohere_runner.py

## Phase 5: [US3] Profile Information Queries

**Goal**: Enable users to retrieve their profile information through natural language queries

**Independent Test Criteria**:
- When user types "Mera email kya hai?" or "Who am I?", chatbot should return user profile information
- Response should include id, email, name, and createdAt timestamp

**Tasks**:
- [X] T033 [P] [US3] Implement get_user_profile MCP tool function in backend/services/mcp_tools.py
- [X] T034 [P] [US3] Add get_user_profile to Cohere-compatible tools schema in backend/services/mcp_tools.py
- [X] T035 [US3] Integrate get_user_profile tool with Cohere runner in backend/services/cohere_runner.py
- [X] T036 [US3] Test profile query responses with sample natural language inputs in backend/services/cohere_runner.py

## Phase 6: [US4] Conversational Task Management with Persistence

**Goal**: Enable persistent conversations with message history stored in database

**Independent Test Criteria**:
- When user sends a message to a conversation, it should be stored in database
- When user returns to a conversation, previous messages should be loaded
- When backend restarts, conversation history should still be available

**Tasks**:
- [X] T037 [P] [US4] Implement conversation history loading in backend/services/cohere_runner.py
- [X] T038 [P] [US4] Implement message saving after Cohere processing in backend/services/cohere_runner.py
- [X] T039 [P] [US4] Add message retrieval to chat endpoint in backend/api/chat.py
- [X] T040 [US4] Implement conversation creation logic in backend/api/chat.py
- [X] T041 [US4] Add proper message sequencing in database operations in backend/services/cohere_runner.py
- [X] T042 [US4] Add conversation updating on message activity in backend/services/cohere_runner.py

## Phase 7: [US4] Backend API Endpoint Implementation

**Goal**: Complete the POST /api/{user_id}/chat endpoint with full functionality

**Independent Test Criteria**:
- When user sends a message to /api/{user_id}/chat, it should return conversation_id, response, and tool_calls
- When invalid JWT is provided, endpoint should return 401
- When user tries to access another user's conversations, endpoint should return 403

**Tasks**:
- [X] T043 [P] [US4] Complete POST /api/{user_id}/chat endpoint implementation in backend/api/chat.py
- [X] T044 [P] [US4] Add JWT authentication validation to chat endpoint in backend/api/chat.py
- [X] T045 [P] [US4] Add user_id extraction from JWT and validation in backend/api/chat.py
- [X] T046 [US4] Add proper error handling for authentication failures in backend/api/chat.py
- [X] T047 [US4] Add validation for conversation ownership in backend/api/chat.py
- [X] T048 [US4] Add response formatting with conversation_id, response, and tool_calls in backend/api/chat.py

## Phase 8: [US4] Frontend Chat Integration

**Goal**: Connect frontend chat interface to backend API

**Independent Test Criteria**:
- When user sends a message in chat window, it should reach backend API
- When backend responds, message should appear in chat window
- When user is not authenticated, chat functionality should be disabled

**Tasks**:
- [X] T049 [P] [US4] Add chat API call function to frontend/lib/api.ts
- [X] T050 [P] [US4] Add message sending functionality to ChatWindow component in frontend/components/ChatWindow.tsx
- [X] T051 [P] [US4] Add message display functionality in ChatWindow component in frontend/components/ChatWindow.tsx
- [X] T052 [US4] Add JWT token passing to chat API calls in frontend/components/ChatWindow.tsx
- [X] T053 [US4] Add typing indicator during message processing in frontend/components/ChatWindow.tsx
- [X] T054 [US4] Add auto-scroll to latest message in ChatWindow component in frontend/components/ChatWindow.tsx
- [ ] T055 [US4] Add message history loading from backend when opening chat in frontend/components/ChatWindow.tsx

## Phase 9: Security and Validation

**Goal**: Ensure all security requirements are met with proper validation

**Independent Test Criteria**:
- When unauthorized user accesses chat endpoint, they receive 401
- When user tries to access others' conversations, they receive 403
- When user sends malformed requests, appropriate error responses are returned

**Tasks**:
- [ ] T056 Add comprehensive input validation to chat endpoint in backend/src/api/chat.py
- [ ] T057 Add rate limiting to chat endpoint if needed in backend/src/api/chat.py
- [ ] T058 Add comprehensive user_id validation in all database queries in backend/src/services/mcp_tools.py
- [ ] T059 Add proper error handling for edge cases in backend/src/services/cohere_runner.py
- [ ] T060 Add validation for message content length to prevent abuse in backend/src/api/chat.py

## Phase 10: Polish and Cross-Cutting Concerns

**Goal**: Complete the feature with polish and performance optimizations

**Tasks**:
- [ ] T061 Add friendly, contextual, multilingual response formatting in backend/src/services/cohere_runner.py
- [ ] T062 Add conversation title auto-generation from first message in backend/src/services/cohere_runner.py
- [ ] T063 Optimize database queries for conversation history retrieval in backend/src/services/cohere_runner.py
- [ ] T064 Add message history truncation (last 20 messages) in backend/src/services/cohere_runner.py
- [ ] T065 Add proper error messages for tool failures in backend/src/services/cohere_runner.py
- [ ] T066 Add graceful degradation when Cohere API is unavailable in backend/src/services/cohere_runner.py
- [ ] T067 Update frontend chat UI for better user experience in frontend/src/components/ChatWindow.tsx
- [ ] T068 Add proper loading states and error handling in frontend/src/components/ChatWindow.tsx
- [ ] T069 Add accessibility features to chat components in frontend/src/components/ChatWindow.tsx
- [X] T070 Update README with Cohere API setup instructions and new environment variables

## Dependencies

**User Story Completion Order**:
- US1 (Chat Interface) must be completed before US4 (Backend Integration)
- US2 (Task Management) and US3 (Profile Queries) can be developed in parallel after foundational components
- US4 (Persistence & API) encompasses US2 and US3 functionality

**Parallel Execution Opportunities**:
- T024-T028: All MCP tool implementations can run in parallel
- T049-T051: Frontend API and UI functionality can develop in parallel
- T017-T019: Chat interface components can be built simultaneously

## Implementation Strategy

**MVP Scope**: Implement US1 (chat interface) and US2 (basic task management) to create a working prototype that allows users to access the chat interface and perform basic task operations through natural language.

**Incremental Delivery**:
1. Foundation + US1: Chat interface available
2. + US2: Task management through chat
3. + US3: Profile queries through chat
4. + US4: Persistent conversations with history
5. + Polish: Optimized and polished experience