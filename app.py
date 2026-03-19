import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Streamlit page settings
st.set_page_config(page_title="🤖 Agile Coach AI", page_icon="🤖")

# Title
st.title("🤖 Agile Coach AI")
st.write("Ask me anything about Agile, Scrum, or team coaching!")

# Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# Initialize session state for conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
user_input = st.text_input("Your question:", key="input")

if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate AI response
    response = llm.invoke([
        HumanMessage(content=f"Act as an Agile Coach. {user_input}")
    ])

    # Save AI message
    st.session_state.messages.append({"role": "assistant", "content": response.content})

# Display conversation
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Coach:** {msg['content']}")