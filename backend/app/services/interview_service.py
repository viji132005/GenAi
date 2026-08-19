import logging
import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel

from app.models.entities import StudentProfile, MockInterview, InterviewQuestion, InterviewResponse, InterviewReport
from app.schemas.all_schemas import (
    InterviewQuestionResponse, InterviewAnswerResponse, InterviewReportResponse, MockInterviewSessionResponse
)
from app.ai.factory import get_llm_provider
from app.ai.prompts import INTERVIEW_SYSTEM_PROMPT, INTERVIEW_REPORT_SYSTEM_PROMPT

logger = logging.getLogger("skillbridge.services.interview")

class LLGeneratedQuestion(BaseModel):
    question_number: int
    question_text: str
    question_type: str
    expected_topics: List[str]

class LLGeneratedQuestionsList(BaseModel):
    questions: List[LLGeneratedQuestion]

class LLEvalAnswerOutput(BaseModel):
    technical_accuracy: float
    completeness: float
    clarity: float
    feedback: str
    follow_up: str
    score: float

class LLInterviewReportOutput(BaseModel):
    overall_score: float
    technical_score: float
    communication_score: float
    rubric_breakdown: Dict[str, Any]
    strengths: List[str]
    weaknesses: List[str]
    improvement_suggestions: List[str]
    recommended_topics: List[str]

class MockInterviewService:
    """
    AI Mock Interview Simulation & Evaluation Engine.
    """

    @classmethod
    async def start_interview(
        cls, 
        user_id: int, 
        profile: StudentProfile, 
        career_title: Optional[str], 
        interview_type: str, 
        difficulty: str, 
        total_questions: int, 
        db: AsyncSession
    ) -> MockInterviewSessionResponse:
        career = career_title or profile.target_career or "AI/ML Engineer"
        num_q = max(min(total_questions, 8), 3)

        # Create Interview Session
        db_interview = MockInterview(
            user_id=user_id,
            career_title=career,
            interview_type=interview_type,
            difficulty=difficulty,
            total_questions=num_q,
            status="in_progress",
            current_question_index=0
        )
        db.add(db_interview)
        await db.flush()

        student_skills = [s.name for s in profile.skills]

        user_prompt = f"""
Generate {num_q} interview questions for a college student applying for a {career} role.
Difficulty: {difficulty}
Interview Type: {interview_type}
Student Skills: {', '.join(student_skills[:6])}

Generate a progressive sequence:
1. One foundational conceptual question.
2. Two deep technical/system problem-solving questions.
3. One behavioral or engineering trade-off question.

For each question, specify:
- question_number (1 to {num_q})
- question_text (clear, challenging, realistic)
- question_type (Technical, System Design, or Behavioral)
- expected_topics (list of key concepts an ideal candidate should mention)
"""

        provider = get_llm_provider()
        questions_data = []

        if provider.is_configured():
            try:
                llm_output = await provider.generate_structured(
                    prompt=user_prompt,
                    schema_cls=LLGeneratedQuestionsList,
                    system_prompt=INTERVIEW_SYSTEM_PROMPT,
                    temperature=0.3
                )
                questions_data = [q.model_dump() for q in llm_output.questions]
            except Exception as e:
                logger.error(f"Error generating interview questions: {e}. Using deterministic question bank.")

        # Fallback question bank
        if not questions_data or len(questions_data) < num_q:
            career_lower = career.lower()
            if "ai" in career_lower or "machine" in career_lower or "data" in career_lower:
                sample_bank = [
                    {
                        "question_number": 1,
                        "question_text": "Can you explain the bias-variance tradeoff in machine learning, and how techniques like L1/L2 regularization and ensemble models affect it?",
                        "question_type": "Technical",
                        "expected_topics": ["Overfitting vs Underfitting", "Model Complexity", "L1 Lasso Sparsity", "L2 Ridge Penalty", "Ensemble Averaging"]
                    },
                    {
                        "question_number": 2,
                        "question_text": "How do self-attention mechanisms in Transformers differ computationally from traditional RNNs and CNNs, and why do they handle long-range dependencies better?",
                        "question_type": "Technical",
                        "expected_topics": ["Query/Key/Value Matmul", "O(N^2) complexity", "Parallel training vs sequential bottlenecks", "Vanishing gradients"]
                    },
                    {
                        "question_number": 3,
                        "question_text": "Describe a scenario where you trained a model with 98% accuracy on training data, but it failed severely in production. How would you diagnose and resolve the issue?",
                        "question_type": "System Design & MLOps",
                        "expected_topics": ["Data Drift / Concept Drift", "Class Imbalance / F1 Score", "Data Leakage", "Validation Split Strategy"]
                    },
                    {
                        "question_number": 4,
                        "question_text": "Tell me about a challenging technical bug or blocker you encountered in a recent project. How did you methodically isolate the root cause?",
                        "question_type": "Behavioral",
                        "expected_topics": ["STAR Method", "Root Cause Analysis", "Debugging Tools / Profiling", "Learning Outcome"]
                    }
                ]
            else:
                sample_bank = [
                    {
                        "question_number": 1,
                        "question_text": "Explain how modern web browsers render an HTML/CSS document from DOM tree parsing to final paint, and how you optimize the Critical Rendering Path.",
                        "question_type": "Technical",
                        "expected_topics": ["DOM and CSSOM Construction", "Render Tree", "Layout / Reflow", "Repaint", "Async/Defer Scripts"]
                    },
                    {
                        "question_number": 2,
                        "question_text": "What are the trade-offs between database indexing using B-Trees vs Hash indexes, and how do composite indexes function with multi-column queries?",
                        "question_type": "Technical",
                        "expected_topics": ["B-Tree range queries", "O(1) vs O(log N)", "Leftmost prefix rule", "Write amplification on INSERTs"]
                    },
                    {
                        "question_number": 3,
                        "question_text": "How would you architect a secure JWT authentication flow with short-lived access tokens and refresh token rotation in a distributed microservice environment?",
                        "question_type": "System Design",
                        "expected_topics": ["HttpOnly secure cookies", "Refresh Token Rotation", "Token revocation / Redis blacklist", "XSS/CSRF mitigations"]
                    },
                    {
                        "question_number": 4,
                        "question_text": "Describe a technical disagreement you had with a teammate or peer during a project. How did you navigate it to reach a high-quality decision?",
                        "question_type": "Behavioral",
                        "expected_topics": ["STAR Method", "Objective Benchmarking", "Collaboration", "Constructive Resolution"]
                    }
                ]
            questions_data = sample_bank[:num_q]

        for q in questions_data:
            db_q = InterviewQuestion(
                interview_id=db_interview.id,
                question_number=q["question_number"],
                question_text=q["question_text"],
                question_type=q.get("question_type", "Technical"),
                expected_topics=q.get("expected_topics", [])
            )
            db.add(db_q)

        await db.commit()

        # Reload with questions and report
        q_load = select(MockInterview).where(MockInterview.id == db_interview.id).options(
            selectinload(MockInterview.questions),
            selectinload(MockInterview.report)
        )
        res = await db.execute(q_load)
        interview_obj = res.scalar_one()

        return MockInterviewSessionResponse.model_validate(interview_obj)

    @classmethod
    async def evaluate_answer(
        cls, 
        interview_id: int, 
        question_id: int, 
        user_answer: str, 
        user_id: int, 
        db: AsyncSession
    ) -> InterviewAnswerResponse:
        # Fetch question and session
        query = select(InterviewQuestion).where(
            InterviewQuestion.id == question_id,
            InterviewQuestion.interview_id == interview_id
        ).options(selectinload(InterviewQuestion.interview).selectinload(MockInterview.questions))
        result = await db.execute(query)
        question = result.scalar_one_or_none()

        if not question or question.interview.user_id != user_id:
            raise ValueError("Interview question not found or unauthorized")

        interview = question.interview
        
        user_prompt = f"""
Career Role: {interview.career_title}
Interview Question: "{question.question_text}"
Expected Technical Topics: {question.expected_topics}

Candidate's Answer:
\"\"\"
{user_answer}
\"\"\"

Evaluate the candidate's response rigorously:
1. technical_accuracy (0 to 100): Correctness of engineering facts, algorithms, or concepts.
2. completeness (0 to 100): Did they cover trade-offs, edge cases, and core mechanisms?
3. clarity (0 to 100): Communication structure, technical terminology, and conciseness.
4. feedback: 2-3 sentences of constructive feedback noting what was good and what was omitted.
5. follow_up: A 1-sentence pointed follow-up question digging into a deeper aspect or edge case.
6. score: Weighted composite score (0.5 * technical_accuracy + 0.3 * completeness + 0.2 * clarity).
"""

        provider = get_llm_provider()
        eval_data = None

        if provider.is_configured() and len(user_answer.strip()) > 10:
            try:
                llm_output = await provider.generate_structured(
                    prompt=user_prompt,
                    schema_cls=LLEvalAnswerOutput,
                    system_prompt=INTERVIEW_SYSTEM_PROMPT,
                    temperature=0.2
                )
                eval_data = llm_output.model_dump()
            except Exception as e:
                logger.error(f"Error evaluating interview answer via LLM: {e}. Using deterministic rubric.")

        # Fallback rubric
        if not eval_data:
            ans_len = len(user_answer.split())
            accuracy = 75.0 if ans_len > 25 else 50.0
            completeness = 70.0 if ans_len > 40 else 55.0
            clarity = 78.0
            score = round((accuracy * 0.5) + (completeness * 0.3) + (clarity * 0.2), 1)

            eval_data = {
                "technical_accuracy": accuracy,
                "completeness": completeness,
                "clarity": clarity,
                "feedback": "Good explanation of the primary concepts. To reach top-percentile scoring, elaborate further on production edge cases, memory trade-offs, and computational complexities.",
                "follow_up": "How would your approach change if your data volume increased by 100x?",
                "score": score
            }

        # Save Response
        db_resp = InterviewResponse(
            question_id=question.id,
            user_answer=user_answer,
            technical_accuracy=eval_data["technical_accuracy"],
            completeness=eval_data["completeness"],
            clarity=eval_data["clarity"],
            feedback=eval_data["feedback"],
            follow_up=eval_data.get("follow_up", ""),
            score=eval_data["score"]
        )
        db.add(db_resp)

        # Increment current question index
        interview.current_question_index = question.question_number

        # Check if next question exists
        all_q = sorted(interview.questions, key=lambda x: x.question_number)
        next_q = next((q for q in all_q if q.question_number > question.question_number), None)

        is_finished = next_q is None

        if is_finished:
            interview.status = "completed"
            interview.completed_at = datetime.datetime.utcnow()

        await db.commit()

        next_q_resp = InterviewQuestionResponse.model_validate(next_q) if next_q else None

        return InterviewAnswerResponse(
            question_id=question.id,
            technical_accuracy=eval_data["technical_accuracy"],
            completeness=eval_data["completeness"],
            clarity=eval_data["clarity"],
            feedback=eval_data["feedback"],
            follow_up=eval_data.get("follow_up", ""),
            score=eval_data["score"],
            next_question=next_q_resp,
            is_finished=is_finished
        )

    @classmethod
    async def generate_final_report(
        cls, 
        interview_id: int, 
        user_id: int, 
        db: AsyncSession
    ) -> InterviewReportResponse:
        """Generate final scorecard and rubric report for completed interview."""
        query = select(MockInterview).where(
            MockInterview.id == interview_id,
            MockInterview.user_id == user_id
        ).options(
            selectinload(MockInterview.questions).selectinload(InterviewQuestion.responses),
            selectinload(MockInterview.report)
        )
        result = await db.execute(query)
        interview = result.scalar_one_or_none()

        if not interview:
            raise ValueError("Interview session not found")

        if interview.report:
            return InterviewReportResponse.model_validate(interview.report)

        # Collect transcript
        transcript = []
        scores = []
        tech_scores = []
        comm_scores = []

        for q in interview.questions:
            resp = q.responses[0] if q.responses else None
            ans_text = resp.user_answer if resp else "(No answer provided)"
            score_val = resp.score if resp else 40.0
            scores.append(score_val)
            tech_scores.append(resp.technical_accuracy if resp else 40.0)
            comm_scores.append(resp.clarity if resp else 50.0)
            
            transcript.append({
                "question": q.question_text,
                "answer": ans_text,
                "feedback": resp.feedback if resp else ""
            })

        avg_overall = round(sum(scores) / (len(scores) or 1), 1)
        avg_tech = round(sum(tech_scores) / (len(tech_scores) or 1), 1)
        avg_comm = round(sum(comm_scores) / (len(comm_scores) or 1), 1)

        user_prompt = f"""
Career Role: {interview.career_title}
Interview Difficulty: {interview.difficulty}
Transcript & Answers:
{transcript}

Generate a comprehensive Interview Performance Report:
- overall_score (0 to 100, approx {avg_overall})
- technical_score (0 to 100, approx {avg_tech})
- communication_score (0 to 100, approx {avg_comm})
- rubric_breakdown: detailed dict with scores and observations for 'Problem Solving', 'Code & Architecture Mastery', 'Clarity & Delivery', 'Handling Ambiguity'.
- strengths: 3 specific technical strengths demonstrated in their answers.
- weaknesses: 2-3 specific knowledge gaps or areas where answers lacked depth.
- improvement_suggestions: 3 actionable steps to prepare before their real interview.
- recommended_topics: 3 specific technical topics to revise.
"""

        provider = get_llm_provider()
        report_data = None

        if provider.is_configured() and transcript:
            try:
                llm_output = await provider.generate_structured(
                    prompt=user_prompt,
                    schema_cls=LLInterviewReportOutput,
                    system_prompt=INTERVIEW_REPORT_SYSTEM_PROMPT,
                    temperature=0.2
                )
                report_data = llm_output.model_dump()
            except Exception as e:
                logger.error(f"Error generating final interview report via LLM: {e}. Using deterministic scorecard.")

        if not report_data:
            report_data = {
                "overall_score": avg_overall or 74.0,
                "technical_score": avg_tech or 72.0,
                "communication_score": avg_comm or 78.0,
                "rubric_breakdown": {
                    "Problem Solving": {"score": avg_tech or 72.0, "comment": "Good conceptual grasp with clear analytical reasoning."},
                    "Technical Depth": {"score": avg_tech or 70.0, "comment": "Understands primary mechanics, needs deeper focus on scale & failure modes."},
                    "Clarity & Delivery": {"score": avg_comm or 80.0, "comment": "Structured answers with effective technical terminology."}
                },
                "strengths": [
                    "Strong foundational understanding of core algorithms and paradigms",
                    "Clear, structured answers utilizing technical vocabulary",
                    "Confident explanation of project experiences and trade-offs"
                ],
                "weaknesses": [
                    "Could elaborate further on edge cases, memory complexity, and distributed bottlenecks",
                    "Mentioning specific real-world latency or profiling benchmarks would strengthen answers"
                ],
                "improvement_suggestions": [
                    "Practice dry-running algorithms with extreme edge cases before stating conclusions",
                    "Incorporate the STAR framework when responding to system failure and debugging scenarios",
                    "Review top system design patterns and caching strategies"
                ],
                "recommended_topics": [
                    "System Concurrency & Caching",
                    "Model Evaluation & Drift Diagnostics",
                    "Database Query Optimization"
                ]
            }

        # Update interview
        interview.overall_score = report_data["overall_score"]
        interview.technical_score = report_data["technical_score"]
        interview.communication_score = report_data["communication_score"]
        interview.status = "completed"
        interview.completed_at = datetime.datetime.utcnow()

        db_report = InterviewReport(
            interview_id=interview.id,
            user_id=user_id,
            overall_score=report_data["overall_score"],
            technical_score=report_data["technical_score"],
            communication_score=report_data["communication_score"],
            rubric_breakdown=report_data["rubric_breakdown"],
            strengths=report_data["strengths"],
            weaknesses=report_data["weaknesses"],
            improvement_suggestions=report_data["improvement_suggestions"],
            recommended_topics=report_data.get("recommended_topics", [])
        )
        db.add(db_report)
        await db.commit()
        await db.refresh(db_report)

        return InterviewReportResponse.model_validate(db_report)
