import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel

from app.database.connection import get_db
from app.models.entities import User, StudentProfile, Resume, ResumeAnalysis
from app.schemas.all_schemas import ResumeAnalysisResponse
from app.services.resume_service import ResumeAnalysisService
from app.middleware.auth import get_current_user
from app.config import settings

router = APIRouter(prefix="/resume", tags=["Resume & ATS Analyzer"])

class RawResumeRequest(BaseModel):
    raw_text: str
    filename: str = "Pasted_Resume.txt"

@router.post("/upload", response_model=ResumeAnalysisResponse)
async def upload_resume_pdf(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not file.filename.lower().endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported.")

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    file_bytes = await file.read()
    
    if len(file_bytes) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds 5MB limit.")

    file_path = os.path.join(settings.UPLOAD_DIR, f"{current_user.id}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    if file.filename.lower().endswith(".pdf"):
        raw_text = ResumeAnalysisService.extract_text_from_pdf_bytes(file_bytes)
    else:
        raw_text = file_bytes.decode("utf-8", errors="ignore")

    if not raw_text or len(raw_text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Could not extract readable text from resume file.")

    # Get student profile
    q_prof = select(StudentProfile).where(StudentProfile.user_id == current_user.id).options(
        selectinload(StudentProfile.skills)
    )
    res_prof = await db.execute(q_prof)
    profile = res_prof.scalar_one_or_none()

    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.add(profile)
        await db.commit()

    return await ResumeAnalysisService.analyze_resume(
        user_id=current_user.id,
        filename=file.filename,
        raw_text=raw_text,
        file_path=file_path,
        profile=profile,
        db=db
    )

@router.post("/analyze-text", response_model=ResumeAnalysisResponse)
async def analyze_resume_text(
    req: RawResumeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if len(req.raw_text.strip()) < 20:
        raise HTTPException(status_code=400, detail="Resume text is too short to analyze.")

    q_prof = select(StudentProfile).where(StudentProfile.user_id == current_user.id).options(
        selectinload(StudentProfile.skills)
    )
    res_prof = await db.execute(q_prof)
    profile = res_prof.scalar_one_or_none()

    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.add(profile)
        await db.commit()

    return await ResumeAnalysisService.analyze_resume(
        user_id=current_user.id,
        filename=req.filename,
        raw_text=req.raw_text,
        file_path="in_memory_text",
        profile=profile,
        db=db
    )

@router.get("/latest", response_model=ResumeAnalysisResponse)
async def get_latest_resume_analysis(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(ResumeAnalysis).where(ResumeAnalysis.user_id == current_user.id).order_by(
        ResumeAnalysis.analyzed_at.desc()
    )
    result = await db.execute(query)
    analysis = result.scalar_one_or_none()

    if not analysis:
        raise HTTPException(status_code=404, detail="No resume analysis found.")

    return ResumeAnalysisResponse.model_validate(analysis)
