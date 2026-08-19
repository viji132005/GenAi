from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database.connection import get_db
from app.models.entities import User, StudentProfile, JobAnalysis
from app.schemas.all_schemas import JobAnalysisRequest, JobAnalysisResponse
from app.services.job_service import JobAnalysisService
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/job", tags=["Job Description Compatibility"])

@router.post("/analyze", response_model=JobAnalysisResponse)
async def analyze_job(
    req: JobAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if len(req.job_description.strip()) < 30:
        raise HTTPException(status_code=400, detail="Job description text is too short to evaluate.")

    q_prof = select(StudentProfile).where(StudentProfile.user_id == current_user.id).options(
        selectinload(StudentProfile.skills)
    )
    res_prof = await db.execute(q_prof)
    profile = res_prof.scalar_one_or_none()

    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.add(profile)
        await db.commit()

    return await JobAnalysisService.analyze_job_description(
        user_id=current_user.id,
        job_title=req.job_title or "Target Role",
        company=req.company or "Tech Company",
        job_description=req.job_description,
        profile=profile,
        db=db
    )

@router.get("/history", response_model=List[JobAnalysisResponse])
async def get_job_analysis_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(JobAnalysis).where(JobAnalysis.user_id == current_user.id).order_by(
        JobAnalysis.analyzed_at.desc()
    )
    result = await db.execute(query)
    analyses = result.scalars().all()
    
    return [
        JobAnalysisResponse(
            id=ja.id,
            job_title=ja.job_title,
            company=ja.company,
            match_score=ja.match_score,
            strong_matches=ja.matching_skills or [],
            skill_gaps=ja.missing_skills or [],
            required_skills=(ja.requirements_extracted or {}).get("required", []),
            preferred_skills=(ja.requirements_extracted or {}).get("preferred", []),
            experience_requirements=(ja.requirements_extracted or {}).get("experience", "Entry-level"),
            recommendations=ja.recommendations or [],
            action_plan=[]
        )
        for ja in analyses
    ]
