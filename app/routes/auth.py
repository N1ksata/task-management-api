"""Authentication routes"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse)
async def register(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user"""
    user = await AuthService.register(db, user_create)
    return user


@router.post("/login", response_model=Token)
async def login(user_login: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login user and get access token"""
    token_data = await AuthService.login(db, user_login)
    return token_data
