from typing import Any, Dict, Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.logging import logger


class ThrewTLEException(Exception):
    def __init__(self, message: str, code: str = "INTERNAL_ERROR", details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)


class ProblemNotFoundException(ThrewTLEException):
    def __init__(self, identifier: str):
        super().__init__(
            message=f"Problem '{identifier}' was not found in the indexed catalogue.",
            code="PROBLEM_NOT_FOUND",
            details={"identifier": identifier}
        )


class UnsupportedProblemFormatException(ThrewTLEException):
    def __init__(self, slug: str, reason: str, schema_type: str):
        super().__init__(
            message=f"Problem '{slug}' requires format '{schema_type}' which is currently unsupported for deterministic synthesis: {reason}",
            code="UNSUPPORTED_FORMAT",
            details={"slug": slug, "reason": reason, "schema_type": schema_type}
        )


class ConstraintValidationException(ThrewTLEException):
    def __init__(self, message: str, violations: list[str]):
        super().__init__(
            message=message,
            code="CONSTRAINT_VIOLATION",
            details={"violations": violations}
        )


class DatabaseUnavailableException(ThrewTLEException):
    def __init__(self, message: str = "Database connection unavailable"):
        super().__init__(
            message=message,
            code="DATABASE_UNAVAILABLE"
        )


async def threwtle_exception_handler(request: Request, exc: ThrewTLEException) -> JSONResponse:
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    if isinstance(exc, ProblemNotFoundException):
        status_code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, (UnsupportedProblemFormatException, ConstraintValidationException)):
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    elif isinstance(exc, DatabaseUnavailableException):
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    logger.warning(f"Handled ThrewTLEException [{exc.code}] at {request.url.path}: {exc.message}")
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(f"Unhandled system exception at {request.url.path}: {exc}")
    # Never expose stack traces or raw database details to client in production
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected server error occurred. Please try again later.",
                "details": {}
            }
        }
    )
