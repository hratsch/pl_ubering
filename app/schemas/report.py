from pydantic import BaseModel

class ChartData(BaseModel):
    date: str
    earnings: float
    expenses: float
    profit: float