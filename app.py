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