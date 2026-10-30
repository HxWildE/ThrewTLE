import random
from app.engine.strategies.boundary import BoundaryStrategy
from app.engine.strategies.extremes import NumericExtremesStrategy
from app.engine.strategies.stress import StressStrategy
from app.engine.strategies.structural import StructuralStrategy


def test_boundary_strategy():
    strat = BoundaryStrategy()
    rng = random.Random(42)
    cases = strat.generate_candidates(
        problem_slug="two-sum",
        input_schema=[{"name": "nums", "type": "integer[]"}, {"name": "target", "type": "integer"}],
        constraints=["2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9"],
        rng=rng
    )
    assert len(cases) > 0
    assert any(c.category == "boundary" for c in cases)
    # Check minimum length respected (2 for two-sum)
    for c in cases:
        assert len(c.structured_input["nums"]) >= 2


def test_structural_strategy():
    strat = StructuralStrategy()
    rng = random.Random(42)
    cases = strat.generate_candidates(
        problem_slug="array-with-elements-not-equal-to-average-of-neighbors",
        input_schema=[{"name": "nums", "type": "integer[]"}],
        constraints=["3 <= nums.length <= 10^5"],
        rng=rng
    )
    assert len(cases) > 0
    assert any(c.category == "structural" for c in cases)


def test_extremes_strategy():
    strat = NumericExtremesStrategy()
    rng = random.Random(42)
    cases = strat.generate_candidates(
        problem_slug="maximum-subarray",
        input_schema=[{"name": "nums", "type": "integer[]"}],
        constraints=["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
        rng=rng
    )
    assert len(cases) > 0
    # Should include negative elements
    assert any(c.category == "numeric_extremes" for c in cases)


def test_stress_strategy():
    strat = StressStrategy()
    rng = random.Random(42)
    cases = strat.generate_candidates(
        problem_slug="two-sum",
        input_schema=[{"name": "nums", "type": "integer[]"}, {"name": "target", "type": "integer"}],
        constraints=["2 <= nums.length <= 10^4"],
        rng=rng
    )
    assert len(cases) > 0
    for c in cases:
        assert len(c.structured_input["nums"]) >= 100


def test_strategies_coin_change():
    rng = random.Random(42)
    schema = [{"name": "coins", "type": "integer[]"}, {"name": "amount", "type": "integer"}]
    constraints = ["1 <= coins.length <= 12", "1 <= coins[i] <= 2^31 - 1", "0 <= amount <= 10^4"]

    b_strat = BoundaryStrategy()
    b_cases = b_strat.generate_candidates("coin-change", schema, constraints, rng)
    assert len(b_cases) > 0
    for c in b_cases:
        assert "coins" in c.structured_input and "amount" in c.structured_input
        assert len(c.structured_input["coins"]) >= 1
        assert c.structured_input["amount"] >= 0

    s_strat = StructuralStrategy()
    s_cases = s_strat.generate_candidates("coin-change", schema, constraints, rng)
    assert len(s_cases) > 0
    for c in s_cases:
        assert "coins" in c.structured_input and "amount" in c.structured_input

    e_strat = NumericExtremesStrategy()
    e_cases = e_strat.generate_candidates("coin-change", schema, constraints, rng)
    assert len(e_cases) > 0
    for c in e_cases:
        assert "coins" in c.structured_input and "amount" in c.structured_input
        # Coins cannot be negative
        assert all(coin >= 1 for coin in c.structured_input["coins"])

    st_strat = StressStrategy()
    st_cases = st_strat.generate_candidates("coin-change", schema, constraints, rng)
    assert len(st_cases) > 0
    for c in st_cases:
        assert "coins" in c.structured_input and "amount" in c.structured_input
        # Must respect max_len = 12
        assert len(c.structured_input["coins"]) <= 12

