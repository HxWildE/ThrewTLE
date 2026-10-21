from abc import ABC, abstractmethod
from typing import Any, Dict, List
from app.engine.strategies.base import CandidateCase


class BaseLLMAdapter(ABC):
    @abstractmethod
    async def suggest_edge_cases(
        self,
        problem_title: str,
        problem_slug: str,
        constraints: List[str],
        input_schema: List[Dict[str, Any]]
    ) -> List[CandidateCase]:
        pass
