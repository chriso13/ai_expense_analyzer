from openai import OpenAI
from typing import List
from dotenv import load_dotenv
import json
import os

from models import  ListExpenses, EXPENSES

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"

if not api_key:
    raise ValueError("OPENAI_API_KEY is not found")

client = OpenAI(api_key=api_key)


def extract_expenses(user_message: str)->List[dict]:

    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {
                "role": "system", 
                "content":("extract every expense from user message"
                           "Use short, lowercase category names. "
                            "Amounts are plain numbers without currency symbols."
                ),
        

            },
            {"role": "user","content": user_message},
        ],
        response_format=ListExpenses

    )

    response = completion.choices[0].message

    if response.parsed is None:
        raise ValueError(f"Could not extract expenses: {response.refusal}")

    return [e.model_dump() for e in response.parsed.expenses]
    
# sum all expenses
def calculate_total()-> float:
    return round( sum(e["amount"] for e in EXPENSES),2)

# Sum of expenses for one category
def category_total(category: str)-> float:

    return round( sum(e["amount"] for e in EXPENSES if e["category"].lower()==category.lower()),2,)

# bigest expense
def largest_expense()->dict:
    return max(EXPENSES, key=lambda e: e["amount"])

# how many expenses we have
def count_expenses()->int:
    return len(EXPENSES)

def average_expense()->float:
    if not EXPENSES:
        return 0.0

    return round(calculate_total()/count_expenses(),2)

TOOL_REGISTRY ={
    "calculate_total": calculate_total,
    "category_total": category_total,
    "largest_expense": largest_expense,
    "count_expenses":count_expenses,
    "average_expense": average_expense
}


# Schema for tools that take no parameters.

def _tool(name: str, description: str, properties: dict | None = None) -> dict:
    properties = properties or {}
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": list(properties.keys()),
                "additionalProperties": False,
            },
            "strict": True,
        },
    }


TOOLS = [
    _tool("calculate_total", "Get the total amount spent across all expenses."),
    _tool(
        "category_total",
        "Get total amount for a specific category of expenses.",
        {"category": {"type": "string", "description": "category name, e.g. 'coffee', 'gas'"}},
    ),
    _tool("largest_expense", "Get the biggest expense."),
    _tool("count_expenses", "Count how many expenses were recorded."),
    _tool("average_expense", "Get the average amount per expense."),
]



def ask_agent(question: str)->str:
    message =[
        {"role":"system",
         "content":("you are an expense assistance, don't calculate numbers yourself."
                    "Always use the provided tools to get figures, then answer clearly.")                   


        },
        {"role":"user", "content": question}
    ]


    response = client.chat.completions.create(
        model=MODEL,
        messages=message,
        tools=TOOLS,
        tool_choice="auto"
    )

    assistance_message = response.choices[0].message

    if not assistance_message.tool_calls:
        return assistance_message.content

    message.append(assistance_message)

    for tool_call in assistance_message.tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        print(f" [tool call] {name}({args})")

        result = TOOL_REGISTRY[name](**args)

        message.append(
            {
                "role":"tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            }
        )

    final = client.chat.completions.create(model=MODEL,messages=message)
    return final.choices[0].message.content