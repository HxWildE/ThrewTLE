from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.errors import ProblemNotFoundException
from app.models.problem import Problem
from app.repositories.problem_repo import ProblemRepository
from app.schemas.problem import ProblemDetail, ProblemSummary
from app.schemas.test_case import TestCaseResponse


class ProblemService:
    def __init__(self, session: AsyncSession):
        self.repo = ProblemRepository(session)

    async def get_by_slug(self, slug: str) -> ProblemDetail:
        problem = await self.repo.get_by_slug(slug)
        if not problem:
            raise ProblemNotFoundException(slug)

        example_cases = []
        for tc in problem.test_cases:
            exp_out = tc.oracle_result.expected_output if tc.oracle_result else None
            ver_status = tc.oracle_result.verification_status if tc.oracle_result else "UNVERIFIED"
            comp_mode = tc.oracle_result.comparison_mode if tc.oracle_result else "EXACT_MATCH"

            example_cases.append(TestCaseResponse(
                id=str(tc.id),
                category=tc.category,
                raw_input=tc.raw_input,
                explanation=tc.explanation,
                generation_method=tc.generation_method,
                validation_status=tc.validation_status,
                expected_output=exp_out,
                verification_status=ver_status,
                comparison_mode=comp_mode
            ))

        return ProblemDetail(
            id=str(problem.id),
            source=problem.source,
            source_id=problem.source_id,
            slug=problem.slug,
            title=problem.title,
            difficulty=problem.difficulty,
            content=problem.content,
            constraints=problem.constraints,
            input_schema=problem.input_schema,
            support_status=problem.support_status,
            example_test_cases=example_cases,
            created_at=problem.created_at,
            updated_at=problem.updated_at
        )

    async def search(
        self,
        query: Optional[str] = None,
        difficulty: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Tuple[List[ProblemSummary], int]:
        problems, total = await self.repo.search(query=query, difficulty=difficulty, limit=limit, offset=offset)
        summaries = [
            ProblemSummary(
                id=str(p.id),
                source=p.source,
                source_id=p.source_id,
                slug=p.slug,
                title=p.title,
                difficulty=p.difficulty,
                support_status=p.support_status,
                constraints_count=len(p.constraints),
                test_cases_count=len(p.test_cases)
            )
            for p in problems
        ]
        return summaries, total
