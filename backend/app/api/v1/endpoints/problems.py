from typing import Optional
from fastapi import APIRouter, Depends, Query
from app.api.deps import get_problem_service
from app.schemas.common import PaginatedResponse
from app.schemas.problem import ProblemDetail, ProblemSummary
from app.services.problem_service import ProblemService

router = APIRouter()


@router.get("/problems", response_model=PaginatedResponse[ProblemSummary], summary="Search Indexed Problems")
async def list_problems(
    query: Optional[str] = Query(None, description="Search query matching title, slug, or problem number"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty (EASY, MEDIUM, HARD)"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    service: ProblemService = Depends(get_problem_service)
):
    items, total = await service.search(query=query, difficulty=difficulty, limit=limit, offset=offset)
    return PaginatedResponse(
        items=items,
        total=total,
        offset=offset,
        limit=limit
    )


@router.get("/problems/{slug}", response_model=ProblemDetail, summary="Get Problem Details & Constraints")
async def get_problem(
    slug: str,
    service: ProblemService = Depends(get_problem_service)
):
    return await service.get_by_slug(slug)
