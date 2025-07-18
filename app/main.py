from fastapi import FastAPI
from fastapi import HTTPException
from dotenv import load_dotenv
import uvicorn
from app.utils.responses import error_response

from app.config import load_config
from app.database import init_db
from app.routers import auth, trips, expenses, reports  # Import routers
from contextlib import asynccontextmanager

load_dotenv()  # Load .env
config = load_config()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Run startup code
    yield

app = FastAPI(title="Uber P&L API", lifespan=lifespan)

# Include routers
app.include_router(auth.router, prefix="/api/auth")
app.include_router(trips.router, prefix="/api/trips", tags=["trips"])
app.include_router(expenses.router, prefix="/api/expenses", tags=["expenses"])
app.include_router(reports.router)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return error_response(exc.detail, exc.status_code)

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(config.PORT))