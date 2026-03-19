import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

# Load API key
load_dotenv()

# Page setup
st.set_page_config(page_title="Agile Coach AI")
st.title("🧠 Agile Coach AI")

# Initialize model
llm = ChatGroq(model="llama-3.3-70b-versatile")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input box
user_input = st.chat_input("Ask your Agile question...")

if user_input:
    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Show user message
    st.chat_message("user").write(user_input)

    # Build conversation context
    conversation_text = ""
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        conversation_text += f"{role}: {content}\n"

    # Create coaching prompt
    prompt = f"""
You are an experienced Agile Coach with 20+ years experience.

Your coaching style:
- Ask powerful questions before giving solutions
- Focus on team ownership and accountability
- Encourage reflection
- Use Agile frameworks like Scrum and retrospectives

Conversation so far:
{conversation_text}

Now respond to this:
{user_input}

Respond like a real coach (ask questions, guide thinking, don't just give answers).
"""

    # Get AI response
    response = llm.invoke([HumanMessage(content=prompt)])

    # Show AI response
    st.chat_message("assistant").write(response.content)

    # Store AI response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response.content
    })