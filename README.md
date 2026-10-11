# AI Expense Analyzer

A command-line app that turns plain-English expense descriptions into structured data, then answers questions about your spending using OpenAI function calling.

You type something like *"coffee 4.50, groceries 82.30, gas 45"*, and the app extracts each expense, stores it, and lets you ask things like *"What is my total spending?"* or *"How much did I spend on groceries?"*

## Features

- **Structured extraction**: converts free-form text into `{category, amount}` records using OpenAI Structured Outputs (Pydantic schema).
- **Tool-based answers**: the model never does the math itself. It calls Python functions, so totals and averages are exact.
- **Interactive loop**: add more expenses at any time and keep asking questions.

### Available tools

| Tool | Description |
|------|-------------|
| `calculate_total` | Total amount spent across all expenses |
| `category_total` | Total for a specific category (e.g. `coffee`, `gas`) |
| `largest_expense` | The single biggest expense |
| `count_expenses` | Number of expenses recorded |
| `average_expense` | Average amount per expense |

## Project Structure

```
AI_Expense_Analyzer/
├── main.py            # CLI entry point and interactive loop
├── clients.py         # OpenAI client, extraction, tools, and agent logic
├── models.py          # Pydantic models and the shared EXPENSES list
├── requirements.txt   # Python dependencies
└── .env               # API key (not committed)
```

## Requirements

- Python 3.10+ (developed on 3.13)
- An [OpenAI API key](https://platform.openai.com/api-keys)

## Setup

1. **Clone or download the project**, then open a terminal in the project folder.

2. **Create and activate a virtual environment** (recommended):

   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

   On macOS/Linux:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API key.** Create a `.env` file in the project root:

   ```
   OPENAI_API_KEY=your_api_key_here
   ```

   Make sure `.env` is listed in your `.gitignore` so the key is never committed.

## Usage

```bash
python main.py
```

Example session:

```
Enter your expenses: coffee 4.50, groceries 82.30, gas 45

Structured output from the AI:
{
  "expenses": [
    {"category": "coffee", "amount": 4.5},
    {"category": "groceries", "amount": 82.3},
    {"category": "gas", "amount": 45.0}
  ]
}

You: What is my total spending?
 [tool call] calculate_total({})
AI: Your total spending is $131.80.
```

### Commands

| Input | Action |
|-------|--------|
| Any question | Ask the AI about your expenses |
| `add` | Enter more expenses in plain English |
| `quit` / `exit` | Leave the program |

### Example questions

- What is my total spending?
- How much did I spend on groceries?
- What was my largest expense?
- How many expenses do I have?
- What is my average expense?

## How It Works

1. **Extraction**: `extract_expenses()` sends your text to `gpt-4o-mini` with a Pydantic schema (`ListExpenses`), so the response comes back as validated `{category, amount}` objects.
2. **Storage**: expenses are kept in the in-memory `EXPENSES` list defined in `models.py` and shared across modules.
3. **Question answering**: `ask_agent()` sends your question along with the tool definitions. The model picks a tool, the app runs the matching Python function, and the result is sent back so the model can phrase the final answer.

## Limitations

- Expenses are stored in memory only and are lost when the program exits.
- Categories are chosen by the model, so wording may vary (e.g. `coffee` vs. `cafe`).
- Amounts are plain numbers with no currency handling.

## Possible Improvements

- Persist expenses to a file or database (JSON, SQLite)
- Add dates and filter by time period
- Support currencies
- Add delete/edit commands
- Export a monthly summary to CSV

## License

Add your preferred license here (for example, MIT).
