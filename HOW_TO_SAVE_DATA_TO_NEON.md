# How to Save Data to Neon DB

Your application is already configured to save data to Neon DB. Here's how it works:

## Database Configuration

The database connection is configured in:
- `backend/config.py` - Contains the settings class
- `backend/.env` - Contains the actual Neon DB URL

The connection string format is:
```
postgresql://username:password@endpoint/database?sslmode=require
```

## Models Available

Your application has several pre-built models that can save data to Neon DB:

1. **Task Model** (`backend/models/task.py`)
   - Fields: title, description, is_completed, due_date, priority, user_id
   - Used for task management

2. **Conversation Model** (`backend/models/conversation.py`)
   - Fields: id, title, user_id, is_active
   - Used for chat conversations

3. **Message Model** (`backend/models/message.py`)
   - Fields: id, conversation_id, role, content, tool_calls, etc.
   - Used for storing chat messages

## How to Save Data

### Method 1: Direct Python Script (as demonstrated in `demonstrate_neon_saving.py`)

```python
from backend.db import get_session_context
from backend.models.task import Task
from datetime import datetime
import uuid

# Create a new task
new_task = Task(
    title="My Task",
    description="Task description",
    is_completed=False,
    priority="medium",
    user_id=str(uuid.uuid4())  # Replace with actual user ID
)

# Save to database
with get_session_context() as session:
    session.add(new_task)
    session.commit()
    session.refresh(new_task)  # Gets the generated ID
    print(f"Task saved with ID: {new_task.id}")
```

### Method 2: Through API Endpoints

The application already has API endpoints for saving data:

- **Tasks API**: `POST /tasks` - Creates new tasks
- **Chat API**: `POST /api/{user_id}/chat` - Saves conversations and messages

### Method 3: Using Session Context Manager

```python
from sqlmodel import Session
from backend.db import engine

with Session(engine) as session:
    # Create your model instance
    new_item = YourModel(field1=value1, field2=value2)

    # Add to session
    session.add(new_item)

    # Commit the transaction
    session.commit()

    # Refresh to get generated fields
    session.refresh(new_item)
```

## Example API Call

To save a task via API:

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Task",
    "description": "Task description",
    "priority": "high"
  }'
```

## Verifying Data

You can connect to your Neon DB directly to verify the data:

1. Go to your Neon dashboard
2. Use the SQL editor or connect with a database client
3. Run queries like:
   ```sql
   SELECT * FROM task LIMIT 10;
   SELECT * FROM conversation LIMIT 10;
   SELECT * FROM message LIMIT 10;
   ```

## Important Notes

1. **Authentication**: Most endpoints require JWT authentication
2. **User Context**: Data is associated with authenticated users
3. **Connection Pooling**: The configuration is optimized for Neon's serverless architecture
4. **SSL Required**: Connections use SSL for security
5. **Error Handling**: The system includes proper transaction rollback on errors

Your application is fully configured to save data to Neon DB, and the demonstration script proves that the connection and saving mechanisms are working correctly!