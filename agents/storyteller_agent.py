from llm.client import LanguageModelClient
from llm.prompts import STORYTELLER_PROMPT

class StorytellerAgent:
    """Agent responsible for writing the initial story draft."""

    def __init__(self, client: LanguageModelClient):
        self.client = client

    def run(self, story_attributes: dict) -> str:
        """
        Generates a story draft based on the classified attributes.
        """
        prompt = STORYTELLER_PROMPT.format(
            genre=story_attributes.get('genre', 'Friendship'),
            characters=", ".join(story_attributes.get('characters', [])),
            theme=story_attributes.get('theme', 'Kindness')
        )
        return self.client.call(prompt, temperature=0.7)
