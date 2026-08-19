from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database.connection import get_db
from app.models.entities import User, StudentProfile, MockInterview
from app.schemas.all_schemas import (
    InterviewStartRequest, InterviewAnswerRequest, InterviewAnswerResponse,
    InterviewReportResponse, MockInterviewSessionResponse
)
from app.services.interview_service import MockInterviewService
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/interview", tags=["AI Mock Interview"])

@router.post("/start", response_model=MockInterviewSessionResponse)
async def start_mock_interview(
    req: InterviewStartRequest,
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

    return await MockInterviewService.start_interview(
        user_id=current_user.id,
        profile=profile,
        career_title=req.career_title,
        interview_type=req.interview_type,
        difficulty=req.difficulty,
        total_questions=req.total_questions,
        db=db
    )

@router.post("/answer", response_model=InterviewAnswerResponse)
async def submit_interview_answer(
    req: InterviewAnswerRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        return await MockInterviewService.evaluate_answer(
            interview_id=req.interview_id,
            question_id=req.question_id,
            user_answer=req.user_answer,
            user_id=current_user.id,
            db=db
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{interview_id}/complete", response_model=InterviewReportResponse)
async def complete_interview_and_generate_report(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        return await MockInterviewService.generate_final_report(
            interview_id=interview_id,
            user_id=current_user.id,
            db=db
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/history", response_model=List[MockInterviewSessionResponse])
async def get_interview_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(MockInterview).where(MockInterview.user_id == current_user.id).options(
        selectinload(MockInterview.questions),
        selectinload(MockInterview.report)
    ).order_by(MockInterview.created_at.desc())
    result = await db.execute(query)
    interviews = result.scalars().all()
    return [MockInterviewSessionResponse.model_validate(i) for i in interviews]

@router.get("/{interview_id}", response_model=MockInterviewSessionResponse)
async def get_interview_session(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(MockInterview).where(
        MockInterview.id == interview_id,
        MockInterview.user_id == current_user.id
    ).options(
        selectinload(MockInterview.questions),
        selectinload(MockInterview.report)
    )
    result = await db.execute(query)
    interview = result.scalar_one_or_none()

    if not interview:
        raise HTTPException(status_code=404, detail="Mock interview not found")

    return MockInterviewSessionResponse.model_validate(interview)
