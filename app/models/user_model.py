from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLAlchemyEnum
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    customer = "customer"
    caregiver = "caregiver"
    
class AuthProvider(str, enum.Enum):
    email = 'email'
    google = 'google'
    facebook = 'facebook'

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    full_name = Column(String)
    role = Column(SQLAlchemyEnum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False, nullable=False)
    verification_token = Column(String, nullable=True)
    auth_provider = Column(SQLAlchemyEnum(AuthProvider), default=AuthProvider.email)
