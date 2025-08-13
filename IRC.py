import time
import random
from datetime import datetime
from gpt4all import GPT4All
from rich.console import Console

console = Console()

# Initialize model (small CPU LLM)
model = GPT4All("gpt4all-j")  # ensure model file is present or auto-download

# Define AI users with personalities
ai_users = [
    {"name": "GhostHunter92", "personality": "conspiracy theorist"},
    {"name": "FactCheckBot", "personality": "sarcastic, pedantic"},
    {"name": "WeirdAlex", "personality": "dramatic, easily impressed"},
    {"name": "TechieTom", "personality": "tech geek, logical"},
    {"name": "ChattyCathy", "personality": "friendly, chatterbox"}
]

chat_log = []

# Helper: current timestamp
def timestamp():
    return datetime.now().strftime("%H:%M")

# Generate AI message based on context
def generate_ai_message(user):
    context = "\n".join([f"{m['user']}: {m['text']}" for m in chat_log[-10:]])
    prompt = f"""
You are {user['name']}, a {user['personality']} in an IRC channel.
The conversation so far is:
{context}
Generate a short, chatty IRC message in character about the topic.
"""
    response = model.generate(prompt, max_tokens=50)
    return response.strip()

# Display message instantly
def display_message(user, text):
    chat_log.append({"user": user, "text": text})
    console.print(f"[{timestamp()}] <{user}> {text}")

# AI chatter loop
def start_ai_conversation():
    for user in ai_users:
        def ai_loop(u=user):
            while True:
                delay = random.uniform(5, 15)  # 5–15 sec
                time.sleep(delay)
                msg = generate_ai_message(u)
                display_message(u["name"], msg)
        import threading
        threading.Thread(target=ai_loop, daemon=True).start()

# Main
def main():
    channel = console.input("Enter channel name: ").strip() or "general"
    display_message("System", f"Channel {channel} created. Topic: Welcome to {channel}!")
    
    start_ai_conversation()

    # Player input loop
    while True:
        user_msg = console.input("[You] ").strip()
        if user_msg.lower() in ("quit", "exit"):
            break
        display_message("You", user_msg)

if __name__ == "__main__":
    main()
