import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Optional

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.db.session import AsyncSessionLocal
from app.engine.validation.deduplication import Deduplicator
from app.db.base import Base, GenerationRun, OracleResult, Problem, TestCase
from app.repositories.problem_repo import ProblemRepository


async def seed_problems(fixtures_path: Optional[str] = None):
    if fixtures_path is None:
        fixtures_path = str(Path(__file__).resolve().parent.parent / "app" / "db" / "fixtures" / "problems_sample.json")

    with open(fixtures_path, "r", encoding="utf-8") as f:
        problems_data = json.load(f)

    async with AsyncSessionLocal() as session:
        repo = ProblemRepository(session)
        inserted_count = 0

        for p_data in problems_data:
            existing = await repo.get_by_slug(p_data["slug"])
            test_cases_data = p_data.pop("test_cases", [])

            if not existing:
                problem = Problem(**p_data)
                session.add(problem)
                await session.flush()

                for tc_data in test_cases_data:
                    exp_output = tc_data.pop("expected_output", None)
                    ver_status = tc_data.pop("verification_status", "UNVERIFIED")
                    comp_mode = tc_data.pop("comparison_mode", "EXACT_MATCH")
                    oracle_src = tc_data.pop("provenance", "public_example")

                    fp = Deduplicator.compute_fingerprint(tc_data["structured_input"])
                    tc_data["fingerprint"] = fp
                    tc_data["problem_id"] = problem.id

                    tc = TestCase(**tc_data)
                    session.add(tc)
                    await session.flush()

                    oracle = OracleResult(
                        test_case_id=tc.id,
                        expected_output=exp_output,
                        verification_status=ver_status,
                        comparison_mode=comp_mode,
                        oracle_source=oracle_src
                    )
                    session.add(oracle)

                inserted_count += 1
                print(f"[Seed] Ingested Problem #{p_data['source_id']}: {p_data['title']} ({p_data['slug']}) with {len(test_cases_data)} curated cases.")
            else:
                print(f"[Seed] Problem #{p_data['source_id']} ({p_data['slug']}) already exists. Skipping.")

        await session.commit()
        print(f"[Seed] Successfully seeded {inserted_count} new problems.")


if __name__ == "__main__":
    asyncio.run(seed_problems())
