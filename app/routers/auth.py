from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.app_config import AppConfig
from app.schemas.auth import LoginRequest, TokenResponse
from app.auth.jwt_utils import generate_token
from app.auth.middleware import get_current_user
from hashlib import pbkdf2_hmac

router = APIRouter()

def hash_password(password: str) -> str:
    salt = b'uber-pl-salt-2024'
    return pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    config = db.query(AppConfig).first()
    if not config:
        hashed = hash_password(request.password)
        config = AppConfig(encryption_key_hash=hashed)
        db.add(config)
        db.commit()
        db.refresh(config)  # Refresh the new config object
    if hash_password(request.password) != config.encryption_key_hash:
        raise HTTPException(401, "Invalid password")
    return TokenResponse(access_token=generate_token("single_user"))

@router.post("/refresh", response_model=TokenResponse)
def refresh(current_user: str = Depends(get_current_user)):
    return TokenResponse(access_token=generate_token(current_user))