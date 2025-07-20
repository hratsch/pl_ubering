from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.trip import get_trips
from app.crud.expense import get_expenses
from datetime import date, timedelta
from typing import Optional, List, Dict
from fpdf import FPDF

def calculate_pl_summary(
    db: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> Dict[str, float]:
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    if not end_date:
        end_date = date.today()

    # Fetch and filter in Python (decrypts automatically)
    trips = get_trips(db)
    expenses = get_expenses(db)

    # Filter by date
    trips = [t for t in trips if start_date <= t.date <= end_date]
    expenses = [e for e in expenses if start_date <= e.date <= end_date]

    total_earnings = sum(t.gross_earnings for t in trips)
    total_expenses = sum(e.amount for e in expenses)
    total_gas = sum(t.gas_cost or 0 for t in trips)
    total_tolls = sum(t.tolls or 0 for t in trips)

    profit = total_earnings - (total_expenses + total_gas + total_tolls)

    return {
        "total_earnings": total_earnings,
        "total_expenses": total_expenses,
        "total_gas": total_gas,
        "total_tolls": total_tolls,
        "profit": profit
    }

def generate_chart_data(
    db: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> List[Dict[str, float]]:
    if not start_date:
        start_date = date.today() - timedelta(days=30)
    if not end_date:
        end_date = date.today()

    # Fetch and filter in Python
    trips = get_trips(db)
    expenses = get_expenses(db)

    trips = [t for t in trips if start_date <= t.date <= end_date]
    expenses = [e for e in expenses if start_date <= e.date <= end_date]

    # Aggregate daily
    daily_data = {}
    for t in trips:
        day = t.date.isoformat()
        if day not in daily_data:
            daily_data[day] = {"earnings": 0, "expenses": 0}
        daily_data[day]["earnings"] += t.gross_earnings

    for e in expenses:
        day = e.date.isoformat()
        if day not in daily_data:
            daily_data[day] = {"earnings": 0, "expenses": 0}
        daily_data[day]["expenses"] += e.amount

    chart_data = []
    for day, values in sorted(daily_data.items()):
        chart_data.append({
            "date": day,
            "earnings": values["earnings"],
            "expenses": values["expenses"],
            "profit": values["earnings"] - values["expenses"]
        })

    return chart_data

def generate_pl_report(db: Session = Depends(get_db), start_date: Optional[date] = None, end_date: Optional[date] = None):
    summary = calculate_pl_summary(db, start_date, end_date)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="P&L Report", ln=1, align='C')
    pdf.cell(200, 10, txt=f"From {start_date or 'default'} to {end_date or 'default'}", ln=1)
    pdf.cell(200, 10, txt=f"Total Earnings: {summary['total_earnings']}", ln=1)
    pdf.cell(200, 10, txt=f"Total Expenses: {summary['total_expenses']}", ln=1)
    pdf.cell(200, 10, txt=f"Profit: {summary['profit']}", ln=1)
    pdf.output("pl_report.pdf")
    return "pl_report.pdf"