from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schemas import UserCreate, LoginRequest
from app.schemas.token_schemas import Token
from app.crud.user_crud import create_user, get_user_by_email
from app.utils.auth_utils import get_password_hash, verify_password, create_access_token
from app.auth.exceptions import InvalidCredentialsException, UnapprovedCaregiverException
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
        return await create_user(self.db, user_data)
    
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
