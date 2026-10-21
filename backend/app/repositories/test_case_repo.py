import uuid
from typing import Any, Dict, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.generation_run import GenerationRun
from app.models.oracle_result import OracleResult
from app.models.test_case import TestCase


class TestCaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_problem_id(self, problem_id: uuid.UUID) -> List[TestCase]:
        stmt = (
            select(TestCase)
            .where(TestCase.problem_id == problem_id)
            .order_by(TestCase.created_at.desc())
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def save_test_case(self, data: dict, oracle_data: dict = None) -> TestCase:
        test_case = TestCase(**data)
        self.session.add(test_case)
        await self.session.flush()

        if oracle_data:
            oracle = OracleResult(test_case_id=test_case.id, **oracle_data)
            self.session.add(oracle)
            await self.session.flush()

        return test_case

    async def log_generation_run(self, data: dict) -> GenerationRun:
        run = GenerationRun(**data)
        self.session.add(run)
        await self.session.flush()
        return run
