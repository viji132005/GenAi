import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel

from app.models.entities import StudentProfile, CareerProfile, CareerSkill, Skill
from app.schemas.all_schemas import SkillGapItem, SkillGapAnalysisResponse
from app.ai.factory import get_llm_provider
from app.ai.prompts import SKILL_GAP_SYSTEM_PROMPT

logger = logging.getLogger("skillbridge.services.skill_gap")

class LLSkillGapItem(BaseModel):
    skill_name: str
    category: str
    importance_level: str
    current_status: str
    current_proficiency: Optional[str] = None
    required_proficiency: str
    recommended_resources: List[Dict[str, str]]
    learning_priority_order: int
    estimated_weeks: int

class LLSkillGapOutput(BaseModel):
    career_title: str
    overall_match_score: float
    acquired_skills: List[LLSkillGapItem]
    partial_skills: List[LLSkillGapItem]
    missing_skills: List[LLSkillGapItem]
    high_priority_gaps: List[str]
    recommended_action_plan: str

class SkillGapService:
    """
    Skill Gap Analysis Service.
    Maps current student skills against target career requirement profiles,
    categorizing into Acquired, Partial, and Missing with prioritized resources.
    """

    @classmethod
    async def analyze_skill_gaps(
        cls, 
        profile: StudentProfile, 
        target_career_title: Optional[str], 
        db: AsyncSession
    ) -> SkillGapAnalysisResponse:
        career_title = target_career_title or profile.target_career or "AI/ML Engineer"

        # Fetch career profile & required skills
        query = select(CareerProfile).where(CareerProfile.title.ilike(f"%{career_title}%")).options(
            selectinload(CareerProfile.skills)
        )
        result = await db.execute(query)
        career = result.scalar_one_or_none()

        if not career:
            # Fallback to first available career
            q2 = select(CareerProfile).options(selectinload(CareerProfile.skills))
            res2 = await db.execute(q2)
            career = res2.scalar_one_or_none()
            if career:
                career_title = career.title

        # Map student skills
        student_skills_map = {s.name.lower().strip(): s.proficiency_level for s in profile.skills}
        
        career_skills = career.skills if career else []
        
        prompt_data = {
            "student_profile": {
                "name": profile.user.full_name if profile.user else "Student",
                "semester": profile.semester,
                "degree": profile.degree,
                "current_skills": [{"name": s.name, "proficiency": s.proficiency_level} for s in profile.skills],
            },
            "target_career": career_title,
            "required_career_skills": [
                {
                    "skill_name": cs.skill_name,
                    "category": cs.category,
                    "importance": cs.importance_level,
                    "min_proficiency": cs.min_proficiency,
                    "resources": cs.learning_resources or []
                }
                for cs in career_skills
            ]
        }

        user_prompt = f"""
Analyze the student's exact skill gaps for the career '{career_title}'.
Input Data:
{prompt_data}

Categorize each skill into:
1. 'acquired' (student has it with sufficient proficiency)
2. 'partial' (student has basic knowledge but needs intermediate/advanced mastery)
3. 'missing' (student does not have this critical requirement)

Provide realistic high-priority gaps, reputable learning resources (documentation, interactive platforms), and estimated study weeks for each missing/partial skill.
"""

        provider = get_llm_provider()

        if provider.is_configured():
            try:
                llm_output = await provider.generate_structured(
                    prompt=user_prompt,
                    schema_cls=LLSkillGapOutput,
                    system_prompt=SKILL_GAP_SYSTEM_PROMPT,
                    temperature=0.2
                )
                return SkillGapAnalysisResponse(
                    career_title=llm_output.career_title,
                    overall_match_score=llm_output.overall_match_score,
                    acquired_skills=[SkillGapItem(**item.model_dump()) for item in llm_output.acquired_skills],
                    partial_skills=[SkillGapItem(**item.model_dump()) for item in llm_output.partial_skills],
                    missing_skills=[SkillGapItem(**item.model_dump()) for item in llm_output.missing_skills],
                    high_priority_gaps=llm_output.high_priority_gaps,
                    recommended_action_plan=llm_output.recommended_action_plan
                )
            except Exception as e:
                logger.error(f"Error calling LLM for skill gap analysis: {e}. Using deterministic engine.")

        # Fallback deterministic analysis
        acquired = []
        partial = []
        missing = []
        high_gaps = []

        proficiency_ranks = {"beginner": 1, "intermediate": 2, "advanced": 3}

        for idx, cs in enumerate(career_skills, 1):
            cs_lower = cs.skill_name.lower().strip()
            student_prof = student_skills_map.get(cs_lower)
            req_rank = proficiency_ranks.get(cs.min_proficiency.lower(), 2)

            resources = cs.learning_resources or [
                {"title": f"Official {cs.skill_name} Documentation", "url": f"https://devdocs.io/{cs_lower}"},
                {"title": f"{cs.skill_name} Hands-on Practice Guide", "url": "https://coursera.org"}
            ]

            if student_prof:
                stu_rank = proficiency_ranks.get(student_prof.lower(), 1)
                if stu_rank >= req_rank:
                    acquired.append(SkillGapItem(
                        skill_name=cs.skill_name,
                        category=cs.category,
                        importance_level=cs.importance_level,
                        current_status="acquired",
                        current_proficiency=student_prof,
                        required_proficiency=cs.min_proficiency,
                        recommended_resources=resources,
                        learning_priority_order=idx,
                        estimated_weeks=0
                    ))
                else:
                    partial.append(SkillGapItem(
                        skill_name=cs.skill_name,
                        category=cs.category,
                        importance_level=cs.importance_level,
                        current_status="partial",
                        current_proficiency=student_prof,
                        required_proficiency=cs.min_proficiency,
                        recommended_resources=resources,
                        learning_priority_order=idx,
                        estimated_weeks=3
                    ))
                    if cs.importance_level == "High":
                        high_gaps.append(cs.skill_name)
            else:
                missing.append(SkillGapItem(
                    skill_name=cs.skill_name,
                    category=cs.category,
                    importance_level=cs.importance_level,
                    current_status="missing",
                    current_proficiency="None",
                    required_proficiency=cs.min_proficiency,
                    recommended_resources=resources,
                    learning_priority_order=idx,
                    estimated_weeks=4 if cs.importance_level == "High" else 2
                ))
                if cs.importance_level == "High":
                    high_gaps.append(cs.skill_name)

        total_req = len(career_skills) or 1
        match_score = round(((len(acquired) + (len(partial) * 0.5)) / total_req) * 100, 1)

        return SkillGapAnalysisResponse(
            career_title=career_title,
            overall_match_score=min(match_score, 95.0),
            acquired_skills=acquired,
            partial_skills=partial,
            missing_skills=missing,
            high_priority_gaps=high_gaps[:3] if high_gaps else (missing[0].skill_name if missing else ["Docker"]),
            recommended_action_plan=f"Focus first on high priority gaps: {', '.join(high_gaps[:3]) if high_gaps else 'Core Specializations'} before starting project integration."
        )
