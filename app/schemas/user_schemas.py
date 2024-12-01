from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum
from app.models.user_model import AuthProvider

class LoginRequest(BaseModel):
    username: str
    password: str

class UserRole(str, Enum):
    admin = "admin"
    customer = "customer"
    caregiver = "caregiver"

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: Optional[str] = None
    full_name: Optional[str] = None
    role: str = 'customer'
    is_verified: Optional[bool] = False
    auth_provider: AuthProvider = AuthProvider.email

class UserResponse(UserBase):
    id: int
    role: UserRole

    class Config:
        from_attributes = True

