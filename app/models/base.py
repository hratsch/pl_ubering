from sqlalchemy import Column, Integer, DateTime, func
from app.database import Base

class TimestampedModel(Base):
    __abstract__ = True  # DRY for all models
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())