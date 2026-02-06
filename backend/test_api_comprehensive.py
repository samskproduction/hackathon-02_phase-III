"""
API Testing Script for Task Management Backend

This script demonstrates how to test the API endpoints.
Note: This requires the backend server to be running first.
"""

import subprocess
import time
import signal
import sys
import os
import threading

def start_server():
    """Start the backend server in a separate thread"""
    print("Starting backend server...")
    try:
        # Start the server using uvicorn
        server_process = subprocess.Popen([
            "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"
        ], cwd="./backend", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return server_process
    except FileNotFoundError:
        print("Error: uvicorn not found. Please install it with 'pip install uvicorn[standard]'")
        return None

def run_tests():
    """Run the API tests after giving the server time to start"""
    time.sleep(3)  # Give the server time to start

    # Import requests only after ensuring the server might be running
    try:
        import requests
    except ImportError:
        print("Error: requests library not installed. Please install it with 'pip install requests'")
        return

    BASE_URL = "http://127.0.0.1:8000"
    API_PREFIX = "/api"

    # Sample JWT token for testing
    TEST_JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjk5OTk5OTk5OTl9.VERY_INSECURE_FAKE_SIGNATURE"

    HEADERS = {
        "Authorization": f"Bearer {TEST_JWT_TOKEN}",
        "Content-Type": "application/json"
    }

    print("\n" + "="*60)
    print("TESTING API ENDPOINTS")
    print("="*60)

    # Test 1: Health check
    print("\n1. Testing Health Endpoint:")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
            print("   ✓ Health endpoint working")
        else:
            print(f"   Response: {response.text}")
            print("   ⚠ Health endpoint returned non-200 status")
    except Exception as e:
        print(f"   ✗ Health endpoint failed: {e}")

    # Test 2: Get tasks
    print("\n2. Testing GET /api/tasks:")
    try:
        response = requests.get(f"{BASE_URL}{API_PREFIX}/tasks", headers=HEADERS)
        print(f"   Status Code: {response.status_code}")
        if response.status_code in [200, 401, 403]:  # Expected responses
            if response.status_code == 200:
                print(f"   Response: {response.json()}")
                print("   ✓ GET /api/tasks responded correctly")
            elif response.status_code == 401:
                print("   Response: 401 Unauthorized (expected if JWT validation is strict)")
                print("   ✓ GET /api/tasks returned proper auth error")
            elif response.status_code == 403:
                print("   Response: 403 Forbidden (expected if token is valid but user has no access)")
                print("   ✓ GET /api/tasks returned proper auth error")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ✗ GET /api/tasks failed: {e}")

    # Test 3: Create a task
    print("\n3. Testing POST /api/tasks:")
    try:
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "due_date": "2024-12-31T10:00:00Z",
            "priority": "medium"
        }

        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/tasks",
            headers=HEADERS,
            json=task_data
        )
        print(f"   Status Code: {response.status_code}")
        if response.status_code in [200, 401, 403, 422]:  # Expected responses
            if response.status_code == 200:
                print(f"   Response: {response.json()}")
                print("   ✓ POST /api/tasks worked correctly")
            elif response.status_code in [401, 403, 422]:
                print(f"   Response: {response.status_code} - Expected auth/validation error")
                print("   ✓ POST /api/tasks returned proper error")
        else:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ✗ POST /api/tasks failed: {e}")

    print("\n" + "="*60)
    print("TESTING COMPLETE")
    print("="*60)
    print("\nNote: 401/403 errors are expected if using fake JWT tokens.")
    print("For full testing, use a valid JWT token from your Better Auth system.")

def main():
    print("Setting up API testing environment...")
    print("This will start the backend server and run tests against it.")

    # Start the server
    server_process = start_server()
    if not server_process:
        return

    try:
        # Wait a bit for the server to start, then run tests
        test_thread = threading.Thread(target=run_tests)
        test_thread.start()

        # Wait for tests to complete
        test_thread.join()

    finally:
        # Terminate the server process
        print("\nShutting down server...")
        server_process.terminate()
        server_process.wait()
        print("Server stopped.")

if __name__ == "__main__":
    main()