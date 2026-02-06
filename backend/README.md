# Task Management API Backend

## Overview
This is a secure, robust FastAPI backend with SQLModel ORM for Neon Serverless PostgreSQL, implementing all RESTful API endpoints for task CRUD operations, JWT-based authentication verification integrated with Better Auth from the frontend, and full enforcement of user data isolation.

## Endpoints
- `GET /api/tasks` - Get all tasks for the authenticated user
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a specific task
- `DELETE /api/tasks/{id}` - Delete a specific task
- `PATCH /api/tasks/{id}/toggle-status` - Toggle task completion status
- `POST /api/{user_id}/chat` - Chat with AI assistant for task management
- `GET /api/conversations/{user_id}` - Get user's conversations
- `GET /api/conversations/{conversation_id}/messages` - Get messages in a conversation
- `GET /health` - Health check endpoint

## Authentication
All endpoints require a valid JWT token in the Authorization header:
`Authorization: Bearer <jwt-token>`

## Response Format
The API returns standardized responses:
- Success: `{ "success": true, "data": { ... }, "message": "..." }`
- Error: `{ "success": false, "error": { "code": "...", "message": "..." } }`

## Environment Variables
- `NEON_DB_URL` - PostgreSQL connection string for Neon Serverless
- `BETTER_AUTH_SECRET` - Secret key for JWT verification
- `FRONTEND_URL` - URL of the frontend application for CORS
- `COHERE_API_KEY` - API key for Cohere AI integration