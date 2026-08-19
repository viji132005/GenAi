# SkillBridge AI

<div align="center">

### *"Bridge the gap between your skills and your career."*

[![Python](https://img.shields.io/badge/Python-3.14%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.0-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-5.4-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-2.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Async_SQLAlchemy-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlalchemy.org/)

</div>

---

## Overview

**SkillBridge AI** is a production-grade, AI-powered career navigation and readiness platform built for college students. It connects university coursework and validated technical skills to industry engineering requirements through diagnostics, milestone curricula, ATS resume optimization, mock interview simulations, and context-aware AI mentorship.

---

## 5-Step Complete Product Loop

```
1. STUDENT PROFILE  ──►  2. AI DIAGNOSTIC  ──►  3. PERSONALIZED ROADMAP  ──►  4. APPLIED PRACTICE  ──►  5. PLACEMENT READY
(Academics & Skills)    (Gaps & Match Scores)   (Phased Milestones)         (Projects & Interviews)    (ATS Resume & Job Fit)
```

---

## Key Features & Platform Modules

### 1. Student Onboarding Wizard & Academic Profile
- 4-step wizard capturing university, degree, branch, semester, graduation year, CGPA, and technical skills with proficiency ratings.
- Real-time profile state persistence with automated career readiness indexing.

### 2. Student Dashboard & KPI Telemetry
- 6 Circular Progress Rings tracking **Career Readiness**, **Target Career Fit**, **Roadmap Progress**, **Skills Acquired**, **Resume ATS Score**, and **Mock Interview Score**.
- Dynamic **Recommended Next Action** hero card guiding the student's next step.
- Multi-Disciplinary **Competency Radar Chart** and **Readiness Growth Line Chart**.

### 3. Career Path Analysis & Fit Engine
- Multi-career scoring (AI/ML Engineer, Data Scientist, Full Stack Developer, Cloud DevOps, Cybersecurity, etc.).
- Deep-dive drawer comparing matched skills, priority gaps, market demand, and compensation benchmarks.
- 1-click **"Set as Target Goal"** syncing with the entire learning engine.

### 4. Interactive Skill Gap Matrix
- Visual 3-column diagnostic: **Acquired Skills (100% fit)**, **Partially Developed (Upgrade needed)**, and **Missing Critical Gaps**.
- High/Medium/Low priority badges, estimated learning durations, and direct learning resource links.

### 5. Milestone-Driven Personalized Roadmap
- AI-synthesized 6-phase curriculum tailored to bridge identified skill deficits.
- Interactive checkboxes to toggle milestone completion with real-time recalculation of roadmap velocity.
- Integrated project checkpoints and recommended study links.

### 6. AI Resume & ATS Quantified Bullet Optimizer
- Dual-mode input: **PDF Drag & Drop** (PyPDF extraction) or raw text paste.
- 6-metric ATS score breakdown (Overall, ATS Keyword Match, Technical Depth, Project Impact, Experience, Formatting).
- **Google XYZ Bullet Point Optimizer**: Rewrites descriptive bullets into high-impact quantified achievements (*"Accomplished [X] as measured by [Y], by doing [Z]"*).

### 7. Job Description Compatibility Analyzer
- Paste any live job posting to parse required frameworks, tools, and experience levels.
- Direct comparison against student profile with match score, strong matches, missing prerequisites, and a 3-step immediate action plan.

### 8. AI Project Recommendations (Capstone Blueprints)
- Filterable by domain and difficulty (Beginner, Intermediate, Advanced).
- Complete 4-stage development plans (Data/API, Business Logic, Interface, Deployment) with portfolio value rationales.

### 9. AI Mock Interview Simulator & Scorecard
- Customizable simulation room (Role, Technical / System Design / Behavioral, Difficulty).
- Multi-turn interaction with question prompts, code/text answer submissions, and instant AI scoring on accuracy, completeness, and clarity.
- Comprehensive final scorecard report with improvement suggestions and revision topics.

### 10. Context-Aware AI Career Co-Pilot (RAG Grounded)
- Multi-turn career counseling chat with automatic injection of student academic profile, verified skills, and roadmap state.
- In-memory vector RAG search citing verified engineering curricula.
- 1-click prompt chips for rapid guidance.

### 11. Progress Analytics & Historical Telemetry
- Longitudinal 4-month readiness velocity curve tracking skill mastery, ATS scores, and interview performance.
- Achievement milestone log celebrating completed phases and projects.

### 12. Model-Agnostic LLM Provider Layer
- Unified abstract interface (`BaseLLMProvider`) supporting **Google Gemini** as primary (`gemini-2.5-flash`), **OpenAI**, or proprietary **SkillBridge-LLM**.
- Grounded offline deterministic fallback guaranteeing 100% platform availability.

---

## Quickstart & Installation

### Backend Setup
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
python -m app.database.seed
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Visit **`http://localhost:5173`** in your browser.

---

## Demo Account Credentials

| Field | Value |
|---|---|
| **Email** | `demo@skillbridge.ai` |
| **Password** | `password123` |
| **Student** | Rahul Sharma (B.E. Computer Science, Sem 6, CGPA 7.8, Target: AI/ML Engineer) |

*(Or click the **"Fill Demo (Rahul - AI/ML)"** button on the login screen).*

---

## Documentation

Detailed architectural and developer guides are available in the [`docs/`](docs/) directory:
- [System Architecture](docs/architecture.md)
- [Database Schema & ER Diagram](docs/database.md)
- [REST API Reference](docs/api.md)
- [GenAI & LLM Provider Layer](docs/ai-architecture.md)
- [RAG Retrieval Engine](docs/rag.md)
- [Installation & Developer Setup](docs/setup.md)

---

## Automated Test Suite

Run pytest to verify all backend API endpoints and domain services:
```bash
cd backend
python -m pytest tests/ -v
```

---

<div align="center">
Built for engineers, students, and future leaders.
</div>
