import random
from typing import Any, Dict, List
from app.engine.generators.array_generators import ArrayGenerator
from app.engine.generators.base import ArrayType, IntegerType, StringType
from app.engine.generators.string_generators import StringGenerator
from app.engine.strategies.base import BaseStrategy, CandidateCase
from app.engine.validation.schema_validator import SchemaValidator


class StressStrategy(BaseStrategy):
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
        b = param_bounds.get(p_name, {"min_len": 1, "max_len": 1000, "min_val": 0, "max_val": 100000})

        # Upper limit for stress testing respecting constraint max_len
        stress_size = max(b.get("min_len", 1), min(b.get("max_len", 1000), 1000))
        min_elem = b.get("min_val", 0)
        max_elem = min(b.get("max_val", 100000), 100000)
        elem_low = max(1, min_elem) if min_elem > 0 else min_elem

        if "[]" in p_type or "array" in p_type:
            spec = ArrayType(element_type=IntegerType(min_val=elem_low, max_val=max_elem), min_size=stress_size, max_size=stress_size)

            # 1. Large Random Array
            rand_arr = self.arr_gen.generate_stress(spec, target_size=stress_size, rng=rng)
            struct_1 = self.populate_parameters({p_name: rand_arr}, input_schema, constraints, rng, variant_hint="max")
            candidates.append(CandidateCase(
                category="stress",
                structured_input=struct_1,
                explanation=f"Stress case: Array of {stress_size} random integers to challenge algorithmic bounds."
            ))

            # 2. Large Reverse-Sorted Array (challenges quicksort worst-case O(N^2))
            step = max(1, (max_elem - elem_low) // max(1, stress_size))
            rev_arr = [max(elem_low, min(max_elem, max_elem - i * step)) for i in range(stress_size)]
            struct_2 = self.populate_parameters({p_name: rev_arr}, input_schema, constraints, rng, variant_hint="max")
            candidates.append(CandidateCase(
                category="stress",
                structured_input=struct_2,
                explanation=f"Stress case: {stress_size} reverse-sorted elements to trigger naive quicksort O(N^2) degradation."
            ))

            # 3. Large Arithmetic Sequence
            seq_arr = [max(elem_low, min(max_elem, elem_low + i * step)) for i in range(stress_size)]
            struct_3 = self.populate_parameters({p_name: seq_arr}, input_schema, constraints, rng, variant_hint="max")
            candidates.append(CandidateCase(
                category="stress",
                structured_input=struct_3,
                explanation=f"Stress case: {stress_size} consecutive sequential elements."
            ))

        elif "string" in p_type:
            spec = StringType(min_len=stress_size, max_len=stress_size)
            stress_str = self.str_gen.generate_stress(spec, size=stress_size, rng=rng)
            struct_s = self.populate_parameters({p_name: stress_str}, input_schema, constraints, rng, variant_hint="max")
            candidates.append(CandidateCase(
                category="stress",
                structured_input=struct_s,
                explanation=f"Stress case: String of length {stress_size} characters to benchmark throughput."
            ))

        return candidates

