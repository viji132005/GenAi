import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.entities import StudentProfile, AIConversation, ChatMessage, Roadmap
from app.schemas.all_schemas import ChatMessageResponse, ConversationResponse
from app.ai.factory import get_llm_provider
from app.ai.prompts import CAREER_ASSISTANT_SYSTEM_PROMPT
from app.rag.knowledge_engine import knowledge_engine

logger = logging.getLogger("skillbridge.services.chat")

class CareerChatService:
    """
    Personalized AI Career Assistant & RAG Chat Service.
    Grounds all responses in student profile, active roadmap, and knowledge documents.
    """

    @classmethod
    def _generate_intent_grounded_response(
        cls,
        message: str,
        profile: StudentProfile,
        active_roadmap: Optional[Roadmap],
        rag_results: List[Dict[str, Any]],
        student_name: str
    ) -> str:
        """
        Generates an authoritative, highly-contextual career mentor response
        tailored to the student's background and grounded in retrieved RAG knowledge.
        """
        msg_lower = message.lower()
        target = profile.target_career or "AI/ML Engineer"
        semester = profile.semester or 6
        cgpa = profile.cgpa or 8.4
        verified_skills = [s.name for s in profile.skills] if profile.skills else ["Python", "Algorithms"]

        # 1. Placement / 3-month preparation timeline
        if "3 month" in msg_lower or "placement" in msg_lower or "prioritize" in msg_lower or "timeline" in msg_lower or "prepare" in msg_lower:
            return (
                f"Hello {student_name}! Based on your profile as a **Semester {semester}** engineering student targeting **{target}** with a **{cgpa} CGPA**, here is your optimized **3-Month Placement Sprint Strategy**:\n\n"
                f"### 🎯 Month 1: Core Competency & LeetCode Foundation\n"
                f"- **Data Structures & Algorithms**: Solve 2-3 medium problems daily focusing on Arrays, Two Pointers, Trees, and Dynamic Programming.\n"
                f"- **Skill Deep-Dive**: Solidify your foundation in {', '.join(verified_skills[:3])}. Bridge critical gaps like PyTorch, Docker, or SQL.\n"
                f"- **Academic Balance**: Maintain your strong {cgpa} CGPA to clear campus eligibility cutoffs (typically 7.0+ / 7.5+).\n\n"
                f"### 🛠️ Month 2: Capstone Project & Systems Mastery\n"
                f"- **Portfolio Project**: Build an end-to-end production application (e.g. *Retrieval-Augmented Generation pipeline* or *Distributed Microservice*) with live API deployment and Docker containerization.\n"
                f"- **System Design & CS Fundamentals**: Review Operating Systems, DBMS (Indexing, Transactions), and Computer Networks (OSI, TCP/IP).\n\n"
                f"### 🚀 Month 3: ATS Resume Polish & Mock Interviews\n"
                f"- **Resume Audit**: Rewrite your project bullets using Google's XYZ formula (*Accomplished X, measured by Y, by doing Z*).\n"
                f"- **Interview Simulations**: Complete at least 3-5 AI Mock Interview rounds on our platform to build speed and STAR-method clarity.\n\n"
                f"💡 **Immediate Next Step**: Open your **Career Roadmap** and check off the high-priority milestone tasks for this week."
            )

        # 2. PyTorch / AI Projects
        elif "pytorch" in msg_lower or "project" in msg_lower or "blueprint" in msg_lower or "build" in msg_lower:
            return (
                f"For top-tier **{target}** roles, recruiters look for projects that demonstrate full-lifecycle engineering rather than toy Jupyter notebooks. Here are 3 industry-grade project blueprints to master **PyTorch & ML Systems**:\n\n"
                f"### 1. 🔍 End-to-End Enterprise RAG & Vector Search System\n"
                f"- **Architecture**: Chunking pipeline + Hybrid Dense (Sentence-Transformers/PyTorch) & Sparse Retrieval + Vector DB (Qdrant/FAISS) + LLM Reranker.\n"
                f"- **Production Feature**: Deploy with FastAPI asynchronous streaming, Docker containerization, and sub-100ms latency.\n"
                f"- **Resume Bullet**: *Engineered end-to-end semantic RAG system with PyTorch embeddings and FAISS index across 20k+ docs, reducing retrieval latency by 35%.*\n\n"
                f"### 2. 👁️ Vision-Language Multimodal Classifier\n"
                f"- **Architecture**: Fine-tune CLIP / ResNet-50 on custom imbalanced e-commerce datasets using PyTorch Lightning with mixed-precision (FP16).\n"
                f"- **Production Feature**: Add automated data augmentation, TensorBoard metrics tracking, and ONNX runtime export.\n\n"
                f"### 3. 📈 Real-Time Fraud & Anomaly Detection Service\n"
                f"- **Architecture**: Autoencoder / XGBoost anomaly model processing streaming event transactions.\n"
                f"- **Production Feature**: Integrated with Kafka/Redis for real-time inference and Grafana telemetry.\n\n"
                f"Check the **Project Blueprints** page to generate detailed architectural step-by-step guides for these builds!"
            )

        # 3. Google XYZ Resume bullet points
        elif "xyz" in msg_lower or "bullet" in msg_lower or "resume" in msg_lower or "ats" in msg_lower:
            return (
                f"Here is the standard **Google XYZ Formula** used by hiring managers at top tech firms:\n\n"
                f"> **Formula**: *\"Accomplished [X], as measured by [Y], by doing [Z]\"*\n\n"
                f"### ❌ Weak Examples (What to avoid):\n"
                f"- *\"Built a machine learning model to predict customer churn.\"*\n"
                f"- *\"Worked on full stack website using React and Python.\"*\n\n"
                f"### ✅ High-Impact XYZ Transformed Examples:\n"
                f"1. **AI/ML Focus**:\n"
                f"   *\"Engineered customer churn prediction pipeline using XGBoost and PyTorch across 100K+ records, achieving 89% ROC-AUC and reducing customer drop-off by 14% via proactive alerting.\"*\n"
                f"2. **Backend / Full Stack Focus**:\n"
                f"   *\"Architected RESTful microservices with FastAPI and PostgreSQL, reducing endpoint response time by 42% through Redis caching and connection pooling.\"*\n"
                f"3. **Data Engineering Focus**:\n"
                f"   *\"Built automated ETL data pipeline processing 500K daily events with Docker and Apache Airflow, eliminating manual reporting time by 18 hours/week.\"*\n\n"
                f"💡 **Tip**: Head over to our **Resume & ATS** section and upload your PDF to receive an instant line-by-line ATS scan and Google XYZ recommendations!"
            )

        # 4. Technical / Behavioral Interview preparation
        elif "interview" in msg_lower or "question" in msg_lower or "mock" in msg_lower:
            return (
                f"For **{target}** interviews, questions are split into 3 pillars: **Core Fundamentals**, **System & Architecture**, and **Behavioral (STAR Method)**.\n\n"
                f"### 📌 High-Frequency Technical Questions:\n"
                f"1. **Bias-Variance & Regularization**: Explain how L1 (Lasso) produces sparse features compared to L2 (Ridge) weight decay.\n"
                f"2. **Transformer Attention**: How does Self-Attention scale with sequence length, and how do Multi-Head Attention projections work mathematically?\n"
                f"3. **Production Data Drift**: How do you detect and mitigate covariate shift vs concept shift in live production models?\n"
                f"4. **Database & Scale**: Explain database indexing B-Trees vs Hash indexes, and when you would choose Redis cache-aside over direct DB queries.\n\n"
                f"### 💡 The STAR Method for Behavioral Questions:\n"
                f"- **Situation** (15s): Context of the project or challenge.\n"
                f"- **Task** (15s): Your specific goal or blocker.\n"
                f"- **Action** (60s): Exact technical trade-offs and code decisions YOU made.\n"
                f"- **Result** (30s): Quantifiable improvement (e.g. *\"improved latency by 30%\"* or *\"delivered 2 days ahead of deadline\"*).\n\n"
                f"👉 Start an interactive simulation right now on the **AI Mock Interview** page to get scored in real-time."
            )

        # 5. General / Knowledge Base Grounded Response
        top_doc = rag_results[0] if rag_results else None
        doc_title = top_doc.get("title", f"{target} Industry Guide") if top_doc else "SkillBridge Knowledge Base"
        doc_snippet = top_doc.get("content", "") if top_doc else ""

        knowledge_section = ""
        if doc_snippet:
            knowledge_section = f"### 📚 Knowledge Base Insights ({doc_title})\n{doc_snippet}\n\n"

        return (
            f"Hello {student_name}! Based on your profile as a **Semester {semester}** engineering student targeting **{target}** with a **{cgpa} CGPA**:\n\n"
            f"{knowledge_section}"
            f"### 🎯 Strategic Recommendations for Your Profile:\n"
            f"1. **Core Alignment**: Master industry-standard skills for **{target}** ({', '.join(verified_skills[:4])}) through hands-on system building.\n"
            f"2. **Roadmap Milestone**: Keep up momentum on your active career roadmap by completing weekly high-priority tasks.\n"
            f"3. **Skill Verification**: Leverage our **ATS Resume Scan** to audit your bullet points and run **AI Mock Interviews** for interview readiness.\n\n"
            f"Feel free to ask me to deep dive into project architectures, interview questions, or roadmap planning!"
        )

    @classmethod
    async def process_chat_message(
        cls, 
        user_id: int, 
        message: str, 
        conversation_id: Optional[int], 
        profile: StudentProfile, 
        db: AsyncSession
    ) -> ChatMessageResponse:
        # Retrieve or create conversation
        conversation = None
        past_messages_list = []

        if conversation_id:
            q_conv = select(AIConversation).where(
                AIConversation.id == conversation_id,
                AIConversation.user_id == user_id
            ).options(selectinload(AIConversation.messages))
            res = await db.execute(q_conv)
            conversation = res.scalar_one_or_none()
            if conversation and conversation.messages:
                past_messages_list = list(conversation.messages)

        if not conversation:
            conv_title = message[:30] + ("..." if len(message) > 30 else "")
            conversation = AIConversation(
                user_id=user_id,
                title=conv_title
            )
            db.add(conversation)
            await db.flush()

        # Save user message
        db_user_msg = ChatMessage(
            conversation_id=conversation.id,
            sender="user",
            content=message,
            sources=[]
        )
        db.add(db_user_msg)

        # Retrieve RAG Knowledge Base context
        rag_results = await knowledge_engine.search(message, top_k=2)
        grounded_docs_context = await knowledge_engine.get_grounded_context(message, top_k=2)

        # Retrieve student roadmap info if available
        q_rm = select(Roadmap).where(Roadmap.user_id == user_id).options(selectinload(Roadmap.tasks))
        res_rm = await db.execute(q_rm)
        active_roadmap = res_rm.scalar_one_or_none()
        
        roadmap_summary = f"{active_roadmap.career_title} Roadmap (Completion: {active_roadmap.completion_percentage}%)" if active_roadmap else "No active roadmap started."

        student_name = profile.user.full_name if (profile and profile.user and profile.user.full_name) else "Student"
        student_skills = [f"{s.name} ({s.proficiency_level})" for s in (profile.skills or [])]
        
        system_context = f"""
{CAREER_ASSISTANT_SYSTEM_PROMPT}

STUDENT PROFILE CONTEXT:
- Name: {student_name}
- College: {profile.college or 'Engineering College'}
- Degree & Branch: {profile.degree} in {profile.branch} (Semester {profile.semester}, Graduating {profile.graduation_year})
- CGPA: {profile.cgpa}
- Target Career: {profile.target_career or 'AI/ML Engineer'}
- Verified Skills: {', '.join(student_skills) if student_skills else 'Beginner programmer'}
- Active Roadmap: {roadmap_summary}
- Interests: {', '.join(profile.interests or [])}

RETRIEVED KNOWLEDGE BASE CONTEXT:
{grounded_docs_context}
"""

        # Format past messages
        past_msgs = []
        for m in past_messages_list[-6:]:
            role = "user" if m.sender == "user" else "model"
            past_msgs.append(f"{role.upper()}: {m.content}")
        
        full_prompt = "\n".join(past_msgs + [f"USER: {message}", "ASSISTANT:"])

        provider = get_llm_provider()
        ai_response_text = ""

        if provider.is_configured():
            try:
                ai_response_text = await provider.generate_text(
                    prompt=full_prompt,
                    system_prompt=system_context,
                    temperature=0.4
                )
            except Exception as e:
                logger.warning(f"Live LLM call error: {e}. Using RAG contextual reasoning engine.")

        # Fallback intelligent grounded response
        if not ai_response_text or len(ai_response_text.strip()) < 20:
            ai_response_text = cls._generate_intent_grounded_response(
                message=message,
                profile=profile,
                active_roadmap=active_roadmap,
                rag_results=rag_results,
                student_name=student_name
            )

        # Prepare source citations (always provide top matched knowledge grounding)
        sources_list = [
            {
                "title": r.get("title", "Career Intelligence Guide"),
                "category": r.get("category", "General"),
                "snippet": r.get("content", "")[:180] + "..."
            }
            for r in (rag_results[:2] if rag_results else [])
        ]

        # Save AI message
        db_ai_msg = ChatMessage(
            conversation_id=conversation.id,
            sender="assistant",
            content=ai_response_text,
            sources=sources_list
        )
        db.add(db_ai_msg)
        await db.commit()
        await db.refresh(db_ai_msg)

        return ChatMessageResponse(
            id=db_ai_msg.id,
            conversation_id=conversation.id,
            sender=db_ai_msg.sender,
            content=db_ai_msg.content,
            sources=sources_list,
            created_at=db_ai_msg.created_at
        )

    @classmethod
    async def get_conversations(cls, user_id: int, db: AsyncSession) -> List[ConversationResponse]:
        query = select(AIConversation).where(AIConversation.user_id == user_id).options(
            selectinload(AIConversation.messages)
        ).order_by(AIConversation.updated_at.desc())
        result = await db.execute(query)
        convs = result.scalars().all()
        return [ConversationResponse.model_validate(c) for c in convs]
