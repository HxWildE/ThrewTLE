import datetime
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.schemas.test_case import TestCaseResponse


class ProblemBase(BaseModel):
    source: str = "leetcode"
    source_id: int
    slug: str
    title: str
    difficulty: str  # EASY, MEDIUM, HARD
    support_status: str = "SUPPORTED"


class ProblemSummary(ProblemBase):
    id: str
    constraints_count: int = 0
    test_cases_count: int = 0

    model_config = {"from_attributes": True}


class ProblemDetail(ProblemBase):
    id: str
    content: str
    constraints: List[str]
    input_schema: List[Dict[str, Any]]
    example_test_cases: List[TestCaseResponse] = Field(default_factory=list)
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = {"from_attributes": True}


class ProblemCreate(BaseModel):
    source: str = "leetcode"
    source_id: int
    slug: str
    title: str
    difficulty: str
    content: str = ""
    constraints: List[str] = Field(default_factory=list)
    input_schema: List[Dict[str, Any]] = Field(default_factory=list)
    support_status: str = "SUPPORTED"
