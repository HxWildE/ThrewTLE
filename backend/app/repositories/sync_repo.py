import datetime
import uuid
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sync_run import SyncRun


class SyncRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def start_run(self, source: str = "huggingface") -> SyncRun:
        run = SyncRun(source=source, status="RUNNING")
        self.session.add(run)
        await self.session.flush()
        return run

    async def finish_run(
        self,
        run_id: uuid.UUID,
        inserted: int,
        updated: int,
        status: str = "SUCCESS",
        error: Optional[str] = None
    ) -> SyncRun:
        stmt = select(SyncRun).where(SyncRun.id == run_id)
        res = await self.session.execute(stmt)
        run = res.scalar_one()
        run.completed_at = datetime.datetime.now(datetime.timezone.utc)
        run.inserted_count = inserted
        run.updated_count = updated
        run.status = status
        run.error_summary = error
        await self.session.flush()
        return run
