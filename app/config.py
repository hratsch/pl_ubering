from dataclasses import dataclass
from os import getenv

@dataclass
class Config:
    DATABASE_URL: str = getenv("DATABASE_URL", "postgresql://hugh:december90@localhost/uberpl_db")
    JWT_SECRET: str = getenv("JWT_SECRET", "your-super-secret-jwt-key-change-this-in-production")
    ENCRYPTION_PASSWORD: str = getenv("ENCRYPTION_PASSWORD", "your-encryption-password")
    PORT: str = getenv("PORT", "8000")
    ENVIRONMENT: str = getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = getenv("LOG_LEVEL", "info")

def load_config() -> Config:
    return Config()
