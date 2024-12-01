from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schemas import UserCreate, LoginRequest
from app.schemas.token_schemas import Token
from app.crud.user_crud import *
from app.utils.auth_utils import get_password_hash, verify_password, create_access_token, send_verification_email, send_password_reset_email
from app.auth.exceptions import InvalidCredentialsException, EmailNotVerifiedException, UnapprovedCaregiverException, UserNotFoundException, InvalidTokenException, EmailAlreadyVerifiedException, InvalidAuthProviderException
from app.logging_config import logger
from app.auth.oauth import oauth

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
        
    async def request_password_reset(self, email: str) -> None:
        user = await get_user_by_email(self.db, email)
        if not user:
            raise UserNotFoundException(email)
        if user.auth_provider != AuthProvider.email:
            raise InvalidAuthProviderException("Password reset is not available for social login users.")
        if not user.is_verified:
            raise EmailNotVerifiedException()
        token = await update_verification_token(self.db, user)
        await send_password_reset_email(user.email, token)
        
    async def reset_password(self, token: str, new_password: str) -> None:
        user = await get_user_by_verification_token(self.db, token)
        if not user:
            raise InvalidTokenException("Invalid or expired token.")
        # Ensure the user is verified
        if not user.is_verified:
            raise EmailNotVerifiedException()
        # Update the user's password
        user.hashed_password = get_password_hash(new_password)
        user.verification_token = None  # Clear the token
        self.db.add(user)
        await self.db.commit()
        
    async def authenticate_with_google(self, request):
        token = await oauth.google.authorize_access_token(request)
        logger.debug(f"Token received: {token}")

        # Try to get user info from the token
        user_info = token.get('userinfo')

        if not user_info:
            logger.debug("Fetching user info from userinfo endpoint")
            resp = await oauth.google.get('userinfo', token=token)
            user_info = resp.json()

        if not user_info:
            logger.error("Failed to obtain user info from Google")
            raise HTTPException(status_code=400, detail="Failed to obtain user info from Google")

        # Extract user information
        email = user_info.get('email')
        full_name = user_info.get('name')

        # Proceed with your existing logic
        user = await get_user_by_email(self.db, email)

        if user:
            if user.auth_provider != AuthProvider.google:
                user.auth_provider = AuthProvider.google
                self.db.add(user)
                await self.db.commit()
                await self.db.refresh(user)
        else:
            user_create = UserCreate(
                email=email,
                full_name=full_name,
                auth_provider=AuthProvider.google,
                is_verified=True,
                role='customer'
            )
            user = await create_user(self.db, user_create)

        access_token = create_access_token(data={"sub": user.email, "role": user.role})
        return {"access_token": access_token, "token_type": "bearer"}

    async def authenticate_with_facebook(self, request):
        token = await oauth.facebook.authorize_access_token(request)
        user_info_response = await oauth.facebook.get('me?fields=id,name,email', token=token)
        user_info = user_info_response.json()
        email = user_info.get('email')
        full_name = user_info.get('name')

        user = await get_user_by_email(self.db, email)

        if user:
            if user.auth_provider != AuthProvider.facebook:
                user.auth_provider = AuthProvider.facebook
                self.db.add(user)
                await self.db.commit()
                await self.db.refresh(user)
        else:
            user_create = UserCreate(
                email=email,
                full_name=full_name,
                auth_provider=AuthProvider.facebook,
                role='customer'
            )
            user = await create_user(self.db, user_create)

        access_token = create_access_token(data={"sub": user.email, "role": user.role})
        return {"access_token": access_token, "token_type": "bearer"}