from typing import Dict, Any, List, Optional
import json
from datetime import datetime
from models.message import Message, MessageCreate
from models.conversation import Conversation, ConversationCreate
from .mcp_tools import get_cohere_tool_schemas, execute_tool_call
from .cohere_client import cohere_client
from database.database import get_session
from sqlmodel import select


class CohereRunner:
    def __init__(self):
        self.client = cohere_client.get_client()
        self.tools = get_cohere_tool_schemas()

    def load_conversation_history(self, conversation_id: str) -> List[Dict[str, str]]:
        """
        Load conversation history from the database
        """
        session_gen = get_session()
        session = next(session_gen)
        try:
            # Get messages for this conversation, ordered by sequence number
            statement = select(Message).where(
                Message.conversation_id == conversation_id
            ).order_by(Message.sequence_number)
            messages = session.exec(statement).all()

            # Convert to Cohere-compatible format
            history = []
            for msg in messages:
                history.append({
                    "role": msg.role,
                    "message": msg.content
                })

            return history
        finally:
            try:
                next(session_gen)
            except StopIteration:
                pass  # Generator finished normally

    def save_message(self, conversation_id: str, role: str, content: str,
                     tool_calls: Optional[List[Dict]] = None,
                     tool_call_results: Optional[List[Dict]] = None) -> Message:
        """
        Save a message to the database
        """
        session_gen = get_session()
        session = next(session_gen)
        try:
            # Count existing messages to determine sequence number
            count_statement = select(Message).where(Message.conversation_id == conversation_id)
            existing_messages = session.exec(count_statement).all()
            sequence_number = len(existing_messages)

            # Create message
            message = Message(
                conversation_id=conversation_id,
                role=role,
                content=content,
                tool_calls=tool_calls,
                tool_call_results=tool_call_results,
                sequence_number=sequence_number
            )

            session.add(message)
            session.commit()
            session.refresh(message)

            return message
        finally:
            try:
                next(session_gen)
            except StopIteration:
                pass  # Generator finished normally

    def create_conversation(self, user_id: str, title: Optional[str] = None) -> Conversation:
        """
        Create a new conversation in the database
        """
        session_gen = get_session()
        session = next(session_gen)
        try:
            # Create conversation with auto-generated title from first message or generic title
            if not title:
                title = f"Conversation {datetime.utcnow().strftime('%Y-%m-%d')}"

            conversation = Conversation(
                user_id=user_id,
                title=title
            )

            session.add(conversation)
            session.commit()
            session.refresh(conversation)

            return conversation
        finally:
            try:
                next(session_gen)
            except StopIteration:
                pass  # Generator finished normally

    def update_conversation(self, conversation_id: str) -> None:
        """
        Update conversation's last activity timestamp
        """
        session_gen = get_session()
        session = next(session_gen)
        try:
            statement = select(Conversation).where(Conversation.id == conversation_id)
            conv = session.exec(statement).first()

            if conv:
                conv.updated_at = datetime.utcnow()
                session.add(conv)
                session.commit()
        finally:
            try:
                next(session_gen)
            except StopIteration:
                pass  # Generator finished normally

    def run(self, user_message: str, user_id: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Main method to run the Cohere chat with tool calling
        """
        # If no conversation_id is provided, create a new conversation
        if not conversation_id:
            conversation = self.create_conversation(user_id=user_id, title=f"Chat with {user_id[:8]}...")
            conversation_id = conversation.id
        else:
            # Verify conversation belongs to user
            session_gen = get_session()
            session = next(session_gen)
            try:
                statement = select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id
                )
                conv = session.exec(statement).first()

                if not conv:
                    return {
                        "error": "Conversation not found or you don't have permission to access it",
                        "conversation_id": conversation_id,
                        "response": "Sorry, I couldn't access this conversation.",
                        "tool_calls": []
                    }
            finally:
                try:
                    next(session_gen)
                except StopIteration:
                    pass  # Generator finished normally

        # Load conversation history
        history = self.load_conversation_history(conversation_id)

        # Save user message to database
        user_msg = self.save_message(
            conversation_id=conversation_id,
            role="USER",
            content=user_message
        )

        # Prepare the chat request with tools
        try:
            response = self.client.chat(
                message=user_message,
                chat_history=history[:-1] if history else [],  # Exclude current message from history
                model='command-r-08-2024',  # Use command-r-08-2024 for best tool calling
                tools=self.tools,
                connectors=[],  # No web search connectors for now
            )
        except Exception as e:
            print(f"Cohere API error: {str(e)}")  # Log the error
            # If there's an error with the Cohere API, return a default response
            default_response = {
                "conversation_id": conversation_id,
                "response": "Hello! I'm your AI assistant. I'm currently experiencing connectivity issues with my advanced features, but I'm here to help you manage your tasks. You can ask me to add, list, complete, or delete tasks.",
                "tool_calls": []
            }

            # Save default response to database
            self.save_message(
                conversation_id=conversation_id,
                role="ASSISTANT",
                content=default_response["response"],
                tool_calls=[],
                tool_call_results=[]
            )

            return default_response

        # Process the response
        ai_response = response.text

        # Handle tool calls if any
        tool_calls_executed = []
        if hasattr(response, 'tool_calls') and response.tool_calls:
            for tool_call in response.tool_calls:
                # Ensure the user_id is properly set in the tool parameters
                tool_parameters = tool_call.parameters.copy()
                tool_parameters['user_id'] = user_id  # Override with authenticated user_id
                
                # Execute the tool with the corrected parameters
                tool_result = execute_tool_call(
                    tool_name=tool_call.name,
                    tool_parameters=tool_parameters
                )

                # Record that this tool was called
                tool_calls_executed.append({
                    "name": tool_call.name,
                    "parameters": tool_parameters,  # Use corrected parameters
                    "result": tool_result
                })
                
        # Update conversation with latest activity
        self.update_conversation(conversation_id)

        # Save AI response to database
        assistant_msg = self.save_message(
            conversation_id=conversation_id,
            role="ASSISTANT",
            content=ai_response,
            tool_calls=[{
                "name": tc["name"],
                "parameters": tc["parameters"]
            } for tc in tool_calls_executed] if tool_calls_executed else [],
            tool_call_results=[tc["result"] for tc in tool_calls_executed] if tool_calls_executed else []
        )

        # Format the final response
        final_response = {
            "conversation_id": conversation_id,
            "response": ai_response,
            "tool_calls": [{
                "name": tc["name"],
                "parameters": tc["parameters"]
            } for tc in tool_calls_executed] if tool_calls_executed else []
        }

        # Add friendly multilingual response formatting
        if tool_calls_executed:
            # Add friendly messages for task operations in English and Urdu
            for tool_call in tool_calls_executed:
                if tool_call["name"] == "add_task" and "success" in tool_call["result"]:
                    final_response["response"] += "\n\n✅ Task added successfully! (Task add kar diya gaya!)"
                elif tool_call["name"] == "complete_task" and "success" in tool_call["result"]:
                    final_response["response"] += "\n\n✅ Task completed! (Task complete ho gaya!)"
                elif tool_call["name"] == "delete_task" and "success" in tool_call["result"]:
                    final_response["response"] += "\n\n🗑️ Task deleted! (Task delete kar diya gaya!)"
                elif tool_call["name"] == "get_user_profile" and "email" in tool_call["result"]:
                    email = tool_call["result"].get("email", "N/A")
                    final_response["response"] += f"\n\n📧 Your email is {email} (Aap ka email hai {email})"

        return final_response