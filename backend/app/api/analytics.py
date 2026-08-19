from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database.connection import get_db
from app.models.entities import User, StudentProfile
from app.schemas.all_schemas import DashboardOverviewResponse
from app.services.analytics_service import AnalyticsService
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/analytics", tags=["Dashboard & Analytics"])

@router.get("/dashboard", response_model=DashboardOverviewResponse)
async def get_dashboard_data(
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
        profile = StudentProfile(user_id=current_user.id)
        db.add(profile)
        await db.commit()

    return await AnalyticsService.get_dashboard_overview(profile, db)
