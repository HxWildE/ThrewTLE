import asyncio
from typing import Any, Dict, Optional
import httpx
from app.core.logging import logger


class LeetCodeClient:
    GRAPHQL_URL = "https://leetcode.com/graphql"

    def __init__(self, timeout_sec: float = 8.0, max_retries: int = 3):
        self.timeout_sec = timeout_sec
        self.max_retries = max_retries

    async def fetch_question_metadata(self, title_slug: str) -> Optional[Dict[str, Any]]:
        """
        Fetches question data from LeetCode public GraphQL with resilient backoff and retries.
        Returns None gracefully upon network/schema failure without raising unhandled exceptions.
        """
        query = """
        query questionData($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            questionId
            questionFrontendId
            title
            titleSlug
            content
            difficulty
            exampleTestcaseList
            topicTags {
              name
              slug
            }
          }
        }
        """
        payload = {
            "query": query,
            "variables": {"titleSlug": title_slug},
            "operationName": "questionData"
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Referer": f"https://leetcode.com/problems/{title_slug}/"
        }

        for attempt in range(1, self.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout_sec) as client:
                    resp = await client.post(self.GRAPHQL_URL, json=payload, headers=headers)
                    if resp.status_code == 200:
                        data = resp.json().get("data", {}).get("question")
                        if data:
                            return data
                    elif resp.status_code == 429:
                        logger.warning(f"LeetCode rate limited (429) on attempt {attempt}. Backing off.")
                        await asyncio.sleep(2 ** attempt)
                    else:
                        logger.warning(f"LeetCode returned HTTP {resp.status_code} for slug '{title_slug}'.")
            except Exception as e:
                logger.warning(f"LeetCode GraphQL request failed (attempt {attempt}/{self.max_retries}): {e}")
                await asyncio.sleep(1.0 * attempt)

        logger.error(f"Failed to fetch metadata for slug '{title_slug}' after {self.max_retries} attempts.")
        return None
