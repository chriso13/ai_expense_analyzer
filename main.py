import json
from clients import extract_expenses, ask_agent
from models import EXPENSES


 
def main()->None:
    text = input("Enter your expenses: ")
    EXPENSES.extend(extract_expenses(text))
 
    print("\nStructured output from the AI:")
    print(json.dumps({"expenses": EXPENSES}, indent=2))

    print("\nAsk questions (examples below). Type 'add' to add more expenses, 'quit' to exit.")
    print("  - What is my total spending?")
    print("  - How much did I spend on groceries?")
    print("  - What was my largest expense?")
    print("  - How many expenses do I have?")
    print("  - What is my average expense?\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in {"quit", "exit"}:
            break
        if question.lower() == "add":
            more = input("Enter more expenses: ")
            EXPENSES.extend(extract_expenses(more))
            print(f" Now tracking {len(EXPENSES)} expenses.")
            continue
        if not question:
            continue

        print("AI:", ask_agent(question))

if __name__ =="__main__":
    main()






