import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.jobs.sync_catalogue import run_catalogue_sync


async def main():
    print("[Manual Sync] Triggering full metadata catalogue sync...")
    result = await run_catalogue_sync(limit=50)
    print(f"[Manual Sync] Finished: {result}")


if __name__ == "__main__":
    asyncio.run(main())
