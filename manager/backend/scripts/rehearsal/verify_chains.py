"""Verify every audit hash chain with the application's own verifier (read-only).

    cd manager/backend
    DATABASE_URL=postgresql+asyncpg://... PYTHONPATH=. python scripts/rehearsal/verify_chains.py

Checks one chain per tenant plus the platform chain (entries with no tenant) and prints how
many entries it covered and how long that took (about 1 s per 100,000 entries). Exit code 1
if any chain is broken. Safe to run against production after migration 0067.
"""
import asyncio
import sys
import time

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.config import get_settings
from app.services.audit_integrity import verify_chain


async def main() -> int:
    engine = create_async_engine(get_settings().database_url)
    async with AsyncSession(engine) as db:
        tenants = [row[0] for row in (await db.execute(text("SELECT id FROM tenants ORDER BY id"))).all()]
        started = time.time()
        total = broken = 0
        for tenant in [*tenants, None]:
            result = await verify_chain(db, tenant)
            total += result.checked
            if not result.ok:
                broken += 1
                print(f"BROKEN chain {tenant or '(platform)'}: {result.reason} at position "
                      f"{result.first_break_pos} (entry {result.first_break_id})")
        print(f"verified {len(tenants) + 1} chains, {total:,} entries in {time.time() - started:.1f}s; "
              f"broken chains: {broken}")
    await engine.dispose()
    return 1 if broken else 0


sys.exit(asyncio.run(main()))
