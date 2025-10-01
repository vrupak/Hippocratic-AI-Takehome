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

    # --- 2. User Input ---
    user_request = input("What kind of story would you like to hear? ")
    
    # --- 3. Agent Pipeline ---
    narrate("Analyzing your request and brainstorming some ideas")
    story_attributes = classifier.run(user_request)
    print(f"   - Genre: {story_attributes.get('genre')}")
    print(f"   - Theme: {story_attributes.get('theme')}")

    narrate("Coming up with the perfect title")
    story_title = title_agent.run(story_attributes)
    print("   - Title ready!")

    narrate("Writing the first draft of the story")
    story_draft = storyteller.run(story_attributes)
    print("   - Draft completed!")

    narrate("Asking a friendly editor for some feedback")
    feedback = judge.run(story_draft)
    print(f"   - Editor gave a score of {feedback.get('score_age_appropriateness', 'N/A')}/10")

    narrate("Polishing the final version based on the editor's notes")
    print_title(story_title)
    revisionist.run(story_draft, feedback)

if __name__ == "__main__":
    main()
