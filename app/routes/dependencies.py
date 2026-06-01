"""Route dependencies"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.utils.security import decode_token
from app.services.auth_service import AuthService

security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthCredentials = Depends(security), db: AsyncSession = Depends(get_db)):
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = await AuthService.get_user_by_id(db, int(user_id))
    return user
