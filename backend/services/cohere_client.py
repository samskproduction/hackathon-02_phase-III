import os
import cohere
from dotenv import load_dotenv

load_dotenv()

class CohereClient:
    def __init__(self):
        self.api_key = os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY environment variable is not set")

        self.client = cohere.Client(api_key=self.api_key)

    def get_client(self):
        return self.client

    def chat(self, message, conversation_id=None, **kwargs):
        """
        Wrapper for Cohere's chat functionality
        """
        # Prepare chat history if conversation_id is provided
        # In a real implementation, this would load history from database
        chat_history = kwargs.get('chat_history', [])

        # Call Cohere's chat endpoint
        response = self.client.chat(
            message=message,
            conversation_id=conversation_id,
            model=kwargs.get('model', 'command-r-08-2024'),  # Use command-r-08-2024 as default
            chat_history=chat_history,
            **kwargs
        )

        return response

# Global instance
cohere_client = CohereClient()