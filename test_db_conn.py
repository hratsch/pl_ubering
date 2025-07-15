from app.database import engine
from sqlalchemy import text

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Connection successful:", result.scalar())
        # List tables
        tables = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        print("Tables:", [row[0] for row in tables])
except Exception as e:
    print("Connection failed:", str(e))