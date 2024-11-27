from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schemas import UserCreate, UserResponse, LoginRequest
from app.auth.exceptions import UserAlreadyExistsException, UnapprovedCaregiverException, InvalidRoleException, InvalidCredentialsException
from app.services.user_service import UserService
from app.database import get_db
from app.schemas.token_schemas import Token
from app.logging_config import logger

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/signup", response_model=UserResponse)
async def signup(
    user_data: UserCreate, 
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    try:
        user = await service.signup(user_data)
        return user
    except UserAlreadyExistsException as e:
        logger.error(f"Signup error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except InvalidRoleException as e:
        logger.error(f"Signup error: {e}")
        raise HTTPException(status_code=403, detail=str(e))

@router.post("/login", response_model=Token)
async def login(
    login_request: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    try:
        token = await service.login(login_request)
        return token
    except (InvalidCredentialsException, UnapprovedCaregiverException) as e:
        logger.warning(f"Login failed: {e}")
        raise HTTPException(status_code=401, detail=str(e))
    
@router.get("/verify-email")
async def verify_email(
    token: str, 
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    await service.verify_email(token)
    return {"detail": "Email verified successfully"}

@router.post("/resend-verification")
async def resend_verification(
    email: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    await service.resend_verification_email(email)
    return {"detail": "Verification email resent"}

