from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schemas import UserCreate, LoginRequest
from app.schemas.token_schemas import Token
from app.crud.user_crud import *
from app.utils.auth_utils import get_password_hash, verify_password, create_access_token, send_verification_email
from app.auth.exceptions import InvalidCredentialsException, UnapprovedCaregiverException, UserNotFoundException, InvalidTokenException, EmailAlreadyVerifiedException
from app.logging_config import logger

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def signup(self, user_data: UserCreate):
        existing_user = await get_user_by_email(self.db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=400, detail="Email already registered"
            )
            
        if user_data.role not in ["customer", "caregiver"]:
            raise HTTPException(
                status_code=403, detail="Invalid role for signup"
            )
            
        user_data.password = get_password_hash(user_data.password)
        user = await create_user(self.db, user_data)
        await send_verification_email(user.email, user.verification_token)
        return user
    
    async def login(self, login_request: LoginRequest) -> Token:
        user = await get_user_by_email(self.db, login_request.username)
        logger.debug(f"User found: {user.email}, Hashed password in DB: {repr(user.hashed_password)}")
        if not user or not verify_password(login_request.password, user.hashed_password):
            raise InvalidCredentialsException()
        
        if user.role == "caregiver" and not user.is_approved: # will implement for caregiver users
            raise UnapprovedCaregiverException()
        
        access_token = create_access_token(
            data={"sub": user.email, "role": user.role}
        )
        return Token(access_token=access_token, token_type="bearer")
    
    async def verify_email(self, token: str) -> None:
        user = await get_user_by_verification_token(self.db, token)
        if not user:
            raise InvalidTokenException()
        if user.is_verified:
            raise EmailAlreadyVerifiedException()
        await verify_user_email(self.db, user)
        
    async def resend_verification_email(self, email: str) -> None:
        user = await get_user_by_email(self.db, email)
        if not user:
            raise UserNotFoundException()
        if user.is_verified:
            raise EmailAlreadyVerifiedException()
        token = await update_verification_token(self.db, user)
        await send_verification_email(user.email, token)