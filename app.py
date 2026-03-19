import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

# Load env variables
load_dotenv()

# Page config
st.set_page_config(page_title="Agile Coach AI", page_icon="🤖")

# Title
st.title("🤖 Agile Coach AI")

# Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# Session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
user_input = st.text_input("Ask your Agile question:")

if user_input:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get response
    response = llm.invoke([
        HumanMessage(content=f"Act as an Agile Coach. {user_input}")
    ])

    # Store response
    st.session_state.messages.append({"role": "assistant", "content": response.content})

# Display chat
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Coach:** {msg['content']}")