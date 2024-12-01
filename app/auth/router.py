from fastapi import APIRouter, Body, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_schemas import UserCreate, UserResponse, LoginRequest
from app.auth.exceptions import *
from app.services.user_service import UserService
from app.database import get_db
from app.schemas.token_schemas import Token
from app.logging_config import logger
from app.auth.oauth import oauth
from starlette.responses import RedirectResponse

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

@router.post("/forgot-password")
async def forgot_password(
    email: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    try:
        await service.request_password_reset(email)
        return {"detail": "Password reset link sent to your email"}
    except Exception as e:
        logger.error(f"Unexpected error during password reset request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/reset-password")
async def reset_password(
    token: str = Body(..., embed=True),
    new_password: str = Body(..., embed=True),
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    try:
        await service.reset_password(token, new_password)
        return {"detail": "Password reset successful"}
    except Exception as e:
        logger.error(f"Unexpected error during password reset request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get('/google')
async def auth_google(request: Request):
    redirect_uri = request.url_for('auth_google_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/facebook')
async def auth_facebook(request: Request):
    redirect_uri = request.url_for('auth_facebook_callback')
    return await oauth.facebook.authorize_redirect(request, redirect_uri)

@router.get('/google/callback')
async def auth_google_callback(request: Request, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    try:
        token = await service.authenticate_with_google(request)
        return token
    except Exception as e:
        logger.error(f"Google authentication failed: {e}")
        raise HTTPException(status_code=400, detail="Google authentication failed")

@router.get('/facebook/callback')
async def auth_facebook_callback(request: Request, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    try:
        token = await service.authenticate_with_facebook(request)
        return token
    except Exception as e:
        logger.error(f"Facebook authentication failed: {e}")
        raise HTTPException(status_code=400, detail="Facebook authentication failed")