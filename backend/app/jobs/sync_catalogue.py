import asyncio
import sys
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import app.db.base  # noqa: F401
from app.core.logging import logger
from app.db.session import AsyncSessionLocal
from app.integrations.huggingface.pipeline import IngestionPipeline
from app.repositories.sync_repo import SyncRepository


async def run_catalogue_sync(limit: int = 50, source: str = "huggingface") -> dict:
    logger.info(f"Starting catalogue sync job (source={source}, limit={limit})...")
    async with AsyncSessionLocal() as session:
        sync_repo = SyncRepository(session)
        sync_run = await sync_repo.start_run(source=source)
        await session.commit()

        try:
            pipeline = IngestionPipeline(session)
            inserted, updated = await pipeline.ingest_dataset(limit=limit)

            await sync_repo.finish_run(
                run_id=sync_run.id,
                inserted=inserted,
                updated=updated,
                status="SUCCESS"
            )
            await session.commit()
            logger.info(f"Sync run {sync_run.id} finished successfully: {inserted} inserted, {updated} updated.")
            return {
                "sync_id": str(sync_run.id),
                "status": "SUCCESS",
                "inserted": inserted,
                "updated": updated
            }
        except Exception as e:
            await session.rollback()
            logger.exception(f"Sync run {sync_run.id} failed: {e}")
            await sync_repo.finish_run(
                run_id=sync_run.id,
                inserted=0,
                updated=0,
                status="FAILED",
                error=str(e)
            )
            await session.commit()
            return {
                "sync_id": str(sync_run.id),
                "status": "FAILED",
                "error": str(e)
            }


if __name__ == "__main__":
    result = asyncio.run(run_catalogue_sync())
    print("[Sync Catalogue] Job Result:", result)
