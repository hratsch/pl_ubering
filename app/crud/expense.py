from sqlalchemy.orm import Session
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.encryption import EncryptionService
from app.config import load_config
from fastapi import HTTPException

config = load_config()
enc_service = EncryptionService(config.ENCRYPTION_PASSWORD)

def to_response(db_expense: Expense) -> ExpenseResponse:
    return ExpenseResponse(
        id=db_expense.id,
        date=db_expense.date,
        category=db_expense.category,
        amount=enc_service.decrypt_float64(db_expense.amount_encrypted),
        description=enc_service.decrypt(db_expense.description_encrypted),
        created_at=db_expense.created_at,
        updated_at=db_expense.updated_at
    )

def create_expense(db: Session, expense: ExpenseCreate):
    db_expense = Expense(
        date=expense.date,
        category=expense.category,
        amount_encrypted=enc_service.encrypt_float64(expense.amount),
        description_encrypted=enc_service.encrypt(expense.description) if expense.description else ""
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return to_response(db_expense)

def update_expense(db: Session, expense_id: int, expense: ExpenseCreate):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(404, "Expense not found")
    db_expense.date = expense.date
    db_expense.category = expense.category
    db_expense.amount_encrypted = enc_service.encrypt_float64(expense.amount)
    db_expense.description_encrypted = enc_service.encrypt(expense.description) if expense.description else ""
    db.commit()
    db.refresh(db_expense)
    return to_response(db_expense)

def get_expenses(db: Session, skip: int = 0, limit: int = 100):
    expenses = db.query(Expense).offset(skip).limit(limit).all()
    return [ExpenseResponse(
        id=e.id,
        date=e.date,
        category=e.category,
        amount=enc_service.decrypt_float64(e.amount_encrypted),
        description=enc_service.decrypt(e.description_encrypted),
        created_at=e.created_at,
        updated_at=e.updated_at
    ) for e in expenses]

def delete_expense(db: Session, expense_id: int):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(404, "Expense not found")
    db.delete(db_expense)
    db.commit()