import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_job_analysis_and_projects():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        login_res = await ac.post("/api/auth/login", json={
            "email": "demo@skillbridge.ai",
            "password": "password123"
        })
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 1. Job Analysis
        job_res = await ac.post("/api/job/analyze", json={
            "job_title": "AI Engineer",
            "company": "DeepTech Labs",
            "job_description": "Looking for Python, PyTorch, Docker, and SQL experience for machine learning deployment."
        }, headers=headers)
        assert job_res.status_code == 200
        job_data = job_res.json()
        assert job_data["match_score"] > 0
        assert "strong_matches" in job_data
        assert "skill_gaps" in job_data

        # 2. Projects
        proj_res = await ac.get("/api/projects", headers=headers)
        assert proj_res.status_code == 200
        projs = proj_res.json()
        assert len(projs) > 0
        assert "problem_statement" in projs[0]

@pytest.mark.asyncio
async def test_mock_interview_flow():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        login_res = await ac.post("/api/auth/login", json={
            "email": "demo@skillbridge.ai",
            "password": "password123"
        })
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 1. Start Interview
        start_res = await ac.post("/api/interview/start", json={
            "career_title": "AI/ML Engineer",
            "interview_type": "Technical",
            "difficulty": "Intermediate",
            "total_questions": 3
        }, headers=headers)
        assert start_res.status_code == 200
        session_data = start_res.json()
        assert len(session_data["questions"]) == 3

        # 2. Submit Answer
        first_q = session_data["questions"][0]
        ans_res = await ac.post("/api/interview/answer", json={
            "interview_id": session_data["id"],
            "question_id": first_q["id"],
            "user_answer": "The bias-variance tradeoff balances underfitting and overfitting. L1 regularization introduces sparsity while L2 penalizes large weights."
        }, headers=headers)
        assert ans_res.status_code == 200
        ans_data = ans_res.json()
        assert ans_data["score"] > 0
        assert "feedback" in ans_data
