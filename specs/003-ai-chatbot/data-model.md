# Data Model: Phase III AI Chatbot Integration

## Entity Models

### Conversation
**Description**: Represents a single chat conversation thread between user and AI assistant

**Fields**:
- `id` (UUID/string) - Primary identifier for the conversation
- `user_id` (UUID/string) - Foreign key linking to authenticated user
- `title` (string, nullable) - Auto-generated from first message or custom title
- `created_at` (datetime) - Timestamp when conversation started
- `updated_at` (datetime) - Timestamp of last message/activity
- `is_active` (boolean) - Whether conversation is currently active

**Relationships**:
- Belongs to User (via user_id)
- Has many Messages (via conversation_id)

**Validation**:
- user_id must exist in users table
- created_at defaults to current timestamp
- updated_at updates on any message activity

### Message
**Description**: Represents a single message within a conversation

**Fields**:
- `id` (UUID/string) - Primary identifier for the message
- `conversation_id` (UUID/string) - Foreign key linking to conversation
- `role` (string) - Message sender role ("user" or "assistant")
- `content` (text) - The actual message content
- `tool_calls` (JSON, nullable) - Tool calls triggered by this message (if assistant)
- `tool_call_results` (JSON, nullable) - Results of executed tool calls (if assistant)
- `timestamp` (datetime) - When the message was created
- `sequence_number` (int) - Order of message within conversation

**Relationships**:
- Belongs to Conversation (via conversation_id)

**Validation**:
- conversation_id must exist in conversations table
- role must be either "user" or "assistant"
- timestamp defaults to current time
- sequence_number auto-increments within conversation

### User (Existing - Extended Context)
**Description**: User account (existing from Phase II)

**Relevant Fields**:
- `id` (UUID/string) - User identifier
- `email` (string) - Email address
- `name` (string) - Display name
- `created_at` (datetime) - Account creation timestamp

## State Transitions

### Conversation States
- **Created**: When first message is sent to new conversation_id
- **Active**: When user is currently interacting (messages within last 30 mins)
- **Paused**: When conversation has no activity for >30 mins
- **Archived**: After extended inactivity (implementation-dependent)

### Message States
- **Pending**: When message is being processed by Cohere
- **Completed**: When response is received and saved to DB
- **Failed**: When there's an error in processing (with error details)

## Relationships & Constraints

### Referential Integrity
```
users.id → conversations.user_id (ON DELETE CASCADE)
conversations.id → messages.conversation_id (ON DELETE CASCADE)
```

### Access Control
- All queries must filter by user_id to ensure data isolation
- Conversation access limited to owning user
- Message access limited to owning conversation/user

### Indexing Strategy
- Index on conversations.user_id for user-specific queries
- Composite index on conversations.user_id + conversations.updated_at for history retrieval
- Index on messages.conversation_id for conversation-specific queries
- Index on messages.timestamp for chronological ordering

## API Contract Implications

### Request/Response Shapes
The data models directly influence the API contracts:

**POST /api/{user_id}/chat**
Request: `{message: string, conversation_id?: string}`
Response: `{conversation_id: string, response: string, tool_calls: []}`

### Data Validation Rules
- Prevent insertion of messages without valid conversation
- Validate user_id ownership during all operations
- Enforce maximum message length to prevent abuse
- Ensure proper role assignments ("user" for incoming, "assistant" for outgoing)