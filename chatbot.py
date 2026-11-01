import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# the chat object remembers old messages
chat = client.chats.create(model="gemini-3.5-flash-lite")

print("Chatbot ready! Type 'exit' to stop.\n")

while True:
    user = input("You: ")
    if user.lower() in ["exit", "quit"]:
        print("Bye!")
        break

    reply = None
    for attempt in range(3):
        try:
            response = chat.send_message(user)
            reply = response.text
            break
        except Exception as e:
            if "503" in str(e) or "429" in str(e):
                print(f"Server busy, retrying ({attempt + 1}/3)...")
                time.sleep(5)
            else:
                reply = f"Error: {e}"
                break

    if reply is None:
        reply = "Server is still busy. Please try again later."
    print("Bot:", reply, "\n")