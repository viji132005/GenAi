import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "SkillBridge AI"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Security
    SECRET_KEY: str = "skillbridge-super-secret-jwt-key-2026-production-ready"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./skillbridge.db"
    
    # LLM Settings
    LLM_PROVIDER: str = "gemini"
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"
    
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    CUSTOM_LLM_BASE_URL: str = ""
    CUSTOM_LLM_API_KEY: str = ""
    CUSTOM_LLM_MODEL: str = "skillbridge-llm-v1"
    
    # Uploads & CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000"
    UPLOAD_DIR: str = "./uploads"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

settings = Settings()
