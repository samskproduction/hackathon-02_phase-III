from typing import Dict, Any, List, Optional
import json
from database.database import get_session
from models.task import Task
from models.user import User
from sqlmodel import select, Session, func
from datetime import datetime


def get_user_profile_tool(user_id: str) -> Dict[str, Any]:
    """
    MCP tool to retrieve user profile information
    """
    with get_session() as session:
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()

        if not user:
            return {"error": "User not found"}

        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }


def add_task_tool(user_id: str, title: str, description: Optional[str] = None,
                 priority: Optional[str] = "medium", due_date: Optional[str] = None) -> Dict[str, Any]:
    """
    MCP tool to add a new task
    """
    from datetime import datetime

    with get_session() as session:
        # Create new task
        new_task = Task(
            user_id=user_id,
            title=title,
            description=description,
            priority=priority,
            is_completed=False,  # Default to not completed
            created_at=datetime.utcnow()
        )

        if due_date:
            try:
                new_task.due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            except:
                pass  # If date parsing fails, don't set due date

        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        return {
            "success": True,
            "task_id": new_task.id,
            "message": f"Task '{title}' has been added successfully!",
            "task": {
                "id": new_task.id,
                "title": new_task.title,
                "description": new_task.description,
                "priority": new_task.priority,
                "completed": new_task.is_completed,
                "due_date": new_task.due_date.isoformat() if new_task.due_date else None,
                "created_at": new_task.created_at.isoformat() if new_task.created_at else None
            }
        }


def list_tasks_tool(user_id: str, status: Optional[str] = None, priority: Optional[str] = None) -> Dict[str, Any]:
    """
    MCP tool to list tasks with optional filtering
    """
    with get_session() as session:
        # Start with base query
        query = select(Task).where(Task.user_id == user_id)

        # Apply filters if provided
        if status:
            if status.lower() == "completed":
                query = query.where(Task.is_completed == True)
            elif status.lower() == "pending":
                query = query.where(Task.is_completed == False)

        if priority:
            query = query.where(Task.priority == priority.lower())

        tasks = session.exec(query).all()

        task_list = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "completed": task.is_completed,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "created_at": task.created_at.isoformat() if task.created_at else None
            }
            for task in tasks
        ]

        return {
            "count": len(task_list),
            "tasks": task_list,
            "message": f"You have {len(task_list)} task(s)."
        }


def complete_task_tool(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    MCP tool to mark a task as completed
    """
    with get_session() as session:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            return {
                "success": False,
                "error": f"Task with ID {task_id} not found or you don't have permission to modify it."
            }

        task.is_completed = True
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "success": True,
            "message": f"Task '{task.title}' has been marked as completed!",
            "task": {
                "id": task.id,
                "title": task.title,
                "completed": task.completed
            }
        }


def delete_task_tool(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    MCP tool to delete a task
    """
    with get_session() as session:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            return {
                "success": False,
                "error": f"Task with ID {task_id} not found or you don't have permission to delete it."
            }

        session.delete(task)
        session.commit()

        return {
            "success": True,
            "message": f"Task '{task.title}' has been deleted successfully!"
        }


def update_task_tool(user_id: str, task_id: str, title: Optional[str] = None,
                    description: Optional[str] = None, priority: Optional[str] = None,
                    completed: Optional[bool] = None, due_date: Optional[str] = None) -> Dict[str, Any]:
    """
    MCP tool to update a task
    """
    with get_session() as session:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if not task:
            return {
                "success": False,
                "error": f"Task with ID {task_id} not found or you don't have permission to modify it."
            }

        # Update fields if provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if priority is not None:
            task.priority = priority.lower()
        if completed is not None:
            task.is_completed = completed
        if due_date:
            try:
                task.due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            except:
                pass  # If date parsing fails, don't update due date

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "success": True,
            "message": f"Task '{task.title}' has been updated successfully!",
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "completed": task.is_completed,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "created_at": task.created_at.isoformat() if task.created_at else None
            }
        }


def get_cohere_tool_schemas():
    """
    Return Cohere-compatible tool schemas for all available tools
    """
    return [
        {
            "name": "get_user_profile",
            "description": "Retrieve the authenticated user's profile information including id, email, name, and account creation date.",
            "parameter_definitions": {
                "user_id": {
                    "description": "The unique identifier of the user whose profile is being retrieved",
                    "type": "str",
                    "required": True
                }
            }
        },
        {
            "name": "add_task",
            "description": "Add a new task to the user's task list",
            "parameter_definitions": {
                "user_id": {
                    "description": "The unique identifier of the user creating the task",
                    "type": "str",
                    "required": True
                },
                "title": {
                    "description": "The title or name of the task",
                    "type": "str",
                    "required": True
                },
                "description": {
                    "description": "An optional detailed description of the task",
                    "type": "str",
                    "required": False
                },
                "priority": {
                    "description": "The priority of the task (low, medium, high)",
                    "type": "str",
                    "required": False
                },
                "due_date": {
                    "description": "The due date for the task in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)",
                    "type": "str",
                    "required": False
                }
            }
        },
        {
            "name": "list_tasks",
            "description": "List tasks with optional filtering by status and priority",
            "parameter_definitions": {
                "user_id": {
                    "description": "The unique identifier of the user whose tasks are being listed",
                    "type": "str",
                    "required": True
                },
                "status": {
                    "description": "Filter tasks by status (completed, pending, or all)",
                    "type": "str",
                    "required": False
                },
                "priority": {
                    "description": "Filter tasks by priority (low, medium, high)",
                    "type": "str",
                    "required": False
                }
            }
        },
        {
            "name": "complete_task",
            "description": "Mark a task as completed",
            "parameter_definitions": {
                "user_id": {
                    "description": "The unique identifier of the user who owns the task",
                    "type": "str",
                    "required": True
                },
                "task_id": {
                    "description": "The unique identifier of the task to be completed",
                    "type": "str",
                    "required": True
                }
            }
        },
        {
            "name": "delete_task",
            "description": "Delete a task from the user's task list",
            "parameter_definitions": {
                "user_id": {
                    "description": "The unique identifier of the user who owns the task",
                    "type": "str",
                    "required": True
                },
                "task_id": {
                    "description": "The unique identifier of the task to be deleted",
                    "type": "str",
                    "required": True
                }
            }
        },
        {
            "name": "update_task",
            "description": "Update the details of an existing task",
            "parameter_definitions": {
                "user_id": {
                    "description": "The unique identifier of the user who owns the task",
                    "type": "str",
                    "required": True
                },
                "task_id": {
                    "description": "The unique identifier of the task to be updated",
                    "type": "str",
                    "required": True
                },
                "title": {
                    "description": "The new title of the task (optional)",
                    "type": "str",
                    "required": False
                },
                "description": {
                    "description": "The new description of the task (optional)",
                    "type": "str",
                    "required": False
                },
                "priority": {
                    "description": "The new priority of the task (optional)",
                    "type": "str",
                    "required": False
                },
                "completed": {
                    "description": "Whether the task is completed (optional)",
                    "type": "bool",
                    "required": False
                },
                "due_date": {
                    "description": "The new due date for the task in ISO format (optional)",
                    "type": "str",
                    "required": False
                }
            }
        }
    ]


def execute_tool_call(tool_name: str, tool_parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a tool call based on the tool name and parameters
    """
    # All tool functions expect user_id as the first parameter
    user_id = tool_parameters.get('user_id')

    if not user_id:
        return {"error": "Missing user_id parameter"}

    # Remove user_id from parameters to pass the rest to the function
    params = {k: v for k, v in tool_parameters.items() if k != 'user_id'}

    # Map tool names to functions
    tool_functions = {
        'get_user_profile': get_user_profile_tool,
        'add_task': add_task_tool,
        'list_tasks': list_tasks_tool,
        'complete_task': complete_task_tool,
        'delete_task': delete_task_tool,
        'update_task': update_task_tool
    }

    if tool_name not in tool_functions:
        return {"error": f"Unknown tool: {tool_name}"}

    try:
        # Call the appropriate function with user_id as the first parameter
        func = tool_functions[tool_name]
        return func(user_id, **params) if params else func(user_id)
    except Exception as e:
        return {"error": f"Error executing tool {tool_name}: {str(e)}"}