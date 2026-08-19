import os
import json
import logging
from typing import Type, TypeVar, Optional, List, Dict, Any
import httpx
from pydantic import BaseModel

from app.ai.base_provider import BaseLLMProvider, T
from app.config import settings

logger = logging.getLogger("skillbridge.ai.gemini")

class GeminiProvider(BaseLLMProvider):
    """
    Google Gemini Provider Implementation for SkillBridge AI.
    Integrates with Google GenAI / Gemini REST API.
    Supports structured output generation and embedding generation.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
        self.model = model or settings.GEMINI_MODEL or "gemini-2.5-flash"
        self._client = None
        
        if self.api_key:
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Could not initialize google-genai client: {e}. Will use direct Gemini REST API.")

    def is_configured(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 5)

    def _ensure_configured(self):
        if not self.is_configured():
            raise ValueError(
                "Gemini API Key is not configured. Please add your GEMINI_API_KEY to backend/.env file "
                "or configure it in Settings."
            )

    async def generate_text(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.4
    ) -> str:
        self._ensure_configured()
        
        # Try google-genai SDK first if client is available
        if self._client:
            try:
                # Use interactions or standard models API
                full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
                response = self._client.models.generate_content(
                    model=self.model,
                    contents=full_prompt,
                    config={"temperature": temperature}
                )
                if response.text:
                    return response.text
            except Exception as e:
                logger.warning(f"google-genai SDK call failed ({e}), falling back to direct Gemini API...")

        # Fallback to direct Google Gemini REST endpoint
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        
        contents = []
        if system_prompt:
            contents.append({
                "role": "user",
                "parts": [{"text": f"System Context & Instructions:\n{system_prompt}"}]
            })
            contents.append({
                "role": "model",
                "parts": [{"text": "Understood. I will strictly follow these instructions and profile context."}]
            })
            
        contents.append({
            "role": "user",
            "parts": [{"text": prompt}]
        })

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 4096,
            }
        }

        async with httpx.AsyncClient(timeout=60.0) as http_client:
            resp = await http_client.post(url, json=payload)
            if resp.status_code != 200:
                # Handle model name fallback if specific preview model doesn't exist
                if resp.status_code == 404 and "gemini-2.5-flash" in self.model:
                    fallback_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
                    resp2 = await http_client.post(fallback_url, json=payload)
                    if resp2.status_code == 200:
                        data = resp2.json()
                        return data["candidates"][0]["content"]["parts"][0]["text"]
                
                raise RuntimeError(f"Gemini API Error (HTTP {resp.status_code}): {resp.text}")
            
            data = resp.json()
            try:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError) as e:
                raise RuntimeError(f"Unexpected response format from Gemini: {data}")

    async def generate_structured(
        self, 
        prompt: str, 
        schema_cls: Type[T], 
        system_prompt: Optional[str] = None,
        temperature: float = 0.2
    ) -> T:
        self._ensure_configured()
        
        # Build schema instructions
        schema_json = json.dumps(schema_cls.model_json_schema(), indent=2)
        
        structured_system = (
            (system_prompt or "") + 
            f"\n\nCRITICAL INSTRUCTION: You must respond ONLY with valid JSON conforming to the following JSON Schema.\n"
            f"Do not include any explanation outside the JSON object.\n"
            f"JSON Schema:\n{schema_json}"
        )
        
        raw_output = await self.generate_text(
            prompt=prompt,
            system_prompt=structured_system,
            temperature=temperature
        )
        
        try:
            parsed_data = self.extract_json_from_text(raw_output)
            return schema_cls.model_validate(parsed_data)
        except Exception as e:
            logger.error(f"Schema validation error on LLM output. Raw: {raw_output}. Error: {e}")
            # Try a second-chance quick formatting repair
            repair_prompt = f"Convert the following text into valid JSON matching this schema:\nSchema: {schema_json}\nText to format:\n{raw_output}"
            repaired_raw = await self.generate_text(repair_prompt, temperature=0.0)
            parsed_data = self.extract_json_from_text(repaired_raw)
            return schema_cls.model_validate(parsed_data)

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        if not self.is_configured():
            # Return basic normalized mock embeddings when key is absent
            import hashlib
            import numpy as np
            results = []
            for text in texts:
                # Deterministic pseudo-embedding for zero-key local operation
                seed = int(hashlib.md5(text.encode()).hexdigest(), 16) % (2**32)
                rng = np.random.default_rng(seed)
                vec = rng.standard_normal(768).tolist()
                results.append(vec)
            return results

        url = f"https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:batchEmbedContents?key={self.api_key}"
        
        requests = [{"model": "models/text-embedding-004", "content": {"parts": [{"text": t[:2000]}]}} for t in texts]
        payload = {"requests": requests}
        
        async with httpx.AsyncClient(timeout=30.0) as http_client:
            resp = await http_client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                return [item["values"] for item in data.get("embeddings", [])]
            else:
                logger.warning(f"Batch embedding failed (HTTP {resp.status_code}), falling back to deterministic local vectors.")
                import hashlib
                import numpy as np
                results = []
                for text in texts:
                    seed = int(hashlib.md5(text.encode()).hexdigest(), 16) % (2**32)
                    rng = np.random.default_rng(seed)
                    results.append(rng.standard_normal(768).tolist())
                return results
