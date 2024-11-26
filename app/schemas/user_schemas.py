from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from enum import Enum

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

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role: UserRole

class UserResponse(UserBase):
    id: int
    role: UserRole

    class Config:
        orm_mode = True

