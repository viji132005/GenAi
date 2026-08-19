# SkillBridge AI — System Architecture

SkillBridge AI is a full-stack, AI-powered student career navigation and readiness platform. It connects a student's academic profile and verified technical skills to target industry career requirements through automated diagnostics, individualized milestone roadmaps, ATS resume optimization, mock interview simulations, and context-aware AI mentorship.

---

## High-Level Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                                 CLIENT TIER                                       |
|                                                                                   |
|  React 19 SPA + Vite + TailwindCSS + Lucide Icons + Recharts                      |
|  ├── Dynamic Dark Glassmorphic UI & KPI Telemetry Dashboard                       |
|  ├── Multi-Step Student Onboarding Wizard                                         |
|  ├── Career Match & Multi-Disciplinary Radar Explorer                             |
|  ├── Interactive Skill Gap Diagnostic Matrix                                      |
|  ├── Phased Milestone Roadmap with Progress Tracking                              |
|  ├── AI Resume & ATS Quantified Bullet Optimizer (Google XYZ)                    |
|  ├── Job Description Parser & Compatibility Evaluator                             |
|  ├── AI Capstone Project Recommendations (4-Stage Blueprints)                     |
|  ├── Multi-Turn Technical Mock Interview Simulator & Scorecard                    |
|  └── Context-Aware RAG Career Assistant                                           |
+-----------------------------------------+-----------------------------------------+
                                          |
                                          | JSON REST API over HTTP/HTTPS
                                          | (Bearer JWT Token Injection)
                                          v
+-----------------------------------------------------------------------------------+
|                                BACKEND TIER                                       |
|                                                                                   |
|  FastAPI (Python 3.14) + Uvicorn Async Web Server                                 |
|  ├── Middleware: CORS, Request Timing, Pure Bcrypt + JWT Auth Middleware          |
|  ├── API Routers: /auth, /profile, /career, /skills, /roadmap, /resume,           |
|  │                /job, /projects, /interview, /chat, /analytics, /health         |
|  └── Domain Services:                                                             |
|      ├── CareerService: Match scoring, taxonomy exploration                       |
|      ├── SkillGapService: Acquired, partial, and missing skills matrix            |
|      ├── RoadmapService: Milestone sequencing, duration estimation, task sync     |
|      ├── ResumeService: PyPDF text extraction, ATS scoring, XYZ bullet rewrites   |
|      ├── JobService: JD requirement parsing, match score, 3-step action plan       |
|      ├── ProjectService: Domain capstones, 4-stage milestones, portfolio value    |
|      ├── InterviewService: Question generation, multi-turn evaluation, report     |
|      ├── ChatService: Student context injection, RAG grounding, prompt chips      |
|      └── AnalyticsService: Readiness trajectory telemetry, radar metrics          |
+-----------------------------------+-----------------------------------------------+
                                    |
                  +-----------------+-----------------+
                  |                                   |
                  v                                   v
+-----------------------------------+   +-------------------------------------------+
|          PERSISTENCE TIER         |   |                 AI TIER                   |
|                                   |   |                                           |
|  SQLAlchemy 2.0 Async Engine      |   |  Modular LLM Provider Layer               |
|  aiosqlite / SQLite Database      |   |  ├── BaseLLMProvider Interface            |
|  ├── Users & StudentProfiles      |   |  ├── GeminiProvider (google-genai)        |
|  ├── Skills & CareerProfiles      |   |  ├── OpenAIProvider / SkillBridge-LLM     |
|  ├── CareerSkills & Resumes       |   |  ├── LLMProviderFactory (Singleton)       |
|  ├── ResumeAnalyses & Roadmaps    |   |  └── RAG Knowledge Engine                 |
|  ├── RoadmapTasks & JobAnalyses   |   |      ├── 10+ Career Knowledge Docs        |
|  ├── ProjectRecommendations       |   |      ├── TF-IDF / Cosine Vector Index     |
|  ├── MockInterviews & Questions   |   |      └── Top-K Semantic Citation Retriever|
|  └── ProgressMetrics & ChatHistory|   +-------------------------------------------+
+-----------------------------------+
```

---

## Architectural Principles

1. **Model-Agnostic LLM Provider Layer**:
   All AI functionality interacts strictly through `BaseLLMProvider`. Google Gemini (`gemini-2.5-flash` / `gemini-1.5-flash`) acts as the primary cloud provider, while an OpenAI-compatible interface or a proprietary `SkillBridge-LLM` can be substituted with zero changes to services or controllers.

2. **Grounded Offline Deterministic Fallback**:
   If an external LLM API key is missing or offline, domain services seamlessly engage an internal deterministic grounding engine. The application remains 100% operational with structured recommendations.

3. **Domain-Driven Service Layer**:
   FastAPI controllers only handle request validation and HTTP status codes. All business logic, scoring formulas, RAG vector searches, and LLM prompt assembly are encapsulated in isolated service modules.

4. **Pure Async I/O**:
   Database access uses SQLAlchemy async sessions with SQLite via `aiosqlite`, and HTTP calls use `httpx.AsyncClient` to prevent thread blocking.
