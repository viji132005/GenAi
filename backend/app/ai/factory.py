import logging
from typing import Optional
from app.config import settings
from app.ai.base_provider import BaseLLMProvider
from app.ai.gemini_provider import GeminiProvider
from app.ai.openai_provider import OpenAICompatibleProvider

logger = logging.getLogger("skillbridge.ai.factory")

_cached_provider: Optional[BaseLLMProvider] = None

def get_llm_provider(force_refresh: bool = False) -> BaseLLMProvider:
    """
    Factory function to retrieve the active LLM Provider.
    Supports modular swapping between Gemini, OpenAI, or custom SkillBridge-LLM.
    """
    global _cached_provider
    if _cached_provider is not None and not force_refresh:
        return _cached_provider

    provider_name = (settings.LLM_PROVIDER or "gemini").lower().strip()
    
    if provider_name == "gemini":
        logger.info(f"Initializing Google Gemini Provider with model: {settings.GEMINI_MODEL}")
        _cached_provider = GeminiProvider(
            api_key=settings.GEMINI_API_KEY,
            model=settings.GEMINI_MODEL
        )
    elif provider_name in ["openai", "custom", "skillbridge"]:
        logger.info(f"Initializing OpenAI-Compatible/Custom Provider with model: {settings.OPENAI_MODEL}")
        _cached_provider = OpenAICompatibleProvider(
            base_url=settings.CUSTOM_LLM_BASE_URL or "https://api.openai.com/v1",
            api_key=settings.OPENAI_API_KEY or settings.CUSTOM_LLM_API_KEY,
            model=settings.OPENAI_MODEL or settings.CUSTOM_LLM_MODEL
        )
    else:
        logger.warning(f"Unknown provider '{provider_name}', defaulting to Google Gemini.")
        _cached_provider = GeminiProvider(
            api_key=settings.GEMINI_API_KEY,
            model=settings.GEMINI_MODEL
        )
        
    return _cached_provider
