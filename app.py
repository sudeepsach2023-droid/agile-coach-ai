from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile")

print("Agile Coach AI is ready! Type 'exit' to stop.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    response = llm.invoke([
        HumanMessage(content=f"Act as an Agile Coach. {user_input}")
    ])

    print("\nCoach:", response.content)
    print("-" * 50)