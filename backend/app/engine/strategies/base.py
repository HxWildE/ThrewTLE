from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import random


@dataclass
class CandidateCase:
    category: str
    structured_input: Dict[str, Any]
    explanation: str
    generation_method: str = "DETERMINISTIC_STRATEGY"
    expected_output: Optional[str] = None
    verification_status: str = "UNVERIFIED"
    comparison_mode: str = "EXACT_MATCH"
    fingerprint: Optional[str] = None
    raw_input: Optional[str] = None


class BaseStrategy(ABC):
    @abstractmethod
    def generate_candidates(
        self,
        problem_slug: str,
        input_schema: List[Dict[str, Any]],
        constraints: List[str],
        rng: random.Random
    ) -> List[CandidateCase]:
        pass
