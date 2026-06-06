#!/usr/bin/env python3
"""
Task Manager CLI with Database
Day 3: Database Implementation
"""

import sys
from datetime import datetime
from database import (
    add_task, list_tasks, complete_task, delete_task,
    update_task, search_tasks, get_statistics, migrate_from_json
)

def show_help():
    print("""
╔════════════════════════════════════════════════════════════╗
║           📋 Task Manager CLI - Database Version           ║
╚════════════════════════════════════════════════════════════╝

COMMANDS:
  add <title>              Add a new task
  list                     Show all tasks
  list-pending             Show incomplete tasks
  list-completed           Show completed tasks
  search <keyword>         Search tasks
  done <id>                Mark task as completed
  delete <id>              Delete a task
  update <id> <title>      Update task title
  stats                    Show statistics
  migrate                  Migrate from JSON to database
  help                     Show this help message

EXAMPLES:
  python3 tasks_cli.py add "Buy groceries"
  python3 tasks_cli.py list
  python3 tasks_cli.py done 1
  python3 tasks_cli.py search "groceries"
  python3 tasks_cli.py stats
    """)

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    # Add task
    if command == "add" and len(sys.argv) > 2:
        title = " ".join(sys.argv[2:])
        add_task(title)
    
    # List tasks
    elif command == "list":
        list_tasks()
    
    elif command == "list-pending":
        list_tasks(filter_completed=False)
    
    elif command == "list-completed":
        list_tasks(filter_completed=True)
    
    # Search tasks
    elif command == "search" and len(sys.argv) > 2:
        keyword = " ".join(sys.argv[2:])
        search_tasks(keyword)
    
    # Mark as done
    elif command == "done" and len(sys.argv) > 2:
        try:
            task_id = int(sys.argv[2])
            complete_task(task_id)
        except ValueError:
            print("❌ Task ID must be a number")
    
    # Delete task
    elif command == "delete" and len(sys.argv) > 2:
        try:
            task_id = int(sys.argv[2])
            delete_task(task_id)
        except ValueError:
            print("❌ Task ID must be a number")
    
    # Update task
    elif command == "update" and len(sys.argv) > 3:
        try:
            task_id = int(sys.argv[2])
            new_title = " ".join(sys.argv[3:])
            update_task(task_id, title=new_title)
        except ValueError:
            print("❌ Task ID must be a number")
    
    # Statistics
    elif command == "stats":
        get_statistics()
    
    # Migrate from JSON
    elif command == "migrate":
        migrate_from_json()
    
    # Help
    elif command == "help":
        show_help()
    
    else:
        print("❌ Unknown command. Use 'help' for available commands.")

if __name__ == "__main__":
    main()
