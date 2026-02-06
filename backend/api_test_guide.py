#!/usr/bin/env python3
"""
Simple API Test Script for Task Management Backend

Before running this script:
1. Make sure the backend server is running: uvicorn main:app --reload --port 8000
2. Have a valid JWT token from Better Auth
"""

import requests
import json
import os
from datetime import datetime

def test_api_endpoints():
    """
    Test all API endpoints with sample requests
    """
    print("Task Management API - Manual Testing Guide")
    print("="*50)

    print("\n1. Start the backend server first:")
    print("   cd backend")
    print("   uvicorn main:app --reload --port 8000")

    print("\n2. Once the server is running, you can test the endpoints using curl or a tool like Postman.")
    print("   Below are example curl commands:")

    print("\n--- HEALTH CHECK ---")
    print("# Check if the server is running")
    print("curl -X GET http://localhost:8000/health")

    print("\n--- TASK OPERATIONS (requires valid JWT token) ---")
    print("# Replace YOUR_VALID_JWT_TOKEN with an actual token from Better Auth")

    print("\n# Get all tasks for the authenticated user")
    print("curl -X GET http://localhost:8000/api/tasks \\")
    print("  -H \"Authorization: Bearer YOUR_VALID_JWT_TOKEN\" \\")
    print("  -H \"Content-Type: application/json\"")

    print("\n# Create a new task")
    print("curl -X POST http://localhost:8000/api/tasks \\")
    print("  -H \"Authorization: Bearer YOUR_VALID_JWT_TOKEN\" \\")
    print("  -H \"Content-Type: application/json\" \\")
    print("  -d '{")
    print("    \"title\": \"Test Task\",")
    print("    \"description\": \"This is a test task\",")
    print("    \"due_date\": \"2024-12-31T10:00:00Z\",")
    print("    \"priority\": \"medium\"")
    print("  }'")

    print("\n# Get a specific task (replace TASK_ID with actual task ID)")
    print("curl -X GET http://localhost:8000/api/tasks/TASK_ID \\")
    print("  -H \"Authorization: Bearer YOUR_VALID_JWT_TOKEN\" \\")
    print("  -H \"Content-Type: application/json\"")

    print("\n# Update a task (replace TASK_ID with actual task ID)")
    print("curl -X PUT http://localhost:8000/api/tasks/TASK_ID \\")
    print("  -H \"Authorization: Bearer YOUR_VALID_JWT_TOKEN\" \\")
    print("  -H \"Content-Type: application/json\" \\")
    print("  -d '{")
    print("    \"title\": \"Updated Task Title\",")
    print("    \"description\": \"Updated description\",")
    print("    \"is_completed\": true,")
    print("    \"due_date\": \"2024-12-31T10:00:00Z\",")
    print("    \"priority\": \"high\"")
    print("  }'")

    print("\n# Toggle task completion status (replace TASK_ID with actual task ID)")
    print("curl -X PATCH http://localhost:8000/api/tasks/TASK_ID/toggle-status \\")
    print("  -H \"Authorization: Bearer YOUR_VALID_JWT_TOKEN\" \\")
    print("  -H \"Content-Type: application/json\" \\")
    print("  -d '{\"completed\": true}'")

    print("\n# Delete a task (replace TASK_ID with actual task ID)")
    print("curl -X DELETE http://localhost:8000/api/tasks/TASK_ID \\")
    print("  -H \"Authorization: Bearer YOUR_VALID_JWT_TOKEN\" \\")
    print("  -H \"Content-Type: application/json\"")

    print("\n--- ERROR CONDITIONS TO TEST ---")
    print("# Test with invalid/missing JWT token (should return 401)")
    print("curl -X GET http://localhost:8000/api/tasks")

    print("\n# Test with valid token but non-existent task ID (should return 404)")
    print("curl -X GET http://localhost:8000/api/tasks/999999 \\")
    print("  -H \"Authorization: Bearer YOUR_VALID_JWT_TOKEN\" \\")
    print("  -H \"Content-Type: application/json\"")

    print("\n--- FILTERING AND SORTING EXAMPLES ---")
    print("# Get completed tasks only")
    print("curl -X GET \"http://localhost:8000/api/tasks?status_filter=completed\" \\")
    print("  -H \"Authorization: Bearer YOUR_VALID_JWT_TOKEN\" \\")
    print("  -H \"Content-Type: application/json\"")

    print("\n# Get high priority tasks, sorted by due date")
    print("curl -X GET \"http://localhost:8000/api/tasks?priority_filter=high&sort_by=due_date&order=asc\" \\")
    print("  -H \"Authorization: Bearer YOUR_VALID_JWT_TOKEN\" \\")
    print("  -H \"Content-Type: application/json\"")

    print("\n--- ADDITIONAL NOTES ---")
    print("- The API uses standardized response format:")
    print("  Success: {\"success\": true, \"data\": {...}, \"message\": \"...\"}")
    print("  Error: {\"success\": false, \"error\": {\"code\": \"...\", \"message\": \"...\"}}")
    print("- All endpoints require valid JWT authentication")
    print("- Users can only access their own tasks (403 for unauthorized access)")
    print("- Refer to the API documentation at http://localhost:8000/docs when running")

    print("\nFor automated testing, run: python test_api.py")
    print("For comprehensive testing: python test_api_comprehensive.py")

if __name__ == "__main__":
    test_api_endpoints()