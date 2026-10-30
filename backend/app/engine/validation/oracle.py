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

        # Problem 322: Coin Change
        elif "coin-change" in slug:
            coins = structured_input.get("coins", [])
            amount = structured_input.get("amount", 0)
            if amount == 0:
                return "0", "VERIFIED", "EXACT_MATCH"
            if amount < 0 or not coins:
                return "-1", "VERIFIED", "EXACT_MATCH"
            valid_coins = sorted(set(c for c in coins if isinstance(c, int) and c > 0))
            if not valid_coins:
                return "-1", "VERIFIED", "EXACT_MATCH"
            # Fast DP for coin change
            dp = [float('inf')] * (amount + 1)
            dp[0] = 0
            for c in valid_coins:
                if c > amount:
                    continue
                for i in range(c, amount + 1):
                    if dp[i - c] + 1 < dp[i]:
                        dp[i] = dp[i - c] + 1
            ans = dp[amount] if dp[amount] != float('inf') else -1
            return str(ans), "VERIFIED", "EXACT_MATCH"

        # Default fallback for arbitrary uncatalogued problems
        return None, "UNVERIFIED", "NONE"
