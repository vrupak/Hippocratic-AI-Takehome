from llm.client import LanguageModelClient
from llm.prompts import REVISIONIST_PROMPT
# Import both printing functions
from ui.printer import stream_story, type_story_string

class RevisionistAgent:
    """Agent responsible for revising the story based on feedback."""

    def __init__(self, client: LanguageModelClient):
        self.client = client

    def run(self, story_draft: str, feedback: dict):
        """
        Streams the final, revised story to the console.
        """
        suggestions = "\n- ".join(feedback.get('suggestions_for_improvement', []))
        
        # This is the fallback case
        if not suggestions:
            print("No improvement suggestions received. Presenting original draft.")
            # Use the new function for printing a plain string
            type_story_string(story_draft)
            return

        prompt = REVISIONIST_PROMPT.format(
            story_draft=story_draft,
            feedback=suggestions
        )
        
        # This is the normal streaming case
        story_stream = self.client.stream_call(prompt, temperature=0.7)
        # Use the function designed for handling streams
        stream_story(story_stream)

