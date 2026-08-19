# SkillBridge AI — Installation & Developer Setup Guide

This guide walks you through setting up and running SkillBridge AI locally on your machine.

---

## Prerequisites
- **Python**: Version 3.10+ (tested on Python 3.14.0)
- **Node.js**: Version 18.0+ (tested on Node v20.18.3)
- **npm**: Version 9.0+ (tested on npm 10.8.2)
- **Git**

---

## 1. Backend Setup

1. Open a terminal and navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure Environment Variables:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=AIzaSy...your_gemini_api_key
   LLM_PROVIDER=gemini
   GEMINI_MODEL=gemini-2.5-flash
   SECRET_KEY=skillbridge_super_secret_jwt_key_2026
   ```

5. Seed the Database:
   ```bash
   python -m app.database.seed
   ```
   *(Initializes `skillbridge.db` with demo student Rahul Sharma, 7 career profiles, 50+ skills, roadmap, and analytics).*

6. Start the FastAPI Server:
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```
   - API Health Check: `http://127.0.0.1:8000/api/health`
   - Interactive Swagger Docs: `http://127.0.0.1:8000/docs`

---

## 2. Frontend Setup

1. Open a new terminal and navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Start the Vite Development Server:
   ```bash
   npm run dev
   ```
   - Web App UI: `http://localhost:5173`

---

## 3. Demo Credentials

You can sign in immediately using pre-seeded student credentials:
- **Email**: `demo@skillbridge.ai`
- **Password**: `password123`

Or click the **"Fill Demo (Rahul - AI/ML)"** quick-login button on the login screen.

---

## 4. Running Backend Tests
To execute the automated test suite:
```bash
cd backend
python -m pytest tests/ -v
```
