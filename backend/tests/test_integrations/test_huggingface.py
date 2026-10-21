import pytest
from app.integrations.huggingface.normalizer import HuggingFaceNormalizer


def test_normalizer_extraction():
    desc = """
    Given an array of integers nums.
    Constraints:
    * 1 <= nums.length <= 10^5
    * -10^9 <= nums[i] <= 10^9
    """
    constraints = HuggingFaceNormalizer.extract_constraints(desc)
    assert len(constraints) >= 2
    assert any("length" in c for c in constraints)


def test_normalizer_row_conversion():
    row = {
        "question_id": 1968,
        "task_id": "array-with-elements-not-equal-to-average-of-neighbors",
        "difficulty": "Medium",
        "problem_description": "Rearrange array... Constraints: 3 <= nums.length <= 10^5",
        "metadata": {"canonical_parameter_names": ["nums"]}
    }
    norm = HuggingFaceNormalizer.normalize_row(row)
    assert norm is not None
    assert norm["source_id"] == 1968
    assert norm["slug"] == "array-with-elements-not-equal-to-average-of-neighbors"
    assert norm["difficulty"] == "MEDIUM"
    assert norm["input_schema"] == [{"name": "nums", "type": "integer[]"}]
