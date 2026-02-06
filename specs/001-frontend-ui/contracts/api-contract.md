# API Contract: Frontend-Backend Interface for Todo Application

## Overview
This document defines the API contract between the frontend UI and backend services for the Todo application. The frontend will interact with backend endpoints to manage user authentication and task operations.

## Base URL
`http://localhost:8000/api/v1` (development)
`https://your-domain.com/api/v1` (production)

## Authentication
All protected endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt-token>
```

## Common Response Format
Successful responses follow this format:
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation successful"
}
```

Error responses follow this format:
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": { ... }
  }
}
```

## Authentication Endpoints

### POST /auth/login
Authenticate user and return JWT token

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200)**:
```json
{
  "success": true,
  "data": {
    "token": "jwt-token-string",
    "user": {
      "id": "user-id",
      "email": "user@example.com",
      "name": "John Doe"
    }
  },
  "message": "Login successful"
}
```

### POST /auth/signup
Register a new user

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Response (201)**:
```json
{
  "success": true,
  "data": {
    "token": "jwt-token-string",
    "user": {
      "id": "user-id",
      "email": "user@example.com",
      "name": "John Doe"
    }
  },
  "message": "Account created successfully"
}
```

### POST /auth/logout
Logout user and invalidate token

**Headers**:
```
Authorization: Bearer <jwt-token>
```

**Response (200)**:
```json
{
  "success": true,
  "message": "Logout successful"
}
```

## Task Management Endpoints

### GET /tasks
Retrieve all tasks for the authenticated user

**Headers**:
```
Authorization: Bearer <jwt-token>
```

**Query Parameters**:
- `status`: "all", "active", "completed" (default: "all")
- `limit`: number (default: 50, max: 100)
- `offset`: number (default: 0)

**Response (200)**:
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": "task-id-1",
        "userId": "user-id",
        "title": "Sample Task",
        "description": "Task description",
        "isCompleted": false,
        "createdAt": "2023-01-01T00:00:00Z",
        "updatedAt": "2023-01-01T00:00:00Z",
        "dueDate": "2023-01-15T00:00:00Z",
        "priority": "medium"
      }
    ],
    "total": 1,
    "limit": 50,
    "offset": 0
  },
  "message": "Tasks retrieved successfully"
}
```

### POST /tasks
Create a new task for the authenticated user

**Headers**:
```
Authorization: Bearer <jwt-token>
```

**Request Body**:
```json
{
  "title": "New Task",
  "description": "Task description",
  "dueDate": "2023-01-15T00:00:00Z",
  "priority": "medium"
}
```

**Response (201)**:
```json
{
  "success": true,
  "data": {
    "task": {
      "id": "new-task-id",
      "userId": "user-id",
      "title": "New Task",
      "description": "Task description",
      "isCompleted": false,
      "createdAt": "2023-01-01T00:00:00Z",
      "updatedAt": "2023-01-01T00:00:00Z",
      "dueDate": "2023-01-15T00:00:00Z",
      "priority": "medium"
    }
  },
  "message": "Task created successfully"
}
```

### GET /tasks/{id}
Retrieve a specific task for the authenticated user

**Headers**:
```
Authorization: Bearer <jwt-token>
```

**Path Parameters**:
- `id`: Task ID

**Response (200)**:
```json
{
  "success": true,
  "data": {
    "task": {
      "id": "task-id",
      "userId": "user-id",
      "title": "Sample Task",
      "description": "Task description",
      "isCompleted": false,
      "createdAt": "2023-01-01T00:00:00Z",
      "updatedAt": "2023-01-01T00:00:00Z",
      "dueDate": "2023-01-15T00:00:00Z",
      "priority": "medium"
    }
  },
  "message": "Task retrieved successfully"
}
```

### PUT /tasks/{id}
Update a specific task for the authenticated user

**Headers**:
```
Authorization: Bearer <jwt-token>
```

**Path Parameters**:
- `id`: Task ID

**Request Body**:
```json
{
  "title": "Updated Task Title",
  "description": "Updated description",
  "isCompleted": true,
  "dueDate": "2023-01-20T00:00:00Z",
  "priority": "high"
}
```

**Response (200)**:
```json
{
  "success": true,
  "data": {
    "task": {
      "id": "task-id",
      "userId": "user-id",
      "title": "Updated Task Title",
      "description": "Updated description",
      "isCompleted": true,
      "createdAt": "2023-01-01T00:00:00Z",
      "updatedAt": "2023-01-02T00:00:00Z",
      "dueDate": "2023-01-20T00:00:00Z",
      "priority": "high"
    }
  },
  "message": "Task updated successfully"
}
```

### DELETE /tasks/{id}
Delete a specific task for the authenticated user

**Headers**:
```
Authorization: Bearer <jwt-token>
```

**Path Parameters**:
- `id`: Task ID

**Response (200)**:
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

### PATCH /tasks/{id}/toggle-completion
Toggle the completion status of a specific task

**Headers**:
```
Authorization: Bearer <jwt-token>
```

**Path Parameters**:
- `id`: Task ID

**Response (200)**:
```json
{
  "success": true,
  "data": {
    "task": {
      "id": "task-id",
      "userId": "user-id",
      "title": "Sample Task",
      "description": "Task description",
      "isCompleted": true,
      "createdAt": "2023-01-01T00:00:00Z",
      "updatedAt": "2023-01-02T00:00:00Z",
      "dueDate": "2023-01-15T00:00:00Z",
      "priority": "medium"
    }
  },
  "message": "Task completion status updated"
}
```

## Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| AUTH_001 | Invalid credentials | 401 |
| AUTH_002 | Account not found | 404 |
| AUTH_003 | Token expired | 401 |
| AUTH_004 | Invalid token | 401 |
| TASK_001 | Task not found | 404 |
| TASK_002 | User not authorized to access task | 403 |
| TASK_003 | Missing required fields | 400 |
| TASK_004 | Validation error | 400 |
| GENERAL_001 | Internal server error | 500 |
| GENERAL_002 | Rate limit exceeded | 429 |

## Rate Limiting
API requests are rate-limited to 100 requests per minute per IP address.

## CORS Policy
API supports CORS for all origins during development. In production, only the frontend domain will be whitelisted.

## Versioning
This contract represents API version 1. Future breaking changes will be introduced with a new version number (e.g., `/api/v2`).