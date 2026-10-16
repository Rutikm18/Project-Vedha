"""Verify the audit trail's hash chain, and purge what retention has expired.

The chain (migration 0066) is built by a database trigger: each entry's row_hash is
sha256 over the previous entry's hash and its own fields. Verifying recomputes every
hash with the same SQL function and checks each link, so a changed field, a removed
entry or an inserted one shows up as the first broken position.

A retention purge deletes the OLDEST entries only, so the chain stays verifiable from the
first remaining entry; that entry's own link back (to a purged one) is therefore not
checked, only that its hash is correct.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

ZERO_KEY = uuid.UUID(int=0)
# Never keep audit entries for less than this, whatever an organisation sets. CERT-In's
# directions require logs to be retained for a rolling 180 days.
MIN_RETENTION_DAYS = 180
DEFAULT_RETENTION_DAYS = 365
MAX_RETENTION_DAYS = 3650


@dataclass(frozen=True)
class Integrity:
    checked: int
    ok: bool
    first_break_pos: int | None = None
    first_break_id: uuid.UUID | None = None
    reason: str | None = None
    oldest: datetime | None = None
    newest: datetime | None = None


_VERIFY_SQL = text("""
WITH ordered AS (
    SELECT id, chain_pos, prev_hash, row_hash, "timestamp",
           lag(row_hash)  OVER w AS expected_prev,
           lag(chain_pos) OVER w AS previous_pos,
           audit_row_hash(prev_hash, chain_pos, id, tenant_id, actor_id, action, outcome,
                          resource_type, resource_id, engagement_id, ip_address, "timestamp",
                          detail, changes) AS recomputed
      FROM audit_logs
     WHERE chain_key = :key
    WINDOW w AS (ORDER BY chain_pos)
), flagged AS (
    SELECT id, chain_pos,
           CASE
             WHEN row_hash IS DISTINCT FROM recomputed THEN 'an entry was changed'
             WHEN previous_pos IS NOT NULL AND chain_pos <> previous_pos + 1 THEN 'an entry is missing'
             WHEN previous_pos IS NOT NULL AND prev_hash IS DISTINCT FROM expected_prev THEN 'the chain is broken'
           END AS reason
      FROM ordered
)
SELECT (SELECT count(*) FROM ordered),
       (SELECT min("timestamp") FROM ordered),
       (SELECT max("timestamp") FROM ordered),
       f.id, f.chain_pos, f.reason
  FROM (SELECT 1) one
  LEFT JOIN LATERAL (
      SELECT id, chain_pos, reason FROM flagged WHERE reason IS NOT NULL
       ORDER BY chain_pos LIMIT 1
  ) f ON true
""")


async def verify_chain(db: AsyncSession, tenant_id: uuid.UUID | None) -> Integrity:
    """Check one tenant's chain (``None`` is the platform chain: events with no tenant)."""
    row = (await db.execute(_VERIFY_SQL, {"key": tenant_id or ZERO_KEY})).one()
    checked, oldest, newest, bad_id, bad_pos, reason = row
    return Integrity(
        checked=int(checked or 0), ok=bad_pos is None, first_break_pos=bad_pos,
        first_break_id=bad_id, reason=reason, oldest=oldest, newest=newest)


def clamp_retention_days(value: int | None) -> int:
    """An organisation's retention period, held between the legal floor and a sane ceiling."""
    if value is None:
        return DEFAULT_RETENTION_DAYS
    return max(MIN_RETENTION_DAYS, min(MAX_RETENTION_DAYS, int(value)))


async def purge_expired(
    db: AsyncSession, tenant_id: uuid.UUID | None, retention_days: int | None, *,
    now: datetime | None = None,
) -> int:
    """Delete one tenant's entries older than its retention period (never under the floor).
    ``None`` is the platform chain (events with no tenant, e.g. a sign-in by an unknown email).
    Returns how many were removed. Runs in the caller's transaction; the setting that lets
    the append-only trigger allow a DELETE lasts for that transaction only."""
    days = clamp_retention_days(retention_days)
    cutoff = (now or datetime.now(timezone.utc)) - timedelta(days=days)
    await db.execute(text("SELECT set_config('vedha.audit_purge', 'on', true)"))
    # Delete a PREFIX of the chain (everything up to the last expired entry), not "every
    # expired row": two entries written within milliseconds can land in the chain in the
    # opposite order to their timestamps, and deleting by timestamp alone could then leave
    # a hole in the middle that verification would rightly flag.
    result = await db.execute(
        text("""
            DELETE FROM audit_logs
             WHERE chain_key = COALESCE(CAST(:t AS uuid), CAST(:zero AS uuid))
               AND chain_pos <= (
                   SELECT max(chain_pos) FROM audit_logs
                    WHERE chain_key = COALESCE(CAST(:t AS uuid), CAST(:zero AS uuid))
                      AND "timestamp" < :cutoff)
        """),
        {"t": tenant_id, "zero": ZERO_KEY, "cutoff": cutoff})
    await db.execute(text("SELECT set_config('vedha.audit_purge', 'off', true)"))
    return int(result.rowcount or 0)
