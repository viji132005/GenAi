import logging
import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel

from app.models.entities import StudentProfile, Roadmap, RoadmapTask, Skill
from app.schemas.all_schemas import RoadmapResponse, RoadmapTaskResponse
from app.ai.factory import get_llm_provider
from app.ai.prompts import ROADMAP_SYSTEM_PROMPT

logger = logging.getLogger("skillbridge.services.roadmap")

class LLRoadmapTask(BaseModel):
    phase_number: int
    phase_name: str
    task_title: str
    description: str
    skills_covered: List[str]
    learning_resources: List[Dict[str, str]]
    project_checkpoint: str
    estimated_hours: int
    sort_order: int

class LLRoadmapOutput(BaseModel):
    career_title: str
    title: str
    target_duration_months: int
    overview_summary: str
    tasks: List[LLRoadmapTask]

class RoadmapService:
    """
    Personalized Career Roadmap Generator & Progress Tracker.
    """

    @classmethod
    async def get_or_generate_roadmap(
        cls, 
        profile: StudentProfile, 
        db: AsyncSession,
        regenerate: bool = False
    ) -> RoadmapResponse:
        career_title = profile.target_career or "AI/ML Engineer"

        # Check existing roadmap
        if not regenerate:
            query = select(Roadmap).where(
                Roadmap.user_id == profile.user_id,
                Roadmap.career_title == career_title
            ).options(selectinload(Roadmap.tasks))
            result = await db.execute(query)
            existing_roadmap = result.scalar_one_or_none()
            if existing_roadmap and existing_roadmap.tasks:
                return RoadmapResponse.model_validate(existing_roadmap)

        # Delete older roadmap for this career if regenerating
        del_query = select(Roadmap).where(Roadmap.user_id == profile.user_id)
        res = await db.execute(del_query)
        old_roadmaps = res.scalars().all()
        for r in old_roadmaps:
            await db.delete(r)
        await db.commit()

        # Build LLM context
        student_skills = [f"{s.name} ({s.proficiency_level})" for s in profile.skills]
        
        prompt_data = {
            "name": profile.user.full_name if profile.user else "Student",
            "target_career": career_title,
            "current_semester": profile.semester,
            "graduation_year": profile.graduation_year,
            "existing_skills": student_skills,
            "coursework": profile.coursework or [],
            "interests": profile.interests or []
        }

        user_prompt = f"""
Generate a personalized, highly structured 6-phase career readiness roadmap for:
Student Profile:
{prompt_data}

Target Career: {career_title}

Design 6 to 7 progressive phases:
Phase 1: Foundational Prerequisites & Revision
Phase 2: Deep Core Specialization
Phase 3: Modern Frameworks & Tooling
Phase 4: Production Deployment & MLOps/DevOps
Phase 5: Real-World Portfolio Projects
Phase 6: Resume & ATS Optimization
Phase 7: Technical & Behavioral Mock Interview Preparation

Each task MUST have:
- Clear objective and description
- Specific skills covered
- 2 reputable resource links with titles and URLs
- A concrete project/exercise checkpoint
- Realistic estimated study hours
"""

        provider = get_llm_provider()
        tasks_data = []
        roadmap_title = f"{career_title} Career Mastery Roadmap"
        duration_months = 6
        overview_summary = f"A customized {duration_months}-month milestone roadmap to transition from college foundations to a job-ready {career_title}."

        if provider.is_configured():
            try:
                llm_output = await provider.generate_structured(
                    prompt=user_prompt,
                    schema_cls=LLRoadmapOutput,
                    system_prompt=ROADMAP_SYSTEM_PROMPT,
                    temperature=0.3
                )
                roadmap_title = llm_output.title
                duration_months = llm_output.target_duration_months
                overview_summary = llm_output.overview_summary
                tasks_data = [t.model_dump() for t in llm_output.tasks]
            except Exception as e:
                logger.error(f"Error generating roadmap via LLM: {e}. Using deterministic curriculum.")

        # Fallback curriculum if LLM not configured or failed
        if not tasks_data:
            tasks_data = [
                {
                    "phase_number": 1,
                    "phase_name": "Phase 1: Core Engineering Foundations",
                    "task_title": "Python & Data Structures Mastery",
                    "description": "Master clean coding, OOP, time complexity, and data manipulation libraries.",
                    "skills_covered": ["Python", "Algorithms", "NumPy"],
                    "learning_resources": [
                        {"title": "Python Official Documentation", "url": "https://docs.python.org/3/"},
                        {"title": "LeetCode Clean Code Patterns", "url": "https://leetcode.com"}
                    ],
                    "project_checkpoint": "Implement custom matrix operations and benchmark against NumPy arrays.",
                    "estimated_hours": 20,
                    "sort_order": 1
                },
                {
                    "phase_number": 2,
                    "phase_name": "Phase 2: Deep Core Specialization",
                    "task_title": "Applied Machine Learning & Statistical Modeling",
                    "description": "Implement regression, classification, clustering, cross-validation, and hyperparameter tuning.",
                    "skills_covered": ["Scikit-Learn", "Pandas", "Statistics"],
                    "learning_resources": [
                        {"title": "Scikit-Learn User Guide", "url": "https://scikit-learn.org"},
                        {"title": "Kaggle Micro-courses on ML", "url": "https://kaggle.com/learn"}
                    ],
                    "project_checkpoint": "Build an end-to-end churn prediction pipeline with 85%+ ROC-AUC.",
                    "estimated_hours": 30,
                    "sort_order": 2
                },
                {
                    "phase_number": 3,
                    "phase_name": "Phase 3: Modern Deep Learning Frameworks",
                    "task_title": "PyTorch Neural Architectures & Training",
                    "description": "Build CNNs, Transformers, autograd mechanics, custom datasets, and loss functions.",
                    "skills_covered": ["PyTorch", "Deep Learning", "Transformers"],
                    "learning_resources": [
                        {"title": "PyTorch Official Tutorials", "url": "https://pytorch.org/tutorials"},
                        {"title": "Hugging Face Course", "url": "https://huggingface.co/course"}
                    ],
                    "project_checkpoint": "Train and fine-tune a Transformer model for domain-specific text classification.",
                    "estimated_hours": 35,
                    "sort_order": 3
                },
                {
                    "phase_number": 4,
                    "phase_name": "Phase 4: Production Deployment & MLOps",
                    "task_title": "Containerization & FastAPI Microservice Serving",
                    "description": "Wrap models into REST endpoints, containerize using Docker, and configure caching.",
                    "skills_covered": ["FastAPI", "Docker", "REST APIs"],
                    "learning_resources": [
                        {"title": "FastAPI Documentation", "url": "https://fastapi.tiangolo.com"},
                        {"title": "Docker Getting Started Guide", "url": "https://docs.docker.com/get-started/"}
                    ],
                    "project_checkpoint": "Deploy a multi-worker Dockerized API container with sub-100ms response time.",
                    "estimated_hours": 25,
                    "sort_order": 4
                },
                {
                    "phase_number": 5,
                    "phase_name": "Phase 5: Real-World Portfolio Project",
                    "task_title": "Full-Stack AI Application with RAG",
                    "description": "Construct a production RAG system with ChromaDB/FAISS vector retrieval and streaming UI.",
                    "skills_covered": ["RAG", "Vector Databases", "LangChain", "React"],
                    "learning_resources": [
                        {"title": "ChromaDB Documentation", "url": "https://docs.trychroma.com"},
                        {"title": "Building Production RAG Systems", "url": "https://github.com"}
                    ],
                    "project_checkpoint": "Publish public GitHub repo with live cloud demo link and architecture diagram.",
                    "estimated_hours": 40,
                    "sort_order": 5
                },
                {
                    "phase_number": 6,
                    "phase_name": "Phase 6: Resume & Interview Readiness",
                    "task_title": "ATS Resume Audit & Live Mock Interviews",
                    "description": "Quantify resume project bullets using Google XYZ format and practice 10+ mock interview rounds.",
                    "skills_covered": ["Resume Optimization", "Mock Interview", "STAR Method"],
                    "learning_resources": [
                        {"title": "SkillBridge AI Resume Guide", "url": "https://skillbridge.ai/guide"},
                        {"title": "Tech Interview Handbook", "url": "https://techinterviewhandbook.org"}
                    ],
                    "project_checkpoint": "Achieve 80%+ on Resume ATS Score and 75%+ on SkillBridge Mock Interview.",
                    "estimated_hours": 15,
                    "sort_order": 6
                }
            ]

        # Save to Database
        db_roadmap = Roadmap(
            user_id=profile.user_id,
            career_title=career_title,
            title=roadmap_title,
            target_duration_months=duration_months,
            completion_percentage=0.0,
            overview_summary=overview_summary
        )
        db.add(db_roadmap)
        await db.flush()

        for t_dict in tasks_data:
            db_task = RoadmapTask(
                roadmap_id=db_roadmap.id,
                phase_number=t_dict.get("phase_number", 1),
                phase_name=t_dict.get("phase_name", "Phase 1"),
                task_title=t_dict.get("task_title", "Task"),
                description=t_dict.get("description", ""),
                skills_covered=t_dict.get("skills_covered", []),
                learning_resources=t_dict.get("learning_resources", []),
                project_checkpoint=t_dict.get("project_checkpoint", ""),
                estimated_hours=t_dict.get("estimated_hours", 10),
                is_completed=False,
                sort_order=t_dict.get("sort_order", 1)
            )
            db.add(db_task)

        await db.commit()

        # Re-query with tasks loaded
        query = select(Roadmap).where(Roadmap.id == db_roadmap.id).options(selectinload(Roadmap.tasks))
        res = await db.execute(query)
        saved_roadmap = res.scalar_one()

        return RoadmapResponse.model_validate(saved_roadmap)

    @classmethod
    async def toggle_task_status(
        cls, 
        task_id: int, 
        is_completed: bool, 
        user_id: int, 
        db: AsyncSession
    ) -> RoadmapResponse:
        """Toggle a roadmap task status and update overall progress percentage."""
        query = select(RoadmapTask).where(RoadmapTask.id == task_id).options(
            selectinload(RoadmapTask.roadmap).selectinload(Roadmap.tasks)
        )
        result = await db.execute(query)
        task = result.scalar_one_or_none()

        if not task or task.roadmap.user_id != user_id:
            raise ValueError("Task not found or access denied")

        task.is_completed = is_completed
        task.completed_at = datetime.datetime.utcnow() if is_completed else None

        # Recalculate roadmap completion percentage
        roadmap = task.roadmap
        total_tasks = len(roadmap.tasks)
        completed_tasks = sum(1 for t in roadmap.tasks if t.is_completed)
        roadmap.completion_percentage = round((completed_tasks / (total_tasks or 1)) * 100, 1)

        await db.commit()
        await db.refresh(roadmap)

        return RoadmapResponse.model_validate(roadmap)
