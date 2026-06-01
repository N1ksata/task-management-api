"""Task tests"""

import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_create_task():
    """Test task creation"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Register user first
        reg_response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "password123",
            },
        )
        assert reg_response.status_code == 200

        # Login
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123",
            },
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Create task
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.post(
            "/api/v1/tasks",
            json={
                "title": "Test Task",
                "description": "This is a test task",
                "priority": "high",
            },
            headers=headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
