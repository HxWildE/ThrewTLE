import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.jobs.sync_catalogue import run_catalogue_sync


async def main():
    print("[Ingest Sample] Running sample dataset ingestion...")
    result = await run_catalogue_sync(limit=20)
    print(f"[Ingest Sample] Completed: {result}")


if __name__ == "__main__":
    asyncio.run(main())
