"""Task service"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate, TaskStatusUpdate
from fastapi import HTTPException, status
from typing import List


class TaskService:
    """Service for handling task operations"""

    @staticmethod
    async def create_task(db: AsyncSession, user_id: int, task_create: TaskCreate) -> Task:
        """Create a new task"""
        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            priority=task_create.priority,
            due_date=task_create.due_date,
            owner_id=user_id,
        )
        db.add(db_task)
        await db.commit()
        await db.refresh(db_task)
        return db_task

    @staticmethod
    async def get_tasks(
        db: AsyncSession, user_id: int, status: str = None, skip: int = 0, limit: int = 10
    ) -> tuple[List[Task], int]:
        """Get user's tasks with optional filtering"""
        # Build query
        query = select(Task).where(Task.owner_id == user_id)
        if status:
            query = query.where(Task.status == status)

        # Get total count
        count_stmt = select(Task).where(Task.owner_id == user_id)
        if status:
            count_stmt = count_stmt.where(Task.status == status)
        count_result = await db.execute(count_stmt)
        total = len(count_result.scalars().all())

        # Get paginated results
        query = query.offset(skip).limit(limit).order_by(Task.created_at.desc())
        result = await db.execute(query)
        tasks = result.scalars().all()
        return tasks, total

    @staticmethod
    async def get_task(db: AsyncSession, task_id: int, user_id: int) -> Task:
        """Get a specific task"""
        stmt = select(Task).where(and_(Task.id == task_id, Task.owner_id == user_id))
        result = await db.execute(stmt)
        task = result.scalars().first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        return task

    @staticmethod
    async def update_task(
        db: AsyncSession, task_id: int, user_id: int, task_update: TaskUpdate
    ) -> Task:
        """Update a task"""
        task = await TaskService.get_task(db, task_id, user_id)

        # Update fields
        if task_update.title is not None:
            task.title = task_update.title
        if task_update.description is not None:
            task.description = task_update.description
        if task_update.priority is not None:
            task.priority = task_update.priority
        if task_update.due_date is not None:
            task.due_date = task_update.due_date

        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task

    @staticmethod
    async def update_task_status(
        db: AsyncSession, task_id: int, user_id: int, status_update: TaskStatusUpdate
    ) -> Task:
        """Update task status"""
        task = await TaskService.get_task(db, task_id, user_id)
        task.status = status_update.status
        task.is_completed = status_update.status == TaskStatus.COMPLETED
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task

    @staticmethod
    async def delete_task(db: AsyncSession, task_id: int, user_id: int) -> None:
        """Delete a task"""
        task = await TaskService.get_task(db, task_id, user_id)
        await db.delete(task)
        await db.commit()
