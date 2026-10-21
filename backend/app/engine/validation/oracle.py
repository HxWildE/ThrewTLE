import json
import re
from typing import Any, Dict, Optional, Tuple


class ProblemOracle:
    @staticmethod
    def evaluate(problem_slug: str, structured_input: Dict[str, Any]) -> Tuple[Optional[str], str, str]:
        """
        Returns: (expected_output, verification_status, comparison_mode)
        Honest Verification Labeling: Never fabricate outputs.
        """
        slug = problem_slug.lower()

        # Problem 1: Two Sum
        if "two-sum" in slug:
            nums = structured_input.get("nums", [])
            target = structured_input.get("target", 0)
            seen = {}
            for i, num in enumerate(nums):
                diff = target - num
                if diff in seen:
                    return json.dumps([seen[diff], i], separators=(',', ':')), "VERIFIED", "EXACT_MATCH"
                seen[num] = i
            # If no pair sums to target
            return json.dumps([], separators=(',', ':')), "VERIFIED", "EXACT_MATCH"

        # Problem 125: Valid Palindrome
        elif "valid-palindrome" in slug or "palindrome" in slug:
            s = structured_input.get("s", "")
            cleaned = "".join(ch.lower() for ch in s if ch.isalnum())
            is_pal = (cleaned == cleaned[::-1])
            return "true" if is_pal else "false", "VERIFIED", "EXACT_MATCH"

        # Problem 53: Maximum Subarray
        elif "maximum-subarray" in slug:
            nums = structured_input.get("nums", [])
            if not nums:
                return "0", "VERIFIED", "EXACT_MATCH"
            max_so_far = nums[0]
            curr_max = nums[0]
            for x in nums[1:]:
                curr_max = max(x, curr_max + x)
                max_so_far = max(max_so_far, curr_max)
            return str(max_so_far), "VERIFIED", "EXACT_MATCH"

        # Problem 1968: Array With Elements Not Equal to Average of Neighbors
        # Problem allows ANY valid rearrangement; simple equality check is invalid.
        elif "1968" in slug or "not-equal-to-average" in slug:
            return None, "UNVERIFIED", "ANY_VALID_PERMUTATION"

        # Default fallback for arbitrary uncatalogued problems
        return None, "UNVERIFIED", "NONE"
