import random
from typing import Optional
from app.engine.generators.base import BaseGenerator, StringType


class StringGenerator(BaseGenerator):
    def generate(self, spec: StringType, rng: random.Random) -> str:
        length = rng.randint(spec.min_len, min(spec.max_len, 50))
        return "".join(rng.choice(spec.charset) for _ in range(length))

    def generate_empty_or_minimal(self, spec: StringType) -> str:
        if spec.min_len == 0:
            return ""
        return "a" * spec.min_len

    def generate_single_char(self, spec: StringType, char: str = "a") -> str:
        size = max(1, spec.min_len)
        return char * size

    def generate_repeated_char(self, spec: StringType, size: int, char: str = "a") -> str:
        s = max(spec.min_len, min(spec.max_len, size))
        return char * s

    def generate_palindrome(self, spec: StringType, half_size: int = 5, rng: Optional[random.Random] = None) -> str:
        r = rng or random.Random(42)
        half = [r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(half_size)]
        pal = "".join(half) + "".join(reversed(half))
        if len(pal) < spec.min_len:
            pal = pal + ("a" * (spec.min_len - len(pal)))
        return pal[:spec.max_len]

    def generate_non_alphanumeric_mix(self, spec: StringType) -> str:
        """Great for problems like LeetCode 125 (Valid Palindrome) where punctuation must be handled."""
        return "A man, a plan, a canal: Panama!"

    def generate_stress(self, spec: StringType, size: int = 1000, rng: Optional[random.Random] = None) -> str:
        s = max(spec.min_len, min(spec.max_len, size))
        r = rng or random.Random(42)
        return "".join(r.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(s))
