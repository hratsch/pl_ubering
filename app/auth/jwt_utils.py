import jwt
from datetime import datetime, timedelta
from app.config import load_config

config = load_config()

def generate_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow(),
        "sub": user_id
    }
    return jwt.encode(payload, config.JWT_SECRET, algorithm="HS256")

def validate_token(token: str) -> dict:
    try:
        return jwt.decode(token, config.JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")