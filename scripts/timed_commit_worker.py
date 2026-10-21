#!/usr/bin/env python3
"""
ThrewTLE Timed Commit Worker
----------------------------
An operational worker script to manage subsequent timed, staggered commits cleanly
without polluting repository history during rapid build iterations.

Usage:
    python scripts/timed_commit_worker.py --check-only
    python scripts/timed_commit_worker.py --execute
    python scripts/timed_commit_worker.py --daemon --interval-minutes 60
"""

import argparse
import datetime
import os
import subprocess
import sys
import time


def run_cmd(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


def get_changed_files() -> list[str]:
    result = run_cmd(["git", "status", "--porcelain"], check=False)
    if result.returncode != 0:
        return []
    lines = result.stdout.strip().splitlines()
    files = []
    for line in lines:
        if line.strip():
            # Format: ' M filename' or '?? filename'
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                files.append(parts[1])
    return files


def perform_staggered_commit(batch_size: int = 5) -> bool:
    changes = get_changed_files()
    if not changes:
        print("[Timed Worker] No outstanding changes to commit.")
        return False

    print(f"[Timed Worker] Detected {len(changes)} modified/untracked files.")
    batch = changes[:batch_size]

    for f in batch:
        run_cmd(["git", "add", f], check=False)

    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    msg = f"chore(staggered): automated commit batch ({len(batch)} files) at {timestamp}"
    res = run_cmd(["git", "commit", "-m", msg], check=False)

    if res.returncode == 0:
        print(f"[Timed Worker] Successfully committed {len(batch)} files: {batch}")
        return True
    else:
        print(f"[Timed Worker] Commit failed or nothing staged: {res.stderr}")
        return False


def main():
    parser = argparse.ArgumentParser(description="ThrewTLE Staggered Timed Commit Worker")
    parser.add_argument("--check-only", action="store_true", help="Inspect git status without committing")
    parser.add_argument("--execute", action="store_true", help="Perform one timed commit batch now")
    parser.add_argument("--daemon", action="store_true", help="Run indefinitely in background with interval")
    parser.add_argument("--interval-minutes", type=int, default=60, help="Interval between commit batches in daemon mode")
    parser.add_argument("--batch-size", type=int, default=5, help="Number of files per staggered commit batch")

    args = parser.parse_args()

    if args.check_only:
        changes = get_changed_files()
        print(f"[Timed Worker] Pending changes count: {len(changes)}")
        for c in changes:
            print(f"  - {c}")
        sys.exit(0)

    if args.execute:
        perform_staggered_commit(batch_size=args.batch_size)
        sys.exit(0)

    if args.daemon:
        print(f"[Timed Worker] Daemon started. Checking every {args.interval_minutes} minutes...")
        while True:
            perform_staggered_commit(batch_size=args.batch_size)
            time.sleep(args.interval_minutes * 60)

    # Default to check if no arguments given
    changes = get_changed_files()
    print(f"[Timed Worker] Pending changes: {len(changes)}. Pass --execute to commit batch.")


if __name__ == "__main__":
    main()
