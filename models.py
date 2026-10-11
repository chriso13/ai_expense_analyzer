from pydantic import BaseModel
from typing import List

class Expense(BaseModel):
    category: str
    amount: float

class ListExpenses(BaseModel):

    expenses: List[Expense]

EXPENSES: List[dict]=[]
