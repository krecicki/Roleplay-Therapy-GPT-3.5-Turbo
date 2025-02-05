# Updated from the old version
import os
from openai import OpenAI
import time
from typing import Optional

# Configuration
TOPIC = "Discuss a boy's love of his mother."
ACTORS = ("Carl Jung", "Sigmund Freud")
MAX_TURNS = 20  # Total exchanges (10 each)
MODEL = "gpt-4-turbo-preview"  # Use latest model
MAX_TOKENS = 150
TEMPERATURE = 0.7

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_response(
    actor: str,
    other_actor: str,
    conversation_history: list[tuple[str, str]],
    topic: str,
    retries: int = 3
) -> Optional[str]:
    """
    Generates a response using modern chat completion with conversation history
    and error handling.
    """
    system_prompt = f"""You are {actor}, a renowned psychologist. You are engaged in a thoughtful 
    discussion with {other_actor} about {topic}. Maintain your theoretical perspective while 
    responding directly to your colleague's most recent argument. Keep responses concise 
    (1-2 sentences) and professional."""
    
    # Build message history with alternating speaker/listener roles
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history with alternating roles
    for i, (speaker, message) in enumerate(conversation_history[-4:]):  # Keep last 4 exchanges
        role = "assistant" if speaker == actor else "user"
        messages.append({"role": role, "content": f"{speaker}: {message}"})

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if attempt == retries - 1:
                print(f"Error after {retries} attempts: {e}")
                return None
            time.sleep(2 ** attempt)

def conduct_dialog() -> None:
    """Manages the conversation flow between two actors with proper turn-taking"""
    conversation_history = []
    print(f"\n{ACTORS[0]} and {ACTORS[1]} discussing: {TOPIC}\n{'='*50}")

    # Initialize with first actor's opening statement
    current_speaker, next_speaker = ACTORS
    opening_statement = generate_response(
        current_speaker, 
        next_speaker,
        [("Moderator", TOPIC)],
        TOPIC
    )
    
    if not opening_statement:
        print("Failed to initialize conversation")
        return

    print(f"{current_speaker}: {opening_statement}")
    conversation_history.append((current_speaker, opening_statement))

    # Alternate speakers for specified turns
    for _ in range(MAX_TURNS):
        current_speaker, next_speaker = next_speaker, current_speaker
        
        response = generate_response(
            current_speaker,
            next_speaker,
            conversation_history,
            TOPIC
        )
        
        if not response:
            print(f"{current_speaker}: [Response unavailable]")
            continue
        
        print(f"\n{current_speaker}: {response}")
        conversation_history.append((current_speaker, response))
        time.sleep(1)  # Pacing for readability

if __name__ == "__main__":
    conduct_dialog()
