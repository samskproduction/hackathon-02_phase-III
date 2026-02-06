# API Contract: Backend API for Todo Application

## Overview
This document defines the REST API contract for the Todo application backend. The frontend will interact with these endpoints to manage user tasks while maintaining proper authentication and data isolation.

## Base URL
`http://localhost:8000/api/v1` (development)
`https://your-domain.com/api/v1` (production)

## Authentication
All endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt-token>
```

The backend verifies the token using the shared BETTER_AUTH_SECRET and extracts the user_id to enforce data isolation.

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
    "message": "Human readable error message"
  }
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
- `status`: "all", "pending", "completed" (default: "all")
- `sort`: "created", "title", "due_date" (default: "created")

**Response (200)**:
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "id": 1,
        "user_id": "user-uuid",
        "title": "Sample Task",
        "description": "Task description",
        "is_completed": false,
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z",
        "due_date": "2023-01-15T00:00:00Z",
        "priority": "medium"
      }
    ]
  },
  "message": "Tasks retrieved successfully"
}
```

### POST /tasks
Create a new task for the authenticated user

**Headers**:
```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "New Task",
  "description": "Task description",
  "due_date": "2023-01-15T00:00:00Z",
  "priority": "medium"
}
```

**Response (201)**:
```json
{
  "success": true,
  "data": {
    "task": {
      "id": 1,
      "user_id": "user-uuid",
      "title": "New Task",
      "description": "Task description",
      "is_completed": false,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z",
      "due_date": "2023-01-15T00:00:00Z",
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
      "id": 1,
      "user_id": "user-uuid",
      "title": "Sample Task",
      "description": "Task description",
      "is_completed": false,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z",
      "due_date": "2023-01-15T00:00:00Z",
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
Content-Type: application/json
```

**Path Parameters**:
- `id`: Task ID

**Request Body**:
```json
{
  "title": "Updated Task Title",
  "description": "Updated description",
  "is_completed": true,
  "due_date": "2023-01-20T00:00:00Z",
  "priority": "high"
}
```

**Response (200)**:
```json
{
  "success": true,
  "data": {
    "task": {
      "id": 1,
      "user_id": "user-uuid",
      "title": "Updated Task Title",
      "description": "Updated description",
      "is_completed": true,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-02T00:00:00Z",
      "due_date": "2023-01-20T00:00:00Z",
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

### PATCH /tasks/{id}/complete
Toggle the completion status of a specific task

**Headers**:
```
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

**Path Parameters**:
- `id`: Task ID

**Request Body**:
```json
{
  "completed": true
}
```

**Response (200)**:
```json
{
  "success": true,
  "data": {
    "task": {
      "id": 1,
      "user_id": "user-uuid",
      "title": "Sample Task",
      "description": "Task description",
      "is_completed": true,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-02T00:00:00Z",
      "due_date": "2023-01-15T00:00:00Z",
      "priority": "medium"
    }
  },
  "message": "Task completion status updated"
}
```

## Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| AUTH_001 | Invalid or expired token | 401 |
| AUTH_002 | Missing authorization header | 401 |
| AUTH_003 | Token malformed | 401 |
| TASK_001 | Task not found | 404 |
| TASK_002 | User not authorized to access task | 403 |
| TASK_003 | Missing required fields | 400 |
| TASK_004 | Validation error | 400 |
| GENERAL_001 | Internal server error | 500 |
| GENERAL_002 | Database connection error | 500 |

## Security Requirements

1. All endpoints require valid JWT authentication
2. Users can only access their own tasks (filtered by user_id from JWT)
3. Proper validation of all input parameters
4. SQL injection protection via SQLModel/SQLAlchemy ORM
5. Proper error handling without sensitive information exposure

## Performance Requirements

1. All endpoints should respond within 500ms under normal load
2. Database queries should utilize indexes on user_id and completed fields
3. Connection pooling for efficient resource usage
4. Proper handling of concurrent requests