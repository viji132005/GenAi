from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field
import datetime

# --- User & Auth ---
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime.datetime
    onboarding_completed: Optional[bool] = False

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


# --- Skills & Profile ---
class SkillCreate(BaseModel):
    name: str
    category: str = "Technical"
    proficiency_level: str = "Beginner"  # Beginner, Intermediate, Advanced

class SkillResponse(BaseModel):
    id: int
    name: str
    category: str
    proficiency_level: str
    verified: bool

    class Config:
        from_attributes = True

class ProfileUpdate(BaseModel):
    college: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    semester: Optional[int] = None
    graduation_year: Optional[int] = None
    cgpa: Optional[float] = None
    target_career: Optional[str] = None
    interests: Optional[List[str]] = None
    coursework: Optional[List[str]] = None
    certifications: Optional[List[Dict[str, Any]]] = None
    experience: Optional[List[Dict[str, Any]]] = None
    achievements: Optional[List[str]] = None
    skills: Optional[List[SkillCreate]] = None

class StudentProfileResponse(BaseModel):
    id: int
    user_id: int
    college: str
    degree: str
    branch: str
    semester: int
    graduation_year: int
    cgpa: float
    target_career: str
    interests: List[str]
    coursework: List[str]
    certifications: List[Dict[str, Any]]
    experience: List[Dict[str, Any]]
    achievements: List[str]
    onboarding_completed: bool
    skills: List[SkillResponse]

    class Config:
        from_attributes = True


# --- Career & Recommendations ---
class CareerRecommendationItem(BaseModel):
    career_title: str
    category: str
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

class CareerAnalysisResponse(BaseModel):
    target_career: str
    top_recommendations: List[CareerRecommendationItem]
    overall_profile_summary: str
    readiness_score: float
    next_immediate_action: str


# --- Skill Gap ---
class SkillGapItem(BaseModel):
    skill_name: str
    category: str
    importance_level: str  # High, Medium, Low
    current_status: str    # acquired, partial, missing
    current_proficiency: Optional[str] = None
    required_proficiency: str
    recommended_resources: List[Dict[str, str]]
    learning_priority_order: int
    estimated_weeks: int

class SkillGapAnalysisResponse(BaseModel):
    career_title: str
    overall_match_score: float
    acquired_skills: List[SkillGapItem]
    partial_skills: List[SkillGapItem]
    missing_skills: List[SkillGapItem]
    high_priority_gaps: List[str]
    recommended_action_plan: str


# --- Roadmap ---
class RoadmapTaskUpdate(BaseModel):
    is_completed: bool

class RoadmapTaskResponse(BaseModel):
    id: int
    phase_number: int
    phase_name: str
    task_title: str
    description: str
    skills_covered: List[str]
    learning_resources: List[Dict[str, str]]
    project_checkpoint: str
    estimated_hours: int
    is_completed: bool
    completed_at: Optional[datetime.datetime]
    sort_order: int

    class Config:
        from_attributes = True

class RoadmapResponse(BaseModel):
    id: int
    career_title: str
    title: str
    target_duration_months: int
    completion_percentage: float
    overview_summary: str
    tasks: List[RoadmapTaskResponse]

    class Config:
        from_attributes = True


# --- Resume ---
class ImprovedBullet(BaseModel):
    original: str
    improved: str
    rationale: str

class ResumeAnalysisResponse(BaseModel):
    id: int
    resume_id: int
    overall_score: float
    ats_score: float
    skills_score: float
    experience_score: float
    project_score: float
    formatting_score: float
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    improved_bullets: List[ImprovedBullet]
    missing_elements: List[str]
    analyzed_at: datetime.datetime

    class Config:
        from_attributes = True


# --- Job Analysis ---
class JobAnalysisRequest(BaseModel):
    job_title: Optional[str] = "Target Role"
    company: Optional[str] = ""
    job_description: str

class JobAnalysisResponse(BaseModel):
    id: int
    job_title: str
    company: str
    match_score: float
    strong_matches: List[str]
    skill_gaps: List[str]
    required_skills: List[str]
    preferred_skills: List[str]
    experience_requirements: str
    recommendations: List[str]
    action_plan: List[str]

    class Config:
        from_attributes = True


# --- Projects ---
class ProjectRecommendationResponse(BaseModel):
    id: int
    career_goal: str
    title: str
    difficulty: str
    domain: str
    problem_statement: str
    why_suitable: str
    skills_learned: List[str]
    tech_stack: List[str]
    development_phases: List[Dict[str, Any]]
    portfolio_value: str
    is_bookmarked: bool
    is_completed: bool

    class Config:
        from_attributes = True


# --- Mock Interview ---
class InterviewStartRequest(BaseModel):
    career_title: Optional[str] = None
    interview_type: str = "Technical"  # Technical, Behavioral, Mixed
    difficulty: str = "Intermediate"
    total_questions: int = 5

class InterviewAnswerRequest(BaseModel):
    interview_id: int
    question_id: int
    user_answer: str

class InterviewQuestionResponse(BaseModel):
    id: int
    question_number: int
    question_text: str
    question_type: str
    expected_topics: List[str]

    class Config:
        from_attributes = True

class InterviewAnswerResponse(BaseModel):
    question_id: int
    technical_accuracy: float
    completeness: float
    clarity: float
    feedback: str
    follow_up: Optional[str] = None
    score: float
    next_question: Optional[InterviewQuestionResponse] = None
    is_finished: bool = False

class InterviewReportResponse(BaseModel):
    id: int
    interview_id: int
    overall_score: float
    technical_score: float
    communication_score: float
    rubric_breakdown: Dict[str, Any]
    strengths: List[str]
    weaknesses: List[str]
    improvement_suggestions: List[str]
    recommended_topics: List[str]

    class Config:
        from_attributes = True

class MockInterviewSessionResponse(BaseModel):
    id: int
    career_title: str
    interview_type: str
    difficulty: str
    total_questions: int
    status: str
    current_question_index: int
    questions: List[InterviewQuestionResponse]
    report: Optional[InterviewReportResponse] = None

    class Config:
        from_attributes = True


# --- Chat & Assistant ---
class ChatMessageRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ChatSource(BaseModel):
    title: str
    category: str
    snippet: str

class ChatMessageResponse(BaseModel):
    id: int
    conversation_id: Optional[int] = None
    sender: str
    content: str
    sources: List[Dict[str, Any]] = []
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: int
    title: str
    messages: List[ChatMessageResponse] = []
    created_at: datetime.datetime

    class Config:
        from_attributes = True


# --- Analytics & Dashboard ---
class DashboardOverviewResponse(BaseModel):
    user_name: str
    target_career: str
    career_match_percentage: float
    career_readiness_score: float
    resume_score: float
    skill_completion_percentage: float
    interview_readiness_score: float
    roadmap_progress_percentage: float
    top_missing_skills: List[str]
    recommended_next_action: str
    recent_insights: List[Dict[str, Any]]
    radar_metrics: Dict[str, float]
    timeline_metrics: List[Dict[str, Any]]
