from sqlalchemy import Column, Date, String
from .base import TimestampedModel

class Expense(TimestampedModel):
    __tablename__ = "expenses"
    date = Column(Date, nullable=False)
    category = Column(String(50), nullable=False)
    amount_encrypted = Column(String)
    description_encrypted = Column(String)