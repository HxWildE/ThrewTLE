import random
import time
from typing import Any, Dict, List, Optional
from app.core.errors import UnsupportedProblemFormatException
from app.engine.formatters.leetcode_raw import LeetCodeRawFormatter
from app.engine.problem_registry import ProblemRegistry
from app.engine.strategies.base import CandidateCase
from app.engine.strategies.boundary import BoundaryStrategy
from app.engine.strategies.extremes import NumericExtremesStrategy
from app.engine.strategies.stress import StressStrategy
from app.engine.strategies.structural import StructuralStrategy
from app.engine.validation.deduplication import Deduplicator
from app.engine.validation.oracle import ProblemOracle
from app.engine.validation.schema_validator import SchemaValidator
from app.schemas.test_case import TestCaseResponse


class GenerationPipeline:
    def __init__(self):
        self.boundary_strat = BoundaryStrategy()
        self.structural_strat = StructuralStrategy()
        self.extremes_strat = NumericExtremesStrategy()
        self.stress_strat = StressStrategy()
        self.validator = SchemaValidator()
        self.formatter = LeetCodeRawFormatter()

    def run(
        self,
        problem_slug: str,
        input_schema: List[Dict[str, Any]],
        constraints: List[str],
        requested_count: int = 20,
        requested_categories: Optional[List[str]] = None,
        seed: int = 42,
        curated_cases: Optional[List[CandidateCase]] = None
    ) -> Dict[str, Any]:
        start_time = time.perf_counter()
        rng = random.Random(seed)

        if not requested_categories:
            requested_categories = ["basic", "boundary", "structural", "numeric_extremes", "stress"]

        # Check format compatibility
        support_status, reason = ProblemRegistry.check_support(problem_slug, input_schema)
        if support_status == "UNSUPPORTED_FORMAT":
            raise UnsupportedProblemFormatException(
                slug=problem_slug,
                reason=reason or "Unsupported parameter schema",
                schema_type=str(input_schema)
            )

        raw_candidates: List[CandidateCase] = []

        # Layer A: Curated Public Cases
        if curated_cases:
            for c in curated_cases:
                if c.category in requested_categories:
                    raw_candidates.append(c)

        # Layer C: Problem-Specific High-Fidelity Cases
        spec_cases = ProblemRegistry.generate_problem_specific(problem_slug, input_schema, constraints)
        for sc in spec_cases:
            if sc.category in requested_categories:
                raw_candidates.append(sc)

        # Layer B: Deterministic Strategies
        if "boundary" in requested_categories:
            raw_candidates.extend(self.boundary_strat.generate_candidates(problem_slug, input_schema, constraints, rng))

        if "structural" in requested_categories:
            raw_candidates.extend(self.structural_strat.generate_candidates(problem_slug, input_schema, constraints, rng))

        if "numeric_extremes" in requested_categories:
            raw_candidates.extend(self.extremes_strat.generate_candidates(problem_slug, input_schema, constraints, rng))

        if "stress" in requested_categories:
            raw_candidates.extend(self.stress_strat.generate_candidates(problem_slug, input_schema, constraints, rng))

        # Layer D: Hypothesis-inspired bounded randoms to fill diversity
        first_param = input_schema[0] if input_schema else {}
        p_name = first_param.get("name", "nums")
        p_type = first_param.get("type", "integer[]")
        param_bounds = self.validator.parse_param_constraints(constraints, input_schema)
        b = param_bounds.get(p_name, {"min_len": 1, "max_len": 1000, "min_val": -100, "max_val": 100})
        min_len, max_len = b.get("min_len", 1), b.get("max_len", 1000)
        min_val, max_val = b.get("min_val", -100), b.get("max_val", 100)

        for _ in range(10):
            struct = {}
            if "[]" in p_type or "array" in p_type:
                rand_size = rng.randint(min_len, min(max_len, 8))
                low = max(min_val, 1) if min_val > 0 else max(-50, min_val)
                high = min(max_val, 50)
                if high < low:
                    high = low
                rand_arr = [rng.randint(low, high) for _ in range(max(1, rand_size))]
                struct[p_name] = rand_arr
            elif "string" in p_type:
                slen = rng.randint(min_len, min(max_len, 10))
                struct[p_name] = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(max(1, slen)))
            else:
                struct[p_name] = rng.randint(max(min_val, -50), min(max_val, 50))

            full_struct = self.boundary_strat.populate_parameters(struct, input_schema, constraints, rng, variant_hint="default")
            raw_candidates.append(CandidateCase(
                category="basic",
                structured_input=full_struct,
                explanation="Sanity baseline: Randomized bounded input."
            ))

        # Layer F: Validation
        valid_candidates: List[CandidateCase] = []
        for cand in raw_candidates:
            is_valid, _ = self.validator.validate_input(cand.structured_input, input_schema, constraints)
            if is_valid:
                valid_candidates.append(cand)

        # Layer F: Deduplication
        unique_candidates = Deduplicator.filter_unique(valid_candidates)

        # Layer F: Diversity Ranking across requested categories
        by_category: Dict[str, List[CandidateCase]] = {cat: [] for cat in requested_categories}
        for cand in unique_candidates:
            if cand.category in by_category:
                by_category[cand.category].append(cand)

        selected_cases: List[CandidateCase] = []
        # Round-robin selection across categories to ensure balanced diversity
        cat_keys = [cat for cat in requested_categories if by_category[cat]]
        while len(selected_cases) < requested_count and cat_keys:
            remaining_keys = []
            for cat in cat_keys:
                if by_category[cat] and len(selected_cases) < requested_count:
                    selected_cases.append(by_category[cat].pop(0))
                    if by_category[cat]:
                        remaining_keys.append(cat)
            cat_keys = remaining_keys

        # Format and finalize
        final_test_cases: List[TestCaseResponse] = []
        raw_inputs_for_batch: List[str] = []

        for idx, case in enumerate(selected_cases):
            raw_inp = self.formatter.format_input(case.structured_input, input_schema)
            raw_inputs_for_batch.append(raw_inp)

            # Evaluate Oracle if not already verified
            exp_out, ver_status, comp_mode = case.expected_output, case.verification_status, case.comparison_mode
            if ver_status == "UNVERIFIED" or exp_out is None:
                exp_out, ver_status, comp_mode = ProblemOracle.evaluate(problem_slug, case.structured_input)

            final_test_cases.append(TestCaseResponse(
                id=case.fingerprint[:12] if case.fingerprint else f"tc_{idx+1}",
                category=case.category,
                raw_input=raw_inp,
                explanation=case.explanation,
                generation_method=case.generation_method,
                validation_status="VALIDATED",
                expected_output=exp_out,
                verification_status=ver_status,
                comparison_mode=comp_mode
            ))

        raw_batch_str = self.formatter.format_batch(raw_inputs_for_batch)
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

        limitations_msg = None
        if len(final_test_cases) < requested_count:
            limitations_msg = f"Generated {len(final_test_cases)} strictly distinct verified cases respecting problem constraints."

        return {
            "problem_slug": problem_slug,
            "requested_count": requested_count,
            "returned_count": len(final_test_cases),
            "seed": seed,
            "duration_ms": duration_ms,
            "test_cases": final_test_cases,
            "raw_batch_input": raw_batch_str,
            "limitations": limitations_msg
        }
