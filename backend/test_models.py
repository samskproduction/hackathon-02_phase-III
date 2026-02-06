import os
from dotenv import load_dotenv
import cohere

# Load environment variables
load_dotenv()

# Get the API key
api_key = os.getenv("COHERE_API_KEY")
print(f"API Key loaded: {'Yes' if api_key else 'No'}")

if api_key:
    try:
        # Initialize the client
        client = cohere.Client(api_key=api_key)
        
        # List available models
        models = client.models.list()
        print("Available models:")
        for model in models.models:
            print(f"- {model.name}")
        
    except Exception as e:
        print(f"Error with Cohere API: {str(e)}")
else:
    print("No API key found!")