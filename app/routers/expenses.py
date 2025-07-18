from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.crud.expense import create_expense, get_expenses, update_expense, delete_expense
from app.auth.middleware import get_current_user

router = APIRouter()

@router.post("/", response_model=ExpenseResponse)
def create(expense: ExpenseCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return create_expense(db, expense)

@router.get("/", response_model=list[ExpenseResponse])
def read(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return get_expenses(db, skip, limit)

@router.put("/{expense_id}", response_model=ExpenseResponse)
def update(expense_id: int, expense: ExpenseCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return update_expense(db, expense_id, expense)

@router.delete("/{expense_id}", response_model=dict)
def delete(expense_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    delete_expense(db, expense_id)
    return {"detail": "Expense deleted"}