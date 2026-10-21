import random
from typing import List
from app.engine.generators.base import BaseGenerator, IntegerType


class NumericGenerator(BaseGenerator):
    def generate(self, spec: IntegerType, rng: random.Random) -> int:
        return rng.randint(spec.min_val, spec.max_val)

    def generate_boundary_points(self, spec: IntegerType) -> List[int]:
        """Generate critical numeric boundary values within permitted range."""
        candidates = [
            spec.min_val,
            spec.min_val + 1 if spec.min_val + 1 <= spec.max_val else spec.min_val,
            0 if spec.min_val <= 0 <= spec.max_val else spec.min_val,
            -1 if spec.min_val <= -1 <= spec.max_val else spec.min_val,
            1 if spec.min_val <= 1 <= spec.max_val else spec.max_val,
            spec.max_val - 1 if spec.max_val - 1 >= spec.min_val else spec.max_val,
            spec.max_val
        ]
        # Include 32-bit signed integer limits if within constraints
        int32_limits = [-2147483648, 2147483647, -2147483647, 2147483646]
        for lim in int32_limits:
            if spec.min_val <= lim <= spec.max_val:
                candidates.append(lim)

        return sorted(list(set(candidates)))
