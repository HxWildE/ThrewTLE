import datetime
import uuid
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class TestCaseBase(BaseModel):
    category: str
    raw_input: str
    explanation: str
    generation_method: str = "DETERMINISTIC_STRATEGY"
    validation_status: str = "VALIDATED"


class TestCaseCreate(TestCaseBase):
    structured_input: Dict[str, Any] = Field(default_factory=dict)
    provenance: str = "generator"
    fingerprint: str
    expected_output: Optional[str] = None
    verification_status: str = "UNVERIFIED"
    comparison_mode: str = "EXACT_MATCH"


class TestCaseResponse(BaseModel):
    id: str
    category: str
    raw_input: str
    explanation: str
    generation_method: str
    validation_status: str
    expected_output: Optional[str] = None
    verification_status: str = "UNVERIFIED"
    comparison_mode: Optional[str] = "EXACT_MATCH"

    model_config = {"from_attributes": True}


class TestCaseBatchResponse(BaseModel):
    test_cases: list[TestCaseResponse]
    raw_batch_string: str
