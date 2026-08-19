import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_career_catalogs_and_analysis():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Login
        login_res = await ac.post("/api/auth/login", json={
            "email": "demo@skillbridge.ai",
            "password": "password123"
        })
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 1. Career Catalogs
        cat_res = await ac.get("/api/career/catalogs", headers=headers)
        assert cat_res.status_code == 200
        catalogs = cat_res.json()
        assert len(catalogs) >= 5
        assert any("AI/ML Engineer" in c["title"] for c in catalogs)

        # 2. Career Analysis
        an_res = await ac.post("/api/career/analyze", headers=headers)
        assert an_res.status_code == 200
        data = an_res.json()
        assert "target_career" in data
        assert len(data["top_recommendations"]) > 0
        assert data["top_recommendations"][0]["match_percentage"] > 0

@pytest.mark.asyncio
async def test_skill_gaps_and_roadmap():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        login_res = await ac.post("/api/auth/login", json={
            "email": "demo@skillbridge.ai",
            "password": "password123"
        })
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 1. Skill Gap Analysis
        gap_res = await ac.post("/api/skills/analyze", json={"career_title": "AI/ML Engineer"}, headers=headers)
        assert gap_res.status_code == 200
        gap_data = gap_res.json()
        assert "acquired_skills" in gap_data
        assert "missing_skills" in gap_data
        assert len(gap_data["acquired_skills"]) > 0

        # 2. Roadmap
        rm_res = await ac.get("/api/roadmap", headers=headers)
        assert rm_res.status_code == 200
        rm_data = rm_res.json()
        assert "tasks" in rm_data
        assert len(rm_data["tasks"]) > 0

        # 3. Toggle Task
        first_task = rm_data["tasks"][0]
        toggle_res = await ac.put(f"/api/roadmap/tasks/{first_task['id']}", json={"is_completed": True}, headers=headers)
        assert toggle_res.status_code == 200
