from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.auth.exceptions import InvalidTokenException
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from app.logging_config import logger
import secrets
from pydantic import EmailStr

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET", "fallback-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=os.getenv("MAIL_PORT"),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    is_valid = pwd_context.verify(plain_password, hashed_password)
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
    
def generate_verification_token():
    logger.info("Generating verifcation token")
    return secrets.token_urlsafe(32)

async def send_verification_email(email: EmailStr, token: str):
    verification_link = f"http://yourdomain.com/verify-email?token={token}"
    message = MessageSchema(
        subject="Verify your email",
        recipients=[email],
        body=f"Please verify your email by clicking on the following link: {verification_link}",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    
async def send_password_reset_email(email: EmailStr, token: str):
    reset_link = f"http://yourdomain.com/reset-password?token={token}"
    message = MessageSchema(
        subject="Reset Your Password",
        recipients=[email],
        body=f"Please reset your password by clicking on the following link: {reset_link}",
        subtype="plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)