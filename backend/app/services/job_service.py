import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.models.entities import StudentProfile, JobAnalysis
from app.schemas.all_schemas import JobAnalysisResponse
from app.ai.factory import get_llm_provider
from app.ai.prompts import JOB_ANALYSIS_SYSTEM_PROMPT

logger = logging.getLogger("skillbridge.services.job")

class LLJobAnalysisOutput(BaseModel):
    match_score: float
    strong_matches: List[str]
    skill_gaps: List[str]
    required_skills: List[str]
    preferred_skills: List[str]
    experience_requirements: str
    recommendations: List[str]
    action_plan: List[str]

class JobAnalysisService:
    """
    Job Description Compatibility & Gap Analyzer Service.
    """

    @classmethod
    async def analyze_job_description(
        cls, 
        user_id: int, 
        job_title: str, 
        company: str, 
        job_description: str, 
        profile: StudentProfile, 
        db: AsyncSession
    ) -> JobAnalysisResponse:
        student_skills = [s.name for s in profile.skills]
        
        prompt_data = {
            "student_profile": {
                "name": profile.user.full_name if profile.user else "Student",
                "degree": profile.degree,
                "branch": profile.branch,
                "semester": profile.semester,
                "cgpa": profile.cgpa,
                "target_career": profile.target_career,
                "skills": [f"{s.name} ({s.proficiency_level})" for s in profile.skills],
                "projects": profile.achievements or []
            },
            "job_posting": {
                "title": job_title,
                "company": company,
                "description": job_description[:4000]
            }
        }

        user_prompt = f"""
Compare the student's background against this job posting:
{prompt_data}

1. Extract all REQUIRED technical skills and PREFERRED skills from the job description.
2. Cross-reference against the student's actual skills.
3. Compute an objective Job Match Score (0 to 100%).
4. List strong matching competencies and missing critical gaps.
5. Create a prioritized 3-step immediate action plan to make the student competitive for this specific role.
"""

        provider = get_llm_provider()
        analysis_dict = None

        if provider.is_configured() and len(job_description.strip()) > 30:
            try:
                llm_output = await provider.generate_structured(
                    prompt=user_prompt,
                    schema_cls=LLJobAnalysisOutput,
                    system_prompt=JOB_ANALYSIS_SYSTEM_PROMPT,
                    temperature=0.2
                )
                analysis_dict = llm_output.model_dump()
            except Exception as e:
                logger.error(f"Error calling LLM for job analysis: {e}. Using deterministic parser.")

        # Fallback deterministic analysis
        if not analysis_dict:
            jd_lower = job_description.lower()
            
            # Common tech skills to check
            sample_techs = ["python", "sql", "javascript", "react", "docker", "aws", "machine learning", "pytorch", "tensorflow", "fastapi", "git", "linux", "c++", "java"]
            required = [t.title() for t in sample_techs if t in jd_lower] or ["Python", "SQL", "Git"]
            preferred = ["Docker", "AWS", "CI/CD", "PyTorch"]
            
            matches = [s for s in student_skills if any(s.lower() in req.lower() for req in required)]
            gaps = [r for r in required if not any(s.lower() in r.lower() for s in student_skills)]
            
            total_req = len(required) or 1
            score = round((len(matches) / total_req) * 100.0, 1)
            score = max(min(score, 92.0), 35.0)

            analysis_dict = {
                "match_score": score,
                "strong_matches": matches if matches else ["Core Computer Science Fundamentals"],
                "skill_gaps": gaps[:4] if gaps else ["Cloud Deployment Basics"],
                "required_skills": required,
                "preferred_skills": preferred,
                "experience_requirements": "0-2 years / Entry-level or College Graduate",
                "recommendations": [
                    f"Build a focused mini-project showcasing {gaps[0] if gaps else 'Docker'}",
                    "Tailor your resume headline and summary to highlight matching skills: " + ", ".join(matches[:3]),
                    "Review core interview questions on " + (gaps[0] if gaps else "System Architecture")
                ],
                "action_plan": [
                    f"Step 1: Dedicate 1 week to complete a crash course on {gaps[0] if gaps else 'AWS'}.",
                    f"Step 2: Add a containerized demonstration project to your GitHub linking to this job's requirements.",
                    "Step 3: Practice mock interview questions focused on technical problem solving and live coding."
                ]
            }

        # Save to DB
        db_job = JobAnalysis(
            user_id=user_id,
            job_title=job_title or "Target Role",
            company=company or "Technology Company",
            raw_job_description=job_description[:5000],
            match_score=analysis_dict["match_score"],
            matching_skills=analysis_dict["strong_matches"],
            missing_skills=analysis_dict["skill_gaps"],
            requirements_extracted={
                "required": analysis_dict["required_skills"],
                "preferred": analysis_dict["preferred_skills"],
                "experience": analysis_dict["experience_requirements"]
            },
            recommendations=analysis_dict["recommendations"]
        )
        db.add(db_job)
        await db.commit()
        await db.refresh(db_job)

        return JobAnalysisResponse(
            id=db_job.id,
            job_title=db_job.job_title,
            company=db_job.company,
            match_score=analysis_dict["match_score"],
            strong_matches=analysis_dict["strong_matches"],
            skill_gaps=analysis_dict["skill_gaps"],
            required_skills=analysis_dict["required_skills"],
            preferred_skills=analysis_dict["preferred_skills"],
            experience_requirements=analysis_dict["experience_requirements"],
            recommendations=analysis_dict["recommendations"],
            action_plan=analysis_dict.get("action_plan", [])
        )
