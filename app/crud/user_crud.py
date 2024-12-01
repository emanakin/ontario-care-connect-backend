from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user_model import User, AuthProvider
from app.schemas import user_schemas
from app.utils.auth_utils import generate_verification_token
import secrets

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: user_schemas.UserCreate):
    if user.auth_provider == AuthProvider.email:
        hashed_password = user.password
        is_verified = False
        verification_token = generate_verification_token()
    else:
        hashed_password = None
        is_verified = True
        verification_token = None

    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role,
        is_verified=is_verified,
        verification_token=verification_token,
        auth_provider=user.auth_provider
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_verification_token(db: AsyncSession, token: str) -> User:
    result = await db.execute(select(User).where(User.verification_token == token))
    return result.scalars().first()

async def verify_user_email(db: AsyncSession, user: User) -> None:
    user.is_verified = True
    user.verification_token = None
    db.add(user)
    await db.commit()
    
async def update_verification_token(db: AsyncSession, user: User) -> str:
    user.verification_token = secrets.token_urlsafe(32)
    db.add(user)
    await db.commit()
    return user.verification_token