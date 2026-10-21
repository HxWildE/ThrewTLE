from app.engine.validation.schema_validator import SchemaValidator


def test_schema_validator_valid():
    validator = SchemaValidator()
    schema = [{"name": "nums", "type": "integer[]"}, {"name": "target", "type": "integer"}]
    constraints = ["2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9", "-10^9 <= target <= 10^9"]

    valid, violations = validator.validate_input(
        {"nums": [2, 7, 11, 15], "target": 9},
        schema,
        constraints
    )
    assert valid is True
    assert len(violations) == 0


def test_schema_validator_violations():
    validator = SchemaValidator()
    schema = [{"name": "nums", "type": "integer[]"}]
    constraints = ["3 <= nums.length <= 10^5", "0 <= nums[i] <= 100"]

    # Violation 1: Length too small (2 < 3)
    valid, violations = validator.validate_input(
        {"nums": [1, 2]},
        schema,
        constraints
    )
    assert valid is False
    assert any("below minimum constraint" in v for v in violations)

    # Violation 2: Value exceeds upper bound (150 > 100)
    valid, violations = validator.validate_input(
        {"nums": [10, 20, 150]},
        schema,
        constraints
    )
    assert valid is False
    assert any("exceeds constraint bounds" in v for v in violations)
