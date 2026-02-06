# Quickstart Guide: Backend API for Todo Application

## Setup Environment

### Prerequisites
- Python 3.11+ installed
- pip for package management
- Git for version control
- Neon Serverless PostgreSQL account

### Initial Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables
Create a `.env` file in the backend directory with the following variables:

```env
BETTER_AUTH_SECRET=your-shared-secret-key-here
NEON_DB_URL=postgresql://username:password@ep-xxx-neon-tech.neon.tech/dbname?sslmode=require
```

## Running the Application

### Development Mode
```bash
# Start the development server with auto-reload
uvicorn main:app --reload --port 8000
```

### Production Mode
```bash
# Start the production server
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Key Technologies & Structure

### Tech Stack
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.11+
- **Database**: SQLModel ORM with Neon Serverless PostgreSQL
- **Authentication**: JWT token verification using PyJWT
- **Environment**: python-dotenv for config management

### Project Structure
```
backend/
├── main.py              # FastAPI application entry point with CORS setup
├── models.py            # SQLModel database models (User, Task)
├── db.py                # Database connection and session management
├── auth.py              # JWT middleware and authentication utilities
├── schemas.py           # Pydantic schemas for request/response validation
├── routes/
│   └── tasks.py         # Task CRUD endpoint implementations
├── config.py            # Configuration and environment variables
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables template
```

## Key Components to Build

### 1. Database Models
```python
# models.py
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    # Task model with proper relationships and constraints
    pass
```

### 2. Request/Response Schemas
```python
# schemas.py
from pydantic import BaseModel

class TaskCreate(BaseModel):
    # Schema for creating new tasks
    pass

class TaskUpdate(BaseModel):
    # Schema for updating tasks
    pass
```

### 3. Authentication Utilities
```python
# auth.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

def get_current_user(token: str = Depends(HTTPBearer())):
    # Validates JWT token and extracts user info
    pass
```

### 4. Database Connection
```python
# db.py
from sqlmodel import create_engine
from contextlib import contextmanager

# Database engine and session management
engine = None
```

### 5. Task Endpoints
```python
# routes/tasks.py
from fastapi import APIRouter, Depends
from typing import List

router = APIRouter(prefix="/api/tasks")

@router.get("/")
async def get_tasks(user_id: str = Depends(get_current_user)) -> List[Task]:
    # Returns tasks for authenticated user
    pass
```

## Running Tests

### Unit Tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=.
```

### Linting
```bash
# Check code for linting issues
flake8 .

# Format code
black .
```

## API Integration

### Testing with Curl
```bash
# Get tasks for user
curl -X GET "http://localhost:8000/api/tasks" \
     -H "Authorization: Bearer your-jwt-token-here"

# Create a new task
curl -X POST "http://localhost:8000/api/tasks" \
     -H "Authorization: Bearer your-jwt-token-here" \
     -H "Content-Type: application/json" \
     -d '{"title": "New Task", "description": "Task description"}'
```

## Common Commands

| Command | Description |
|---------|-------------|
| `uvicorn main:app --reload` | Start development server |
| `pytest` | Run unit tests |
| `black .` | Format code |
| `flake8 .` | Check for linting issues |
| `mypy .` | Run type checker |

## Next Steps
1. Begin with creating the database models in `models.py`
2. Implement the Pydantic schemas in `schemas.py`
3. Build the authentication middleware in `auth.py`
4. Create the database connection in `db.py`
5. Implement the task endpoints in `routes/tasks.py`
6. Add the routes to the main application in `main.py`