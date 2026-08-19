import datetime
from typing import List, Optional
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
)
from sqlalchemy.orm import relationship
from app.database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="student")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    profile = relationship("StudentProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    resume_analyses = relationship("ResumeAnalysis", back_populates="user", cascade="all, delete-orphan")
    roadmaps = relationship("Roadmap", back_populates="user", cascade="all, delete-orphan")
    job_analyses = relationship("JobAnalysis", back_populates="user", cascade="all, delete-orphan")
    project_recommendations = relationship("ProjectRecommendation", back_populates="user", cascade="all, delete-orphan")
    mock_interviews = relationship("MockInterview", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("AIConversation", back_populates="user", cascade="all, delete-orphan")
    progress_metrics = relationship("ProgressMetric", back_populates="user", cascade="all, delete-orphan")


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    college = Column(String(255), default="")
    degree = Column(String(100), default="")
    branch = Column(String(100), default="")
    semester = Column(Integer, default=1)
    graduation_year = Column(Integer, default=2026)
    cgpa = Column(Float, default=0.0)
    target_career = Column(String(150), default="")
    interests = Column(JSON, default=list)  # List[str]
    coursework = Column(JSON, default=list)  # List[str]
    certifications = Column(JSON, default=list)  # List[dict]
    experience = Column(JSON, default=list)  # List[dict]
    achievements = Column(JSON, default=list)  # List[str]
    onboarding_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="profile")
    skills = relationship("Skill", back_populates="profile", cascade="all, delete-orphan")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False, index=True)
    category = Column(String(100), default="Technical")  # Language, Framework, Database, Cloud, AI/ML, etc.
    proficiency_level = Column(String(50), default="Beginner")  # Beginner, Intermediate, Advanced
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    profile = relationship("StudentProfile", back_populates="skills")


class CareerProfile(Base):
    __tablename__ = "career_profiles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), unique=True, index=True, nullable=False)
    category = Column(String(100), default="Engineering")
    description = Column(Text, default="")
    average_salary = Column(String(100), default="")
    growth_outlook = Column(String(100), default="Very High")
    responsibilities = Column(JSON, default=list)
    typical_technologies = Column(JSON, default=list)

    skills = relationship("CareerSkill", back_populates="career", cascade="all, delete-orphan")


class CareerSkill(Base):
    __tablename__ = "career_skills"

    id = Column(Integer, primary_key=True, index=True)
    career_id = Column(Integer, ForeignKey("career_profiles.id", ondelete="CASCADE"), nullable=False)
    skill_name = Column(String(100), nullable=False, index=True)
    category = Column(String(100), default="Technical")
    importance_level = Column(String(50), default="High")  # High, Medium, Low
    min_proficiency = Column(String(50), default="Intermediate")
    learning_resources = Column(JSON, default=list)

    career = relationship("CareerProfile", back_populates="skills")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    raw_text = Column(Text, default="")
    parsed_json = Column(JSON, default=dict)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="resumes")
    analysis = relationship("ResumeAnalysis", back_populates="resume", uselist=False, cascade="all, delete-orphan")


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    overall_score = Column(Float, default=0.0)
    ats_score = Column(Float, default=0.0)
    skills_score = Column(Float, default=0.0)
    experience_score = Column(Float, default=0.0)
    project_score = Column(Float, default=0.0)
    formatting_score = Column(Float, default=0.0)
    strengths = Column(JSON, default=list)
    weaknesses = Column(JSON, default=list)
    suggestions = Column(JSON, default=list)
    improved_bullets = Column(JSON, default=list)  # List[dict(original, improved, rationale)]
    missing_elements = Column(JSON, default=list)
    analyzed_at = Column(DateTime, default=datetime.datetime.utcnow)

    resume = relationship("Resume", back_populates="analysis")
    user = relationship("User", back_populates="resume_analyses")


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    career_title = Column(String(150), nullable=False)
    title = Column(String(255), default="Personalized Career Roadmap")
    target_duration_months = Column(Integer, default=6)
    completion_percentage = Column(Float, default=0.0)
    overview_summary = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="roadmaps")
    tasks = relationship("RoadmapTask", back_populates="roadmap", cascade="all, delete-orphan", order_by="RoadmapTask.sort_order")


class RoadmapTask(Base):
    __tablename__ = "roadmap_tasks"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id", ondelete="CASCADE"), nullable=False)
    phase_number = Column(Integer, default=1)
    phase_name = Column(String(150), default="")
    task_title = Column(String(255), nullable=False)
    description = Column(Text, default="")
    skills_covered = Column(JSON, default=list)
    learning_resources = Column(JSON, default=list)
    project_checkpoint = Column(Text, default="")
    estimated_hours = Column(Integer, default=10)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    sort_order = Column(Integer, default=1)

    roadmap = relationship("Roadmap", back_populates="tasks")


class JobAnalysis(Base):
    __tablename__ = "job_analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_title = Column(String(200), default="Target Role")
    company = Column(String(200), default="")
    raw_job_description = Column(Text, nullable=False)
    match_score = Column(Float, default=0.0)
    matching_skills = Column(JSON, default=list)
    missing_skills = Column(JSON, default=list)
    requirements_extracted = Column(JSON, default=dict)
    recommendations = Column(JSON, default=list)
    analyzed_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="job_analyses")


class ProjectRecommendation(Base):
    __tablename__ = "project_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    career_goal = Column(String(150), default="")
    title = Column(String(255), nullable=False)
    difficulty = Column(String(50), default="Intermediate")  # Beginner, Intermediate, Advanced
    domain = Column(String(100), default="AI/ML")
    problem_statement = Column(Text, default="")
    why_suitable = Column(Text, default="")
    skills_learned = Column(JSON, default=list)
    tech_stack = Column(JSON, default=list)
    development_phases = Column(JSON, default=list)
    portfolio_value = Column(Text, default="")
    is_bookmarked = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="project_recommendations")


class MockInterview(Base):
    __tablename__ = "mock_interviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    career_title = Column(String(150), nullable=False)
    interview_type = Column(String(50), default="Technical")  # Technical, Behavioral, System Design, Mixed
    difficulty = Column(String(50), default="Intermediate")
    total_questions = Column(Integer, default=5)
    status = Column(String(50), default="in_progress")  # in_progress, completed, abandoned
    current_question_index = Column(Integer, default=0)
    overall_score = Column(Float, default=0.0)
    technical_score = Column(Float, default=0.0)
    communication_score = Column(Float, default=0.0)
    feedback_summary = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="mock_interviews")
    questions = relationship("InterviewQuestion", back_populates="interview", cascade="all, delete-orphan", order_by="InterviewQuestion.question_number")
    report = relationship("InterviewReport", back_populates="interview", uselist=False, cascade="all, delete-orphan")


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("mock_interviews.id", ondelete="CASCADE"), nullable=False)
    question_number = Column(Integer, default=1)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), default="Technical")
    expected_topics = Column(JSON, default=list)

    interview = relationship("MockInterview", back_populates="questions")
    responses = relationship("InterviewResponse", back_populates="question", cascade="all, delete-orphan")


class InterviewResponse(Base):
    __tablename__ = "interview_responses"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("interview_questions.id", ondelete="CASCADE"), nullable=False)
    user_answer = Column(Text, default="")
    technical_accuracy = Column(Float, default=0.0)
    completeness = Column(Float, default=0.0)
    clarity = Column(Float, default=0.0)
    feedback = Column(Text, default="")
    follow_up = Column(Text, default="")
    score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    question = relationship("InterviewQuestion", back_populates="responses")


class InterviewReport(Base):
    __tablename__ = "interview_reports"

    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("mock_interviews.id", ondelete="CASCADE"), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    overall_score = Column(Float, default=0.0)
    technical_score = Column(Float, default=0.0)
    communication_score = Column(Float, default=0.0)
    rubric_breakdown = Column(JSON, default=dict)
    strengths = Column(JSON, default=list)
    weaknesses = Column(JSON, default=list)
    improvement_suggestions = Column(JSON, default=list)
    recommended_topics = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    interview = relationship("MockInterview", back_populates="report")


class AIConversation(Base):
    __tablename__ = "ai_conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), default="Career Advisory Session")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="conversations")
    messages = relationship("ChatMessage", back_populates="conversation", cascade="all, delete-orphan", order_by="ChatMessage.created_at")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("ai_conversations.id", ondelete="CASCADE"), nullable=False)
    sender = Column(String(50), default="user")  # user, assistant, system
    content = Column(Text, nullable=False)
    sources = Column(JSON, default=list)  # Citations from RAG
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    conversation = relationship("AIConversation", back_populates="messages")


class ProgressMetric(Base):
    __tablename__ = "progress_metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    recorded_date = Column(String(50), nullable=False)  # "2026-05", "2026-06", etc.
    career_readiness = Column(Float, default=0.0)
    skill_completion = Column(Float, default=0.0)
    resume_score = Column(Float, default=0.0)
    interview_readiness = Column(Float, default=0.0)
    roadmap_progress = Column(Float, default=0.0)
    active_career_match = Column(Float, default=0.0)

    user = relationship("User", back_populates="progress_metrics")


class KnowledgeDoc(Base):
    __tablename__ = "knowledge_docs"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), default="career_guide")  # career_guide, tech_concept, interview_prep, project_guide
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    metadata_json = Column(JSON, default=dict)
    embedding_json = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
