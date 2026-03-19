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

# Sidebar (UI polish)
st.sidebar.title("About")
st.sidebar.write("Built by Sudeep - Agile Coach")

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []

# Mode selection
mode = st.selectbox(
    "Select Coaching Mode",
    ["General Coaching", "Scrum Master Support", "Retrospective Facilitator", "Leadership Coaching"]
)

# Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔥 Coaching function
def get_coach_response(user_input, chat_history, mode):
    messages = []

    # Mode-based persona
    mode_instruction = {
        "General Coaching": "Focus on general Agile coaching and team improvement.",
        "Scrum Master Support": "Act as an expert Scrum Master helping with ceremonies and impediments.",
        "Retrospective Facilitator": "Help design and facilitate effective retrospectives.",
        "Leadership Coaching": "Coach leaders on Agile mindset, culture, and transformation."
    }

    system_prompt = f"""
You are an experienced Agile Coach with 20+ years of experience.

Mode: {mode}
{mode_instruction[mode]}

Your coaching style:
- Ask clarifying questions before solutions
- Focus on root causes
- Encourage ownership and accountability
- Be practical and concise

Always structure your response as:
1. Understanding the situation
2. Possible root causes
3. Actionable steps
4. Coaching questions

Be a coach, not just an advisor.
"""

    messages.append(HumanMessage(content=system_prompt))

    # Add memory
    for msg in chat_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(HumanMessage(content=f"Coach: {msg['content']}"))

    messages.append(HumanMessage(content=user_input))

    response = llm.invoke(messages)
    return response.content


# 🎯 Quick Coaching Buttons
st.write("### ⚡ Quick Coaching Help")

col1, col2, col3 = st.columns(3)

quick_prompt = None

if col1.button("Sprint Retrospective"):
    quick_prompt = "Help me run an effective sprint retrospective"

if col2.button("Team Conflict"):
    quick_prompt = "How do I resolve conflict in my Scrum team?"

if col3.button("Improve Accountability"):
    quick_prompt = "How to improve accountability in my team?"

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask your Agile question...")

# Use quick prompt if clicked
if quick_prompt:
    user_input = quick_prompt

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response
    response_text = get_coach_response(user_input, st.session_state.messages, mode)

    # Show response
    with st.chat_message("assistant"):
        st.markdown(response_text)

    # Save response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text
    })