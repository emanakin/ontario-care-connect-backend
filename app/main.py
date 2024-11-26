from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.routers import customers, caregivers
from app.auth import router as auth
from app.database import engine, Base
from app.exception_handlers import (
    user_already_exists_handler,
    invalid_role_handler,
    invalid_credentials_handler,
    unapproved_caregiver_handler,
)
from app.auth.exceptions import (
    UserAlreadyExistsException,
    InvalidRoleException,
    InvalidCredentialsException,
    UnapprovedCaregiverException,
)
from app.logging_config import logger

# Create the database tables
# Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_exception_handler(UserAlreadyExistsException, user_already_exists_handler)
app.add_exception_handler(InvalidRoleException, invalid_role_handler)
app.add_exception_handler(InvalidCredentialsException, invalid_credentials_handler)
app.add_exception_handler(UnapprovedCaregiverException, unapproved_caregiver_handler)

# Allow CORS (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Set to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
# app.include_router(customers.router)
# app.include_router(caregivers.router)
