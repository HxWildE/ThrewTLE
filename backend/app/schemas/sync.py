import datetime
from typing import Optional
from pydantic import BaseModel


class SyncRequest(BaseModel):
    source: str = "huggingface"
    sample_only: bool = True
    limit: int = 50


class SyncRunResponse(BaseModel):
    id: str
    source: str
    started_at: datetime.datetime
    completed_at: Optional[datetime.datetime] = None
    inserted_count: int
    updated_count: int
    status: str
    error_summary: Optional[str] = None

    class Config:
        from_attributes = True
