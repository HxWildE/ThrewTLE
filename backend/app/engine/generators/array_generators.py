import random
from typing import Any, List
from app.engine.generators.base import ArrayType, BaseGenerator, IntegerType
from app.engine.generators.numeric_generators import NumericGenerator


class ArrayGenerator(BaseGenerator):
    def __init__(self):
        self.num_gen = NumericGenerator()

    def generate(self, spec: ArrayType, rng: random.Random) -> List[Any]:
        size = rng.randint(spec.min_size, min(spec.max_size, 20))
        elem_spec = spec.element_type if isinstance(spec.element_type, IntegerType) else IntegerType()
        return [self.num_gen.generate(elem_spec, rng) for _ in range(size)]

    def generate_single_element(self, spec: ArrayType, val: int = 0) -> List[int]:
        elem_spec = spec.element_type if isinstance(spec.element_type, IntegerType) else IntegerType()
        clamped_val = max(elem_spec.min_val, min(elem_spec.max_val, val))
        size = max(spec.min_size, 1)
        return [clamped_val] * size

    def generate_all_identical(self, spec: ArrayType, size: int, val: int) -> List[int]:
        s = max(spec.min_size, min(spec.max_size, size))
        elem_spec = spec.element_type if isinstance(spec.element_type, IntegerType) else IntegerType()
        clamped = max(elem_spec.min_val, min(elem_spec.max_val, val))
        return [clamped] * s

    def generate_sorted_ascending(self, spec: ArrayType, size: int, rng: random.Random) -> List[int]:
        s = max(spec.min_size, min(spec.max_size, size))
        elem_spec = spec.element_type if isinstance(spec.element_type, IntegerType) else IntegerType()
        raw = [self.num_gen.generate(elem_spec, rng) for _ in range(s)]
        return sorted(raw)

    def generate_sorted_descending(self, spec: ArrayType, size: int, rng: random.Random) -> List[int]:
        s = max(spec.min_size, min(spec.max_size, size))
        elem_spec = spec.element_type if isinstance(spec.element_type, IntegerType) else IntegerType()
        raw = [self.num_gen.generate(elem_spec, rng) for _ in range(s)]
        return sorted(raw, reverse=True)

    def generate_alternating_high_low(self, spec: ArrayType, size: int) -> List[int]:
        s = max(spec.min_size, min(spec.max_size, size))
        elem_spec = spec.element_type if isinstance(spec.element_type, IntegerType) else IntegerType()
        lo = elem_spec.min_val
        hi = elem_spec.max_val
        return [lo if i % 2 == 0 else hi for i in range(s)]

    def generate_arithmetic_sequence(self, spec: ArrayType, size: int, start: int = 1, step: int = 2) -> List[int]:
        """Adversarial input for algorithms like LeetCode 1968 where average of neighbors must differ."""
        s = max(spec.min_size, min(spec.max_size, size))
        elem_spec = spec.element_type if isinstance(spec.element_type, IntegerType) else IntegerType()
        res = []
        curr = start
        for _ in range(s):
            clamped = max(elem_spec.min_val, min(elem_spec.max_val, curr))
            res.append(clamped)
            curr += step
            if curr > elem_spec.max_val:
                curr = elem_spec.min_val
        return res

    def generate_stress(self, spec: ArrayType, target_size: int = 1000, rng: Optional[random.Random] = None) -> List[int]:
        s = max(spec.min_size, min(spec.max_size, target_size))
        r = rng or random.Random(42)
        elem_spec = spec.element_type if isinstance(spec.element_type, IntegerType) else IntegerType()
        return [r.randint(elem_spec.min_val, elem_spec.max_val) for _ in range(s)]
