from fastapi import APIRouter, Depends
from app.api.deps import get_generator_service
from app.schemas.generation import GenerateRequest, GenerateResponse
from app.services.generator_service import GeneratorService

router = APIRouter()


@router.post("/problems/{slug}/generate", response_model=GenerateResponse, summary="Generate Problem-Specific Test Cases")
async def generate_test_cases(
    slug: str,
    request: GenerateRequest,
    service: GeneratorService = Depends(get_generator_service)
):
    return await service.generate_for_problem(slug, request)
