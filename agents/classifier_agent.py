import json
from llm.client import LanguageModelClient
from llm.prompts import CLASSIFIER_PROMPT

class ClassifierAgent:
    """Agent responsible for classifying the user's story request."""

    def __init__(self, client: LanguageModelClient):
        self.client = client

    def run(self, user_request: str) -> dict:
        """
        Analyzes the user request and returns a dictionary of attributes.
        """
        prompt = CLASSIFIER_PROMPT.format(user_request=user_request)
        response_text = self.client.call(prompt, temperature=0.1)

        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            print("Classifier agent failed to return valid JSON. Returning default values.")
            return {
                "genre": "Friendship",
                "characters": ["a kind animal", "a curious child"],
                "theme": "The importance of being kind to others."
            }
