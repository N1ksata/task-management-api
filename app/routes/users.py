"""User routes"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.services.auth_service import AuthService
from app.routes.dependencies import get_current_user
from app.models.user import User
from sqlalchemy.future import select

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update current user profile"""
    if user_update.username is not None:
        # Check if username is already taken
        stmt = select(User).where(
            (User.username == user_update.username) & (User.id != current_user.id)
        )
        result = await db.execute(stmt)
        if result.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )
        current_user.username = user_update.username

    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete current user account"""
    await db.delete(current_user)
    await db.commit()
