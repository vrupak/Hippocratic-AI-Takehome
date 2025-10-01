import os
import openai
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found. Please set it in your .env file.")
openai.api_key = API_KEY

# --- CLIENT ---
class LanguageModelClient:
    """A wrapper for the OpenAI API client."""

    def __init__(self, model="gpt-3.5-turbo"):
        """Initializes the client with a specified model."""
        self.model = model

    def call(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1500) -> str:
        """
        Calls the OpenAI API with a given prompt.
        Returns the text response.
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False,
            )
            return response.choices[0].message["content"]
        except Exception as e:
            print(f"An error occurred during the API call: {e}")
            return "" # Return empty string on failure

    def stream_call(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1500):
        """
        Calls the OpenAI API and streams the response.
        Yields chunks of the response as they are received.
        """
        try:
            response_stream = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
            )
            for chunk in response_stream:
                yield chunk
        except Exception as e:
            print(f"\nAn error occurred during the streaming API call: {e}")
