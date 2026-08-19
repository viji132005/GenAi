# SkillBridge AI — GenAI Architecture & LLM Provider Layer

SkillBridge AI features an enterprise-grade, **model-agnostic Generative AI layer**. It decouples application business logic from specific AI model vendors, enabling seamless plug-and-play transitions between Google Gemini, OpenAI, open-source models (vLLM / Ollama), or a proprietary fine-tuned `SkillBridge-LLM`.

---

## Modular Provider Interface (`BaseLLMProvider`)

All AI operations invoke the unified abstract interface defined in `backend/app/ai/base_provider.py`:

```python
class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate_text(self, prompt: str, system_instruction: Optional[str] = None, ...) -> str:
        """Generates plain text response."""
        pass

    @abstractmethod
    async def generate_structured(self, prompt: str, response_schema: Any, system_instruction: Optional[str] = None, ...) -> Dict[str, Any]:
        """Generates structured JSON adhering strictly to a Pydantic schema."""
        pass

    @abstractmethod
    async def get_embedding(self, text: str) -> List[float]:
        """Generates semantic text embeddings."""
        pass
```

---

## LLM Providers Implemented

### 1. Google Gemini Provider (`GeminiProvider`)
- Uses official SDK (`google-genai` / `google.genai`).
- Models: `gemini-2.5-flash` (default), `gemini-1.5-flash`, `gemini-3.6-flash`.
- Uses native structured output decoding with Pydantic schemas.
- Configured via `GEMINI_API_KEY` in `backend/.env`.

### 2. OpenAI-Compatible Provider (`OpenAIProvider`)
- Uses async `httpx` client targeting OpenAI `/v1/chat/completions` API format.
- Models: `gpt-4o-mini`, `gpt-4o`, `deepseek-chat`, or locally hosted `vllm`/`ollama`.
- Configured via `OPENAI_API_KEY` and optional `OPENAI_BASE_URL`.

---

## How to Substitute with a Custom `SkillBridge-LLM`

To connect a proprietary or self-hosted model:
1. Inherit from `BaseLLMProvider` in `backend/app/ai/skillbridge_llm_provider.py`.
2. Implement `generate_text`, `generate_structured`, and `get_embedding`.
3. Register the provider in `backend/app/ai/factory.py`:
   ```python
   elif provider_name == "skillbridge-llm":
       _provider_instance = SkillBridgeLLMProvider(
           base_url=settings.SKILLBRIDGE_LLM_URL,
           api_key=settings.SKILLBRIDGE_LLM_API_KEY
       )
   ```
4. Update `LLM_PROVIDER=skillbridge-llm` in `backend/.env`.
5. **No changes to frontend, services, or controllers are required.**

---

## Grounded Offline Fallback Engine

If an API key is not supplied or an external network failure occurs, the platform automatically engages deterministic semantic fallback algorithms:
- **Taxonomy Matching Engine**: Computes exact skill overlaps and deficit weights.
- **RAG Knowledge Synthesizer**: Injects validated recommendations from the internal curriculum knowledge corpus.
- **Quantification Bullet Transformer**: Applies Google XYZ template patterns (`Accomplished [X] as measured by [Y], by doing [Z]`) to raw resume lines.
