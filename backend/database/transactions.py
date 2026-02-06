"""
Database transaction management utilities
"""
from sqlmodel import Session
from contextlib import contextmanager
from typing import Generator
import logging

logger = logging.getLogger(__name__)

@contextmanager
def get_transaction(session: Session) -> Generator[Session, None, None]:
    """
    Context manager for database transactions with automatic rollback on exceptions
    """
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Transaction failed, rolled back: {e}")
        raise
    finally:
        session.close()


def execute_in_transaction(func, *args, **kwargs):
    """
    Execute a function inside a transaction
    """
    from .database import get_session

    with get_session() as session:
        with get_transaction(session) as trans_session:
            return func(trans_session, *args, **kwargs)