import json
from llm.client import LanguageModelClient
from llm.prompts import JUDGE_PROMPT

class JudgeAgent:
    """Agent responsible for critiquing the story draft."""

    def __init__(self, client: LanguageModelClient):
        self.client = client

    def run(self, story_draft: str) -> dict:
        """
        Analyzes the story draft and returns structured feedback.
        """
        prompt = JUDGE_PROMPT.format(story_draft=story_draft)
        response_text = self.client.call(prompt, temperature=0.1)

        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            print("Judge agent failed to return valid JSON. Returning empty feedback.")
            return {}
