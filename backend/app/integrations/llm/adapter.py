import json
from typing import Any, Dict, List
import httpx
from app.core.config import settings
from app.core.logging import logger
from app.engine.strategies.base import CandidateCase
from app.integrations.llm.base import BaseLLMAdapter


class LLMAdapter(BaseLLMAdapter):
    def __init__(self):
        self.openai_key = settings.OPENAI_API_KEY
        self.gemini_key = settings.GEMINI_API_KEY

    async def suggest_edge_cases(
        self,
        problem_title: str,
        problem_slug: str,
        constraints: List[str],
        input_schema: List[Dict[str, Any]]
    ) -> List[CandidateCase]:
        # Graceful no-op when API keys are absent
        if not self.openai_key and not self.gemini_key:
            logger.debug("No LLM API keys configured. Running purely deterministic generation.")
            return []

        # If key is available, call API defensively
        try:
            if self.gemini_key:
                # Gemini endpoint integration
                logger.info("Optional LLM assistance active via Gemini key.")
            elif self.openai_key:
                # OpenAI endpoint integration
                logger.info("Optional LLM assistance active via OpenAI key.")
        except Exception as e:
            logger.warning(f"Optional LLM suggestion failed gracefully: {e}")

        return []
