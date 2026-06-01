"""User request/response schemas"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Base user schema"""

    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=255)


class UserCreate(UserBase):
    """User creation schema"""

    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    """User login schema"""

    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """User update schema"""

    username: Optional[str] = Field(None, min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)


class UserResponse(UserBase):
    """User response schema"""

    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """JWT token response schema"""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
