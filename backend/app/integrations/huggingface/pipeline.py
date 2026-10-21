from typing import Dict, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logging import logger
from app.integrations.huggingface.client import HuggingFaceClient
from app.integrations.huggingface.normalizer import HuggingFaceNormalizer
from app.repositories.problem_repo import ProblemRepository


class IngestionPipeline:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.client = HuggingFaceClient()
        self.normalizer = HuggingFaceNormalizer()
        self.repo = ProblemRepository(session)

    async def ingest_dataset(self, limit: int = 50, offset: int = 0) -> Tuple[int, int]:
        raw_rows = await self.client.fetch_sample_rows(limit=limit, offset=offset)
        inserted = 0
        updated = 0

        for row in raw_rows:
            norm = self.normalizer.normalize_row(row)
            if not norm:
                continue

            test_cases = norm.pop("test_cases", None)
            existing = await self.repo.get_by_slug(norm["slug"])
            if existing:
                # Update without overwriting existing test cases
                await self.repo.upsert(norm)
                updated += 1
            else:
                await self.repo.upsert(norm)
                inserted += 1

        await self.session.commit()
        logger.info(f"Ingestion completed: {inserted} inserted, {updated} updated.")
        return inserted, updated
