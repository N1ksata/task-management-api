"""Authentication service"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.utils.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status
from datetime import timedelta


class AuthService:
    """Service for handling authentication operations"""

    @staticmethod
    async def register(db: AsyncSession, user_create: UserCreate) -> User:
        """Register a new user"""
        # Check if user already exists
        stmt = select(User).where(
            (User.email == user_create.email) | (User.username == user_create.username)
        )
        existing_user = await db.execute(stmt)
        if existing_user.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email or username already registered",
            )

        # Create new user
        hashed_password = hash_password(user_create.password)
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            full_name=user_create.full_name,
            hashed_password=hashed_password,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def login(db: AsyncSession, user_login: UserLogin) -> dict:
        """Authenticate user and return access token"""
        # Find user by email
        stmt = select(User).where(User.email == user_login.email)
        result = await db.execute(stmt)
        user = result.scalars().first()

        if not user or not verify_password(user_login.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
            )

        # Create access token
        access_token = create_access_token(data={"sub": str(user.id)})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": 30 * 60,  # 30 minutes in seconds
        }

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
        """Get user by ID"""
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalars().first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user
