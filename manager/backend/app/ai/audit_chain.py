"""
audit_chain.py — a tamper-evident record of every AI egress.

Each model call becomes an ``audit_logs`` row (action ``ai.call``) whose detail
holds WHAT was decided and SHA-256 digests of what actually left the manager
(after pseudonymization) and what came back — never the payloads themselves.
Every row also carries the previous row's hash, so editing or deleting any
record breaks the chain from that point on (``verify_chain``).

Writers take a transaction-scoped Postgres advisory lock before reading the
chain head, so concurrent requests append in sequence instead of forking it.
Stored in the existing append-only audit table: no migration.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Iterable

from sqlalchemy import select, text

from app.models.audit_log import AuditLog

ACTION = "ai.call"
GENESIS = "0" * 64
_LOCK_KEY = "vedha_ai_audit_chain"


def _sha(value: Any) -> str:
    raw = value if isinstance(value, str) else json.dumps(value, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode()).hexdigest()


def ai_call_record(*, task: str | None, provider: str, model: str, profile: str, decision: str,
                   system: str, messages: list[dict], response: str | None,
                   replaced: dict[str, int] | None) -> dict[str, Any]:
    return {
        "at": datetime.now(timezone.utc).isoformat(),
        "task": task, "provider": provider, "model": model, "profile": profile,
        "decision": decision,
        "request_sha256": _sha({"system": system, "messages": messages}),
        "response_sha256": _sha(response) if response is not None else None,
        "redactions": dict(replaced or {}),
    }


def chain_hash(prev_hash: str, detail: dict[str, Any]) -> str:
    body = {k: v for k, v in detail.items() if k != "hash"}
    return hashlib.sha256((prev_hash + json.dumps(body, sort_keys=True, default=str)).encode()).hexdigest()


async def persist_ai_calls(db, records: Iterable[dict], *, actor_id, engagement_id) -> None:
    """Append records to the chain inside the caller's transaction."""
    records = list(records)
    if not records:
        return
    await db.execute(text(f"SELECT pg_advisory_xact_lock(hashtext('{_LOCK_KEY}'))"))
    head = (await db.execute(
        select(AuditLog.detail).where(AuditLog.action == ACTION)
        .order_by(AuditLog.timestamp.desc()).limit(1)
    )).scalar_one_or_none()
    prev = (head or {}).get("hash") or GENESIS
    for record in records:
        detail = {**record, "prev_hash": prev}
        detail["hash"] = chain_hash(prev, detail)
        prev = detail["hash"]
        db.add(AuditLog(actor_id=str(actor_id), engagement_id=engagement_id, action=ACTION,
                        resource_type="ai", resource_id=None, detail=detail,
                        timestamp=datetime.now(timezone.utc)))


def verify_chain(rows: Iterable[Any]) -> dict[str, Any]:
    """rows in chain order (oldest first). Returns the first broken position."""
    prev = GENESIS
    count = 0
    for index, row in enumerate(rows):
        detail = row.detail or {}
        if detail.get("prev_hash") != prev or chain_hash(prev, detail) != detail.get("hash"):
            return {"ok": False, "records": index, "broken_at": index}
        prev = detail["hash"]
        count += 1
    return {"ok": True, "records": count, "broken_at": None}
