#!/usr/bin/env python3
"""
Comprehensive script to demonstrate saving different types of data to Neon DB
This script shows how to save tasks, conversations, and messages to the Neon PostgreSQL database
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), 'backend', '.env'))

# Add the backend directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.db import get_session_context
from backend.models.task import Task
from backend.models.conversation import Conversation
from backend.models.message import Message
from datetime import datetime
import uuid

def save_sample_task():
    """
    Save a sample task to Neon DB
    """
    print("Saving sample task to Neon DB...")

    # Sample user ID (in a real scenario, this would come from authentication)
    user_id = str(uuid.uuid4())

    # Create a new task
    new_task = Task(
        title="Complete Project Proposal",
        description="Finish writing and review the project proposal document",
        is_completed=False,
        due_date=datetime.now().replace(hour=23, minute=59, second=59),  # Due today
        priority="high",
        user_id=user_id
    )

    # Save to database using the context manager
    with get_session_context() as session:
        session.add(new_task)
        session.commit()
        session.refresh(new_task)  # Refresh to get the generated ID

        print("[SUCCESS] Task saved successfully!")
        print(f"  Task ID: {new_task.id}")
        print(f"  Task Title: {new_task.title}")
        print(f"  User ID: {new_task.user_id}")
        print(f"  Created at: {new_task.created_at}")
        print()

def save_sample_conversation_and_messages():
    """
    Save a sample conversation with messages to Neon DB
    """
    print("Saving sample conversation and messages to Neon DB...")

    user_id = str(uuid.uuid4())
    conversation_id = str(uuid.uuid4())

    # Create a new conversation
    new_conversation = Conversation(
        id=conversation_id,
        title="Project Discussion",
        user_id=user_id,
        is_active=True
    )

    # Create sample messages
    user_message = Message(
        id=str(uuid.uuid4()),
        conversation_id=conversation_id,
        role="user",
        content="Can you help me with my project?",
        sequence_number=1
    )

    assistant_message = Message(
        id=str(uuid.uuid4()),
        conversation_id=conversation_id,
        role="assistant",
        content="Sure, I'd be happy to help you with your project. What specifically do you need assistance with?",
        sequence_number=2
    )

    with get_session_context() as session:
        # Add conversation first
        session.add(new_conversation)
        session.commit()

        # Add messages
        session.add(user_message)
        session.add(assistant_message)
        session.commit()

        # Refresh to get updated data
        session.refresh(new_conversation)
        session.refresh(user_message)
        session.refresh(assistant_message)

        print("[SUCCESS] Conversation saved successfully!")
        print(f"  Conversation ID: {new_conversation.id}")
        print(f"  Title: {new_conversation.title}")
        print(f"  User ID: {new_conversation.user_id}")
        print()
        print("[SUCCESS] Messages saved successfully!")
        print(f"  Total messages: 2")
        print(f"  User message ID: {user_message.id}")
        print(f"  Assistant message ID: {assistant_message.id}")
        print()

def save_multiple_tasks():
    """
    Save multiple tasks to demonstrate batch operations
    """
    print("Saving multiple tasks to Neon DB...")

    user_id = str(uuid.uuid4())

    # Create multiple tasks
    tasks = [
        Task(
            title="Research market trends",
            description="Analyze current market trends for Q4",
            is_completed=False,
            priority="high",
            user_id=user_id
        ),
        Task(
            title="Schedule team meeting",
            description="Organize a meeting with the development team",
            is_completed=True,
            priority="medium",
            user_id=user_id
        ),
        Task(
            title="Review documentation",
            description="Go through the API documentation",
            is_completed=False,
            priority="low",
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

        print(f"[SUCCESS] {len(tasks)} tasks saved successfully!")
        for i, task in enumerate(tasks, 1):
            print(f"  {i}. Task ID: {task.id}, Title: {task.title}, Completed: {task.is_completed}")
        print()

def demonstrate_different_priority_levels():
    """
    Save tasks with different priority levels to show the priority system
    """
    print("Saving tasks with different priority levels...")

    user_id = str(uuid.uuid4())

    priorities = ["low", "medium", "high", "urgent"]
    tasks = []

    for i, priority in enumerate(priorities, 1):
        task = Task(
            title=f"Priority {priority} task",
            description=f"This is a {priority} priority task",
            is_completed=False,
            priority=priority,
            user_id=user_id
        )
        tasks.append(task)

    with get_session_context() as session:
        for task in tasks:
            session.add(task)
        session.commit()

        for task in tasks:
            session.refresh(task)

        print(f"[SUCCESS] {len(tasks)} tasks with different priorities saved successfully!")
        for task in tasks:
            print(f"  - Priority: {task.priority}, Title: {task.title}, ID: {task.id}")
        print()

def main():
    """
    Main function to run all demonstrations
    """
    print("Neon DB Data Saving Demonstrations")
    print("=" * 50)
    print("This script demonstrates how to save various types of data to Neon DB")
    print()

    try:
        # Save a single task
        save_sample_task()

        # Save multiple tasks
        save_multiple_tasks()

        # Save conversation and messages
        save_sample_conversation_and_messages()

        # Demonstrate different priority levels
        demonstrate_different_priority_levels()

        print("[SUCCESS] All data has been successfully saved to Neon DB!")
        print("Check your Neon database to verify the records were created.")

    except Exception as e:
        print(f"[ERROR] Error occurred while saving data: {str(e)}")
        print("Make sure your Neon DB connection is properly configured in the .env file.")

if __name__ == "__main__":
    main()