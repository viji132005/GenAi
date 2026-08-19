import abc
import json
import re
from typing import Type, TypeVar, Optional, List, Dict, Any
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class BaseLLMProvider(abc.ABC):
    """
    Abstract Base Class for LLM Providers in SkillBridge AI.
    Allows seamlessly swapping between Google Gemini, OpenAI, Groq, 
    or a custom fine-tuned SkillBridge-LLM without changing application logic.
    """

    @abc.abstractmethod
    async def generate_text(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.4
    ) -> str:
        """Generate unstructured text from prompt."""
        pass

    @abc.abstractmethod
    async def generate_structured(
        self, 
        prompt: str, 
        schema_cls: Type[T], 
        system_prompt: Optional[str] = None,
        temperature: float = 0.2
    ) -> T:
        """Generate structured data adhering to a Pydantic schema."""
        pass

    @abc.abstractmethod
    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Compute vector embeddings for a list of text strings."""
        pass

    @abc.abstractmethod
    def is_configured(self) -> bool:
        """Check if provider credentials/API keys are configured."""
        pass

    @staticmethod
    def extract_json_from_text(text: str) -> Dict[str, Any]:
        """
        Helper method to extract and parse JSON from model output, 
        handling markdown fences and trailing text.
        """
        cleaned = text.strip()
        # Look for markdown code fence ```json ... ```
        json_pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
        match = re.search(json_pattern, cleaned)
        if match:
            cleaned = match.group(1).strip()
        else:
            # Look for outermost curly braces or brackets
            first_brace = cleaned.find("{")
            last_brace = cleaned.rfind("}")
            if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
                cleaned = cleaned[first_brace:last_brace+1]
        
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            # Try cleaning up potential trailing commas or formatting issues
            cleaned_loose = re.sub(r",\s*([\]}])", r"\1", cleaned)
            return json.loads(cleaned_loose)
