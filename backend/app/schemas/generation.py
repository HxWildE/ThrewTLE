import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.test_case import TestCaseResponse


class GenerateRequest(BaseModel):
    count: int = Field(default=20, ge=1, le=20, description="Target number of test cases (1 to 20)")
    categories: List[str] = Field(
        default_factory=lambda: ["basic", "boundary", "structural", "numeric_extremes", "stress"],
        description="Categories of test cases to include"
    )
    seed: Optional[int] = Field(default=42, description="Deterministic seed for generation")


class GenerateResponse(BaseModel):
    problem_slug: str
    requested_count: int
    returned_count: int
    seed: int
    test_cases: List[TestCaseResponse]
    raw_batch_input: str
    limitations: Optional[str] = None


class GenerationRunSummary(BaseModel):
    id: str
    problem_id: str
    requested_count: int
    generated_count: int
    deduplicated_count: int
    duration_ms: float
    status: str
    created_at: datetime.datetime

    model_config = {"from_attributes": True}
