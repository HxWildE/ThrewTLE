import random
from typing import Any, Dict, List
from app.engine.generators.array_generators import ArrayGenerator
from app.engine.generators.base import ArrayType, IntegerType, StringType
from app.engine.generators.numeric_generators import NumericGenerator
from app.engine.generators.string_generators import StringGenerator
from app.engine.strategies.base import BaseStrategy, CandidateCase
from app.engine.validation.schema_validator import SchemaValidator


class BoundaryStrategy(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.num_gen = NumericGenerator()
        self.arr_gen = ArrayGenerator()
        self.str_gen = StringGenerator()
        self.validator = SchemaValidator()

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

        param_bounds = self.validator.parse_param_constraints(constraints, input_schema)
        first_param = input_schema[0]
        p_name = first_param.get("name", "nums")
        p_type = first_param.get("type", "integer[]")
        b = param_bounds.get(p_name, {"min_len": 1, "max_len": 1000, "min_val": -1000, "max_val": 1000})

        # Determine minimum size from constraints or defaults
        min_size = b.get("min_len", 1)
        if "two-sum" in problem_slug:
            min_size = max(min_size, 2)
        elif "not-equal-to-average" in problem_slug or "1968" in problem_slug:
            min_size = max(min_size, 3)

        min_elem_val = b.get("min_val", -1000)
        max_elem_val = b.get("max_val", 1000)

        if "[]" in p_type or "array" in p_type:
            # Case 1: Minimum valid length array
            low_sample = max(1, min_elem_val) if min_elem_val > 0 else max(-10, min_elem_val)
            high_sample = min(max_elem_val, low_sample + 10)
            min_arr = [rng.randint(low_sample, high_sample) for _ in range(min_size)]
            struct_1 = self.populate_parameters({p_name: min_arr}, input_schema, constraints, rng, variant_hint="sum")

            candidates.append(CandidateCase(
                category="boundary",
                structured_input=struct_1,
                explanation=f"Boundary case: Minimal permitted array length ({min_size})."
            ))

            # Case 2: Array with minimum possible value
            safe_min_val = min_elem_val if -1000000 <= min_elem_val <= 1000000 else (1 if min_elem_val > 0 else -1000)
            min_val_arr = [safe_min_val] * min_size
            struct_2 = self.populate_parameters({p_name: min_val_arr}, input_schema, constraints, rng, variant_hint="min")
            candidates.append(CandidateCase(
                category="boundary",
                structured_input=struct_2,
                explanation=f"Boundary case: Array elements positioned exactly at minimum bound ({safe_min_val})."
            ))

            # Case 3: Array with maximum possible value (capped for reasonable representation)
            safe_max_val = min(max_elem_val, 1000)
            max_val_arr = [safe_max_val] * min_size
            struct_3 = self.populate_parameters({p_name: max_val_arr}, input_schema, constraints, rng, variant_hint="max")
            candidates.append(CandidateCase(
                category="boundary",
                structured_input=struct_3,
                explanation=f"Boundary case: Array elements positioned at high bound ({safe_max_val})."
            ))

            # Case 4: Zero or minimal secondary parameter (e.g. amount=0, target=0, k=0)
            if len(input_schema) > 1:
                struct_4 = self.populate_parameters({p_name: min_arr}, input_schema, constraints, rng, variant_hint="zero")
                candidates.append(CandidateCase(
                    category="boundary",
                    structured_input=struct_4,
                    explanation="Boundary case: Secondary scalar parameter positioned at minimal/zero bound."
                ))

        elif "string" in p_type:
            str_min_len = b.get("min_len", 0 if "palindrome" not in problem_slug else 1)
            single_or_empty = "a" * str_min_len
            struct_s1 = self.populate_parameters({p_name: single_or_empty}, input_schema, constraints, rng, variant_hint="min")
            candidates.append(CandidateCase(
                category="boundary",
                structured_input=struct_s1,
                explanation="Boundary case: Minimum allowed string length."
            ))

            struct_s2 = self.populate_parameters({p_name: "a" * max(1, str_min_len)}, input_schema, constraints, rng, variant_hint="default")
            candidates.append(CandidateCase(
                category="boundary",
                structured_input=struct_s2,
                explanation="Boundary case: Single character string."
            ))

        elif "integer" in p_type or "int" in p_type:
            safe_min = max(-1000000, min_elem_val)
            safe_max = min(1000000, max_elem_val)
            struct_i1 = self.populate_parameters({p_name: safe_min}, input_schema, constraints, rng, variant_hint="min")
            candidates.append(CandidateCase(
                category="boundary",
                structured_input=struct_i1,
                explanation=f"Boundary case: Integer at lowest constraint bound ({safe_min})."
            ))
            struct_i2 = self.populate_parameters({p_name: safe_max}, input_schema, constraints, rng, variant_hint="max")
            candidates.append(CandidateCase(
                category="boundary",
                structured_input=struct_i2,
                explanation=f"Boundary case: Integer at highest constraint bound ({safe_max})."
            ))

        return candidates

