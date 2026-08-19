import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.middleware.auth import create_access_token

@pytest.mark.asyncio
async def test_multi_persona_personalization():
    """Verify that different users receive distinct career scores and tailored recommendations."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # 1. Test Rahul (AI/ML Aspirant)
        token_rahul = create_access_token({"sub": "demo@skillbridge.ai"})
        res_rahul = await ac.post("/api/career/analyze", headers={"Authorization": f"Bearer {token_rahul}"})
        assert res_rahul.status_code == 200
        rahul_data = res_rahul.json()
        assert rahul_data["target_career"] == "AI/ML Engineer"
        
        # 2. Test Priya (Full Stack Developer)
        token_priya = create_access_token({"sub": "priya@skillbridge.ai"})
        res_priya = await ac.post("/api/career/analyze", headers={"Authorization": f"Bearer {token_priya}"})
        assert res_priya.status_code == 200
        priya_data = res_priya.json()
        assert priya_data["target_career"] == "Full Stack Developer"
        
        # Verify Priya has higher Full Stack match than Rahul
        priya_fs = next((r["match_percentage"] for r in priya_data["top_recommendations"] if "full stack" in r["career_title"].lower()), 0)
        rahul_fs = next((r["match_percentage"] for r in rahul_data["top_recommendations"] if "full stack" in r["career_title"].lower()), 0)
        assert priya_fs > rahul_fs

        # 3. Test Rohan (Data Analyst)
        token_rohan = create_access_token({"sub": "rohan@skillbridge.ai"})
        res_rohan = await ac.post("/api/career/analyze", headers={"Authorization": f"Bearer {token_rohan}"})
        assert res_rohan.status_code == 200
        rohan_data = res_rohan.json()
        assert rohan_data["target_career"] == "Data Analyst"

        rohan_da = next((r["match_percentage"] for r in rohan_data["top_recommendations"] if "data analyst" in r["career_title"].lower()), 0)
        assert rohan_da >= 70.0

@pytest.mark.asyncio
async def test_individual_skill_gaps_and_roadmap():
    """Verify that skill gaps and roadmaps differ per individual student profile."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Priya Skill Gaps for Full Stack Developer
        token_priya = create_access_token({"sub": "priya@skillbridge.ai"})
        res_gaps = await ac.post("/api/skills/analyze", json={"career_title": "Full Stack Developer"}, headers={"Authorization": f"Bearer {token_priya}"})
        assert res_gaps.status_code == 200
        gaps_data = res_gaps.json()
        
        # Priya should have React, JavaScript, HTML/CSS as acquired
        acquired_names = [s["skill_name"].lower() for s in gaps_data["acquired_skills"]]
        assert any("react" in s or "javascript" in s or "html" in s for s in acquired_names)

        # Priya Roadmap for Full Stack
        res_roadmap = await ac.get("/api/roadmap", headers={"Authorization": f"Bearer {token_priya}"})
        assert res_roadmap.status_code == 200
        roadmap_data = res_roadmap.json()
        assert "Full Stack" in roadmap_data["career_title"] or len(roadmap_data["tasks"]) > 0

@pytest.mark.asyncio
async def test_individual_dashboard_overview():
    """Verify that dashboard overview returns genuine metadata for each user."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        token_alex = create_access_token({"sub": "alex@skillbridge.ai"})
        res_dash = await ac.get("/api/analytics/dashboard", headers={"Authorization": f"Bearer {token_alex}"})
        assert res_dash.status_code == 200
        dash = res_dash.json()
        assert dash["user_name"] == "Alex Chen"
        assert dash["target_career"] == "Cloud / DevOps Engineer"
        assert dash["degree"] == "B.E."
        assert dash["semester"] == 8
        assert dash["career_match_percentage"] > 0
        assert "radar_metrics" in dash
        assert "timeline_metrics" in dash
