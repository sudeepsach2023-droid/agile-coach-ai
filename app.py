import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

# Load environment variables
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

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔥 Coaching function with persona + memory
def get_coach_response(user_input, chat_history):
    messages = []

    # Coaching persona
    system_prompt = """
You are an experienced Agile Coach with 20+ years of experience.

Your coaching style:
- Ask clarifying questions before jumping to solutions
- Focus on root causes, not symptoms
- Encourage team ownership and accountability
- Use Scrum, Kanban, and Agile principles where relevant
- Be practical and concise

Always structure your response as:
1. Understanding the situation
2. Possible root causes
3. Actionable steps
4. Coaching questions to reflect

Be a coach, not just an advisor.
"""

    messages.append(HumanMessage(content=system_prompt))

    # Add chat history (memory)
    for msg in chat_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(HumanMessage(content=f"Coach: {msg['content']}"))

    # Current user input
    messages.append(HumanMessage(content=user_input))

    # Get response
    response = llm.invoke(messages)

    return response.content

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask your Agile question...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get AI response
    response_text = get_coach_response(user_input, st.session_state.messages)

    # Show AI response
    with st.chat_message("assistant"):
        st.markdown(response_text)

    # Save response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text
    })