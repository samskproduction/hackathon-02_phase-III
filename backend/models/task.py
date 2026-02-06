from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    due_date: Optional[datetime] = None
    priority: str = "medium"  # low, medium, high, urgent

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # Better Auth user ID
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to User (optional if we're keeping user data in Better Auth)
    # user: Optional["User"] = Relationship(back_populates="tasks")

class TaskCreate(TaskBase):
    title: str
    class Config:
        json_schema_extra = {
            "example": {
                "title": "New Task",
                "description": "Task description",
                "due_date": "2023-12-31T10:00:00Z",
                "priority": "high"
            }
        }

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None

class TaskResponse(TaskBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime
