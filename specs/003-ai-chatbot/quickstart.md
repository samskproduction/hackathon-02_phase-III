# Quickstart Guide: Phase III AI Chatbot Integration

## Prerequisites

- Python 3.11+ with pip
- Node.js 18+ with npm/yarn
- Cohere API key (available at https://dashboard.cohere.ai/api-keys)
- Existing Phase II application running (FastAPI backend + Next.js frontend)

## Setup Instructions

### 1. Environment Configuration

Add to your `.env` file:
```bash
# Cohere API configuration
COHERE_API_KEY=your_cohere_api_key_here

# Existing Phase II configurations (ensure these are set)
NEON_DB_URL=your_neon_db_url
BETTER_AUTH_SECRET=your_auth_secret
```

### 2. Backend Setup

#### Install Cohere Dependency
```bash
cd backend
pip install cohere-toolkit
```

#### Database Migration
Run migrations to create Conversation and Message tables:
```bash
# From backend directory
python -m alembic revision --autogenerate -m "Add Conversation and Message models for chatbot"
python -m alembic upgrade head
```

#### Verify Chat Endpoint
Test the chat endpoint:
```bash
curl -X POST http://localhost:8000/api/{your_user_id}/chat \
  -H "Authorization: Bearer {your_jwt_token}" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, add a test task!"}'
```

### 3. Frontend Setup

#### Install Chat Components
```bash
cd frontend
# No additional dependencies needed for basic chat functionality
# If using ChatKit, follow OpenAI's domain allowlist setup
```

#### Start Development Servers
```bash
# Terminal 1 - Start backend
cd backend
uvicorn src.main:app --reload

# Terminal 2 - Start frontend
cd frontend
npm run dev
```

## Initial Testing

### 1. Verify Chat Endpoint
```bash
# Get your user_id and JWT token from existing auth system
USER_ID="your_user_id_here"
JWT_TOKEN="your_jwt_token_here"

curl -X POST "http://localhost:8000/api/$USER_ID/chat" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi, create a task to buy groceries"}'
```

### 2. Test Natural Language Commands
Try these sample commands:
- `"Add task: Buy groceries"`
- `"Show my pending tasks"`
- `"Complete task 1"`
- `"What is my email address?"`
- `"Mera email kya hai?"`

### 3. Verify UI Integration
- Login to the frontend application
- Look for floating chatbot icon in bottom-right corner
- Click to open chat window
- Send a test message and verify response

## Troubleshooting

### Common Issues

1. **Cohere API Connection Error**:
   - Verify `COHERE_API_KEY` is set correctly
   - Check internet connectivity to Cohere services

2. **JWT Authentication Failure**:
   - Ensure using valid JWT from existing auth system
   - Verify user_id in URL matches JWT user_id

3. **Database Schema Issues**:
   - Run migrations if Conversation/Message tables missing
   - Verify foreign key relationships

4. **Chat UI Not Appearing**:
   - Confirm user is properly authenticated
   - Check browser console for JavaScript errors

### Sample Test Flow
1. Login to existing app
2. Open browser developer tools
3. Click floating chat icon
4. Send message: "Add task: Test chat integration"
5. Verify task appears in main task list
6. Check database: new Conversation and Message records exist

## Production Deployment Notes

### Environment Variables
Ensure these are set in production:
- `COHERE_API_KEY` (securely managed)
- Database connection strings
- Authentication secrets
- Domain allowlist for ChatKit (if used)

### Scaling Considerations
- Monitor Cohere API usage and costs
- Database indexes for conversation/message queries
- JWT validation performance

### Security Checklist
- All chat endpoints require valid JWT
- User isolation enforced at database level
- No PII exposed through chat responses
- Rate limiting considered for production