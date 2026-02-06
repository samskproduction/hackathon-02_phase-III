"""
Simple health check script to verify the application is running correctly
"""
import requests
import sys

def check_backend_health():
    """Check if the backend is running and healthy"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            if health_data.get("status") == "healthy":
                print("✓ Backend is healthy")
                return True
        print(f"✗ Backend health check failed: {response.status_code}")
        return False
    except Exception as e:
        print(f"✗ Backend is not accessible: {e}")
        return False

def check_api_docs():
    """Check if API documentation is available"""
    try:
        response = requests.get("http://localhost:8000/docs", timeout=10)
        if response.status_code == 200:
            print("✓ API documentation is accessible")
            return True
        print(f"✗ API docs check failed: {response.status_code}")
        return False
    except Exception as e:
        print(f"✗ API docs are not accessible: {e}")
        return False

def run_all_checks():
    """Run all health checks"""
    print("Running backend health checks...")

    results = []
    results.append(check_backend_health())
    results.append(check_api_docs())

    if all(results):
        print("\n✓ All health checks passed!")
        return True
    else:
        print("\n✗ Some health checks failed")
        return False

if __name__ == "__main__":
    success = run_all_checks()
    sys.exit(0 if success else 1)