"""Authentication tests"""

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_register_user():
    """Test user registration"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "password123",
                "full_name": "Test User",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"


@pytest.mark.asyncio
async def test_register_duplicate_email():
    """Test registration with duplicate email"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First registration
        await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "password123",
            },
        )

        # Duplicate registration
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser2",
                "password": "password123",
            },
        )
        assert response.status_code == 400
