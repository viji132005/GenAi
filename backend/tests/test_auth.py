import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.get("/api/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"
        assert "llm_provider" in data

@pytest.mark.asyncio
async def test_demo_user_login():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        res = await ac.post("/api/auth/login", json={
            "email": "demo@skillbridge.ai",
            "password": "password123"
        })
        assert res.status_code == 200
        data = res.json()
        assert "access_token" in data
        assert data["user"]["email"] == "demo@skillbridge.ai"
        assert data["user"]["full_name"] == "Rahul Sharma"

@pytest.mark.asyncio
async def test_register_and_get_me():
    import uuid
    unique_email = f"test_{uuid.uuid4().hex[:8]}@college.edu"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Register
        reg_res = await ac.post("/api/auth/register", json={
            "full_name": "Test Student",
            "email": unique_email,
            "password": "securepassword123"
        })
        assert reg_res.status_code == 200
        token = reg_res.json()["access_token"]

        # Get Me
        headers = {"Authorization": f"Bearer {token}"}
        me_res = await ac.get("/api/auth/me", headers=headers)
        assert me_res.status_code == 200
        assert me_res.json()["email"] == unique_email
