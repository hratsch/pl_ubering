from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class TripCreate(BaseModel):
    date: date
    gross_earnings: float
    miles_driven: Optional[float] = None
    hours_worked: Optional[float] = None
    gas_cost: Optional[float] = None
    tolls: Optional[float] = None

class TripResponse(BaseModel):
    id: int
    date: date
    gross_earnings: float
    miles_driven: Optional[float]
    hours_worked: Optional[float]
    gas_cost: Optional[float]
    tolls: Optional[float]
    created_at: datetime
    updated_at: datetime