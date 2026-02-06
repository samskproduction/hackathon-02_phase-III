#!/usr/bin/env python3
"""
Script to demonstrate saving data to Neon DB
This script shows how to create and save data to the Neon PostgreSQL database
"""

from backend.db import get_session_context
from backend.models.task import Task
from datetime import datetime
import uuid

def save_sample_data():
    """
    Save sample task data to Neon DB
    """
    print("Saving data to Neon DB...")

    # Sample user ID (in a real scenario, this would come from authentication)
    user_id = str(uuid.uuid4())

    # Create a new task
    new_task = Task(
        title="Sample Task",
        description="This is a sample task saved to Neon DB",
        is_completed=False,
        due_date=datetime.now().replace(hour=23, minute=59, second=59),  # Due today
        priority="medium",
        user_id=user_id
    )

    # Save to database using the context manager
    with get_session_context() as session:
        session.add(new_task)
        session.commit()
        session.refresh(new_task)  # Refresh to get the generated ID

        print(f"Task saved successfully!")
        print(f"Task ID: {new_task.id}")
        print(f"Task Title: {new_task.title}")
        print(f"User ID: {new_task.user_id}")
        print(f"Created at: {new_task.created_at}")

def save_multiple_tasks():
    """
    Save multiple tasks to demonstrate batch operations
    """
    print("\nSaving multiple tasks to Neon DB...")

    user_id = str(uuid.uuid4())

    # Create multiple tasks
    tasks = [
        Task(
            title="Task 1",
            description="First sample task",
            is_completed=False,
            priority="low",
            user_id=user_id
        ),
        Task(
            title="Task 2",
            description="Second sample task",
            is_completed=True,
            priority="high",
            user_id=user_id
        ),
        Task(
            title="Task 3",
            description="Third sample task",
            is_completed=False,
            priority="medium",
            user_id=user_id
        )
    ]

    with get_session_context() as session:
        # Add all tasks to the session
        for task in tasks:
            session.add(task)

        # Commit all changes at once
        session.commit()

        # Refresh to get the generated IDs
        for task in tasks:
            session.refresh(task)

        print(f"{len(tasks)} tasks saved successfully!")
        for task in tasks:
            print(f"- Task ID: {task.id}, Title: {task.title}, Completed: {task.is_completed}")

if __name__ == "__main__":
    print("Neon DB Data Saving Demo")
    print("=" * 30)

    # Save a single task
    save_sample_data()

    # Save multiple tasks
    save_multiple_tasks()

    print("\nData has been successfully saved to Neon DB!")
    print("Check your Neon database to verify the records were created.")