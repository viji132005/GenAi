import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from app.models.entities import StudentProfile, ProjectRecommendation
from app.schemas.all_schemas import ProjectRecommendationResponse
from app.ai.factory import get_llm_provider
from app.ai.prompts import PROJECT_RECOMMENDATION_SYSTEM_PROMPT

logger = logging.getLogger("skillbridge.services.project")

class LLProjectItem(BaseModel):
    title: str
    difficulty: str
    domain: str
    problem_statement: str
    why_suitable: str
    skills_learned: List[str]
    tech_stack: List[str]
    development_phases: List[Dict[str, Any]]
    portfolio_value: str

class LLProjectsOutput(BaseModel):
    career_goal: str
    recommendations: List[LLProjectItem]

class ProjectRecommendationService:
    """
    AI Project Recommendation Engine.
    Generates personalized project blueprints tailored to missing skills.
    """

    @classmethod
    async def get_or_generate_projects(
        cls, 
        profile: StudentProfile, 
        db: AsyncSession,
        domain_filter: Optional[str] = None,
        difficulty_filter: Optional[str] = None,
        regenerate: bool = False
    ) -> List[ProjectRecommendationResponse]:
        career_goal = profile.target_career or "AI/ML Engineer"

        # Check existing saved projects in DB
        if not regenerate:
            query = select(ProjectRecommendation).where(ProjectRecommendation.user_id == profile.user_id)
            if domain_filter and domain_filter.lower() != "all":
                query = query.where(ProjectRecommendation.domain.ilike(f"%{domain_filter}%"))
            if difficulty_filter and difficulty_filter.lower() != "all":
                query = query.where(ProjectRecommendation.difficulty.ilike(f"%{difficulty_filter}%"))
            
            result = await db.execute(query)
            existing = result.scalars().all()
            if existing and len(existing) >= 3:
                return [ProjectRecommendationResponse.model_validate(p) for p in existing]

        # Generate fresh projects using LLM
        student_skills = [s.name for s in profile.skills]
        
        prompt_data = {
            "name": profile.user.full_name if profile.user else "Student",
            "target_career": career_goal,
            "current_skills": student_skills,
            "domain_preference": domain_filter or "Relevant to Career",
            "difficulty_preference": difficulty_filter or "Intermediate"
        }

        user_prompt = f"""
Generate 4 unique, impressive, and resume-ready software engineering project blueprints for:
{prompt_data}

Include:
1. One Beginner-to-Intermediate foundational project
2. Two Intermediate specialized full-stack/AI projects
3. One Advanced production-grade capstone project

Each project MUST include:
- A realistic business/engineering problem statement (NO generic To-Do apps or Iris classification)
- Specific new skills learned
- Modern tech stack
- 4-stage development phases (Data/API, Business Logic, Frontend/Interface, Deployment & Monitoring)
- Strong resume portfolio value proposition with Google XYZ bullet suggestion.
"""

        provider = get_llm_provider()
        project_dicts = []

        if provider.is_configured():
            try:
                llm_output = await provider.generate_structured(
                    prompt=user_prompt,
                    schema_cls=LLProjectsOutput,
                    system_prompt=PROJECT_RECOMMENDATION_SYSTEM_PROMPT,
                    temperature=0.3
                )
                project_dicts = [p.model_dump() for p in llm_output.recommendations]
            except Exception as e:
                logger.error(f"Error generating projects with LLM: {e}. Using deterministic blueprints.")

        # Fallback blueprints
        if not project_dicts:
            project_dicts = [
                {
                    "title": "Autonomous PDF Research Assistant with Hybrid RAG & Citation Tracking",
                    "difficulty": "Intermediate",
                    "domain": "AI/ML",
                    "problem_statement": "Academic researchers and students struggle to extract synthesized insights from 50+ page technical papers without hallucinations.",
                    "why_suitable": f"Directly bridges your Python foundation into advanced PyTorch, vector embeddings, and LangChain orchestration for {career_goal}.",
                    "skills_learned": ["PyTorch", "ChromaDB", "FastAPI", "Vector Embeddings", "Prompt Engineering"],
                    "tech_stack": ["Python", "FastAPI", "ChromaDB", "Google Gemini API", "React", "Docker"],
                    "development_phases": [
                        {"stage": "Phase 1", "objective": "Document parsing, chunking with overlap, and vector indexing in ChromaDB."},
                        {"stage": "Phase 2", "objective": "Semantic search retrieval pipeline with reciprocal rank fusion (RRF)."},
                        {"stage": "Phase 3", "objective": "FastAPI streaming endpoints with source citation metadata."},
                        {"stage": "Phase 4", "objective": "Modern dark glassmorphic React UI and Docker containerization."}
                    ],
                    "portfolio_value": "Demonstrates practical GenAI and MLOps engineering beyond simple wrapper scripts."
                },
                {
                    "title": "Real-time High-Throughput E-Commerce Anomaly & Fraud Detection Engine",
                    "difficulty": "Intermediate",
                    "domain": "Data Science",
                    "problem_statement": "Payment gateways experience fraudulent micro-transactions that slip past rule-based triggers, causing merchant chargebacks.",
                    "why_suitable": "Showcases end-to-end data pipeline design, feature engineering, and real-time model inference.",
                    "skills_learned": ["Scikit-Learn", "XGBoost", "Redis Caching", "Docker", "SQL"],
                    "tech_stack": ["Python", "Pandas", "Scikit-Learn", "Redis", "PostgreSQL", "FastAPI"],
                    "development_phases": [
                        {"stage": "Phase 1", "objective": "Feature engineering on transaction velocity, geolocation deviation, and amount ratios."},
                        {"stage": "Phase 2", "objective": "Isolation Forest and XGBoost model training with cross-validation."},
                        {"stage": "Phase 3", "objective": "Sub-40ms Redis cached scoring pipeline with REST API trigger."},
                        {"stage": "Phase 4", "objective": "Interactive analytics dashboard for live risk visualization."}
                    ],
                    "portfolio_value": "Proves quantitative impact on financial loss prevention with measurable low-latency SLAs."
                },
                {
                    "title": "Distributed Multi-Tenant Task Orchestrator & Worker Pipeline",
                    "difficulty": "Advanced",
                    "domain": "Web Development",
                    "problem_statement": "Background data-processing jobs cause CPU spikes and timeouts in synchronous web backends.",
                    "why_suitable": "Highlights distributed systems mastery, concurrency, caching, and robust database transactions.",
                    "skills_learned": ["Distributed Systems", "Message Queues", "Docker", "PostgreSQL Indexing"],
                    "tech_stack": ["Node.js / Python", "Redis", "Celery / BullMQ", "Docker", "PostgreSQL", "React"],
                    "development_phases": [
                        {"stage": "Phase 1", "objective": "Queue architecture design with priority queues and exponential backoff retry."},
                        {"stage": "Phase 2", "objective": "Worker pool scaling and concurrency management."},
                        {"stage": "Phase 3", "objective": "Real-time WebSocket telemetry for execution progress."},
                        {"stage": "Phase 4", "objective": "Containerized multi-service deployment with Docker Compose."}
                    ],
                    "portfolio_value": "Signals senior backend competency in asynchronous architectures and reliability engineering."
                },
                {
                    "title": "Zero-Trust Cloud Infrastructure & Security Vulnerability Scanner",
                    "difficulty": "Advanced",
                    "domain": "Cybersecurity",
                    "problem_statement": "Misconfigured S3 buckets and exposed API secrets frequently cause compliance and data privacy breaches.",
                    "why_suitable": "Establishes domain knowledge in cloud security automation, IAM, and static security auditing.",
                    "skills_learned": ["Cloud Security", "OWASP Top 10", "Python AST Analysis", "Docker"],
                    "tech_stack": ["Python", "AWS SDK (Boto3)", "FastAPI", "React", "Docker"],
                    "development_phases": [
                        {"stage": "Phase 1", "objective": "Rule engine for detecting open ports, IAM wildcards, and exposed credentials."},
                        {"stage": "Phase 2", "objective": "Automated remediation script triggers and Slack webhook notifications."},
                        {"stage": "Phase 3", "objective": "Compliance scorecard generator against CIS benchmarks."},
                        {"stage": "Phase 4", "objective": "Deploying as a scheduled serverless cron job."}
                    ],
                    "portfolio_value": "Highly valued for enterprise security analyst and DevSecOps engineering roles."
                }
            ]

        # Save to DB
        saved_entities = []
        for p in project_dicts:
            db_p = ProjectRecommendation(
                user_id=profile.user_id,
                career_goal=career_goal,
                title=p["title"],
                difficulty=p.get("difficulty", "Intermediate"),
                domain=p.get("domain", "AI/ML"),
                problem_statement=p.get("problem_statement", ""),
                why_suitable=p.get("why_suitable", ""),
                skills_learned=p.get("skills_learned", []),
                tech_stack=p.get("tech_stack", []),
                development_phases=p.get("development_phases", []),
                portfolio_value=p.get("portfolio_value", ""),
                is_bookmarked=False,
                is_completed=False
            )
            db.add(db_p)
            saved_entities.append(db_p)

        await db.commit()
        for e in saved_entities:
            await db.refresh(e)

        return [ProjectRecommendationResponse.model_validate(e) for e in saved_entities]

    @classmethod
    async def toggle_project_bookmark(cls, project_id: int, user_id: int, db: AsyncSession) -> ProjectRecommendationResponse:
        query = select(ProjectRecommendation).where(
            ProjectRecommendation.id == project_id, 
            ProjectRecommendation.user_id == user_id
        )
        res = await db.execute(query)
        proj = res.scalar_one_or_none()
        if not proj:
            raise ValueError("Project not found")
        
        proj.is_bookmarked = not proj.is_bookmarked
        await db.commit()
        await db.refresh(proj)
        return ProjectRecommendationResponse.model_validate(proj)
