from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database.connection import get_db
from app.models.entities import User, StudentProfile
from app.schemas.all_schemas import ChatMessageRequest, ChatMessageResponse, ConversationResponse
from app.services.chat_service import CareerChatService
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/chat", tags=["AI Career Assistant & RAG Chat"])

@router.post("", response_model=ChatMessageResponse)
async def send_chat_message(
    req: ChatMessageRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    q_prof = select(StudentProfile).where(StudentProfile.user_id == current_user.id).options(
        selectinload(StudentProfile.skills),
        selectinload(StudentProfile.user)
    )
    res_prof = await db.execute(q_prof)
    profile = res_prof.scalar_one_or_none()

    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.add(profile)
        await db.commit()

    return await CareerChatService.process_chat_message(
        user_id=current_user.id,
        message=req.message,
        conversation_id=req.conversation_id,
        profile=profile,
        db=db
    )

@router.get("/conversations", response_model=List[ConversationResponse])
async def get_chat_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await CareerChatService.get_conversations(current_user.id, db)
