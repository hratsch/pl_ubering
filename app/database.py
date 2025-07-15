from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import load_config

config = load_config()
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    # For migrations, use Alembic CLI: alembic upgrade head
    # Run once: alembic init migrations
    # Then edit migrations/env.py to use Base.metadata
    # Base.metadata.create_all(bind=engine)  # For dev, create tables if missing
    pass