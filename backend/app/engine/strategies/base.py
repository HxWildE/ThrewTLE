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

    def populate_parameters(
        self,
        struct: Dict[str, Any],
        input_schema: List[Dict[str, Any]],
        constraints: List[str],
        rng: random.Random,
        variant_hint: str = "default"
    ) -> Dict[str, Any]:
        """
        Fills in any parameters defined in input_schema that are missing from struct,
        respecting parameter-specific bounds and semantic relationships.
        """
        from app.engine.validation.schema_validator import SchemaValidator
        result = dict(struct)
        validator = SchemaValidator()
        param_bounds = validator.parse_param_constraints(constraints, input_schema)

        primary_arr = None
        for v in result.values():
            if isinstance(v, list) and v:
                primary_arr = v
                break

        for param in input_schema:
            name = param.get("name")
            if not name or name in result:
                continue
            p_type = param.get("type", "integer")
            bounds = param_bounds.get(name, {
                "min_len": 1, "max_len": 1000,
                "min_val": 0, "max_val": 1000
            })
            min_len, max_len = bounds["min_len"], bounds["max_len"]
            min_val, max_val = bounds["min_val"], bounds["max_val"]

            if "[]" in p_type or "array" in p_type:
                size = min_len if variant_hint == "min" else (min(max_len, 10) if variant_hint == "max" else rng.randint(min_len, min(max_len, 8)))
                low = min_val if variant_hint == "min" else max(-100, min_val)
                high = min_val if variant_hint == "min" else (max_val if variant_hint == "max" else min(100, max_val))
                result[name] = [rng.randint(low, high) for _ in range(max(1, size))]

            elif "string" in p_type:
                slen = min_len if variant_hint == "min" else (min(max_len, 10) if variant_hint == "max" else rng.randint(min_len, min(max_len, 10)))
                result[name] = "a" * max(1, slen)

            elif "integer" in p_type or "int" in p_type:
                if name == "amount":
                    if variant_hint == "min" or variant_hint == "zero":
                        result[name] = max(0, min_val)
                    elif variant_hint == "max":
                        result[name] = min(max_val, 10000)
                    elif variant_hint == "sum" and primary_arr:
                        result[name] = sum(primary_arr[:min(len(primary_arr), 3)])
                    elif variant_hint == "impossible" and primary_arr:
                        pos = [c for c in primary_arr if isinstance(c, int) and c > 0]
                        min_pos = min(pos) if pos else 2
                        result[name] = max(0, min_pos - 1)
                    else:
                        if primary_arr and rng.random() > 0.4:
                            result[name] = sum(primary_arr[:min(len(primary_arr), 2)])
                        else:
                            result[name] = rng.randint(max(min_val, 0), min(max_val, 100))
                elif name == "target":
                    if variant_hint == "min":
                        result[name] = min_val
                    elif variant_hint == "max":
                        result[name] = min(max_val, 1000)
                    elif primary_arr and len(primary_arr) >= 2 and variant_hint in ["sum", "default"]:
                        result[name] = primary_arr[0] + primary_arr[1]
                    else:
                        result[name] = rng.randint(max(-50, min_val), min(50, max_val))
                elif name in ["k", "val"]:
                    if variant_hint == "min":
                        result[name] = max(0, min_val)
                    elif variant_hint == "max":
                        result[name] = min(max_val, 100)
                    elif primary_arr:
                        result[name] = min(len(primary_arr), max_val)
                    else:
                        result[name] = rng.randint(max(0, min_val), min(10, max_val))
                else:
                    if variant_hint == "min":
                        result[name] = min_val
                    elif variant_hint == "max":
                        result[name] = min(max_val, 1000)
                    else:
                        result[name] = rng.randint(max(-50, min_val), min(50, max_val))

        return result
