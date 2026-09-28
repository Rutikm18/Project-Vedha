"""
entitlements.py — the customer's plan (POC / licensed) and portal scan quota.

``evaluate`` is pure: a row + a clock → a state the portal and the operator
dashboard both render. ``consume_scan`` is the only writer that spends quota and
takes a row lock first, so two parallel launches can't both take the last scan.
Refunds are idempotent: each consumer (a scan request, a job) carries a flag that
the refund clears, so a request rejected twice or a job cancelled twice gives
back exactly one scan.

States, in precedence order (the first that applies wins):
  unconfigured → not_started → expired → exhausted → active
"""
from __future__ import annotations

import math
import secrets
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select

from app.models.customer_entitlement import PLAN_POC, CustomerEntitlement

JOB_QUOTA_FLAG = "_quota_consumed"

# Crockford-ish alphabet: no 0/O/1/I, so a key read over the phone survives.
_KEY_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


@dataclass(frozen=True)
class EntitlementView:
    state: str                  # unconfigured | not_started | expired | exhausted | active
    can_scan: bool
    reason: str | None
    plan_type: str | None
    starts_at: datetime | None
    expires_at: datetime | None
    days_left: int | None       # None = no expiry
    scan_quota: int | None      # None = unlimited
    scans_used: int
    scans_left: int | None      # None = unlimited
    license_key: str | None


def _plan_label(plan_type: str | None) -> str:
    return "POC" if plan_type == PLAN_POC else "licence"


def evaluate(row, *, now: datetime | None = None) -> EntitlementView:
    now = now or datetime.now(timezone.utc)
    if row is None:
        return EntitlementView(
            state="unconfigured", can_scan=False,
            reason="Scanning isn't activated for your account yet. "
                   "Ask your security team to activate your plan.",
            plan_type=None, starts_at=None, expires_at=None, days_left=None,
            scan_quota=None, scans_used=0, scans_left=None, license_key=None)

    used = max(int(row.scans_used or 0), 0)
    quota = row.scan_quota
    scans_left = None if quota is None else max(quota - used, 0)
    days_left = None
    if row.expires_at is not None:
        days_left = max(math.ceil((row.expires_at - now).total_seconds() / 86400), 0)
    label = _plan_label(row.plan_type)

    state, reason = "active", None
    if row.starts_at is not None and now < row.starts_at:
        state = "not_started"
        reason = f"Your {label} starts on {row.starts_at:%d %b %Y}."
    elif row.expires_at is not None and now >= row.expires_at:
        state = "expired"
        reason = (f"Your {label} expired on {row.expires_at:%d %b %Y}. Your results stay "
                  "available; contact your security team to extend it.")
    elif scans_left == 0:
        state = "exhausted"
        reason = (f"You've used all {quota} scans in your {label}. "
                  "Contact your security team for more.")

    return EntitlementView(
        state=state, can_scan=state == "active", reason=reason,
        plan_type=row.plan_type, starts_at=row.starts_at, expires_at=row.expires_at,
        days_left=days_left, scan_quota=quota, scans_used=used, scans_left=scans_left,
        license_key=row.license_key)


def generate_license_key() -> str:
    groups = ("".join(secrets.choice(_KEY_ALPHABET) for _ in range(4)) for _ in range(4))
    return "VDH-" + "-".join(groups)


async def get_entitlement(db, engagement_id: uuid.UUID, *, for_update: bool = False):
    stmt = select(CustomerEntitlement).where(CustomerEntitlement.engagement_id == engagement_id)
    if for_update:
        stmt = stmt.with_for_update()
    return (await db.execute(stmt)).scalar_one_or_none()


async def view_for(db, engagement_id: uuid.UUID) -> EntitlementView:
    return evaluate(await get_entitlement(db, engagement_id))


async def assert_can_scan(db, engagement_id: uuid.UUID) -> EntitlementView:
    """Read-only check (no quota spent) — for paths that must refuse early."""
    view = await view_for(db, engagement_id)
    if not view.can_scan:
        raise HTTPException(status.HTTP_403_FORBIDDEN, view.reason)
    return view


async def consume_scan(db, engagement_id: uuid.UUID, *, now: datetime | None = None):
    """Spend one portal scan, or 403 with the customer-facing reason."""
    row = await get_entitlement(db, engagement_id, for_update=True)
    view = evaluate(row, now=now)
    if not view.can_scan:
        raise HTTPException(status.HTTP_403_FORBIDDEN, view.reason)
    row.scans_used = view.scans_used + 1
    await db.flush()
    return row


async def _give_back(db, engagement_id: uuid.UUID) -> None:
    row = await get_entitlement(db, engagement_id, for_update=True)
    if row is not None:
        row.scans_used = max(int(row.scans_used or 0) - 1, 0)
        await db.flush()


async def refund_for_request(db, scan_request) -> None:
    if not getattr(scan_request, "quota_consumed", False):
        return
    await _give_back(db, scan_request.engagement_id)
    scan_request.quota_consumed = False


async def refund_for_job(db, job) -> None:
    result = job.result or {}
    if not result.get(JOB_QUOTA_FLAG):
        return
    await _give_back(db, job.engagement_id)
    # Reassign (not mutate) so SQLAlchemy sees the JSONB change.
    job.result = {**result, JOB_QUOTA_FLAG: False}
