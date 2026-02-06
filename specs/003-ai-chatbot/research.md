# Research Summary: Phase III AI Chatbot Integration

## Decision Log

### 1. Cohere Model Selection
**Decision**: Use Cohere command-r-plus model
**Rationale**: Offers superior reasoning and tool-calling capabilities needed for accurate task management commands. Better suited for the complex intent recognition required in the chatbot.
**Alternatives considered**:
- command-r (faster but less capable for tool calling)
- Other models (not supported by Cohere's tool-calling API)

### 2. Chat UI Technology
**Decision**: Hybrid approach - try OpenAI ChatKit first with custom component as fallback
**Rationale**: OpenAI ChatKit provides polished UI out of the box but requires domain configuration. Custom component ensures complete control and no external dependencies.
**Alternatives considered**:
- Pure custom implementation (more work but full control)
- Third-party chat libraries (potentially introduces unwanted dependencies)

### 3. Tool Calling Implementation
**Decision**: Use Cohere's native tool calling
**Rationale**: More reliable and supports parallel tool execution as needed. Aligns with Cohere's best practices.
**Alternatives considered**:
- Force JSON mode (less reliable, doesn't support parallel execution)

### 4. Floating Icon Style
**Decision**: Modern circular FAB with subtle animation
**Rationale**: Familiar UX pattern inspired by popular messaging apps, space-efficient, and can indicate new messages.
**Alternatives considered**:
- Traditional chat bubble (can be visually intrusive)
- Menu item (less discoverable)

### 5. Message History Limit
**Decision**: Truncate to last 20 messages per conversation
**Rationale**: Balances context preservation with performance and cost considerations (token usage).
**Alternatives considered**:
- Unlimited history (could lead to token overflow and high costs)
- More aggressive truncation (might lose important context)

### 6. Tool Execution Order
**Decision**: Parallel execution when possible
**Rationale**: Cohere supports parallel tool execution which can improve response times for complex queries.
**Alternatives considered**:
- Sequential execution (simpler but slower for multiple tools)

### 7. Response Simulation
**Decision**: Simulate typing effect in frontend
**Rationale**: Provides better UX while keeping the backend implementation simpler (no real-time streaming initially).
**Alternatives considered**:
- Real-time streaming (more complex backend implementation)

### 8. Conversation Naming
**Decision**: Auto-generate from first message
**Rationale**: Reduces user friction while providing meaningful conversation titles.
**Alternatives considered**:
- Manual naming (increased user effort)
- Generic names (less informative)

## Technology Deep Dive

### Cohere Integration Patterns
- Use `cohere.Client` with proper API key handling
- Define tools in JSON Schema format compatible with Cohere
- Handle tool call responses and pass results back to Cohere for final response generation
- Implement proper error handling for Cohere API calls

### MCP Tools Implementation for Cohere
- Map standard MCP tool schemas to Cohere's tool definition format
- Ensure each tool function enforces user isolation via JWT-derived user_id
- Implement proper validation and error handling for all tool calls
- Handle edge cases like task not found, permission denied, etc.

### Database Schema Extensions
- Create Conversation model with user_id relationship, timestamps, and optional title
- Create Message model with conversation_id, role (user/assistant), content, and timestamps
- Implement proper indexing for performance
- Ensure foreign key relationships and proper cascade behaviors

### Frontend Integration Points
- Add chatbot icon component that appears conditionally when user is logged in
- Create chat window/modal component with proper message display
- Implement JWT token passing to chat API calls
- Add typing indicators and proper message loading states