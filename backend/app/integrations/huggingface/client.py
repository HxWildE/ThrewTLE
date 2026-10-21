import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import httpx
from app.core.config import settings
from app.core.logging import logger


class HuggingFaceClient:
    def __init__(self, dataset_name: Optional[str] = None):
        self.dataset_name = dataset_name or settings.HUGGINGFACE_DATASET_NAME
        self.fixtures_path = Path(__file__).resolve().parent.parent.parent / "db" / "fixtures" / "problems_sample.json"

    async def fetch_sample_rows(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Attempts to query Hugging Face datasets server via HTTP API with resilient fallback
        to the bundled verified local fixtures.
        """
        api_url = f"https://datasets-server.huggingface.co/rows?dataset={self.dataset_name}&config=default&split=train&offset={offset}&length={limit}"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(api_url)
                if res.status_code == 200:
                    data = res.json()
                    rows = [item["row"] for item in data.get("rows", [])]
                    logger.info(f"Successfully fetched {len(rows)} raw rows from Hugging Face ({self.dataset_name}).")
                    return rows
        except Exception as e:
            logger.warning(f"Hugging Face API request failed or timed out ({e}). Falling back to bundled verified fixtures.")

        # Resilient deterministic fallback
        if self.fixtures_path.exists():
            with open(self.fixtures_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.info(f"Loaded {len(data)} problems from local fallback fixtures.")
                return data
        return []
