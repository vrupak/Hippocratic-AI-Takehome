from llm.client import LanguageModelClient
from llm.prompts import REVISIONIST_PROMPT, USER_FEEDBACK_PROMPT
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
    
    def revise_with_user_feedback(self, current_story: str, user_feedback: str) -> str:
        """Revises a story based on direct user feedback and returns the new version."""
        prompt = USER_FEEDBACK_PROMPT.format(
            current_story=current_story,
            user_feedback=user_feedback
        )
        story_stream = self.client.stream_call(prompt, temperature=0.7)
        revised_story = stream_story(story_stream)
        return revised_story

