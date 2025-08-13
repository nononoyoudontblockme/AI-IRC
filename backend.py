from flask import Flask, request, jsonify
from gpt4all import GPT4All
import asyncio
import random
from datetime import datetime

app = Flask(__name__)

# ---- LOAD LLaMA MODEL (auto-download) ----
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")

# ---- AI USERS ----
users = [
    {"name": "GhostHunter92", "personality": "excited, conspiracy theorist"},
    {"name": "FactCheckBot", "personality": "sarcastic, pedantic"},
    {"name": "WeirdAlex", "personality": "dramatic, easily impressed"},
    {"name": "TechieTom", "personality": "tech geek, logical"},
    {"name": "ChattyCathy", "personality": "friendly, chatterbox"},
]

chat_log = []

# ---- HELPER FUNCTION ----
def generate_ai_messages(player_message=None):
    recent = "\n".join([f"[{m['time']}] <{m['user']}> {m['text']}" for m in chat_log[-10:]])
    prompt = f"""
Users: {', '.join([u['name'] for u in users])}
Recent messages:
{recent}
Player: {player_message or ''}

Task: Generate 1-2 new messages from AI users in the format:
[HH:MM] <username> message
"""
    try:
        with model.chat_session() as session:
            text = session.generate(prompt, max_tokens=150)
        new_msgs = []
        for line in text.split("\n"):
            if line.startswith("[") and "] <" in line:
                time_part = line.split("] <")[0][1:]
                rest = line.split("] <")[1]
                user = rest.split(">")[0]
                msg = ">".join(rest.split(">")[1:]).strip()
                new_msgs.append({"time": time_part, "user": user, "text": msg})
        if not new_msgs:
            user = random.choice(users)["name"]
            new_msgs.append({"time": datetime.now().strftime("%H:%M"), "user": user, "text": "Hello everyone!"})
        return new_msgs
    except Exception as e:
        return [{"time": datetime.now().strftime("%H:%M"), "user": "System", "text": str(e)}]

# ---- ROUTES ----
@app.route("/send", methods=["POST"])
def send():
    data = request.json
    player_message = data.get("message", "")
    chat_log.append({"time": datetime.now().strftime("%H:%M"), "user": "You", "text": player_message})

    # Generate AI messages
    ai_msgs = generate_ai_messages(player_message)
    chat_log.extend(ai_msgs)

    return jsonify(chat_log[-20:])  # return last 20 messages

@app.route("/history", methods=["GET"])
def history():
    return jsonify(chat_log[-20:])

if __name__ == "__main__":
    app.run(debug=True)
