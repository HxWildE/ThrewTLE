import random
from app.engine.generators.array_generators import ArrayGenerator
from app.engine.generators.base import ArrayType, IntegerType, MatrixType, StringType
from app.engine.generators.matrix_generators import MatrixGenerator
from app.engine.generators.numeric_generators import NumericGenerator
from app.engine.generators.string_generators import StringGenerator


def test_numeric_generator():
    gen = NumericGenerator()
    spec = IntegerType(min_val=-50, max_val=50)
    rng = random.Random(42)
    val = gen.generate(spec, rng)
    assert -50 <= val <= 50

    boundaries = gen.generate_boundary_points(spec)
    assert -50 in boundaries
    assert 50 in boundaries
    assert 0 in boundaries


def test_array_generator():
    gen = ArrayGenerator()
    spec = ArrayType(element_type=IntegerType(min_val=1, max_val=100), min_size=3, max_size=10)
    rng = random.Random(42)

    # Identical
    identical = gen.generate_all_identical(spec, size=5, val=7)
    assert len(identical) == 5
    assert all(x == 7 for x in identical)

    # Sorted ascending
    asc = gen.generate_sorted_ascending(spec, size=6, rng=rng)
    assert asc == sorted(asc)

    # Arithmetic sequence
    seq = gen.generate_arithmetic_sequence(spec, size=5, start=2, step=3)
    assert len(seq) == 5
    assert seq == [2, 5, 8, 11, 14]


def test_string_generator():
    gen = StringGenerator()
    spec = StringType(min_len=0, max_len=10)
    rng = random.Random(42)

    empty = gen.generate_empty_or_minimal(spec)
    assert empty == ""

    pal = gen.generate_palindrome(spec, half_size=3, rng=rng)
    assert pal == pal[::-1]


def test_matrix_generator():
    gen = MatrixGenerator()
    ident = gen.generate_identity(size=3)
    assert len(ident) == 3
    assert ident[0][0] == 1 and ident[0][1] == 0
    assert ident[1][1] == 1 and ident[2][2] == 1
