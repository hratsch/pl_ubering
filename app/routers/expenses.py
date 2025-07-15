from fastapi import APIRouter, Depends
from app.auth.middleware import get_current_user  # For protected routes later

router = APIRouter()

# Expense CRUD endpoints will be added here in Phase 2
# Example placeholder (commented out):
# @router.post("/")
# def create_expense(current_user: str = Depends(get_current_user)):
#     pass