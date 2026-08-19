# SkillBridge AI — API Reference

All requests to protected endpoints require an `Authorization: Bearer <token>` header obtained from `/api/auth/login` or `/api/auth/register`.

Base URL: `http://localhost:8000/api`

---

## 1. Authentication (`/api/auth`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/auth/register` | Create a new student account & profile | No |
| `POST` | `/api/auth/login` | Authenticate with email & password | No |
| `GET` | `/api/auth/me` | Retrieve authenticated user profile | Yes |

---

## 2. Student Profile & Skills (`/api/profile`, `/api/skills`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/profile` | Retrieve student academic profile and skills | Yes |
| `PUT` | `/api/profile` | Update academic attributes and target career | Yes |
| `POST` | `/api/profile/onboarding` | Complete 4-step initial onboarding wizard | Yes |
| `POST` | `/api/profile/skills` | Add technical skill with proficiency level | Yes |
| `DELETE` | `/api/profile/skills/{id}` | Delete skill from profile | Yes |
| `POST` | `/api/skills/analyze` | Run skill gap matrix against a target career | Yes |

---

## 3. Career Recommendations (`/api/career`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/career/catalogs` | List all curated career profiles | Yes |
| `POST` | `/api/career/analyze` | AI career fit scoring across all paths | Yes |
| `PUT` | `/api/career/set-target` | Set target career goal on profile | Yes |

---

## 4. Personalized Roadmap (`/api/roadmap`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/roadmap` | Get active multi-phase roadmap | Yes |
| `POST` | `/api/roadmap/generate` | Generate / regenerate roadmap with AI | Yes |
| `PUT` | `/api/roadmap/tasks/{id}` | Toggle task completion checkbox | Yes |

---

## 5. Resume & ATS Analyzer (`/api/resume`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/resume/upload` | Upload PDF file and run ATS analysis | Yes |
| `POST` | `/api/resume/analyze-text` | Analyze pasted plain text resume | Yes |
| `GET` | `/api/resume/latest` | Retrieve student's latest resume analysis | Yes |

---

## 6. Job Description Compatibility (`/api/job`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/job/analyze` | Parse job posting and evaluate fit | Yes |

---

## 7. Project Recommendations (`/api/projects`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/projects` | List domain/difficulty filtered projects | Yes |
| `POST` | `/api/projects/generate` | Generate new project architectures with AI | Yes |
| `PUT` | `/api/projects/{id}/bookmark` | Bookmark / favorite a project blueprint | Yes |

---

## 8. AI Mock Interview (`/api/interview`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/interview/start` | Initialize a new mock interview session | Yes |
| `POST` | `/api/interview/answer` | Submit answer for immediate AI evaluation | Yes |
| `POST` | `/api/interview/{id}/complete` | Finish interview and generate scorecard | Yes |

---

## 9. AI Career Assistant & RAG (`/api/chat`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/chat/message` | Send message with student context & RAG grounding | Yes |
| `GET` | `/api/chat/history` | Retrieve conversation history | Yes |

---

## 10. Progress Analytics & Health (`/api/analytics`, `/api/health`)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/analytics/dashboard` | Aggregated telemetry, radar metrics, & trajectory | Yes |
| `GET` | `/api/health` | System health check and LLM status | No |
