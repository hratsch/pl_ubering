from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.handlers.reports import calculate_pl_summary, generate_chart_data, generate_pl_report
from app.auth.middleware import get_current_user
from datetime import date
from typing import Dict, List
from app.schemas.report import ChartData  # Add import

router = APIRouter(prefix="/api/reports", tags=["reports"])

@router.get("/summary", response_model=Dict[str, float])
def get_pl_summary(
    start_date: date = Query(None, description="Start date for filter"),
    end_date: date = Query(None, description="End date for filter"),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return calculate_pl_summary(db, start_date, end_date)

@router.get("/chart-data", response_model=List[ChartData])
def get_chart_data(
    start_date: date = Query(None, description="Start date for filter"),
    end_date: date = Query(None, description="End date for filter"),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return generate_chart_data(db, start_date, end_date)

@router.get("/pl/pdf")
def get_pl_report(
    start_date: date = Query(None, description="Start date for filter"),
    end_date: date = Query(None, description="End date for filter"),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    path = generate_pl_report(db, start_date, end_date)
    return {"detail": "Report generated", "path": path}