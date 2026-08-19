import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database.connection import engine, Base
from app.database.seed import seed_database
from app.ai.factory import get_llm_provider
from app.rag.knowledge_engine import knowledge_engine

# Import Routers
from app.api.auth import router as auth_router
from app.api.profile import router as profile_router
from app.api.career import router as career_router
from app.api.skills import router as skills_router
from app.api.roadmap import router as roadmap_router
from app.api.resume import router as resume_router
from app.api.job import router as job_router
from app.api.projects import router as projects_router
from app.api.interview import router as interview_router
from app.api.chat import router as chat_router
from app.api.analytics import router as analytics_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("skillbridge.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables, seed DB, and initialize RAG index
    logger.info("Initializing database tables and seed data...")
    try:
        await seed_database()
        logger.info("Seed data ready.")
    except Exception as e:
        logger.error(f"Error during startup seeding: {e}")

    logger.info("Initializing RAG vector index...")
    try:
        await knowledge_engine.initialize_index()
    except Exception as e:
        logger.warning(f"RAG init warning: {e}")

    yield
    # Shutdown
    logger.info("SkillBridge AI API shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="SkillBridge AI - Bridge the gap between your skills and your career.",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for local dev / flexibility
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception on {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please try again or check server logs."}
    )

# Health & Status Endpoint
@app.get("/api/health")
async def health_check():
    provider = get_llm_provider()
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "llm_provider": settings.LLM_PROVIDER,
        "llm_configured": provider.is_configured(),
        "rag_documents_indexed": len(knowledge_engine.documents)
    }

@app.get("/api/status")
async def system_status():
    provider = get_llm_provider()
    return {
        "llm_provider": settings.LLM_PROVIDER,
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "active_model": settings.GEMINI_MODEL if settings.LLM_PROVIDER == "gemini" else settings.OPENAI_MODEL,
        "database": "SQLite (Async SQLAlchemy)",
        "rag_indexed": knowledge_engine._is_indexed,
        "docs_count": len(knowledge_engine.documents)
    }

# Mount Routers
app.include_router(auth_router, prefix=settings.API_PREFIX)
app.include_router(profile_router, prefix=settings.API_PREFIX)
app.include_router(career_router, prefix=settings.API_PREFIX)
app.include_router(skills_router, prefix=settings.API_PREFIX)
app.include_router(roadmap_router, prefix=settings.API_PREFIX)
app.include_router(resume_router, prefix=settings.API_PREFIX)
app.include_router(job_router, prefix=settings.API_PREFIX)
app.include_router(projects_router, prefix=settings.API_PREFIX)
app.include_router(interview_router, prefix=settings.API_PREFIX)
app.include_router(chat_router, prefix=settings.API_PREFIX)
app.include_router(analytics_router, prefix=settings.API_PREFIX)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
