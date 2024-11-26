from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.auth.exceptions import InvalidTokenException
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from app.logging_config import logger

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET", "fallback-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    is_valid = pwd_context.verify(plain_password, hashed_password)
    logger.debug(f"Verifying password: {plain_password} against hash: {hashed_password} - Valid: {is_valid}")
    return is_valid

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise InvalidTokenException(detail=str(e))