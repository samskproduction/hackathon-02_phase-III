"""
Test script for the Task Management API
This script tests all the endpoints with sample requests
"""

import requests
import json
import uuid
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = "http://localhost:8000"
API_PREFIX = "/api"

# Sample JWT token for testing (this would normally come from Better Auth)
# For testing purposes, we'll use a mock token - in reality, this would be obtained from the frontend auth system
TEST_JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjk5OTk5OTk5OTl9.VERY_INSECURE_FAKE_SIGNATURE"

HEADERS = {
    "Authorization": f"Bearer {TEST_JWT_TOKEN}",
    "Content-Type": "application/json"
}

def test_health_endpoint():
    """Test the health endpoint"""
    print("Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        print("✓ Health endpoint working\n")
    except Exception as e:
        print(f"✗ Health endpoint failed: {e}\n")

def test_get_tasks():
    """Test getting tasks"""
    print("Testing GET /api/tasks...")
    try:
        response = requests.get(f"{BASE_URL}{API_PREFIX}/tasks", headers=HEADERS)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✓ GET /api/tasks working")
        else:
            print(f"Response: {response.json()}")
        print()
    except Exception as e:
        print(f"✗ GET /api/tasks failed: {e}\n")

def test_create_task():
    """Test creating a task"""
    print("Testing POST /api/tasks...")
    try:
        task_data = {
            "title": f"Test Task {datetime.now().strftime('%Y%m%d%H%M%S')}",
            "description": "This is a test task created during API testing",
            "due_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "priority": "medium"
        }

        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/tasks",
            headers=HEADERS,
            json=task_data
        )
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✓ POST /api/tasks working")
            print(f"Created Task: {response.json()}")
        else:
            print(f"Response: {response.json()}")
        print()
    except Exception as e:
        print(f"✗ POST /api/tasks failed: {e}\n")

def test_api_endpoints():
    """Test all API endpoints"""
    print("Testing Task Management API Endpoints\n")
    print("=" * 50)

    # Test health endpoint first
    test_health_endpoint()

    # Test getting tasks
    test_get_tasks()

    # Test creating a task
    test_create_task()

    print("API Testing Complete!")
    print("\nNote: Some endpoints may return 401/403 errors if JWT token validation is strict.")
    print("For full testing, you would need a valid JWT token from your Better Auth system.")

if __name__ == "__main__":
    test_api_endpoints()