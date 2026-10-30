import random
from typing import Any, Dict, List
from app.engine.generators.base import ArrayType, IntegerType
from app.engine.generators.numeric_generators import NumericGenerator
from app.engine.strategies.base import BaseStrategy, CandidateCase
from app.engine.validation.schema_validator import SchemaValidator


class NumericExtremesStrategy(BaseStrategy):
    def __init__(self):
        super().__init__()
        self.num_gen = NumericGenerator()
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
        b = param_bounds.get(p_name, {"min_len": 1, "max_len": 1000, "min_val": -1000000000, "max_val": 1000000000})

        min_size = b.get("min_len", 1)
        if "two-sum" in problem_slug:
            min_size = max(min_size, 2)
        elif "1968" in problem_slug:
            min_size = max(min_size, 3)

        min_elem = b.get("min_val", -1000000000)
        max_elem = b.get("max_val", 1000000000)

        if "[]" in p_type or "array" in p_type:
            # 1. All Negative Numbers (only if negative numbers are allowed by constraints)
            if min_elem < 0:
                neg_arr = [max(min_elem, -5), max(min_elem, -12), max(min_elem, -3), max(min_elem, -40), max(min_elem, -1)]
                if len(neg_arr) < min_size:
                    neg_arr = neg_arr * min_size
                struct_1 = self.populate_parameters({p_name: neg_arr[:max(min_size, len(neg_arr))]}, input_schema, constraints, rng, variant_hint="min")
                candidates.append(CandidateCase(
                    category="numeric_extremes",
                    structured_input=struct_1,
                    explanation="Numeric extremes: Entirely negative numbers (tests negative sum logic / Kadane initialization)."
                ))
            else:
                # When strictly non-negative: elements positioned at minimum bound
                min_arr = [min_elem] * max(min_size, 3)
                struct_1 = self.populate_parameters({p_name: min_arr}, input_schema, constraints, rng, variant_hint="min")
                candidates.append(CandidateCase(
                    category="numeric_extremes",
                    structured_input=struct_1,
                    explanation=f"Numeric extremes: Minimal non-negative elements positioned at lower bound ({min_elem})."
                ))

            # 2. Large Extreme Numbers (near max bound or 32-bit limits)
            low_extreme = max(min_elem, -1000000000)
            high_extreme = min(max_elem, 1000000000)
            mid_val = 0 if min_elem <= 0 <= max_elem else min_elem
            ext_arr = [low_extreme, high_extreme, mid_val]
            if "1968" in problem_slug:
                ext_arr = [0, 500000000, 1000000000]
            if len(ext_arr) < min_size:
                ext_arr = ext_arr * min_size
            struct_2 = self.populate_parameters({p_name: ext_arr[:max(min_size, len(ext_arr))]}, input_schema, constraints, rng, variant_hint="max")
            candidates.append(CandidateCase(
                category="numeric_extremes",
                structured_input=struct_2,
                explanation="Numeric extremes: Elements at upper numeric threshold to detect integer overflow."
            ))

            # 3. All Zeros (only if 0 is permitted within [min_elem, max_elem])
            if min_elem <= 0 <= max_elem:
                zeros_arr = [0] * max(min_size, 4)
                struct_3 = self.populate_parameters({p_name: zeros_arr}, input_schema, constraints, rng, variant_hint="zero")
                candidates.append(CandidateCase(
                    category="numeric_extremes",
                    structured_input=struct_3,
                    explanation="Numeric extremes: All zero elements."
                ))
            else:
                # Powers of 10 or wide spacing within bounds
                pows = [min_elem, min(max_elem, max(min_elem + 1, 10)), min(max_elem, max(min_elem + 2, 100))]
                struct_3 = self.populate_parameters({p_name: pows[:max(min_size, len(pows))]}, input_schema, constraints, rng, variant_hint="default")
                candidates.append(CandidateCase(
                    category="numeric_extremes",
                    structured_input=struct_3,
                    explanation="Numeric extremes: Order-of-magnitude geometric stepping denominations."
                ))

            # 4. Mixed Polarities (if negative and positive elements both permitted)
            if min_elem < 0 < max_elem:
                mixed_arr = [max(min_elem, -100), min(max_elem, 200), max(min_elem, -300), min(max_elem, 400)]
                if len(mixed_arr) < min_size:
                    mixed_arr = mixed_arr * min_size
                struct_4 = self.populate_parameters({p_name: mixed_arr[:max(min_size, len(mixed_arr))]}, input_schema, constraints, rng, variant_hint="default")
                candidates.append(CandidateCase(
                    category="numeric_extremes",
                    structured_input=struct_4,
                    explanation="Numeric extremes: High-magnitude alternating positive/negative values."
                ))

        elif "integer" in p_type or "int" in p_type:
            struct_i1 = self.populate_parameters({p_name: max(min_elem, -1000000000)}, input_schema, constraints, rng, variant_hint="min")
            candidates.append(CandidateCase(
                category="numeric_extremes",
                structured_input=struct_i1,
                explanation="Numeric extremes: Lowest integer boundary."
            ))
            struct_i2 = self.populate_parameters({p_name: min(max_elem, 1000000000)}, input_schema, constraints, rng, variant_hint="max")
            candidates.append(CandidateCase(
                category="numeric_extremes",
                structured_input=struct_i2,
                explanation="Numeric extremes: Highest integer boundary."
            ))

        return candidates

