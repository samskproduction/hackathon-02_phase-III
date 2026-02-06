# Phase III – AI Todo Chatbot Specification (Cohere-Powered, Integrated into Existing Full-Stack Todo App)

## Overview
Build and integrate a powerful, natural-language Todo AI Chatbot into the existing Next.js + FastAPI full-stack application using Cohere as the LLM backend (instead of OpenAI). Adapt OpenAI Agents SDK patterns to work with Cohere's tool-calling and chat completions API. Add a floating chatbot icon in the UI that opens a modern chat interface (using OpenAI ChatKit or custom lightweight chat component). The chatbot must fully control task CRUD operations + provide user profile information via natural language.

## User Scenarios & Testing

### Primary User Flows

1. **Authenticated User Accesses Chatbot**
   - User logs in to existing Phase II application
   - User sees floating chatbot icon in bottom-right corner
   - User clicks icon to open modern chat interface
   - User can close chat window and continue with existing UI

2. **Natural Language Task Management**
   - User types natural language command: "Add task: Buy groceries"
   - Chatbot processes request and responds: "Task 'Buy groceries' add kar diya gaya!"
   - User can see task appears in main task list
   - User can perform other operations: list, complete, update, delete

3. **Profile Information Queries**
   - User types: "Mera email kya hai?" or "Who am I?"
   - Chatbot responds with user profile: "Aap ka email hai user@example.com"

4. **Conversational Task Management**
   - User engages in back-and-forth conversation to manage tasks
   - Chat history persists across sessions in database
   - User receives contextual, multilingual responses

### Acceptance Scenarios

- Given an authenticated user, when they interact with the chatbot, then their tasks can be managed through natural language
- Given a user asks for profile information, when using English or Urdu, then correct information is returned
- Given a user closes the chat window, when they reopen it later, then their conversation history is preserved
- Given a user performs any task operation, when completed, then system confirms with friendly multilingual message

### Edge Cases

- Unauthenticated users cannot access chat functionality
- Invalid commands receive helpful error responses
- Network issues result in appropriate user notifications
- Large conversation histories are handled efficiently

## Functional Requirements

### 1. Chat Interface Requirements
- Floating chatbot icon appears in bottom-right corner only when user is logged in
- Clicking icon opens clean, modern chat window with message history and typing indicators
- Smooth scrolling to latest messages with auto-scroll enabled
- Dark/light mode support matching existing UI aesthetic
- Responsive design that works on mobile and desktop

### 2. Natural Language Processing Requirements
- Chatbot understands and executes natural language commands for all task operations:
  - Add tasks: "Add task buy milk", "Create new task: Pay bills"
  - List tasks: "Show pending tasks", "Mere saare tasks batao"
  - Complete tasks: "Mark task 4 complete", "Complete shopping task"
  - Delete tasks: "Delete the old one", "Remove task with id 3"
  - Update tasks: "Change task name to groceries", "Update priority"
- Responds to user profile queries: "Mera email kya hai?", "Who am I?", "Mera naam batao"
- Returns appropriate information: user id, email, name, createdAt timestamp

### 3. Backend API Requirements
- POST /api/{user_id}/chat endpoint handles every request independently (stateless)
- All requests require valid JWT authentication
- Every operation enforces user ownership via user_id from JWT
- Response format: {conversation_id, response, tool_calls}
- Chat history fetched from database on each request to maintain context

### 4. LLM Integration Requirements
- Uses Cohere API (command-r-plus or command-r model) with tool calling enabled
- Adapts OpenAI Agents SDK structure to Cohere (custom runner using cohere.Client)
- All MCP tools implemented: add_task, list_tasks, complete_task, delete_task, update_task, get_user_profile
- Tool calling functionality correctly processes and executes user intents

### 5. Data Persistence Requirements
- Conversation state persisted only in database with Conversation and Message tables
- All user messages and assistant responses stored in database
- Conversation context preserved across server restarts
- No in-memory state maintained on server

### 6. Security Requirements
- All chat operations protected by JWT authentication
- Strict task/user isolation with no data leakage between users
- Every database query filtered by authenticated user_id
- MCP tools require authenticated user_id and enforce ownership

### 7. Integration Requirements
- Maintains 100% functionality of existing Phase II task CRUD UI/API
- Chatbot functionality integrated seamlessly without breaking existing features
- Existing authentication flows remain unchanged
- New functionality accessible without affecting current user experience

## Non-Functional Requirements

### Performance
- Chat responses delivered within 3 seconds under normal load
- Chat interface remains responsive during processing
- Database queries optimized for conversation history retrieval
- Efficient handling of large conversation histories

### Scalability
- Stateless backend architecture supporting horizontal scaling
- Database design supports high volume of conversations
- Cohere API integration handles concurrent users appropriately

### Usability
- Friendly, contextual, multilingual responses with action confirmations
- Clear visual indication of typing status and message delivery
- Intuitive interface matching existing app aesthetic
- Accessible design following WCAG guidelines

### Reliability
- System remains operational during Cohere API downtime with graceful degradation
- Proper error handling and user notifications for failures
- Robust connection handling between frontend and backend

## Success Criteria

### Quantitative Metrics
- 95% of natural language commands successfully processed and executed
- 100% of user profile queries return correct information
- Under 3-second response time for 90% of chat interactions
- 99% uptime for chat functionality during business hours

### Qualitative Measures
- Users report high satisfaction with conversational task management
- Natural language interactions feel intuitive and helpful
- Chatbot responses are contextually appropriate and multilingual
- Integration feels seamless with existing application flow

### Business Outcomes
- Users can manage all tasks through natural language conversation
- Profile information accessible via chat in English and Urdu
- Judges confirm: "Impressive Cohere-powered agentic chatbot – seamless, secure, delightful UX upgrade"
- Zero regressions in Phase II functionality (task CRUD, auth)
- Application runs smoothly with docker-compose deployment

## Key Entities

### Conversation
- Unique identifier for each conversation thread
- Associated with authenticated user
- Timestamps for creation and last activity
- Metadata for conversation context

### Message
- Individual chat message within conversation
- Sender identification (user or assistant)
- Content of the message
- Timestamp and associated conversation_id

### Task Operations
- Commands mapped to existing task CRUD operations
- Validation of user permissions and ownership
- Transformation of natural language to structured operations

## Constraints & Limitations

### Technical Constraints
- Must integrate into existing Phase II monorepo structure
- LLM: Cohere only, using COHERE_API_KEY environment variable
- Authentication: Reuse existing Better Auth + JWT middleware
- Statelessness: No in-memory session state, everything in Neon DB
- Frontend: Prefer OpenAI ChatKit or lightweight custom component

### Scope Limitations
- Text-only chat (no voice, images, file uploads)
- No advanced memory beyond DB-persisted messages
- Single main agent with tools (no multi-agent swarms)
- No real-time streaming (single response per request)

### Dependencies
- Cohere API availability and rate limits
- Existing Phase II backend infrastructure
- Better Auth for authentication
- Neon PostgreSQL for data persistence

## Assumptions

- Cohere API will maintain stable tool-calling functionality
- Existing Phase II authentication and database schemas remain unchanged
- Users have JavaScript-enabled browsers for chat interface
- Network connectivity supports API calls to Cohere services
- Existing task management business logic remains consistent
- Users are familiar with basic chat interfaces
- Phase II frontend is built with modern JavaScript framework supporting dynamic UI components