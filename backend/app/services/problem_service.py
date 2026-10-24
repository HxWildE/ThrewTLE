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

        # On-demand sync with LeetCode GraphQL if content is basic or constraints empty
        if not problem.constraints or len(problem.constraints) == 0:
            try:
                import re
                from app.integrations.leetcode.client import LeetCodeClient
                client = LeetCodeClient(timeout_sec=4.0)
                lc_data = await client.fetch_question_metadata(problem.slug)
                if lc_data:
                    raw_content = lc_data.get("content") or ""
                    constraints = []
                    if "Constraints:" in raw_content:
                        parts = raw_content.split("Constraints:")
                        if len(parts) > 1:
                            matches = re.findall(r"<li>(.*?)</li>", parts[1], re.DOTALL)
                            constraints = [re.sub(r"<[^>]*>", "", m).strip() for m in matches if m.strip()]
                    
                    if not constraints and raw_content:
                        matches = re.findall(r"<li>(.*?)</li>", raw_content, re.DOTALL)
                        constraints = [re.sub(r"<[^>]*>", "", m).strip() for m in matches if m.strip()][:5]
                    
                    update_data = {
                        "slug": problem.slug,
                        "content": raw_content or problem.content,
                        "constraints": constraints or problem.constraints,
                    }
                    await self.repo.upsert(update_data)
                    await self.repo.session.commit()
                    # Reload problem with new content
                    problem = await self.repo.get_by_slug(slug)
            except Exception:
                pass

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
