import os
import json
import logging
from typing import Type, TypeVar, Optional, List, Dict, Any
import httpx
from pydantic import BaseModel

from app.ai.base_provider import BaseLLMProvider, T
from app.config import settings

logger = logging.getLogger("skillbridge.ai.openai")

class OpenAICompatibleProvider(BaseLLMProvider):
    """
    OpenAI-compatible Provider Implementation for SkillBridge AI.
    Supports OpenAI API, Groq, Ollama, DeepSeek, or custom fine-tuned SkillBridge-LLM.
    """

    def __init__(
        self, 
        base_url: Optional[str] = None, 
        api_key: Optional[str] = None, 
        model: Optional[str] = None
    ):
        self.base_url = base_url or settings.CUSTOM_LLM_BASE_URL or "https://api.openai.com/v1"
        self.api_key = api_key or settings.OPENAI_API_KEY or settings.CUSTOM_LLM_API_KEY or ""
        self.model = model or settings.OPENAI_MODEL or settings.CUSTOM_LLM_MODEL or "gpt-4o-mini"

    def is_configured(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 5)

    def _ensure_configured(self):
        if not self.is_configured():
            raise ValueError(
                "OpenAI/Custom LLM API Key is not configured. Please add OPENAI_API_KEY or "
                "CUSTOM_LLM_API_KEY to backend/.env file."
            )

    async def generate_text(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.4
    ) -> str:
        self._ensure_configured()
        
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }

        async with httpx.AsyncClient(timeout=60.0) as http_client:
            resp = await http_client.post(url, json=payload, headers=headers)
            if resp.status_code != 200:
                raise RuntimeError(f"LLM API Error (HTTP {resp.status_code}): {resp.text}")
            
            data = resp.json()
            return data["choices"][0]["message"]["content"]

    async def generate_structured(
        self, 
        prompt: str, 
        schema_cls: Type[T], 
        system_prompt: Optional[str] = None,
        temperature: float = 0.2
    ) -> T:
        self._ensure_configured()
        
        schema_json = json.dumps(schema_cls.model_json_schema(), indent=2)
        
        structured_system = (
            (system_prompt or "") + 
            f"\n\nCRITICAL INSTRUCTION: Respond ONLY with valid JSON conforming to the following JSON Schema.\n"
            f"Do not write any markdown code fences or other text.\n"
            f"JSON Schema:\n{schema_json}"
        )
        
        raw_output = await self.generate_text(
            prompt=prompt,
            system_prompt=structured_system,
            temperature=temperature
        )
        
        parsed_data = self.extract_json_from_text(raw_output)
        return schema_cls.model_validate(parsed_data)

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        if not self.is_configured():
            import hashlib
            import numpy as np
            results = []
            for text in texts:
                seed = int(hashlib.md5(text.encode()).hexdigest(), 16) % (2**32)
                rng = np.random.default_rng(seed)
                results.append(rng.standard_normal(1536).tolist())
            return results

        url = f"{self.base_url.rstrip('/')}/embeddings"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "text-embedding-3-small",
            "input": texts
        }
        
        async with httpx.AsyncClient(timeout=30.0) as http_client:
            resp = await http_client.post(url, json=payload, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                return [item["embedding"] for item in data.get("data", [])]
            else:
                raise RuntimeError(f"Embedding API error (HTTP {resp.status_code}): {resp.text}")
