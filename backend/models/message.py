from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import JSON
import uuid

if TYPE_CHECKING:
    from .conversation import Conversation


class MessageBase(SQLModel):
    conversation_id: str = Field(index=True, foreign_key="conversations.id")  # Foreign key to Conversation
    role: str = Field(regex=r"^(user|assistant)$")  # Message sender role
    content: str  # The actual message content
    tool_calls: Optional[dict] = Field(default=None, sa_type=JSON)  # Tool calls triggered by this message (if assistant)
    tool_call_results: Optional[dict] = Field(default=None, sa_type=JSON)  # Results of executed tool calls (if assistant)
    sequence_number: int = Field(default=0)  # Order of message within conversation


class Message(MessageBase, table=True):
    """
    Represents a single message within a conversation
    """
    __tablename__ = "messages"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")


class MessageCreate(MessageBase):
    """Schema for creating a new message"""
    pass


class MessageRead(MessageBase):
    """Schema for reading message data"""
    id: str
    timestamp: datetime