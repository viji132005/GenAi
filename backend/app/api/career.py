from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel

from app.database.connection import get_db
from app.models.entities import User, StudentProfile, CareerProfile
from app.schemas.all_schemas import CareerAnalysisResponse
from app.services.career_service import CareerAnalysisService
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/career", tags=["Career Recommendations"])

class TargetCareerRequest(BaseModel):
    career_title: str

@router.get("/catalogs")
async def get_career_catalogs(db: AsyncSession = Depends(get_db)):
    query = select(CareerProfile).options(selectinload(CareerProfile.skills))
    result = await db.execute(query)
    careers = result.scalars().all()
    
    return [
        {
            "id": c.id,
            "title": c.title,
            "category": c.category,
            "description": c.description,
            "average_salary": c.average_salary,
            "growth_outlook": c.growth_outlook,
            "responsibilities": c.responsibilities,
            "typical_technologies": c.typical_technologies,
            "skills": [
                {
                    "name": s.skill_name,
                    "importance": s.importance_level,
                    "min_proficiency": s.min_proficiency
                }
                for s in c.skills
            ]
        }
        for c in careers
    ]

@router.post("/analyze", response_model=CareerAnalysisResponse)
async def analyze_career(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(StudentProfile).where(StudentProfile.user_id == current_user.id).options(
        selectinload(StudentProfile.skills),
        selectinload(StudentProfile.user)
    )
    result = await db.execute(query)
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(status_code=404, detail="Student profile not found")

    return await CareerAnalysisService.analyze_student_career(profile, db)

@router.post("/set-target")
async def set_target_career(
    req: TargetCareerRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    result = await db.execute(query)
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(status_code=404, detail="Student profile not found")

    profile.target_career = req.career_title
    await db.commit()
    return {"message": f"Target career updated to '{req.career_title}'", "target_career": req.career_title}
