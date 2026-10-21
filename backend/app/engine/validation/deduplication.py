import hashlib
import json
from typing import Any, Dict, List, Tuple
from app.engine.strategies.base import CandidateCase


class Deduplicator:
    @staticmethod
    def compute_fingerprint(structured_input: Dict[str, Any]) -> str:
        """Produce deterministic SHA-256 hash of canonically sorted JSON payload."""
        canonical_json = json.dumps(structured_input, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()

    @classmethod
    def filter_unique(cls, candidates: List[CandidateCase]) -> List[CandidateCase]:
        seen_fingerprints = set()
        unique_cases: List[CandidateCase] = []

        for c in candidates:
            fp = c.fingerprint or cls.compute_fingerprint(c.structured_input)
            c.fingerprint = fp
            if fp not in seen_fingerprints:
                seen_fingerprints.add(fp)
                unique_cases.append(c)

        return unique_cases
