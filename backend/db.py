from sqlmodel import create_engine, Session
from contextlib import contextmanager
from typing import Generator
import os
from .config import settings


# Create the database engine
engine = create_engine(
    settings.neon_db_url,
    # Enable connection pooling for Neon Serverless
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
)


def get_session() -> Generator[Session, None, None]:
    """Provide a transactional scope around a series of operations."""
    with Session(engine) as session:
        yield session


@contextmanager
def get_session_context():
    """Context manager for database sessions."""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_tables():
    """Create all tables defined in models."""
    from .models import Task  # Import here to avoid circular imports
    SQLModel.metadata.create_all(engine)