from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: TaskStatus = TaskStatus.MEDIUM


class TaskCreate(TaskBase):
    title: str  # Enforce required field


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[TaskStatus] = None


class TaskResponse(TaskBase):
    id: int
    user_id: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    user_id: str


class TaskFilterParams(BaseModel):
    status: Optional[str] = None  # "all", "pending", "completed"
    sort: Optional[str] = None   # "created", "title", "due_date"