import random
from typing import Any, Dict, List
from app.engine.generators.array_generators import ArrayGenerator
from app.engine.generators.base import ArrayType, IntegerType, StringType
from app.engine.generators.string_generators import StringGenerator
from app.engine.strategies.base import BaseStrategy, CandidateCase


class StructuralStrategy(BaseStrategy):
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

        min_size = 3 if ("1968" in problem_slug or "not-equal" in problem_slug) else 2

        if "[]" in p_type or "array" in p_type:
            spec = ArrayType(element_type=IntegerType(min_val=-100, max_val=100), min_size=min_size, max_size=100)

            # 1. Strictly Sorted Ascending
            asc_arr = sorted(list(set(rng.randint(1, 50) for _ in range(max(min_size + 2, 5)))))
            struct_1 = {p_name: asc_arr}
            if len(input_schema) > 1 and input_schema[1].get("name") == "target":
                struct_1["target"] = asc_arr[0] + asc_arr[-1]
            candidates.append(CandidateCase(
                category="structural",
                structured_input=struct_1,
                explanation="Structural case: Strictly sorted in ascending order."
            ))

            # 2. Strictly Sorted Descending
            desc_arr = sorted(asc_arr, reverse=True)
            struct_2 = {p_name: desc_arr}
            if len(input_schema) > 1 and input_schema[1].get("name") == "target":
                struct_2["target"] = desc_arr[0] + desc_arr[-1]
            candidates.append(CandidateCase(
                category="structural",
                structured_input=struct_2,
                explanation="Structural case: Strictly sorted in reverse/descending order."
            ))

            # 3. All Elements Identical (if problem allows duplicates)
            identical_arr = [7] * max(min_size, 4)
            struct_3 = {p_name: identical_arr}
            if len(input_schema) > 1 and input_schema[1].get("name") == "target":
                struct_3["target"] = 14
            candidates.append(CandidateCase(
                category="structural",
                structured_input=struct_3,
                explanation="Structural case: All elements are identical duplicates."
            ))

            # 4. Arithmetic sequence (Consecutive steps)
            arith_arr = [2 * i + 1 for i in range(max(min_size, 5))]
            struct_4 = {p_name: arith_arr}
            if len(input_schema) > 1 and input_schema[1].get("name") == "target":
                struct_4["target"] = arith_arr[1] + arith_arr[3]
            candidates.append(CandidateCase(
                category="structural",
                structured_input=struct_4,
                explanation="Structural case: Direct arithmetic sequence (neighbors equal average) to challenge wiggle-sort."
            ))

            # 5. Alternating High-Low pattern
            alt_arr = [100 if i % 2 == 0 else 1 for i in range(max(min_size, 6))]
            struct_5 = {p_name: alt_arr}
            if len(input_schema) > 1 and input_schema[1].get("name") == "target":
                struct_5["target"] = 101
            candidates.append(CandidateCase(
                category="structural",
                structured_input=struct_5,
                explanation="Structural case: Alternating high/low peaks and valleys."
            ))

        elif "string" in p_type:
            spec = StringType(min_len=1, max_len=100)
            candidates.append(CandidateCase(
                category="structural",
                structured_input={p_name: "aaaaabbbbb"},
                explanation="Structural case: Block repeated characters."
            ))
            candidates.append(CandidateCase(
                category="structural",
                structured_input={p_name: "racecar"},
                explanation="Structural case: Perfect palindrome sequence."
            ))
            candidates.append(CandidateCase(
                category="structural",
                structured_input={p_name: "ab" * 10},
                explanation="Structural case: Alternating 2-character repeating cycle."
            ))

        return candidates
