"""
test_remediation_upsert_integration.py — real-Postgres verification of the
remediation ON CONFLICT upsert. OPT-IN: skipped unless REMEDIATION_TEST_DB_URL
points at a throwaway Postgres, so the default (mock-based) suite never needs a DB.

    docker run -d --name pg -e POSTGRES_USER=vapt -e POSTGRES_PASSWORD=secret \
        -e POSTGRES_DB=vapt_db -p 5433:5432 postgres:16-alpine
    REMEDIATION_TEST_DB_URL=postgresql+asyncpg://vapt:secret@localhost:5433/vapt_db \
        .venv/bin/python -m pytest tests/test_remediation_upsert_integration.py -m integration

Verifies what mocks/compile-checks cannot: that against a live DB the upsert
(1) resets the review gate on regeneration, (2) refreshes generated_at,
(3) keeps exactly one row per (finding, os), and (4) never raises IntegrityError
under a genuinely concurrent duplicate — the failure mode of the old
read-then-write code.
"""
from __future__ import annotations

import asyncio
import os
import uuid

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.routers import remediation

pytestmark = pytest.mark.integration

_DB_URL = os.environ.get("REMEDIATION_TEST_DB_URL")

# Mirrors the core of migration 0028 (columns + the unique constraint the upsert
# targets); FKs are omitted so the test is self-contained (no parent fixtures).
_DDL = """
CREATE TABLE remediation_plans (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL, engagement_id uuid NOT NULL, finding_id uuid NOT NULL,
  os varchar(16) NOT NULL, plan jsonb NOT NULL, source varchar(16) NOT NULL,
  model varchar(100), reviewed boolean NOT NULL DEFAULT false,
  generated_at timestamptz NOT NULL DEFAULT now(),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT uq_remediation_finding_os UNIQUE (finding_id, os)
);
"""


def _stmt(fid, tid, eid, *, model, publish):
    return remediation._build_upsert_stmt(
        tenant_id=tid, engagement_id=eid, finding_id=fid, os="linux",
        plan={"source": "ai", "model": model, "steps": [{"step": 1}]}, publish=publish)


async def _run(url: str) -> None:
    eng = create_async_engine(url)
    try:
        async with eng.begin() as conn:
            await conn.execute(text("DROP TABLE IF EXISTS remediation_plans"))
            await conn.execute(text(_DDL))

        tid, eid, fid = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
        async with AsyncSession(eng) as db:
            r1 = (await db.execute(_stmt(fid, tid, eid, model="m1", publish=True))).one()
            await db.commit()
            assert r1.reviewed is True
            g1 = r1.generated_at

            # Regenerate the SAME key without publishing → gate MUST reset to False
            # (else new, unreviewed content would leak to the customer portal).
            r2 = (await db.execute(_stmt(fid, tid, eid, model="m2", publish=False))).one()
            await db.commit()
            assert r2.reviewed is False, "review gate not reset on regenerate"
            assert r2.model == "m2"
            assert r2.generated_at >= g1

            cnt = (await db.execute(text(
                "select count(*) from remediation_plans where finding_id=:f"),
                {"f": str(fid)})).scalar()
            assert cnt == 1

        # Genuine concurrency on a NEW key from two connections at once.
        fid2 = uuid.uuid4()

        async def racer(model, publish):
            async with AsyncSession(eng) as s:
                await s.execute(_stmt(fid2, tid, eid, model=model, publish=publish))
                await s.commit()

        await asyncio.wait_for(
            asyncio.gather(racer("a", True), racer("b", False)), timeout=15)

        async with AsyncSession(eng) as db:
            cnt2 = (await db.execute(text(
                "select count(*) from remediation_plans where finding_id=:f"),
                {"f": str(fid2)})).scalar()
            assert cnt2 == 1, f"race produced {cnt2} rows"
    finally:
        await eng.dispose()


@pytest.mark.skipif(not _DB_URL, reason="set REMEDIATION_TEST_DB_URL to run")
def test_upsert_resets_gate_and_is_race_safe():
    asyncio.run(_run(_DB_URL))
