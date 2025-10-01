import time
import sys
import pyfiglet

def narrate(text: str):
    """Prints a narrative step in the process with a typing effect."""
    print(f"\n> {text}", end="", flush=True)
    time.sleep(0.5)
    print(".", end="", flush=True)
    time.sleep(0.5)
    print(".", end="", flush=True)
    time.sleep(0.5)
    print(".", flush=True)
    time.sleep(0.5)

def print_title(title: str):
    """Prints a stylized ASCII art title using pyfiglet."""
    try:
        ascii_title = pyfiglet.figlet_format(title, font="standard")
        print("\n" + "="*70)
        print(ascii_title)
        print("="*70 + "\n")
    except Exception:
        # Fallback in case pyfiglet fails or font is not found
        print(f"\n*** {title} ***\n")

def type_story_string(story: str):
    """Prints a story from a plain string with a typing effect."""
    for char in story:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
    print("\n")

def stream_story(story_stream):
    """
    Prints the story character by character from an OpenAI stream object.
    This version robustly handles the stream's structure.
    """
    full_response = ""
    for chunk in story_stream:
        # Safely check if the chunk has the content we expect
        if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_response += content
            sys.stdout.write(content)
            sys.stdout.flush()
    print("\n")
    return full_response

