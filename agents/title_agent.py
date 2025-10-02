from llm.client import LanguageModelClient
from llm.prompts import TITLE_PROMPT

class TitleAgent:
    """
    Agent responsible for generating a creative title for the story.
    """

    def __init__(self, client: LanguageModelClient):
        self.client = client

    def run(self, story_attributes: dict) -> str:
        """
        Generates a short, whimsical, and child-friendly title based on the
        story's attributes.

        Args:
            story_attributes: A dictionary containing genre, characters, and theme.

        Returns:
            A string containing the generated story title.
        """
        prompt = TITLE_PROMPT.format(
            genre=story_attributes.get('genre', 'Adventure'),
            characters=", ".join(story_attributes.get('characters', ['a brave hero'])),
            theme=story_attributes.get('theme', 'overcoming challenges')
        )
        
        title = self.client.call(prompt, temperature=0.6, max_tokens=30)
        
        return title.strip().replace('"', '')
