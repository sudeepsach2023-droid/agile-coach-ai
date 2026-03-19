import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Title
st.title("🤖 Agile Coach AI")

# Initialize LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# Input box
user_input = st.text_input("Ask your Agile question:")

# Response
if user_input:
    response = llm.invoke([
        HumanMessage(content=f"Act as an Agile Coach. {user_input}")
    ])
    
    st.write("### Coach Response:")
    st.write(response.content)