from enum import Enum
from typing import Generic, List, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class DifficultyEnum(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class SupportStatusEnum(str, Enum):
    SUPPORTED = "SUPPORTED"
    PARTIAL = "PARTIAL"
    UNSUPPORTED_FORMAT = "UNSUPPORTED_FORMAT"


class CategoryEnum(str, Enum):
    BASIC = "basic"
    BOUNDARY = "boundary"
    STRUCTURAL = "structural"
    NUMERIC_EXTREMES = "numeric_extremes"
    STRESS = "stress"


class GenerationMethodEnum(str, Enum):
    DATASET_CURATED = "DATASET_CURATED"
    DETERMINISTIC_STRATEGY = "DETERMINISTIC_STRATEGY"
    STRUCTURED_RANDOM = "STRUCTURED_RANDOM"
    AI_ASSISTED = "AI_ASSISTED"


class ValidationStatusEnum(str, Enum):
    VALIDATED = "VALIDATED"
    REJECTED = "REJECTED"
    UNCHECKED = "UNCHECKED"


class ComparisonModeEnum(str, Enum):
    EXACT_MATCH = "EXACT_MATCH"
    UNORDERED_ARRAY = "UNORDERED_ARRAY"
    ANY_VALID_PERMUTATION = "ANY_VALID_PERMUTATION"
    NONE = "NONE"


class VerificationStatusEnum(str, Enum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class GenerationStatusEnum(str, Enum):
    SUCCESS = "SUCCESS"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"


class SyncStatusEnum(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    offset: int
    limit: int
