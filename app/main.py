from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn

from app.config import load_config
from app.database import init_db
from app.routers import auth, trips, expenses  # Import routers

load_dotenv()  # Load .env
config = load_config()

app = FastAPI(title="Uber P&L API")

# Include routers
app.include_router(auth.router, prefix="/api/auth")
app.include_router(trips.router, prefix="/api/trips", tags=["trips"])
app.include_router(expenses.router, prefix="/api/expenses", tags=["expenses"])

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# Initialize DB on startup
@app.on_event("startup")
async def startup():
    init_db()  # Run migrations if needed

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(config.PORT))