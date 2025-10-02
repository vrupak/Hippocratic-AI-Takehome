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
        
        # This is the fallback case
        if not suggestions:
            print("No improvement suggestions received. Presenting original draft.")
            # Use the new function for printing a plain string
            type_story_string(story_draft)
            return story_draft # <--- FIXED: Return the draft here
            # The original code implicitly returned None here.

        prompt = REVISIONIST_PROMPT.format(
            story_draft=story_draft,
            feedback=suggestions
        )
        
        # This is the normal streaming case
        story_stream = self.client.stream_call(prompt, temperature=0.7)
        # Use the function designed for handling streams
        final_story = stream_story(story_stream) # <--- Assign the returned string
        return final_story # <--- FIXED: Explicitly return the final story
    
    def revise_with_user_feedback(self, current_story: str, user_feedback: str) -> str:
        """Revises a story based on direct user feedback and returns the new version."""
        prompt = USER_FEEDBACK_PROMPT.format(
            current_story=current_story,
            user_feedback=user_feedback
        )
        # Use non-streaming call with moderate temperature for better control
        revised_story = self.client.call(prompt, temperature=0.4)
        # Display the revised story with typing effect
        type_story_string(revised_story)
        return revised_story