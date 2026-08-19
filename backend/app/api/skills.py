from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel

from app.database.connection import get_db
from app.models.entities import User, StudentProfile, CareerProfile
from app.schemas.all_schemas import SkillGapAnalysisResponse
from app.services.skill_gap_service import SkillGapService
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/skills", tags=["Skill Gap Analysis"])

class SkillGapRequest(BaseModel):
    career_title: Optional[str] = None

@router.post("/analyze", response_model=SkillGapAnalysisResponse)
async def analyze_skill_gaps(
    req: SkillGapRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(StudentProfile).where(StudentProfile.user_id == current_user.id).options(
        selectinload(StudentProfile.skills)
    )
    result = await db.execute(query)
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(status_code=404, detail="Student profile not found")

    return await SkillGapService.analyze_skill_gaps(profile, req.career_title, db)

@router.get("/taxonomy")
async def get_skill_taxonomy():
    """Returns curated taxonomy for skill selection in UI."""
    return {
        "Languages": ["Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust", "SQL", "HTML/CSS"],
        "AI / ML": ["PyTorch", "TensorFlow", "Scikit-Learn", "Deep Learning", "NLP", "Computer Vision", "RAG", "LangChain", "LLMs", "Pandas", "NumPy"],
        "Web Frameworks": ["React", "Next.js", "Node.js", "Express", "FastAPI", "Django", "Spring Boot", "TailwindCSS", "Vue.js", "GraphQL"],
        "Databases": ["PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "ChromaDB", "Elasticsearch", "Cassandra"],
        "Cloud & DevOps": ["Docker", "Kubernetes", "AWS", "Google Cloud (GCP)", "Microsoft Azure", "CI/CD", "Terraform", "Linux", "Git"],
        "Cybersecurity": ["Network Security", "OWASP Top 10", "Penetration Testing", "Cryptography", "SIEM (Splunk)", "Wireshark", "Identity & Access Management (IAM)"]
    }
