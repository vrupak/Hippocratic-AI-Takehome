from llm.client import LanguageModelClient
from llm.prompts import REVISIONIST_PROMPT, USER_FEEDBACK_PROMPT
from ui.printer import stream_story, type_story_string

class RevisionistAgent:
    """Agent responsible for revising the story based on feedback."""

    def __init__(self, client: LanguageModelClient):
        self.client = client

    def run(self, story_draft: str, feedback: dict) -> str: # <--- Added type hint for clarity
        """
        Streams the final, revised story to the console and returns the string.
        """
        suggestions = "\n- ".join(feedback.get('suggestions_for_improvement', []))
        
        if not suggestions:
            print("No improvement suggestions received. Presenting original draft.")
            type_story_string(story_draft)
            return story_draft

        prompt = REVISIONIST_PROMPT.format(
            story_draft=story_draft,
            feedback=suggestions
        )
        
        story_stream = self.client.stream_call(prompt, temperature=0.7)
        final_story = stream_story(story_stream)
        return final_story
    
    def revise_with_user_feedback(self, current_story: str, user_feedback: str) -> str:
        """Revises a story based on direct user feedback and returns the new version."""
        prompt = USER_FEEDBACK_PROMPT.format(
            current_story=current_story,
            user_feedback=user_feedback
        )
        revised_story = self.client.call(prompt, temperature=0.4)
        type_story_string(revised_story)
        return revised_story