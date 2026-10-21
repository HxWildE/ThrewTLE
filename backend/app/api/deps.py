from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db_session
from app.services.generator_service import GeneratorService
from app.services.problem_service import ProblemService


def get_problem_service(session: AsyncSession = Depends(get_db_session)) -> ProblemService:
    return ProblemService(session)


def get_generator_service(session: AsyncSession = Depends(get_db_session)) -> GeneratorService:
    return GeneratorService(session)
