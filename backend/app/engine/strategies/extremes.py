import random
from typing import Any, Dict, List
from app.engine.generators.base import ArrayType, IntegerType
from app.engine.generators.numeric_generators import NumericGenerator
from app.engine.strategies.base import BaseStrategy, CandidateCase


class NumericExtremesStrategy(BaseStrategy):
    def __init__(self):
        self.num_gen = NumericGenerator()

    def generate_candidates(
        self,
        problem_slug: str,
        input_schema: List[Dict[str, Any]],
        constraints: List[str],
        rng: random.Random
    ) -> List[CandidateCase]:
        candidates: List[CandidateCase] = []
        if not input_schema:
            return candidates

        first_param = input_schema[0]
        p_name = first_param.get("name", "nums")
        p_type = first_param.get("type", "integer[]")

        min_size = 2 if "two-sum" in problem_slug else (3 if "1968" in problem_slug else 1)

        if "[]" in p_type or "array" in p_type:
            # 1. All Negative Numbers (Classic Kadane's algorithm trap for Problem 53)
            neg_arr = [-5, -12, -3, -40, -1]
            if len(neg_arr) < min_size:
                neg_arr = neg_arr * min_size
            struct_1 = {p_name: neg_arr[:max(min_size, len(neg_arr))]}
            if len(input_schema) > 1 and input_schema[1].get("name") == "target":
                struct_1["target"] = struct_1[p_name][0] + struct_1[p_name][1]
            candidates.append(CandidateCase(
                category="numeric_extremes",
                structured_input=struct_1,
                explanation="Numeric extremes: Entirely negative numbers (tests negative sum logic / Kadane initialization)."
            ))

            # 2. Large Extreme Numbers (near 10^9 or 32-bit limits)
            ext_arr = [-1000000000, 1000000000, 0]
            if "1968" in problem_slug:
                ext_arr = [0, 500000000, 1000000000]
            if len(ext_arr) < min_size:
                ext_arr = ext_arr * min_size
            struct_2 = {p_name: ext_arr[:max(min_size, len(ext_arr))]}
            if len(input_schema) > 1 and input_schema[1].get("name") == "target":
                struct_2["target"] = 0
            candidates.append(CandidateCase(
                category="numeric_extremes",
                structured_input=struct_2,
                explanation="Numeric extremes: Elements at upper numeric threshold (+-10^9) to detect integer overflow."
            ))

            # 3. All Zeros
            zeros_arr = [0] * max(min_size, 4)
            struct_3 = {p_name: zeros_arr}
            if len(input_schema) > 1 and input_schema[1].get("name") == "target":
                struct_3["target"] = 0
            candidates.append(CandidateCase(
                category="numeric_extremes",
                structured_input=struct_3,
                explanation="Numeric extremes: All zero elements."
            ))

            # 4. Mixed Polarities
            mixed_arr = [-100, 200, -300, 400, -500]
            if len(mixed_arr) < min_size:
                mixed_arr = mixed_arr * min_size
            struct_4 = {p_name: mixed_arr[:max(min_size, len(mixed_arr))]}
            if len(input_schema) > 1 and input_schema[1].get("name") == "target":
                struct_4["target"] = 100
            candidates.append(CandidateCase(
                category="numeric_extremes",
                structured_input=struct_4,
                explanation="Numeric extremes: High-magnitude alternating positive/negative values."
            ))

        return candidates
