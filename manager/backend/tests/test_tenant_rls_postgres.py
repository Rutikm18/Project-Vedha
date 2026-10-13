"""F1 — prove the tenant RLS policy isolates tenants with NO application-level
filter. Postgres-only: skipped on the SQLite unit-test backend, and skipped (not
failed) when the DB role is a superuser, since superusers bypass RLS entirely and
the policy cannot be demonstrated against one.

This is the CI-facing version of scripts/validation already run against a
throwaway cluster. It creates a throwaway table, puts it under the real policy
from app.db_rls, and asserts the three guarantees the backstop rests on.
"""
from __future__ import annotations

import uuid

import pytest

from app.config import get_settings
from app.db_rls import GUC, enable_statements

pytestmark = pytest.mark.asyncio


def _pg_dsn() -> str | None:
    url = get_settings().database_url
    if not url.startswith("postgresql"):
        return None
    return url.replace("+asyncpg", "")


async def test_rls_isolates_tenants_without_an_app_filter():
    dsn = _pg_dsn()
    if dsn is None:
        pytest.skip("tenant RLS is Postgres-only")
    import asyncpg

    try:
        conn = await asyncpg.connect(dsn)
    except Exception as exc:  # noqa: BLE001 — no reachable Postgres in this run
        pytest.skip(f"no reachable Postgres: {exc}")

    try:
        if await conn.fetchval("SELECT rolsuper FROM pg_roles WHERE rolname = current_user"):
            pytest.skip("DB role is a superuser; RLS is bypassed, cannot be proven")

        table = f"rls_probe_{uuid.uuid4().hex[:12]}"
        tenant_a, tenant_b = uuid.uuid4(), uuid.uuid4()
        await conn.execute(f"CREATE TABLE {table} (id uuid PRIMARY KEY, tenant_id uuid NOT NULL)")
        try:
            for stmt in enable_statements(table):
                await conn.execute(stmt)

            # Unset GUC is permissive (worker / seed / migration path).
            await conn.execute(f"SELECT set_config('{GUC}', '', false)")
            await conn.execute(f"INSERT INTO {table} VALUES ($1, $2)", uuid.uuid4(), tenant_a)
            await conn.execute(f"INSERT INTO {table} VALUES ($1, $2)", uuid.uuid4(), tenant_b)
            assert await conn.fetchval(f"SELECT count(*) FROM {table}") == 2

            # GUC = tenant A: an UNFILTERED read returns only A (the missing-filter backstop).
            await conn.execute(f"SELECT set_config('{GUC}', $1, false)", str(tenant_a))
            rows = await conn.fetch(f"SELECT tenant_id FROM {table}")
            assert [r["tenant_id"] for r in rows] == [tenant_a]

            # WITH CHECK: cannot write another tenant's row while scoped to A.
            with pytest.raises(asyncpg.exceptions.InsufficientPrivilegeError):
                await conn.execute(f"INSERT INTO {table} VALUES ($1, $2)", uuid.uuid4(), tenant_b)

            # Reset: back to seeing everything (worker path unaffected).
            await conn.execute(f"SELECT set_config('{GUC}', '', false)")
            assert await conn.fetchval(f"SELECT count(*) FROM {table}") == 2
        finally:
            await conn.execute(f"SELECT set_config('{GUC}', '', false)")
            await conn.execute(f"DROP TABLE IF EXISTS {table}")
    finally:
        await conn.close()
