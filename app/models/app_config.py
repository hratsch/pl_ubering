from sqlalchemy import Column, String
from .base import TimestampedModel

class AppConfig(TimestampedModel):
    __tablename__ = "app_config"
    encryption_key_hash = Column(String(255), nullable=False)