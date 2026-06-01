"""Task request/response schemas"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.task import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    """Base task schema"""

    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    """Task creation schema"""

    pass


class TaskUpdate(BaseModel):
    """Task update schema"""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None


class TaskStatusUpdate(BaseModel):
    """Task status update schema"""

    status: TaskStatus


class TaskResponse(TaskBase):
    """Task response schema"""

    id: int
    status: TaskStatus
    is_completed: bool
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
