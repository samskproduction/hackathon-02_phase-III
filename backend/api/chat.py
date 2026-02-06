from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from auth.jwt_handler import get_current_user, TokenData
from services.cohere_runner import CohereRunner
from sqlmodel import Session, select
from models.conversation import Conversation
from models.message import Message
from database.database import get_session
import uuid

router = APIRouter(prefix="/api", tags=["chat"])

# Request and response models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ToolCall(BaseModel):
    name: str
    parameters: Dict[str, Any]

class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: List[ToolCall]


@router.post("/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user: TokenData = Depends(get_current_user)
):
    """
    Chat endpoint that handles natural language requests and returns responses
    with tool calls executed as needed.
    """
    # Verify that the user_id in the path matches the authenticated user
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own chat conversations"
        )

    # Initialize the Cohere runner
    runner = CohereRunner()

    try:
        # Run the chat request through the Cohere runner
        result = runner.run(
            user_message=request.message,
            user_id=current_user.user_id,
            conversation_id=request.conversation_id
        )

        # Check if there was an error in processing
        if "error" in result:
            return {
                "success": False,
                "error": {
                    "code": "CHAT_001",
                    "message": result["error"]
                }
            }

        # Return successful response in the expected format
        return {
            "success": True,
            "data": result  # result already contains conversation_id, response, tool_calls
        }

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Handle unexpected errors
        return {
            "success": False,
            "error": {
                "code": "GENERAL_001",
                "message": f"An unexpected error occurred: {str(e)}"
            }
        }


@router.get("/conversations/{user_id}")
async def get_user_conversations(
    user_id: str,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a list of conversations for the specified user.
    """
    # Verify that the user_id in the path matches the authenticated user
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own conversations"
        )

    try:
        # Retrieve user's conversations from database
        statement = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
        conversations = session.exec(statement).all()

        return {
            "success": True,
            "data": {
                "conversations": conversations,
                "total": len(conversations)
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "code": "CONV_001",
                "message": f"Error retrieving conversations: {str(e)}"
            }
        }


@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: str,
    current_user: TokenData = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get messages for a specific conversation.
    """
    # First, verify the user has access to this conversation
    conversation = session.get(Conversation, conversation_id)
    if not conversation:
        return {
            "success": False,
            "error": {
                "code": "MSG_001",
                "message": "Conversation not found"
            }
        }

    if conversation.user_id != current_user.user_id:
        return {
            "success": False,
            "error": {
                "code": "MSG_002",
                "message": "You don't have access to this conversation"
            }
        }

    try:
        # Retrieve messages for the conversation from database
        statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp.asc())
        messages = session.exec(statement).all()

        return {
            "success": True,
            "data": {
                "messages": messages,
                "total": len(messages)
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "code": "MSG_003",
                "message": f"Error retrieving messages: {str(e)}"
            }
        }