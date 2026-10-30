from app.engine.validation.oracle import ProblemOracle


def test_oracle_two_sum():
    out, status, comp = ProblemOracle.evaluate("two-sum", {"nums": [2, 7, 11, 15], "target": 9})
    assert status == "VERIFIED"
    assert out == "[0,1]"
    assert comp == "EXACT_MATCH"


def test_oracle_valid_palindrome():
    out, status, comp = ProblemOracle.evaluate("valid-palindrome", {"s": "racecar"})
    assert status == "VERIFIED"
    assert out == "true"

    out_neg, _, _ = ProblemOracle.evaluate("valid-palindrome", {"s": "hello"})
    assert out_neg == "false"


def test_oracle_maximum_subarray():
    out, status, comp = ProblemOracle.evaluate("maximum-subarray", {"nums": [-2, 1, -3, 4, -1, 2, 1, -5, 4]})
    assert status == "VERIFIED"
    assert out == "6"


def test_oracle_unverified_special_judge():
    out, status, comp = ProblemOracle.evaluate("array-with-elements-not-equal-to-average-of-neighbors", {"nums": [1, 2, 3]})
    assert status == "UNVERIFIED"
    assert out is None
    assert comp == "ANY_VALID_PERMUTATION"


def test_oracle_coin_change():
    # Greedy trap: greedy gives 4+1+1 (3 coins), optimal is 3+3 (2 coins)
    out, status, comp = ProblemOracle.evaluate("coin-change", {"coins": [1, 3, 4], "amount": 6})
    assert status == "VERIFIED"
    assert out == "2"
    assert comp == "EXACT_MATCH"

    # Impossible change
    out, status, comp = ProblemOracle.evaluate("coin-change", {"coins": [2], "amount": 3})
    assert status == "VERIFIED"
    assert out == "-1"

    # Zero amount
    out, status, comp = ProblemOracle.evaluate("coin-change", {"coins": [1], "amount": 0})
    assert status == "VERIFIED"
    assert out == "0"

