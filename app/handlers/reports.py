from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.trip import get_trips
from app.crud.expense import get_expenses
from fpdf import FPDF
from datetime import datetime

def generate_pl_report(db: Session = Depends(get_db)):
    trips = get_trips(db)
    expenses = get_expenses(db)
    total_earnings = sum(t.gross_earnings for t in trips)
    total_expenses = sum(e.amount for e in expenses)
    profit = total_earnings - total_expenses

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="P&L Report - " + datetime.now().strftime("%Y-%m-%d"), ln=1, align='C')
    pdf.cell(200, 10, txt=f"Total Earnings: ${total_earnings:.2f}", ln=1)
    pdf.cell(200, 10, txt=f"Total Expenses: ${total_expenses:.2f}", ln=1)
    pdf.cell(200, 10, txt=f"Profit: ${profit:.2f}", ln=1)
    # Add section for trips
    pdf.ln(10)
    pdf.cell(200, 10, txt="Trips:", ln=1)
    for t in trips:
      pdf.cell(200, 10, txt=f"{t.date}: Earnings ${t.gross_earnings:.2f}, Miles {t.miles_driven or 0}", ln=1)
    # Add section for expenses
    pdf.ln(10)
    pdf.cell(200, 10, txt="Expenses:", ln=1)
    for e in expenses:
      pdf.cell(200, 10, txt=f"{e.date}: {e.category} ${e.amount:.2f}", ln=1)
    pdf.output("pl_report.pdf")
    return "pl_report.pdf"
