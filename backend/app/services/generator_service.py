from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.errors import ProblemNotFoundException
from app.engine.pipeline import GenerationPipeline
from app.engine.strategies.base import CandidateCase
from app.repositories.problem_repo import ProblemRepository
from app.repositories.test_case_repo import TestCaseRepository
from app.schemas.generation import GenerateRequest, GenerateResponse


class GeneratorService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.problem_repo = ProblemRepository(session)
        self.test_case_repo = TestCaseRepository(session)
        self.pipeline = GenerationPipeline()

    async def generate_for_problem(self, slug: str, req: GenerateRequest) -> GenerateResponse:
        problem = await self.problem_repo.get_by_slug(slug)
        if not problem:
            raise ProblemNotFoundException(slug)

        # Convert database example test cases to CandidateCases for Layer A
        curated_cases: List[CandidateCase] = []
        for tc in problem.test_cases:
            exp_out = tc.oracle_result.expected_output if tc.oracle_result else None
            ver_stat = tc.oracle_result.verification_status if tc.oracle_result else "UNVERIFIED"
            comp_m = tc.oracle_result.comparison_mode if tc.oracle_result else "EXACT_MATCH"
            curated_cases.append(CandidateCase(
                category=tc.category,
                structured_input=tc.structured_input,
                explanation=tc.explanation,
                generation_method=tc.generation_method,
                expected_output=exp_out,
                verification_status=ver_stat,
                comparison_mode=comp_m,
                fingerprint=tc.fingerprint
            ))

        # Check and auto-repair input_schema if parameters were mistyped as scalar instead of array
        input_schema = problem.input_schema
        needs_repair = False
        for param in (input_schema or []):
            p_name = param.get("name", "")
            p_type = param.get("type", "")
            if "[]" not in p_type and "array" not in p_type:
                for c in problem.constraints:
                    if f"{p_name}.length" in c or f"{p_name}[i]" in c:
                        needs_repair = True
                        break
        if needs_repair or not input_schema:
            from app.integrations.huggingface.normalizer import HuggingFaceNormalizer
            repaired_schema = HuggingFaceNormalizer.infer_input_schema({}, problem.content or "", problem.constraints)
            if repaired_schema:
                input_schema = repaired_schema
                problem.input_schema = repaired_schema
                await self.session.commit()

        # If problem.test_cases was empty, extract public examples from problem.content
        if not curated_cases and problem.content:
            from app.integrations.huggingface.normalizer import HuggingFaceNormalizer
            from app.engine.validation.oracle import ProblemOracle
            extracted = HuggingFaceNormalizer.extract_example_cases(problem.content)
            for ex in extracted:
                exp_out = ex.get("expected_output")
                ver_stat = "UNVERIFIED"
                comp_m = "EXACT_MATCH"
                if exp_out is not None:
                    oracle_out, oracle_stat, oracle_mode = ProblemOracle.evaluate(problem.slug, ex["structured_input"])
                    if oracle_stat == "VERIFIED":
                        exp_out = oracle_out
                        ver_stat = oracle_stat
                        comp_m = oracle_mode
                    else:
                        ver_stat = "VERIFIED"
                curated_cases.append(CandidateCase(
                    category="basic",
                    structured_input=ex["structured_input"],
                    explanation=ex.get("explanation", "Standard LeetCode example case."),
                    expected_output=exp_out,
                    verification_status=ver_stat,
                    comparison_mode=comp_m
                ))

        result = self.pipeline.run(
            problem_slug=problem.slug,
            input_schema=input_schema,
            constraints=problem.constraints,
            requested_count=req.count,
            requested_categories=req.categories,
            seed=req.seed or 42,
            curated_cases=curated_cases
        )

        # Record generation run in database
        await self.test_case_repo.log_generation_run({
            "problem_id": problem.id,
            "requested_count": req.count,
            "requested_categories": req.categories,
            "seed": req.seed or 42,
            "generated_count": result["returned_count"],
            "deduplicated_count": result["returned_count"],
            "duration_ms": result["duration_ms"],
            "status": "SUCCESS"
        })

        return GenerateResponse(
            problem_slug=problem.slug,
            requested_count=result["requested_count"],
            returned_count=result["returned_count"],
            seed=result["seed"],
            test_cases=result["test_cases"],
            raw_batch_input=result["raw_batch_input"],
            limitations=result["limitations"]
        )
