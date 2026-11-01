import os
import time
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 My AI Chatbot")
st.caption("Powered by a cloud AI API (Google Gemini)")

MODEL = "gemini-3.5-flash-lite"

@st.cache_resource
def get_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

client = get_client()

# keep chat and messages while the page is open
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(model=MODEL)
    st.session_state.messages = []

# button to start a new chat
if st.sidebar.button("New chat"):
    st.session_state.chat = client.chats.create(model=MODEL)
    st.session_state.messages = []
    st.rerun()

# show old messages
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# input box at the bottom
prompt = st.chat_input("Type your message...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    reply = None
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            for attempt in range(3):
                try:
                    response = st.session_state.chat.send_message(prompt)
                    reply = response.text
                    break
                except Exception as e:
                    if "503" in str(e) or "429" in str(e):
                        time.sleep(5)
                    else:
                        reply = f"Error: {e}"
                        break
        if reply is None:
            reply = "Server is busy. Please try again later."
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})