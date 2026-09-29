"""
entitlements.py — the customer's plan (POC / licensed) and portal scan allowances.

A plan has an optional overall cap plus one allowance per scan type:

  stealth / normal / aggressive — the probe's light / standard / deep presets
  deep                          — every port + full assessment on ONE asset
                                  (uc_deep_port_sweep), with a repeat policy

``evaluate`` is pure: a row + a clock → the state the portal and the operator
dashboard both render, per scan type. ``consume_scan`` is the only writer that
spends an allowance and takes a row lock first, so two parallel launches can't
both take the last scan. Refunds are idempotent: each consumer (a scan request,
a job) carries a flag that the refund clears, and gives back the same type (and,
for a deep scan, releases its asset from the repeat history).

Plan states, in precedence order (the first that applies wins):
  unconfigured → not_started → expired → exhausted → active
"exhausted" = the overall cap is used up, or no scan type has anything left.
"""
from __future__ import annotations

import math
import secrets
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select

from app.models.customer_entitlement import (
    DEEP_DISTINCT, PLAN_LICENSED, PLAN_POC, SCAN_MODES, CustomerEntitlement,
)

JOB_QUOTA_FLAG = "_quota_consumed"
JOB_QUOTA_MODE = "_quota_mode"
JOB_DEEP_TARGET = "_deep_target"

MODE_LABEL = {"stealth": "Stealth", "normal": "Normal", "aggressive": "Aggressive",
              "deep": "Deep"}

# Crockford-ish alphabet: no 0/O/1/I, so a key read over the phone survives.
_KEY_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


@dataclass(frozen=True)
class ModeView:
    enabled: bool               # False = not included in the plan (quota 0)
    quota: int | None           # None = unlimited
    used: int
    left: int | None            # None = unlimited
    can_scan: bool
    reason: str | None


@dataclass(frozen=True)
class EntitlementView:
    state: str                  # unconfigured | not_started | expired | exhausted | active
    can_scan: bool
    reason: str | None
    plan_type: str | None
    starts_at: datetime | None
    expires_at: datetime | None
    days_left: int | None       # None = no expiry
    scan_quota: int | None      # overall cap; None = none
    scans_used: int
    scans_left: int | None      # None = no overall cap
    license_key: str | None
    modes: dict[str, ModeView] = field(default_factory=dict)
    deep_repeat_policy: str = DEEP_DISTINCT
    deep_scanned_targets: list[str] = field(default_factory=list)


def _plan_label(plan_type: str | None) -> str:
    return "POC" if plan_type == PLAN_POC else "licence"


def _int(v) -> int:
    return max(int(v or 0), 0)


def _mode_view(row, mode: str, *, plan_blocked: str | None, total_left: int | None) -> ModeView:
    quota = getattr(row, f"{mode}_quota", None)
    used = _int(getattr(row, f"{mode}_used", 0))
    enabled = quota is None or quota > 0
    left = None if quota is None else max(quota - used, 0)
    reason = plan_blocked
    if reason is None and not enabled:
        reason = f"{MODE_LABEL[mode]} scans aren't included in your plan."
    elif reason is None and left == 0:
        reason = (f"You've used all {quota} {MODE_LABEL[mode].lower()} scans in your plan. "
                  "Contact your security team for more.")
    elif reason is None and total_left == 0:
        reason = "You've used every scan in your plan. Contact your security team for more."
    return ModeView(enabled=enabled, quota=quota, used=used, left=left,
                    can_scan=reason is None, reason=reason)


def evaluate(row, *, now: datetime | None = None) -> EntitlementView:
    now = now or datetime.now(timezone.utc)
    if row is None:
        msg = ("Scanning isn't activated for your account yet. "
               "Ask your security team to activate your plan.")
        return EntitlementView(
            state="unconfigured", can_scan=False, reason=msg,
            plan_type=None, starts_at=None, expires_at=None, days_left=None,
            scan_quota=None, scans_used=0, scans_left=None, license_key=None,
            modes={m: ModeView(False, 0, 0, 0, False, msg) for m in SCAN_MODES})

    used = _int(row.scans_used)
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

    modes = {m: _mode_view(row, m, plan_blocked=reason, total_left=scans_left)
             for m in SCAN_MODES}
    if state == "active" and not any(v.can_scan for v in modes.values()):
        state = "exhausted"
        reason = (f"You've used all {quota} scans in your {label}. "
                  "Contact your security team for more." if scans_left == 0 else
                  f"There are no scans left in your {label}. "
                  "Contact your security team for more.")

    return EntitlementView(
        state=state, can_scan=state == "active", reason=reason,
        plan_type=row.plan_type, starts_at=row.starts_at, expires_at=row.expires_at,
        days_left=days_left, scan_quota=quota, scans_used=used, scans_left=scans_left,
        # A key issued under an earlier licensed term stays on the row (re-licensing
        # restores it) but is only shown while the plan is actually licensed.
        license_key=row.license_key if row.plan_type == PLAN_LICENSED else None,
        modes=modes,
        deep_repeat_policy=getattr(row, "deep_repeat_policy", None) or DEEP_DISTINCT,
        deep_scanned_targets=list(getattr(row, "deep_scanned_targets", None) or []))


def view_dict(view: EntitlementView) -> dict:
    """Plain dict for the response schemas (the dataclasses nest)."""
    d = dict(view.__dict__)
    d["modes"] = {m: dict(v.__dict__) for m, v in view.modes.items()}
    return d


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


async def consume_scan(db, engagement_id: uuid.UUID, mode: str, *,
                       deep_target: str | None = None, now: datetime | None = None):
    """Spend one scan of ``mode``, or 403 with the customer-facing reason.

    For a deep scan, ``deep_target`` is the single normalized asset; under the
    "distinct" policy an asset that was already deep-scanned is refused."""
    if mode not in SCAN_MODES:
        raise ValueError(f"unknown scan mode {mode!r}")
    row = await get_entitlement(db, engagement_id, for_update=True)
    view = evaluate(row, now=now)
    mv = view.modes[mode]
    if not mv.can_scan:
        raise HTTPException(status.HTTP_403_FORBIDDEN, mv.reason)
    if mode == "deep":
        if not deep_target:
            raise ValueError("a deep scan needs its single target")
        history = list(row.deep_scanned_targets or [])
        if row.deep_repeat_policy == DEEP_DISTINCT and deep_target in history:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                f"{deep_target.split('/')[0]} has already had a deep scan. Your plan allows "
                "one deep scan per asset — choose a different asset.")
        # Reassign (not mutate) so SQLAlchemy sees the JSONB change.
        row.deep_scanned_targets = history + [deep_target]
    row.scans_used = view.scans_used + 1
    setattr(row, f"{mode}_used", mv.used + 1)
    await db.flush()
    return row


async def _give_back(db, engagement_id: uuid.UUID, mode: str | None,
                     deep_target: str | None) -> None:
    row = await get_entitlement(db, engagement_id, for_update=True)
    if row is None:
        return
    row.scans_used = max(_int(row.scans_used) - 1, 0)
    if mode in SCAN_MODES:
        setattr(row, f"{mode}_used", max(_int(getattr(row, f"{mode}_used", 0)) - 1, 0))
    if mode == "deep" and deep_target:
        history = list(row.deep_scanned_targets or [])
        if deep_target in history:
            # Drop the LAST occurrence: the scan being given back is the newest.
            idx = len(history) - 1 - history[::-1].index(deep_target)
            row.deep_scanned_targets = history[:idx] + history[idx + 1:]
    await db.flush()


async def refund_for_request(db, scan_request) -> None:
    if not getattr(scan_request, "quota_consumed", False):
        return
    mode = getattr(scan_request, "quota_mode", None)
    targets = list(getattr(scan_request, "targets", None) or [])
    target = targets[0] if mode == "deep" and len(targets) == 1 else None
    await _give_back(db, scan_request.engagement_id, mode, target)
    scan_request.quota_consumed = False


async def refund_for_job(db, job) -> None:
    result = job.result or {}
    if not result.get(JOB_QUOTA_FLAG):
        return
    await _give_back(db, job.engagement_id, result.get(JOB_QUOTA_MODE),
                     result.get(JOB_DEEP_TARGET))
    # Reassign (not mutate) so SQLAlchemy sees the JSONB change.
    job.result = {**result, JOB_QUOTA_FLAG: False}
