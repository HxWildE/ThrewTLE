import pytest
from app.integrations.leetcode.client import LeetCodeClient


@pytest.mark.asyncio
async def test_leetcode_client_graceful_handling():
    # Calling client with invalid slug or network timeout should return None gracefully without raising
    client = LeetCodeClient(timeout_sec=1.0, max_retries=1)
    res = await client.fetch_question_metadata("non-existent-problem-slug-xyz-12345")
    assert res is None or isinstance(res, dict)
