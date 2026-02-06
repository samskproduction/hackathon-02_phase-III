from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

from database.database import get_session
from auth.jwt_handler import get_current_user, TokenData
from models.task import Task, TaskCreate, TaskUpdate, TaskResponse
from utils.responses import create_success_response, create_error_response

router = APIRouter()

@router.post("/tasks", response_model=dict)
async def create_task(
    task_data: TaskCreate,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    '''Create a new task for the authenticated user'''
    if not task_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=create_error_response("TASK_003", "Missing required fields", 422)
        )
    
    task = Task(
        title=task_data.title,
        description=task_data.description,
        is_completed=task_data.is_completed,
        due_date=task_data.due_date,
        priority=task_data.priority,
        user_id=current_user.user_id
    )
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return create_success_response(
        data={"task": task},
        message="Task created successfully"
    )

@router.get("/tasks", response_model=dict)
async def get_tasks(
    status_filter: Optional[str] = Query(None, description="Filter by status: all, pending, completed"),
    priority_filter: Optional[str] = Query(None, description="Filter by priority: low, medium, high, urgent"),
    sort_by: Optional[str] = Query("created_at", description="Sort by: created_at, updated_at, due_date"),
    order: Optional[str] = Query("desc", description="Order: asc, desc"),
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    '''Get all tasks for the authenticated user'''
    query = select(Task).where(Task.user_id == current_user.user_id)
    
    if status_filter and status_filter != "all":
        if status_filter == "pending":
            query = query.where(Task.is_completed == False)
        elif status_filter == "completed":
            query = query.where(Task.is_completed == True)
    
    if priority_filter:
        query = query.where(Task.priority == priority_filter)
    
    # Apply sorting
    if sort_by == "created_at":
        query = query.order_by(Task.created_at.desc() if order == "desc" else Task.created_at.asc())
    elif sort_by == "updated_at":
        query = query.order_by(Task.updated_at.desc() if order == "desc" else Task.updated_at.asc())
    elif sort_by == "due_date":
        query = query.order_by(Task.due_date.desc() if order == "desc" else Task.due_date.asc())
    
    tasks = session.exec(query).all()
    
    return create_success_response(
        data={"tasks": tasks},
        message="Tasks retrieved successfully"
    )

@router.get("/tasks/{task_id}", response_model=dict)
async def get_task(
    task_id: int,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    '''Get a specific task by ID'''
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=create_error_response("TASK_001", "Task not found", 404)
        )
    
    if task.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=create_error_response("TASK_002", "User not authorized to access task", 403)
        )
    
    return create_success_response(
        data={"task": task},
        message="Task retrieved successfully"
    )

@router.put("/tasks/{task_id}", response_model=dict)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    '''Update a specific task'''
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=create_error_response("TASK_001", "Task not found", 404)
        )
    
    if task.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=create_error_response("TASK_002", "User not authorized to access task", 403)
        )
    
    # Update task fields
    update_data = task_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return create_success_response(
        data={"task": task},
        message="Task updated successfully"
    )

@router.patch("/tasks/{task_id}/toggle-status", response_model=dict)
async def toggle_task_status(
    task_id: int,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    '''Toggle task completion status'''
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=create_error_response("TASK_001", "Task not found", 404)
        )
    
    if task.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=create_error_response("TASK_002", "User not authorized to access task", 403)
        )
    
    # Toggle completion status
    task.is_completed = not task.is_completed
    task.updated_at = datetime.utcnow()
    
    session.add(task)
    session.commit()
    session.refresh(task)
    
    return create_success_response(
        data={"task": task},
        message="Task completion status updated"
    )

@router.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(
    task_id: int,
    current_user = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    '''Delete a specific task'''
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=create_error_response("TASK_001", "Task not found", 404)
        )
    
    if task.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=create_error_response("TASK_002", "User not authorized to access task", 403)
        )
    
    session.delete(task)
    session.commit()
    
    return create_success_response(message="Task deleted successfully")
