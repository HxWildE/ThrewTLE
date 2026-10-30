import random
from typing import Any, Dict, List
from app.engine.generators.array_generators import ArrayGenerator
from app.engine.generators.base import ArrayType, IntegerType, StringType
from app.engine.generators.string_generators import StringGenerator
from app.engine.strategies.base import BaseStrategy, CandidateCase
from app.engine.validation.schema_validator import SchemaValidator


class StructuralStrategy(BaseStrategy):
    def __init__(self):
        super().__init__()
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
        b = param_bounds.get(p_name, {"min_len": 1, "max_len": 1000, "min_val": -100, "max_val": 100})

        min_size = b.get("min_len", 1)
        if "1968" in problem_slug or "not-equal" in problem_slug:
            min_size = max(min_size, 3)
        elif "two-sum" in problem_slug:
            min_size = max(min_size, 2)

        min_elem = b.get("min_val", -100)
        max_elem = b.get("max_val", 100)
        low_bound = max(1, min_elem) if min_elem > 0 else max(-50, min_elem)
        high_bound = min(max_elem, low_bound + 50)

        if "[]" in p_type or "array" in p_type:
            # 1. Strictly Sorted Ascending
            target_len = max(min_size, min(b.get("max_len", 1000), 5))
            asc_arr = sorted(list(set(rng.randint(low_bound, high_bound) for _ in range(target_len + 3))))[:target_len]
            if len(asc_arr) < min_size:
                asc_arr = list(range(low_bound, low_bound + min_size))
            struct_1 = self.populate_parameters({p_name: asc_arr}, input_schema, constraints, rng, variant_hint="sum")
            candidates.append(CandidateCase(
                category="structural",
                structured_input=struct_1,
                explanation="Structural case: Strictly sorted in ascending order."
            ))

            # 2. Strictly Sorted Descending
            desc_arr = sorted(asc_arr, reverse=True)
            struct_2 = self.populate_parameters({p_name: desc_arr}, input_schema, constraints, rng, variant_hint="sum")
            candidates.append(CandidateCase(
                category="structural",
                structured_input=struct_2,
                explanation="Structural case: Strictly sorted in reverse/descending order."
            ))

            # 3. All Elements Identical (if problem allows duplicates)
            dup_val = max(low_bound, min(7, high_bound))
            identical_arr = [dup_val] * max(min_size, min(b.get("max_len", 1000), 4))
            struct_3 = self.populate_parameters({p_name: identical_arr}, input_schema, constraints, rng, variant_hint="default")
            candidates.append(CandidateCase(
                category="structural",
                structured_input=struct_3,
                explanation="Structural case: All elements are identical duplicates."
            ))

            # 4. Arithmetic sequence (Consecutive steps)
            step_len = max(min_size, min(b.get("max_len", 1000), 5))
            step = 2 if (low_bound + 2 * step_len) <= max_elem else 1
            arith_arr = [low_bound + step * i for i in range(step_len)]
            struct_4 = self.populate_parameters({p_name: arith_arr}, input_schema, constraints, rng, variant_hint="default")
            candidates.append(CandidateCase(
                category="structural",
                structured_input=struct_4,
                explanation="Structural case: Direct arithmetic sequence to test algorithmic regularity."
            ))

            # 5. Alternating High-Low pattern
            alt_len = max(min_size, min(b.get("max_len", 1000), 6))
            val_hi = min(max_elem, 100)
            val_lo = max(min_elem, 1)
            alt_arr = [val_hi if i % 2 == 0 else val_lo for i in range(alt_len)]
            struct_5 = self.populate_parameters({p_name: alt_arr}, input_schema, constraints, rng, variant_hint="default")
            candidates.append(CandidateCase(
                category="structural",
                structured_input=struct_5,
                explanation="Structural case: Alternating high/low peaks and valleys."
            ))

        elif "string" in p_type:
            struct_s1 = self.populate_parameters({p_name: "aaaaabbbbb"}, input_schema, constraints, rng)
            candidates.append(CandidateCase(
                category="structural",
                structured_input=struct_s1,
                explanation="Structural case: Block repeated characters."
            ))
            struct_s2 = self.populate_parameters({p_name: "racecar"}, input_schema, constraints, rng)
            candidates.append(CandidateCase(
                category="structural",
                structured_input=struct_s2,
                explanation="Structural case: Perfect palindrome sequence."
            ))
            struct_s3 = self.populate_parameters({p_name: "ab" * 5}, input_schema, constraints, rng)
            candidates.append(CandidateCase(
                category="structural",
                structured_input=struct_s3,
                explanation="Structural case: Alternating 2-character repeating cycle."
            ))

        return candidates

