from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.auth_utils import decode_access_token
from app.crud.user_crud import get_user_by_email
from app.database import get_db
from app.auth.exceptions import InvalidTokenException
from app.logging_config import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        role: str = payload.get("role")
        
        if email is None or role is None:
            raise InvalidTokenException(detail="Token payload missing 'sub' or 'role'.")
        user = await get_user_by_email(db, email)
        
        if user is None:
            raise InvalidTokenException(detail="User not found.")
        return user
    
    except InvalidTokenException as e:
        logger.error(f"Invalid token: {e.detail}")
        raise HTTPException(status_code=401, detail=e.detail)

