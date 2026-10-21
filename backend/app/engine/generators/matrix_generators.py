import random
from typing import List, Optional
from app.engine.generators.base import BaseGenerator, IntegerType, MatrixType
from app.engine.generators.numeric_generators import NumericGenerator


class MatrixGenerator(BaseGenerator):
    def __init__(self):
        self.num_gen = NumericGenerator()

    def generate(self, spec: MatrixType, rng: random.Random) -> List[List[int]]:
        rows = rng.randint(spec.min_rows, min(spec.max_rows, 5))
        cols = rng.randint(spec.min_cols, min(spec.max_cols, 5))
        elem_spec = spec.element_type if isinstance(spec.element_type, IntegerType) else IntegerType()
        return [[self.num_gen.generate(elem_spec, rng) for _ in range(cols)] for _ in range(rows)]

    def generate_single_cell(self, spec: MatrixType, val: int = 0) -> List[List[int]]:
        return [[val]]

    def generate_identity(self, size: int) -> List[List[int]]:
        return [[1 if r == c else 0 for c in range(size)] for r in range(size)]

    def generate_uniform(self, spec: MatrixType, rows: int, cols: int, val: int) -> List[List[int]]:
        r = max(spec.min_rows, min(spec.max_rows, rows))
        c = max(spec.min_cols, min(spec.max_cols, cols))
        return [[val for _ in range(c)] for _ in range(r)]
