from app.engine.strategies.base import CandidateCase
from app.engine.validation.deduplication import Deduplicator


def test_fingerprint_deterministic():
    d1 = {"nums": [1, 2, 3], "target": 5}
    d2 = {"target": 5, "nums": [1, 2, 3]}  # Same values, different key order
    fp1 = Deduplicator.compute_fingerprint(d1)
    fp2 = Deduplicator.compute_fingerprint(d2)
    assert fp1 == fp2
    assert len(fp1) == 64  # SHA-256


def test_filter_unique():
    c1 = CandidateCase(category="basic", structured_input={"nums": [1, 2]}, explanation="one")
    c2 = CandidateCase(category="boundary", structured_input={"nums": [1, 2]}, explanation="duplicate input")
    c3 = CandidateCase(category="basic", structured_input={"nums": [3, 4]}, explanation="different")

    unique = Deduplicator.filter_unique([c1, c2, c3])
    assert len(unique) == 2
    assert unique[0].structured_input == {"nums": [1, 2]}
    assert unique[1].structured_input == {"nums": [3, 4]}
