from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class ExpenseCreate(BaseModel):
    date: date
    category: str
    amount: float
    description: Optional[str] = None

class ExpenseResponse(BaseModel):
    id: int
    date: date
    category: str
    amount: float
    description: Optional[str]
    created_at: datetime
    updated_at: datetime