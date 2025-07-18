from fastapi import APIRouter, Depends
from app.handlers.reports import generate_pl_report
from app.auth.middleware import get_current_user
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter(prefix="/api/reports", tags=["reports"])

@router.get("/pl/pdf")
def get_pl_report(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    path = generate_pl_report(db)
    return {"detail": "Report generated", "path": path}