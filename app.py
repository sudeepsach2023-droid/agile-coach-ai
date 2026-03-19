import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

# Load env
load_dotenv()

# Page config
st.set_page_config(page_title="Sudeep Agile Coach Agent", page_icon="🤖")

# Title
st.title("🤖 Sudeep Agile Coach Agent")
st.caption("Your personal Agile & Scrum coaching assistant")

# Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages (ChatGPT style)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input (modern Streamlit UI)
user_input = st.chat_input("Ask your Agile question...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response
    response = llm.invoke([
        HumanMessage(content=f"Act as an Agile Coach. {user_input}")
    ])

    # Show assistant response
    with st.chat_message("assistant"):
        st.markdown(response.content)

    # Save response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response.content
    })