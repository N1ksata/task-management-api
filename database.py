from models import Task, SessionLocal
from datetime import datetime
import json
import os

# Database operations
def add_task(title, description=None, priority="Medium", due_date=None):
    """Add a new task to database"""
    db = SessionLocal()
    try:
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        print(f"✅ Task added: {title} (ID: {task.id})")
        return task
    except Exception as e:
        db.rollback()
        print(f"❌ Error adding task: {e}")
    finally:
        db.close()

def list_tasks(filter_completed=None, priority=None):
    """List all tasks with optional filters"""
    db = SessionLocal()
    try:
        query = db.query(Task)
        
        if filter_completed is not None:
            query = query.filter(Task.completed == filter_completed)
        
        if priority:
            query = query.filter(Task.priority == priority)
        
        tasks = query.order_by(Task.priority.desc(), Task.created_at.desc()).all()
        
        if not tasks:
            print("📭 No tasks found!")
            return []
        
        print("\n📋 Your Tasks:")
        print("-" * 70)
        for task in tasks:
            due = f" | Due: {task.due_date.strftime('%Y-%m-%d')}" if task.due_date else ""
            print(f"{task} {due}")
        print("-" * 70 + "\n")
        return tasks
    finally:
        db.close()

def complete_task(task_id):
    """Mark task as completed"""
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            task.completed = True
            task.updated_at = datetime.now()
            db.commit()
            print(f"✅ Task {task_id} marked as done!")
            return task
        else:
            print(f"❌ Task {task_id} not found")
    finally:
        db.close()

def delete_task(task_id):
    """Delete a task"""
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            db.delete(task)
            db.commit()
            print(f"🗑️ Task {task_id} deleted!")
            return True
        else:
            print(f"❌ Task {task_id} not found")
            return False
    finally:
        db.close()

def update_task(task_id, title=None, description=None, priority=None, due_date=None):
    """Update task details"""
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            if title:
                task.title = title
            if description:
                task.description = description
            if priority:
                task.priority = priority
            if due_date:
                task.due_date = due_date
            task.updated_at = datetime.now()
            db.commit()
            print(f"✏️ Task {task_id} updated!")
            return task
        else:
            print(f"❌ Task {task_id} not found")
    finally:
        db.close()

def search_tasks(keyword):
    """Search tasks by keyword"""
    db = SessionLocal()
    try:
        tasks = db.query(Task).filter(
            Task.title.ilike(f"%{keyword}%") | 
            Task.description.ilike(f"%{keyword}%")
        ).all()
        
        if not tasks:
            print(f"🔍 No tasks found with '{keyword}'")
            return []
        
        print(f"\n🔍 Search results for '{keyword}':")
        print("-" * 70)
        for task in tasks:
            print(f"{task}")
        print("-" * 70 + "\n")
        return tasks
    finally:
        db.close()

def get_statistics():
    """Get task statistics"""
    db = SessionLocal()
    try:
        total = db.query(Task).count()
        completed = db.query(Task).filter(Task.completed == True).count()
        pending = total - completed
        
        if total == 0:
            print("📊 No tasks yet!")
            return
        
        percentage = (completed / total) * 100
        
        print("\n📊 Task Statistics:")
        print("-" * 40)
        print(f"Total Tasks: {total}")
        print(f"Completed: {completed} ✅")
        print(f"Pending: {pending} ⭕")
        print(f"Completion: {percentage:.1f}%")
        print("-" * 40 + "\n")
    finally:
        db.close()

def migrate_from_json():
    """Migrate tasks from tasks.json to database"""
    if not os.path.exists("tasks.json"):
        print("📭 No tasks.json file found. Starting fresh!")
        return
    
    try:
        with open("tasks.json", "r") as f:
            json_tasks = json.load(f)
        
        db = SessionLocal()
        for json_task in json_tasks:
            existing = db.query(Task).filter(Task.id == json_task.get("id")).first()
            if not existing:
                task = Task(
                    id=json_task.get("id"),
                    title=json_task.get("title"),
                    description=json_task.get("description"),
                    priority=json_task.get("priority", "Medium"),
                    completed=json_task.get("completed", False),
                    created_at=datetime.fromisoformat(json_task.get("created_at", datetime.now().isoformat()))
                )
                db.add(task)
        
        db.commit()
        db.close()
        print(f"✅ Migrated {len(json_tasks)} tasks from JSON to database!")
        
        # Backup old file
        os.rename("tasks.json", "tasks.json.backup")
        print("📦 Old tasks.json backed up as tasks.json.backup")
    except Exception as e:
        print(f"❌ Migration error: {e}")
