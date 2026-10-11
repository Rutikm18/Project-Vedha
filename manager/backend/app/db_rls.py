"""Postgres row-level security (RLS) as defense-in-depth for tenant isolation (F1).

Tenant *identity* is established centrally by TenantIsolationMiddleware. Tenant
*enforcement*, until now, is ~117 hand-written ``tenant_id ==`` filters across
the request handlers. One forgotten filter in one new endpoint shows one tenant
another tenant's rows — a reportable incident for BFSI, not a bug. RLS is the
backstop: with a per-transaction ``app.tenant_id`` GUC, Postgres itself limits
every row of a protected table to the request's tenant, so the 118th missing
filter returns *nothing* instead of another tenant's data.

Design (ships DORMANT — zero behaviour change until deliberately enabled):

* The policy is permissive when the GUC is unset (NULL): cross-tenant workers,
  Alembic migrations and any context that does not set the GUC see every row,
  exactly as today. Enforcement happens only for a transaction that set the GUC.
* Only ``get_db`` / ``get_read_db`` set the GUC, and only when
  ``settings.db_rls_enabled`` is true, the backend is PostgreSQL and the request
  carries a tenant. So with the flag off (the default) the GUC is never set and
  the policy is a no-op.
* The GUC is applied by a SQLAlchemy ``after_begin`` listener keyed off an opt-in
  marker in ``session.info``, so it re-applies on *every* transaction of an
  opted-in session (a handler that commits mid-request keeps enforcement) and is
  inert for every session that did not opt in (all worker sessions).
* ``FORCE ROW LEVEL SECURITY`` so the policy applies even when the app connects
  as the table owner (a plain-RLS owner bypasses it). Superusers still bypass
  RLS entirely — the app must connect as a non-superuser role for this to bite.

Before enabling in production, confirm no request-path endpoint legitimately
reads across tenants on these tables. Today none does: operators and portal
clients are both scoped to one tenant by their token.
"""
from __future__ import annotations

from sqlalchemy import event, text
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, SessionTransaction

GUC = "app.tenant_id"

# The marker get_db sets on a session's info to opt it into the GUC. Absent on
# every worker/background session, so the listener below is a no-op for them.
_INFO_KEY = "vedha_rls_tenant_id"

_POLICY = "tenant_isolation"

# Tables with a DIRECT tenant_id column. Findings and assets are scoped
# transitively through engagement_id and are intentionally left for a later
# extension (their policy needs a subquery to engagements). Protecting another
# directly-tenant-owned table is a one-line addition here plus a migration.
RLS_TENANT_TABLES: tuple[str, ...] = (
    "engagements",
    "agents",
    "scan_requests",
    "scan_schedules",
    "remediation_plans",
    "deadline_extension_requests",
    "notification_rules",
    "sla_policies",
    "integrations",
    "tenant_settings",
    "customer_entitlements",
    "probe_sites",
    "probe_enrollment_requests",
    "personal_access_tokens",
    "users",
)


def _predicate() -> str:
    # current_setting(..., true) → NULL when the GUC was never set this txn
    # (missing_ok). NULL or '' → allow (unset context); else must match tenant.
    return (
        f"current_setting('{GUC}', true) IS NULL "
        f"OR current_setting('{GUC}', true) = '' "
        f"OR tenant_id::text = current_setting('{GUC}', true)"
    )


def enable_statements(table: str) -> list[str]:
    """Idempotent DDL putting one table under the tenant RLS policy."""
    pred = _predicate()
    return [
        f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY",
        f"ALTER TABLE {table} FORCE ROW LEVEL SECURITY",
        f"DROP POLICY IF EXISTS {_POLICY} ON {table}",
        f"CREATE POLICY {_POLICY} ON {table} USING ({pred}) WITH CHECK ({pred})",
    ]


def disable_statements(table: str) -> list[str]:
    return [
        f"DROP POLICY IF EXISTS {_POLICY} ON {table}",
        f"ALTER TABLE {table} NO FORCE ROW LEVEL SECURITY",
        f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY",
    ]


def mark_session_tenant(session: AsyncSession, tenant_id, *, enabled: bool, is_postgres: bool) -> None:
    """Opt a request's session into the tenant GUC. The actual SET runs in the
    after_begin listener, on this and every later transaction of the session."""
    if enabled and is_postgres and tenant_id:
        session.sync_session.info[_INFO_KEY] = str(tenant_id)


@event.listens_for(Session, "after_begin")
def _apply_tenant_guc(session: Session, transaction: SessionTransaction, connection: Connection) -> None:
    """Set the tenant GUC at the start of every transaction of an opted-in
    session. Inert for sessions that never opted in (workers) and for non-Postgres
    backends (SQLite unit tests). set_config(..., true) is transaction-local, so a
    pooled connection never carries one request's tenant into the next request."""
    tenant_id = session.info.get(_INFO_KEY)
    if not tenant_id or connection.dialect.name != "postgresql":
        return
    connection.execute(text(f"SELECT set_config('{GUC}', :tid, true)"), {"tid": tenant_id})
