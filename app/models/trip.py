from sqlalchemy import Column, Date, Numeric, String
from .base import TimestampedModel

class Trip(TimestampedModel):
    __tablename__ = "trips"
    date = Column(Date, nullable=False)
    gross_earnings_encrypted = Column(String)  # Encrypted as string
    miles_driven = Column(Numeric(10, 2))
    hours_worked = Column(Numeric(5, 2))
    gas_cost_encrypted = Column(String)
    tolls_encrypted = Column(String)