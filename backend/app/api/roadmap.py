from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database.connection import get_db
from app.models.entities import User, StudentProfile
from app.schemas.all_schemas import RoadmapResponse, RoadmapTaskUpdate
from app.services.roadmap_service import RoadmapService
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/roadmap", tags=["Personalized Roadmap"])

@router.get("", response_model=RoadmapResponse)
async def get_roadmap(
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

    return await RoadmapService.get_or_generate_roadmap(profile, db, regenerate=False)

@router.post("/generate", response_model=RoadmapResponse)
async def regenerate_roadmap(
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

    return await RoadmapService.get_or_generate_roadmap(profile, db, regenerate=True)

@router.put("/tasks/{task_id}", response_model=RoadmapResponse)
async def update_task_status(
    task_id: int,
    task_in: RoadmapTaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        return await RoadmapService.toggle_task_status(task_id, task_in.is_completed, current_user.id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
