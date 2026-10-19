from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.models.user import User
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-only-for-dev")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

def create_access_token(user: User) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": str(user.user_id),
        "username": user.username,
        "role": user.role.value,
        "exp": expire
    }

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None