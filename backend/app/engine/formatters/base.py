from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseFormatter(ABC):
    @abstractmethod
    def format_input(self, structured_input: Dict[str, Any], input_schema: List[Dict[str, Any]]) -> str:
        """Format a single testcase input dictionary into target raw syntax string."""
        pass

    @abstractmethod
    def format_batch(self, raw_inputs: List[str]) -> str:
        """Combine multiple raw inputs into a clean batch block ready for pasting."""
        pass
