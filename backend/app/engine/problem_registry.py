from typing import Any, Dict, List, Optional, Tuple
from app.core.errors import UnsupportedProblemFormatException
from app.engine.strategies.base import CandidateCase


class ProblemRegistry:
    UNSUPPORTED_TYPES = {"treenode", "listnode", "nestedinteger", "graphnode", "custom_binary_tree"}

    @classmethod
    def check_support(cls, slug: str, input_schema: List[Dict[str, Any]]) -> Tuple[str, Optional[str]]:
        """
        Returns (support_status, reason_if_unsupported)
        support_status in ["SUPPORTED", "PARTIAL", "UNSUPPORTED_FORMAT"]
        """
        for param in input_schema:
            p_type = param.get("type", "").lower()
            for unsupp in cls.UNSUPPORTED_TYPES:
                if unsupp in p_type:
                    reason = f"Tree and linked list pointer serializations ({p_type}) require customized deserializer stubs not yet supported in MVP."
                    return "UNSUPPORTED_FORMAT", reason

        # Known first-class supported problems
        benchmark_slugs = {
            "two-sum",
            "array-with-elements-not-equal-to-average-of-neighbors",
            "valid-palindrome",
            "maximum-subarray",
            "coin-change"
        }
        if any(b in slug.lower() for b in benchmark_slugs):
            return "SUPPORTED", None

        # Generic schema support (flat arrays, primitives, strings)
        return "PARTIAL", None

    @classmethod
    def generate_problem_specific(
        cls,
        slug: str,
        input_schema: List[Dict[str, Any]],
        constraints: List[str]
    ) -> List[CandidateCase]:
        """
        Layer C: High-fidelity problem-specific adversarial cases.
        """
        slug_clean = slug.lower()
        cases: List[CandidateCase] = []

        if "two-sum" in slug_clean:
            # Adversarial Case: Duplicate numbers that sum to target
            cases.append(CandidateCase(
                category="boundary",
                structured_input={"nums": [3, 3], "target": 6},
                explanation="Adversarial: Target formed by duplicate numbers at minimal valid array length (2).",
                expected_output="[0,1]",
                verification_status="VERIFIED"
            ))
            # Adversarial Case: Target at extreme opposite ends
            cases.append(CandidateCase(
                category="structural",
                structured_input={"nums": [1, 5, 8, 12, 19, 4], "target": 5},
                explanation="Adversarial: Valid pair elements positioned at extreme first and last indices [0, 5].",
                expected_output="[0,5]",
                verification_status="VERIFIED"
            ))
            # Adversarial Case: Negative target and negative elements
            cases.append(CandidateCase(
                category="numeric_extremes",
                structured_input={"nums": [-10, -1, -18, -19], "target": -19},
                explanation="Adversarial: All negative operands summing to negative target.",
                expected_output="[1,2]",
                verification_status="VERIFIED"
            ))
            # Adversarial Case: Target with zero
            cases.append(CandidateCase(
                category="numeric_extremes",
                structured_input={"nums": [0, 4, 3, 0], "target": 0},
                explanation="Adversarial: Target sum of zero composed of dual zero elements.",
                expected_output="[0,3]",
                verification_status="VERIFIED"
            ))

        elif "1968" in slug_clean or "not-equal-to-average" in slug_clean:
            # Adversarial: 3 elements already in exact arithmetic progression (1, 2, 3) where (1+3)/2 = 2
            cases.append(CandidateCase(
                category="structural",
                structured_input={"nums": [1, 2, 3]},
                explanation="Adversarial: Strict arithmetic progression of length 3 where middle element is exact average of neighbors.",
                expected_output=None,
                verification_status="UNVERIFIED",
                comparison_mode="ANY_VALID_PERMUTATION"
            ))
            # Adversarial: 5 elements in arithmetic progression
            cases.append(CandidateCase(
                category="structural",
                structured_input={"nums": [2, 4, 6, 8, 10]},
                explanation="Adversarial: Strict even arithmetic progression (step 2) across 5 elements.",
                expected_output=None,
                verification_status="UNVERIFIED",
                comparison_mode="ANY_VALID_PERMUTATION"
            ))
            # Adversarial: Reverse arithmetic progression
            cases.append(CandidateCase(
                category="structural",
                structured_input={"nums": [9, 6, 3]},
                explanation="Adversarial: Reverse monotonic arithmetic progression.",
                expected_output=None,
                verification_status="UNVERIFIED",
                comparison_mode="ANY_VALID_PERMUTATION"
            ))
            # Adversarial: Numbers with huge gap
            cases.append(CandidateCase(
                category="numeric_extremes",
                structured_input={"nums": [0, 1000000000, 500000000]},
                explanation="Adversarial: High magnitude elements testing integer average calculation overflow.",
                expected_output=None,
                verification_status="UNVERIFIED",
                comparison_mode="ANY_VALID_PERMUTATION"
            ))

        elif "valid-palindrome" in slug_clean or "palindrome" in slug_clean:
            cases.append(CandidateCase(
                category="basic",
                structured_input={"s": "A man, a plan, a canal: Panama"},
                explanation="Sanity: Classic palindrome with mixed case, spaces, and punctuation.",
                expected_output="true",
                verification_status="VERIFIED"
            ))
            cases.append(CandidateCase(
                category="boundary",
                structured_input={"s": " "},
                explanation="Boundary: String containing only non-alphanumeric whitespace (becomes empty string after filter).",
                expected_output="true",
                verification_status="VERIFIED"
            ))
            cases.append(CandidateCase(
                category="boundary",
                structured_input={"s": ".,"},
                explanation="Boundary: String containing only punctuation symbols.",
                expected_output="true",
                verification_status="VERIFIED"
            ))
            cases.append(CandidateCase(
                category="structural",
                structured_input={"s": "0P"},
                explanation="Adversarial: Two alphanumeric characters that are not equal.",
                expected_output="false",
                verification_status="VERIFIED"
            ))

        elif "maximum-subarray" in slug_clean:
            cases.append(CandidateCase(
                category="numeric_extremes",
                structured_input={"nums": [-1]},
                explanation="Boundary: Single negative element array.",
                expected_output="-1",
                verification_status="VERIFIED"
            ))
            cases.append(CandidateCase(
                category="numeric_extremes",
                structured_input={"nums": [-2, -3, -1, -5]},
                explanation="Numeric extremes: All negative elements; maximum subarray is the single least-negative element (-1).",
                expected_output="-1",
                verification_status="VERIFIED"
            ))
            cases.append(CandidateCase(
                category="structural",
                structured_input={"nums": [5, 4, -1, 7, 8]},
                explanation="Structural: Subarray with only a minor negative dip where total sum is positive.",
                expected_output="23",
                verification_status="VERIFIED"
            ))

        elif "coin-change" in slug_clean:
            # 1. Greedy Trap: Greedy picks 4+1+1 (3 coins), optimal is 3+3 (2 coins)
            cases.append(CandidateCase(
                category="structural",
                structured_input={"coins": [1, 3, 4], "amount": 6},
                explanation="Adversarial greedy trap: Greedy heuristic selects denomination 4 then 1+1 (3 coins), optimal DP is 3+3 (2 coins).",
                expected_output="2",
                verification_status="VERIFIED"
            ))
            # 2. Greedy Trap 2: Greedy picks 9+1+1 (3 coins), optimal is 5+6 (2 coins)
            cases.append(CandidateCase(
                category="structural",
                structured_input={"coins": [1, 5, 6, 9], "amount": 11},
                explanation="Adversarial greedy trap: Greedy algorithm chooses 9+1+1 (3 coins), optimal combination is 5+6 (2 coins).",
                expected_output="2",
                verification_status="VERIFIED"
            ))
            # 3. Impossible Change
            cases.append(CandidateCase(
                category="boundary",
                structured_input={"coins": [2], "amount": 3},
                explanation="Boundary: Target amount cannot be formed by any combination of denominations (returns -1).",
                expected_output="-1",
                verification_status="VERIFIED"
            ))
            # 4. Zero Amount
            cases.append(CandidateCase(
                category="boundary",
                structured_input={"coins": [1], "amount": 0},
                explanation="Boundary: Target amount of zero requires zero coins.",
                expected_output="0",
                verification_status="VERIFIED"
            ))
            # 5. Target strictly smaller than all coins
            cases.append(CandidateCase(
                category="boundary",
                structured_input={"coins": [5, 10, 25], "amount": 3},
                explanation="Boundary: Target amount is strictly less than the smallest available denomination.",
                expected_output="-1",
                verification_status="VERIFIED"
            ))
            # 6. Parity trap (even denominations with odd target)
            cases.append(CandidateCase(
                category="structural",
                structured_input={"coins": [2, 4, 6], "amount": 7},
                explanation="Adversarial parity trap: All available coin denominations are even, target amount is odd (mathematically impossible).",
                expected_output="-1",
                verification_status="VERIFIED"
            ))
            # 7. Exact single coin match
            cases.append(CandidateCase(
                category="basic",
                structured_input={"coins": [1, 2, 5], "amount": 5},
                explanation="Sanity baseline: Target amount matches an existing denomination exactly.",
                expected_output="1",
                verification_status="VERIFIED"
            ))
            # 8. Maximum constraint stress
            cases.append(CandidateCase(
                category="stress",
                structured_input={"coins": [1, 2, 5], "amount": 10000},
                explanation="Stress case: Maximum allowed amount (10^4) testing dynamic programming memory sizing and performance.",
                expected_output="2000",
                verification_status="VERIFIED"
            ))

        return cases
