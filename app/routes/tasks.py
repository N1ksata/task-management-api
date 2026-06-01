"""Task routes"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate, TaskStatusUpdate
from app.services.task_service import TaskService
from app.routes.dependencies import get_current_user
from app.models.user import User
from typing import List

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])


@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    status: str = Query(None, description="Filter by task status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    """List current user's tasks"""
    tasks, _ = await TaskService.get_tasks(db, current_user.id, status, skip, limit)
    return tasks


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_create: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new task"""
    task = await TaskService.create_task(db, current_user.id, task_create)
    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific task"""
    task = await TaskService.get_task(db, task_id, current_user.id)
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a task"""
    task = await TaskService.update_task(db, task_id, current_user.id, task_update)
    return task


@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: int,
    status_update: TaskStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update task status"""
    task = await TaskService.update_task_status(
        db, task_id, current_user.id, status_update
    )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a task"""
    await TaskService.delete_task(db, task_id, current_user.id)
