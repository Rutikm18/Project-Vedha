"""Recompute the stored risk score for every open/confirmed finding.

Findings carry a stored ``risk_score`` that "Highest risk" sorts on. It used to be
written with different inputs from the number shown (for example ``cvss=0.0`` when a
finding has no CVSS), so rows scored before the unification still hold the old value
until their engagement is next prioritised. Run this once after upgrading:

    python scripts/recompute_risk_scores.py            # all engagements
    python scripts/recompute_risk_scores.py --dry-run  # report only, change nothing

Idempotent and safe to re-run. Exit code 0 on success.
"""
from __future__ import annotations

import argparse
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select  # noqa: E402

from app.database import AsyncSessionLocal  # noqa: E402
from app.detection.prioritization import prioritize_engagement_findings  # noqa: E402
from app.models.engagement import Engagement  # noqa: E402


async def main(dry_run: bool) -> int:
    changed_total = 0
    async with AsyncSessionLocal() as db:
        ids = (await db.execute(select(Engagement.id))).scalars().all()
        for eng_id in ids:
            changed = await prioritize_engagement_findings(db, eng_id)
            changed_total += changed
            print(f"engagement {eng_id}: {changed} score(s) {'would change' if dry_run else 'updated'}")
        if dry_run:
            await db.rollback()
        else:
            await db.commit()
    print(f"done: {changed_total} finding score(s) {'would change' if dry_run else 'updated'}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    sys.exit(asyncio.run(main(parser.parse_args().dry_run)))
