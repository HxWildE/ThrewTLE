from typing import List, Optional, Tuple
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.problem import Problem
from app.models.test_case import TestCase


class ProblemRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_slug(self, slug: str) -> Optional[Problem]:
        # If slug is digits, check source_id as fallback
        if slug.strip().isdigit():
            prob = await self.get_by_source_id(int(slug.strip()))
            if prob:
                return prob

        stmt = (
            select(Problem)
            .options(selectinload(Problem.test_cases).selectinload(TestCase.oracle_result))
            .where(func.lower(Problem.slug) == slug.lower())
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_by_source_id(self, source_id: int) -> Optional[Problem]:
        stmt = (
            select(Problem)
            .options(selectinload(Problem.test_cases).selectinload(TestCase.oracle_result))
            .where(Problem.source_id == source_id)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def search(
        self,
        query: Optional[str] = None,
        difficulty: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> Tuple[List[Problem], int]:
        from sqlalchemy import String, cast
        filters = []
        if difficulty:
            filters.append(func.upper(Problem.difficulty) == difficulty.upper())

        if query:
            q = f"%{query.strip().lower()}%"
            # Support search by title, slug, or number (exact and partial substring)
            if query.strip().isdigit():
                num_q = f"%{query.strip()}%"
                filters.append(
                    or_(
                        Problem.source_id == int(query.strip()),
                        cast(Problem.source_id, String).like(num_q),
                        func.lower(Problem.title).like(q),
                        func.lower(Problem.slug).like(q)
                    )
                )
            else:
                filters.append(
                    or_(
                        func.lower(Problem.title).like(q),
                        func.lower(Problem.slug).like(q)
                    )
                )

        count_stmt = select(func.count(Problem.id))
        if filters:
            count_stmt = count_stmt.where(*filters)
        total_res = await self.session.execute(count_stmt)
        total = total_res.scalar_one()

        from sqlalchemy import case, cast, String
        
        # Smart relevance ordering:
        # If query is digits, prioritize exact ID match (0), then prefix ID matches (1), then rest
        order_clauses = []
        if query and query.strip().isdigit():
            target_int = int(query.strip())
            prefix_pattern = f"{query.strip()}%"
            order_clauses.append(
                case(
                    (Problem.source_id == target_int, 0),
                    (cast(Problem.source_id, String).like(prefix_pattern), 1),
                    else_=2
                )
            )
        elif query:
            clean_q = query.strip().lower()
            order_clauses.append(
                case(
                    (func.lower(Problem.title) == clean_q, 0),
                    (func.lower(Problem.slug) == clean_q, 1),
                    (func.lower(Problem.title).like(f"{clean_q}%"), 2),
                    else_=3
                )
            )
        order_clauses.append(Problem.source_id.asc())

        stmt = (
            select(Problem)
            .options(selectinload(Problem.test_cases))
            .order_by(*order_clauses)
            .limit(limit)
            .offset(offset)
        )
        if filters:
            stmt = stmt.where(*filters)

        res = await self.session.execute(stmt)
        problems = list(res.scalars().all())
        return problems, total

    async def upsert(self, data: dict) -> Problem:
        existing = await self.get_by_slug(data["slug"])
        if existing:
            for k, v in data.items():
                if k not in ["id", "created_at"]:
                    setattr(existing, k, v)
            await self.session.flush()
            return existing
        else:
            problem = Problem(**data)
            self.session.add(problem)
            await self.session.flush()
            return problem
