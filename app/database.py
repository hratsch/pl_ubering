from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import load_config

config = load_config()
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

if config.ENVIRONMENT == "production" and "change-this" in config.JWT_SECRET:
    raise ValueError("Update JWT_SECRET for production")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    
    Base.metadata.create_all(bind=engine)  # For dev, create tables if missing