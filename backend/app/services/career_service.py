import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel, Field

from app.models.entities import StudentProfile, CareerProfile, CareerSkill, Skill
from app.schemas.all_schemas import CareerRecommendationItem, CareerAnalysisResponse
from app.ai.factory import get_llm_provider
from app.ai.prompts import CAREER_ANALYSIS_SYSTEM_PROMPT

logger = logging.getLogger("skillbridge.services.career")

class LLCareerItem(BaseModel):
    career_title: str
    match_percentage: float
    why_matches: str
    existing_strengths: List[str]
    missing_skills: List[str]
    suggested_technologies: List[str]
    typical_responsibilities: List[str]
    suggested_projects: List[str]
    learning_path_summary: str
    growth_outlook: str
    average_salary: str

class LLCareerAnalysisOutput(BaseModel):
    target_career: str
    top_recommendations: List[LLCareerItem]
    overall_profile_summary: str
    readiness_score: float
    next_immediate_action: str

class CareerAnalysisService:
    """
    Career Analysis & Recommendation Service.
    Evaluates student background against industry standards using structured algorithms
    and LLM synthesis.
    """

    @staticmethod
    def calculate_deterministic_match(
        student_skills: List[str], 
        career_skills: List[str], 
        academic_bonus: float = 0.0
    ) -> float:
        """Calculates a baseline grounded match percentage between student and career skills."""
        if not career_skills:
            return 50.0
        
        student_set = {s.lower().strip() for s in student_skills}
        matched = sum(1 for cs in career_skills if any(ss in cs.lower() or cs.lower() in ss for ss in student_set))
        base_ratio = matched / len(career_skills)
        
        # Scale to 30-95%
        score = 30.0 + (base_ratio * 60.0) + academic_bonus
        return round(min(max(score, 25.0), 96.0), 1)

    @classmethod
    async def analyze_student_career(
        cls, 
        profile: StudentProfile, 
        db: AsyncSession
    ) -> CareerAnalysisResponse:
        """Generate comprehensive career recommendations for a student profile."""
        
        # Fetch all available career profiles and skills from DB
        query = select(CareerProfile).options(selectinload(CareerProfile.skills))
        result = await db.execute(query)
        careers = result.scalars().all()
        
        student_skill_names = [s.name for s in profile.skills]
        target_career = profile.target_career or (careers[0].title if careers else "AI/ML Engineer")

        # Build prompt payload
        profile_context = {
            "name": profile.user.full_name if profile.user else "Student",
            "college": profile.college,
            "degree": profile.degree,
            "branch": profile.branch,
            "semester": profile.semester,
            "cgpa": profile.cgpa,
            "target_career": target_career,
            "interests": profile.interests or [],
            "skills": [f"{s.name} ({s.proficiency_level})" for s in profile.skills],
            "coursework": profile.coursework or [],
            "certifications": profile.certifications or [],
            "experience": profile.experience or [],
            "achievements": profile.achievements or []
        }

        career_catalogs = []
        for c in careers:
            c_skills = [cs.skill_name for cs in c.skills]
            match_est = cls.calculate_deterministic_match(student_skill_names, c_skills)
            career_catalogs.append({
                "title": c.title,
                "category": c.category,
                "required_skills": c_skills,
                "base_match_estimate": match_est,
                "growth": c.growth_outlook,
                "salary": c.average_salary
            })

        user_prompt = f"""
Student Profile:
{profile_context}

Available Career Pathways Catalog:
{career_catalogs}

Generate a comprehensive Career Recommendation analysis.
Ensure the top recommendations include the student's target career ('{target_career}') along with 3-4 other closely aligned pathways.
Calculate realistic match percentages and explain the technical reasoning based strictly on the student's real skills and coursework.
"""

        provider = get_llm_provider()
        
        if provider.is_configured():
            try:
                llm_output = await provider.generate_structured(
                    prompt=user_prompt,
                    schema_cls=LLCareerAnalysisOutput,
                    system_prompt=CAREER_ANALYSIS_SYSTEM_PROMPT,
                    temperature=0.3
                )
                
                # Transform to response schema
                recommendations = [
                    CareerRecommendationItem(
                        career_title=item.career_title,
                        category=item.category if hasattr(item, 'category') else "Engineering",
                        match_percentage=item.match_percentage,
                        why_matches=item.why_matches,
                        existing_strengths=item.existing_strengths,
                        missing_skills=item.missing_skills,
                        suggested_technologies=item.suggested_technologies,
                        typical_responsibilities=item.typical_responsibilities,
                        suggested_projects=item.suggested_projects,
                        learning_path_summary=item.learning_path_summary,
                        growth_outlook=item.growth_outlook,
                        average_salary=item.average_salary
                    )
                    for item in llm_output.top_recommendations
                ]
                
                return CareerAnalysisResponse(
                    target_career=llm_output.target_career,
                    top_recommendations=recommendations,
                    overall_profile_summary=llm_output.overall_profile_summary,
                    readiness_score=llm_output.readiness_score,
                    next_immediate_action=llm_output.next_immediate_action
                )
            except Exception as e:
                logger.error(f"Error calling LLM for career analysis: {e}. Using deterministic engine.")

        # Fallback deterministic analysis when LLM API key is not configured or fails
        fallback_recs = []
        for c in careers[:5]:
            c_skills = [cs.skill_name for cs in c.skills]
            match_score = cls.calculate_deterministic_match(student_skill_names, c_skills)
            
            # Find matched vs missing
            matched = [s for s in c_skills if any(ss.lower() in s.lower() for ss in student_skill_names)]
            missing = [s for s in c_skills if s not in matched]
            
            fallback_recs.append(CareerRecommendationItem(
                career_title=c.title,
                category=c.category,
                match_percentage=match_score,
                why_matches=f"Your foundation in {', '.join(matched[:3]) if matched else 'core programming'} gives you a direct bridge into {c.title}.",
                existing_strengths=matched if matched else ["Core Engineering Fundamentals"],
                missing_skills=missing[:4] if missing else ["Advanced Production Deployment"],
                suggested_technologies=c.typical_technologies or c_skills[:5],
                typical_responsibilities=c.responsibilities or ["Build, optimize, and maintain scalable systems."],
                suggested_projects=[f"Build an end-to-end {c.title} portfolio project with {missing[0] if missing else 'Docker'}"],
                learning_path_summary=f"Focus on mastering {', '.join(missing[:3]) if missing else 'advanced concepts'} over the next 12-16 weeks.",
                growth_outlook=c.growth_outlook or "High",
                average_salary=c.average_salary or "$115,000 - $155,000"
            ))

        fallback_recs.sort(key=lambda x: x.match_percentage, reverse=True)
        
        target_match = next((r.match_percentage for r in fallback_recs if r.career_title.lower() == target_career.lower()), fallback_recs[0].match_percentage if fallback_recs else 65.0)

        return CareerAnalysisResponse(
            target_career=target_career,
            top_recommendations=fallback_recs,
            overall_profile_summary=f"Student has solid foundations in {', '.join(student_skill_names[:4]) if student_skill_names else 'computer science'} with strong alignment toward {target_career}.",
            readiness_score=round(target_match * 0.85, 1),
            next_immediate_action=f"Complete the fundamental module for {fallback_recs[0].missing_skills[0] if fallback_recs and fallback_recs[0].missing_skills else 'PyTorch'}."
        )
