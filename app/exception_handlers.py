from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.auth.exceptions import (
    UserAlreadyExistsException,
    InvalidRoleException,
    InvalidCredentialsException,
    UnapprovedCaregiverException,
    InvalidTokenException
)
from app.logging_config import logger

async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsException):
    logger.error(f"User already exists: {exc}")
    return JSONResponse(status_code=400, content={"detail": str(exc)})

async def invalid_role_handler(request: Request, exc: InvalidRoleException):
    logger.error(f"Invalid role: {exc}")
    return JSONResponse(status_code=403, content={"detail": str(exc)})

async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsException):
    logger.warning(f"Invalid credentials attempt: {exc}")
    return JSONResponse(status_code=401, content={"detail": str(exc)})

async def invalid_token_handler(request: Request, exc: InvalidTokenException):
    logger.warning(f"Invalid token: {exc}")
    return JSONResponse(status_code=401, content={"detail": str(exc)})

async def unapproved_caregiver_handler(request: Request, exc: UnapprovedCaregiverException):
    logger.warning(f"Unapproved caregiver login attempt: {exc}")
    return JSONResponse(status_code=403, content={"detail": str(exc)})
