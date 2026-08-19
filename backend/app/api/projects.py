from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database.connection import get_db
from app.models.entities import User, StudentProfile, ProjectRecommendation
from app.schemas.all_schemas import ProjectRecommendationResponse
from app.services.project_service import ProjectRecommendationService
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["Project Recommendations"])

@router.get("", response_model=List[ProjectRecommendationResponse])
async def get_recommended_projects(
    domain: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    q_prof = select(StudentProfile).where(StudentProfile.user_id == current_user.id).options(
        selectinload(StudentProfile.skills)
    )
    res_prof = await db.execute(q_prof)
    profile = res_prof.scalar_one_or_none()

    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.add(profile)
        await db.commit()

    return await ProjectRecommendationService.get_or_generate_projects(
        profile=profile,
        db=db,
        domain_filter=domain,
        difficulty_filter=difficulty,
        regenerate=False
    )

@router.post("/generate", response_model=List[ProjectRecommendationResponse])
async def regenerate_projects(
    domain: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    q_prof = select(StudentProfile).where(StudentProfile.user_id == current_user.id).options(
        selectinload(StudentProfile.skills)
    )
    res_prof = await db.execute(q_prof)
    profile = res_prof.scalar_one_or_none()

    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.add(profile)
        await db.commit()

    return await ProjectRecommendationService.get_or_generate_projects(
        profile=profile,
        db=db,
        domain_filter=domain,
        difficulty_filter=difficulty,
        regenerate=True
    )

@router.post("/{project_id}/bookmark", response_model=ProjectRecommendationResponse)
async def bookmark_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        return await ProjectRecommendationService.toggle_project_bookmark(project_id, current_user.id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
