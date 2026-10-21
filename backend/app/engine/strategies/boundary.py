import random
from typing import Any, Dict, List
from app.engine.generators.array_generators import ArrayGenerator
from app.engine.generators.base import ArrayType, IntegerType, StringType
from app.engine.generators.numeric_generators import NumericGenerator
from app.engine.generators.string_generators import StringGenerator
from app.engine.strategies.base import BaseStrategy, CandidateCase


class BoundaryStrategy(BaseStrategy):
    def __init__(self):
        self.num_gen = NumericGenerator()
        self.arr_gen = ArrayGenerator()
        self.str_gen = StringGenerator()

    def generate_candidates(
        self,
        problem_slug: str,
        input_schema: List[Dict[str, Any]],
        constraints: List[str],
        rng: random.Random
    ) -> List[CandidateCase]:
        candidates: List[CandidateCase] = []

        # Parse primary parameter from schema
        if not input_schema:
            return candidates

        first_param = input_schema[0]
        p_name = first_param.get("name", "nums")
        p_type = first_param.get("type", "integer[]")

        # Determine minimum size from constraints or defaults
        min_size = 1
        if "two-sum" in problem_slug:
            min_size = 2
        elif "not-equal-to-average" in problem_slug or "1968" in problem_slug:
            min_size = 3

        if "[]" in p_type or "array" in p_type:
            elem_spec = IntegerType(min_val=-1000, max_val=1000)
            arr_spec = ArrayType(element_type=elem_spec, min_size=min_size, max_size=1000)

            # Case 1: Minimum valid length array
            min_arr = [rng.randint(1, 10) for _ in range(min_size)]
            struct_1 = {p_name: min_arr}
            if len(input_schema) > 1 and input_schema[1].get("name") == "target":
                struct_1["target"] = sum(min_arr)

            candidates.append(CandidateCase(
                category="boundary",
                structured_input=struct_1,
                explanation=f"Boundary case: Minimal permitted array length ({min_size})."
            ))

            # Case 2: Array with minimum possible value
            min_val_arr = [elem_spec.min_val] * min_size
            struct_2 = {p_name: min_val_arr}
            if len(input_schema) > 1 and input_schema[1].get("name") == "target":
                struct_2["target"] = elem_spec.min_val * 2
            candidates.append(CandidateCase(
                category="boundary",
                structured_input=struct_2,
                explanation=f"Boundary case: Array elements positioned exactly at minimum bound ({elem_spec.min_val})."
            ))

            # Case 3: Array with maximum possible value
            max_val_arr = [elem_spec.max_val] * min_size
            struct_3 = {p_name: max_val_arr}
            if len(input_schema) > 1 and input_schema[1].get("name") == "target":
                struct_3["target"] = elem_spec.max_val * 2
            candidates.append(CandidateCase(
                category="boundary",
                structured_input=struct_3,
                explanation=f"Boundary case: Array elements positioned exactly at maximum bound ({elem_spec.max_val})."
            ))

        elif "string" in p_type:
            str_spec = StringType(min_len=0 if "palindrome" not in problem_slug else 1, max_len=1000)
            empty_or_single = self.str_gen.generate_empty_or_minimal(str_spec)
            candidates.append(CandidateCase(
                category="boundary",
                structured_input={p_name: empty_or_single},
                explanation="Boundary case: Minimum allowed string length."
            ))
            candidates.append(CandidateCase(
                category="boundary",
                structured_input={p_name: "a"},
                explanation="Boundary case: Single character string."
            ))

        elif "integer" in p_type or "int" in p_type:
            num_spec = IntegerType(min_val=-1000, max_val=1000)
            candidates.append(CandidateCase(
                category="boundary",
                structured_input={p_name: num_spec.min_val},
                explanation="Boundary case: Integer at lowest constraint bound."
            ))
            candidates.append(CandidateCase(
                category="boundary",
                structured_input={p_name: num_spec.max_val},
                explanation="Boundary case: Integer at highest constraint bound."
            ))

        return candidates
