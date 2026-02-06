from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING, Optional
import uuid

if TYPE_CHECKING:
    from .user import User
    from .message import Message


class ConversationBase(SQLModel):
    title: Optional[str] = Field(default=None)
    user_id: str = Field(index=True, foreign_key="user.id")  # Foreign key to User
    is_active: bool = Field(default=True)


class Conversation(ConversationBase, table=True):
    """
    Represents a single chat conversation thread between user and AI assistant
    """
    __tablename__ = "conversations"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(
        back_populates="conversations",
        sa_relationship_kwargs={
            "primaryjoin": "Conversation.user_id == User.id"
        }
    )
    messages: list["Message"] = Relationship(back_populates="conversation")


class ConversationCreate(ConversationBase):
    """Schema for creating a new conversation"""
    pass


class ConversationRead(ConversationBase):
    """Schema for reading conversation data"""
    id: str
    created_at: datetime
    updated_at: datetime