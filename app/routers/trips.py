from fastapi import APIRouter, Depends
from app.auth.middleware import get_current_user  # For protected routes later

router = APIRouter()

# Trip CRUD endpoints will be added here in Phase 2
# Example placeholder (commented out):
# @router.post("/")
# def create_trip(current_user: str = Depends(get_current_user)):
#     pass