from llm.client import LanguageModelClient
from agents.classifier_agent import ClassifierAgent
from agents.storyteller_agent import StorytellerAgent
from agents.judge_agent import JudgeAgent
from agents.revisionist_agent import RevisionistAgent
from agents.title_agent import TitleAgent
from ui.printer import narrate, print_title

"""
Before submitting the assignment, describe here in a few sentences what you would have built next if you spent 2 more hours on this project:

"""

def main():
    """The main function to run the story generation pipeline."""
    # --- 1. Initialization ---
    client = LanguageModelClient()
    classifier = ClassifierAgent(client)
    storyteller = StorytellerAgent(client)
    judge = JudgeAgent(client)
    revisionist = RevisionistAgent(client)
    title_agent = TitleAgent(client)

    # --- 2. User Input & Initial Generation (Happens Once) ---
    user_request = input("What kind of story would you like to hear? ")
    
    narrate("Analyzing your request and brainstorming some ideas")
    story_attributes = classifier.run(user_request)
    
    narrate("Coming up with the perfect title")
    story_title = title_agent.run(story_attributes)

    narrate("Writing the first draft of the story")
    story_draft = storyteller.run(story_attributes)

    narrate("Asking a friendly editor for some feedback")
    feedback = judge.run(story_draft)
    
    narrate("Polishing the final version based on the editor's notes")
    # This is the first, complete version of the story
    print_title(story_title)
    current_story = revisionist.run(story_draft, feedback)

    # --- 3. User Feedback Loop ---
    while True:
        prompt_text = "\nWhat do you think? Are you happy with the story, or would you like to make any changes?\n(e.g., 'make the squirrel brave' or type 'exit' to finish)\n> "
        user_feedback = input(prompt_text)

        if user_feedback.lower() in ['exit', 'quit', 'done', 'yes', 'i am happy']:
            print("\nGreat! Enjoy the story. ✨")
            break

        narrate("Revising the story based on your feedback")
        # The story is updated with each revision
        current_story = revisionist.revise_with_user_feedback(current_story, user_feedback)

if __name__ == "__main__":
    main()