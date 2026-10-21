import random
from typing import Any, Dict, List
from app.engine.generators.array_generators import ArrayGenerator
from app.engine.generators.base import ArrayType, IntegerType, StringType
from app.engine.generators.string_generators import StringGenerator
from app.engine.strategies.base import BaseStrategy, CandidateCase


class StressStrategy(BaseStrategy):
    def __init__(self):
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
        if not input_schema:
            return candidates

        first_param = input_schema[0]
        p_name = first_param.get("name", "nums")
        p_type = first_param.get("type", "integer[]")

        # Upper limit for stress testing in custom testcase window (1000 items is fast to paste & execute)
        stress_size = 1000

        if "[]" in p_type or "array" in p_type:
            spec = ArrayType(element_type=IntegerType(min_val=0, max_val=100000), min_size=stress_size, max_size=stress_size)

            # 1. Large Random Array
            rand_arr = self.arr_gen.generate_stress(spec, target_size=stress_size, rng=rng)
            struct_1 = {p_name: rand_arr}
            if len(input_schema) > 1 and input_schema[1].get("name") == "target":
                struct_1["target"] = rand_arr[0] + rand_arr[-1]
            candidates.append(CandidateCase(
                category="stress",
                structured_input=struct_1,
                explanation=f"Stress case: Large array of {stress_size} random integers to challenge O(N^2) time limits."
            ))

            # 2. Large Reverse-Sorted Array (challenges quicksort worst-case O(N^2))
            rev_arr = list(range(stress_size, 0, -1))
            struct_2 = {p_name: rev_arr}
            if len(input_schema) > 1 and input_schema[1].get("name") == "target":
                struct_2["target"] = rev_arr[0] + rev_arr[-1]
            candidates.append(CandidateCase(
                category="stress",
                structured_input=struct_2,
                explanation=f"Stress case: {stress_size} reverse-sorted elements to trigger naive quicksort O(N^2) degradation."
            ))

            # 3. Large Arithmetic Sequence (challenging Problem 1968 greedy rearrangement)
            seq_arr = list(range(1, stress_size + 1))
            struct_3 = {p_name: seq_arr}
            if len(input_schema) > 1 and input_schema[1].get("name") == "target":
                struct_3["target"] = seq_arr[10] + seq_arr[20]
            candidates.append(CandidateCase(
                category="stress",
                structured_input=struct_3,
                explanation=f"Stress case: {stress_size} consecutive sequential elements."
            ))

        elif "string" in p_type:
            spec = StringType(min_len=stress_size, max_len=stress_size)
            stress_str = self.str_gen.generate_stress(spec, size=stress_size, rng=rng)
            candidates.append(CandidateCase(
                category="stress",
                structured_input={p_name: stress_str},
                explanation=f"Stress case: String of length {stress_size} characters to benchmark throughput."
            ))

        return candidates
