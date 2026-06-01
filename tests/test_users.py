"""User tests"""

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_get_current_user():
    """Test getting current user profile"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Register user
        await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "password123",
            },
        )

        # Login
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        token = login_response.json()["access_token"]

        # Get current user
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("/api/v1/users/me", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
