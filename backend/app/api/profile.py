from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database.connection import get_db
from app.models.entities import User, StudentProfile, Skill
from app.schemas.all_schemas import StudentProfileResponse, ProfileUpdate, SkillCreate, SkillResponse
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/profile", tags=["Student Profile"])

@router.get("", response_model=StudentProfileResponse)
async def get_student_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(StudentProfile).where(StudentProfile.user_id == current_user.id).options(
        selectinload(StudentProfile.skills)
    )
    result = await db.execute(query)
    profile = result.scalar_one_or_none()

    if not profile:
        profile = StudentProfile(user_id=current_user.id, target_career="AI/ML Engineer")
        db.add(profile)
        await db.commit()
        await db.refresh(profile)

    return StudentProfileResponse.model_validate(profile)

@router.put("", response_model=StudentProfileResponse)
async def update_student_profile(
    profile_in: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(StudentProfile).where(StudentProfile.user_id == current_user.id).options(
        selectinload(StudentProfile.skills)
    )
    result = await db.execute(query)
    profile = result.scalar_one_or_none()

    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.add(profile)

    update_dict = profile_in.model_dump(exclude_unset=True)
    skills_in = update_dict.pop("skills", None)

    for field, value in update_dict.items():
        if value is not None:
            setattr(profile, field, value)

    if skills_in is not None:
        # Replace skills
        # Clear existing
        del_query = select(Skill).where(Skill.profile_id == profile.id)
        res = await db.execute(del_query)
        existing_skills = res.scalars().all()
        for s in existing_skills:
            await db.delete(s)
        
        for sk in skills_in:
            new_sk = Skill(
                profile_id=profile.id,
                name=sk["name"],
                category=sk.get("category", "Technical"),
                proficiency_level=sk.get("proficiency_level", "Beginner")
            )
            db.add(new_sk)

    await db.commit()
    
    # Reload with skills
    query_reload = select(StudentProfile).where(StudentProfile.id == profile.id).options(
        selectinload(StudentProfile.skills)
    )
    res_reload = await db.execute(query_reload)
    updated_profile = res_reload.scalar_one()

    return StudentProfileResponse.model_validate(updated_profile)

@router.post("/onboarding", response_model=StudentProfileResponse)
async def complete_onboarding(
    profile_in: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(StudentProfile).where(StudentProfile.user_id == current_user.id).options(
        selectinload(StudentProfile.skills)
    )
    result = await db.execute(query)
    profile = result.scalar_one_or_none()

    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.add(profile)
        await db.flush()

    update_dict = profile_in.model_dump(exclude_unset=True)
    skills_in = update_dict.pop("skills", None)

    for field, value in update_dict.items():
        if value is not None:
            setattr(profile, field, value)

    profile.onboarding_completed = True

    if skills_in is not None:
        # Clear existing skills to avoid duplicates
        del_query = select(Skill).where(Skill.profile_id == profile.id)
        res = await db.execute(del_query)
        existing_skills = res.scalars().all()
        for s in existing_skills:
            await db.delete(s)

        for sk in skills_in:
            new_sk = Skill(
                profile_id=profile.id,
                name=sk["name"],
                category=sk.get("category", "Technical"),
                proficiency_level=sk.get("proficiency_level", "Beginner")
            )
            db.add(new_sk)

    await db.commit()

    query_reload = select(StudentProfile).where(StudentProfile.id == profile.id).options(
        selectinload(StudentProfile.skills)
    )
    res_reload = await db.execute(query_reload)
    updated_profile = res_reload.scalar_one()

    return StudentProfileResponse.model_validate(updated_profile)

@router.post("/skills", response_model=SkillResponse)
async def add_skill(
    skill_in: SkillCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(StudentProfile).where(StudentProfile.user_id == current_user.id)
    result = await db.execute(query)
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(status_code=404, detail="Student profile not found")

    new_skill = Skill(
        profile_id=profile.id,
        name=skill_in.name,
        category=skill_in.category,
        proficiency_level=skill_in.proficiency_level
    )
    db.add(new_skill)
    await db.commit()
    await db.refresh(new_skill)

    return SkillResponse.model_validate(new_skill)

@router.delete("/skills/{skill_id}")
async def delete_skill(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Skill).join(StudentProfile).where(
        Skill.id == skill_id,
        StudentProfile.user_id == current_user.id
    )
    result = await db.execute(query)
    skill = result.scalar_one_or_none()

    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    await db.delete(skill)
    await db.commit()
    return {"message": "Skill deleted successfully"}
