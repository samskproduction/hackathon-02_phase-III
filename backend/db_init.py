"""
Database initialization script for adding Conversation and Message tables
"""
from sqlmodel import SQLModel
from database.database import engine
from models import Conversation, Message  # Import the new models


def create_db_and_tables():
    """
    Create/update database tables including new Conversation and Message tables
    """
    print("Creating/updating database tables for Phase III AI Chatbot...")

    # Import all models to register them with SQLModel metadata
    from models.user import User
    from models.task import Task

    # Create all tables
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables created/updated successfully including Conversation and Message tables.")


if __name__ == "__main__":
    create_db_and_tables()