
import google.generativeai as genai
from dotenv import load_dotenv
from .retry import retry_gemini_api
import os
import tiktoken
from jinja2 import Template
from .logging import log

class Gemini:
    def __init__(self):
        with load_dotenv():
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                
                raise ValueError("GOOGLE_API_KEY not found in environment variables.")

        genai.configure(api_key=api_key)
        

        try:
            model_name = "gemini-1.5-flash"
            self.model = genai.GenerativeModel(model_name)
        except Exception as e:
            
            raise

class GeminiChat(Gemini):

    @retry_gemini_api
    def generate(self, messages: list, **kwargs):
        try:
            response = self.model.generate_content(self.messages, stream=True)
            for chunk in response:
                yield chunk.text
        except Exception as e:
            
            yield f"I apologize, but I encountered an error: {e}"


class Embedding:

    def generate(self, text: str) -> list[float]:
        return self.client.embeddings.create(
            input=text, model=os.environ.get("EMBEDDING_MODEL_DEPLOYMENT_NAME")
        ).data[0].embedding


def count_token(text: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def render_with_token_limit(template: Template, token_limit: int, **kwargs) -> str:
    text = template.render(**kwargs)
    token_count = count_token(text)
    if token_count > token_limit:
        message = f"token count {token_count} exceeds limit {token_limit}"
        
        raise ValueError(message)
    return text


if __name__ == "__main__":
    # Create an instance of GeminiChat
    gemini_chat = GeminiChat()

    # Define the initial messages
    messages = [{"role": "system", "parts": ["You are a helpful AI assistant."]}]

    while True:
        # Get user input
        user_input = input("You: ")

        # Exit the loop if the user input is 'exit'
        if user_input.lower() == 'exit':
            break

        # Append user input to messages
        messages.append({"role": "user", "parts": [user_input]})

        # Generate response
        response = gemini_chat.generate(messages)

        # Print the response
        for chunk in response:
            print(chunk, end="")

        print()  # Add a newline after each response