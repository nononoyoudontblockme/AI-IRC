import os
import time
import random
import threading
from datetime import datetime
from gpt4all import GPT4All
from rich.console import Console

console = Console()

# --- Auto-download or load small CPU LLM ---
MODEL_NAME = "gpt4all-j"
model_path = f"{MODEL_NAME}.bin"  # adjust if needed

console.print("Loading model, please wait...")
model = GPT4All(MODEL_NAME)  # GPT4All will auto-download if missing
console.print("Model loaded!\n")

# --- AI users with personalities ---
ai_users = [
    {"name": "GhostHunter92", "personality": "conspiracy theorist"},
    {"name": "FactCheckBot", "personality": "sarcastic, pedantic"},
    {"name": "WeirdAlex", "personality": "dramatic, easily impressed"},
    {"name": "TechieTom", "personality": "tech geek, logical"},
    {"name": "ChattyCathy", "personality": "friendly, chatterbox"}
]

chat_log = []

# --- Helper functions ---
def timestamp():
    return datetime.now().strftime("%H:%M")

def display_message(user, text):
    chat_log.append({"user": user, "text": text})
    console.print(f"[{timestamp()}] <{user}> {text}")

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

# --- AI chatter loop ---
def ai_loop(user):
    while True:
        delay = random.uniform(5, 15)  # 5–15 sec
        time.sleep(delay)
        msg = generate_ai_message(user)
        display_message(user["name"], msg)

def start_ai_conversation():
    for user in ai_users:
        threading.Thread(target=ai_loop, args=(user,), daemon=True).start()

# --- Main ---
def main():
    channel = console.input("Enter channel name: ").strip() or "general"
    display_message("System", f"Channel {channel} created. Topic: Welcome to {channel}!")
    
    start_ai_conversation()

    while True:
        user_msg = console.input("[You] ").strip()
        if user_msg.lower() in ("quit", "exit"):
            break
        display_message("You", user_msg)

if __name__ == "__main__":
    main()
