"""Tenant row-level security (F1 defense-in-depth)

Enables Postgres RLS on the directly-tenant-owned tables with a policy that is
permissive when the per-request `app.tenant_id` GUC is unset. This is DORMANT:
nothing sets that GUC unless DB_RLS_ENABLED is turned on, so with the flag off
(the default) every row still passes and behaviour is unchanged. See
app/db_rls.py for the full rationale.

Postgres-only: on SQLite (unit tests) this is a no-op, since SQLite has no RLS.
Downgrading removes the policies and disables RLS; no data is touched.

Revision ID: 0062
Revises: 0061
"""
from typing import Sequence, Union

from alembic import op

from app.db_rls import RLS_TENANT_TABLES, disable_statements, enable_statements

revision: str = "0062"
down_revision: Union[str, None] = "0061"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return
    for table in RLS_TENANT_TABLES:
        for stmt in enable_statements(table):
            op.execute(stmt)


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return
    for table in RLS_TENANT_TABLES:
        for stmt in disable_statements(table):
            op.execute(stmt)
