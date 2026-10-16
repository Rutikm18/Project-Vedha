"""
org_settings.py — an organisation's authentication, scanning and new-customer policy.

Each section is a strict Pydantic model (unknown keys refused, every value bounded
and validated) stored as JSON in tenant_settings. A missing row or key means the
defaults here, and the defaults are the product's behaviour before these settings
existed, so nothing changes for a tenant until an admin edits a policy.

The helpers at the bottom are pure (no database) so the rules are easy to test:
who may sign in from where, whether a blackout window is active, and how a set of
global exclusions merges into a job's.
"""
from __future__ import annotations

import ipaddress
import re
import uuid
from datetime import datetime, time, timedelta, timezone
from typing import Any, Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from sqlalchemy import select

from app.models.tenant_settings import TenantSettings

SECTIONS = ("auth", "scan", "customer-defaults", "audit")
_COLUMN = {"auth": "auth_policy", "scan": "scan_policy", "customer-defaults": "customer_defaults",
           "audit": "audit_policy"}

_HHMM = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")
_SEVERITIES = ("critical", "high", "medium", "low", "info")
_FEATURES = ("ai_assistant", "compliance", "remediation", "reports")


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


def _networks(values: list[str], *, label: str, allow_hosts: bool) -> list[str]:
    """Validate and normalise CIDRs (or single hosts). Duplicates collapse."""
    out: list[str] = []
    for raw in values:
        try:
            net = ipaddress.ip_network(raw, strict=False)
        except ValueError as exc:
            raise ValueError(f"{label}: '{raw}' is not a valid CIDR or address") from exc
        if not allow_hosts and net.num_addresses == 1 and "/" not in raw:
            raise ValueError(f"{label}: '{raw}' needs a prefix length, e.g. {raw}/32")
        text = str(net)
        if text not in out:
            out.append(text)
    return out


# ── authentication policy ───────────────────────────────────────────────────────

class AuthPolicy(_Strict):
    # Sign-in is refused from outside these networks. Empty = no restriction.
    ip_allowlist: list[str] = Field(default_factory=list, max_length=50)
    # Off by default: customers sign in from anywhere unless this is switched on.
    ip_allowlist_applies_to_portal: bool = False
    # Absolute limit: sign in again after this many hours, however active.
    # None = no absolute limit (sessions slide, as they always have).
    operator_session_max_hours: int | None = Field(default=None, ge=1, le=720)
    customer_session_max_hours: int | None = Field(default=None, ge=1, le=720)
    # Two-step sign-in (TOTP). When required, a user without it enrols at their
    # next sign-in before a session is issued.
    mfa_required_for_operators: bool = False
    mfa_required_for_customers: bool = False

    @field_validator("ip_allowlist")
    @classmethod
    def _check_networks(cls, v: list[str]) -> list[str]:
        return _networks(v, label="IP allowlist", allow_hosts=True)


# ── scanning policy ─────────────────────────────────────────────────────────────

class BlackoutWindow(_Strict):
    name: str = Field(min_length=1, max_length=80)
    kind: Literal["weekly", "once"] = "weekly"
    timezone: str = Field(default="UTC", max_length=64)
    # weekly: days 0=Monday … 6=Sunday, local start/end "HH:MM". end <= start means
    # the window runs past midnight into the next day.
    days: list[int] = Field(default_factory=list, max_length=7)
    start: str | None = None
    end: str | None = None
    # once: absolute instants (timezone-aware ISO 8601).
    starts_at: datetime | None = None
    ends_at: datetime | None = None

    @field_validator("timezone")
    @classmethod
    def _tz(cls, v: str) -> str:
        try:
            ZoneInfo(v)
        except (ZoneInfoNotFoundError, ValueError, OSError) as exc:
            raise ValueError(f"unknown time zone '{v}'") from exc
        return v

    @model_validator(mode="after")
    def _shape(self) -> "BlackoutWindow":
        if self.kind == "weekly":
            if not self.days or any(d < 0 or d > 6 for d in self.days) or len(set(self.days)) != len(self.days):
                raise ValueError("a weekly window needs one or more distinct days, 0 (Mon) to 6 (Sun)")
            if not (self.start and self.end and _HHMM.match(self.start) and _HHMM.match(self.end)):
                raise ValueError("a weekly window needs start and end as HH:MM")
            if self.start == self.end:
                raise ValueError("start and end must differ")
        else:
            if self.starts_at is None or self.ends_at is None:
                raise ValueError("a one-off window needs starts_at and ends_at")
            if self.starts_at.tzinfo is None or self.ends_at.tzinfo is None:
                raise ValueError("starts_at and ends_at must include a time zone offset")
            if self.ends_at <= self.starts_at:
                raise ValueError("ends_at must be after starts_at")
            if self.ends_at - self.starts_at > timedelta(days=366):
                raise ValueError("a one-off window can last at most a year")
        return self


class ScanPolicy(_Strict):
    blackouts: list[BlackoutWindow] = Field(default_factory=list, max_length=20)
    # Whether an admin may still start a manual scan during a blackout (audited).
    admin_override: bool = True
    # Addresses or ranges that are never scanned for any customer or engagement.
    global_exclusions: list[str] = Field(default_factory=list, max_length=100)

    @field_validator("global_exclusions")
    @classmethod
    def _check_exclusions(cls, v: list[str]) -> list[str]:
        return _networks(v, label="Global exclusions", allow_hosts=True)


# ── new-customer defaults ───────────────────────────────────────────────────────

class CustomerDefaults(_Strict):
    # What a newly provisioned POC customer starts with. Existing customers are
    # never changed by editing these.
    poc_locked_severities: list[Literal["critical", "high", "medium", "low", "info"]] = Field(
        default_factory=lambda: ["critical", "high"], max_length=5)
    poc_locked_features: list[Literal["ai_assistant", "compliance", "remediation", "reports"]] = Field(
        default_factory=list, max_length=4)
    poc_duration_days: int = Field(default=14, ge=1, le=365)
    # Shown on lock panels ("Contact …"). Empty = the generic wording.
    support_contact: str = Field(default="", max_length=200)

    @field_validator("poc_locked_severities", "poc_locked_features")
    @classmethod
    def _dedupe(cls, v: list[str]) -> list[str]:
        return list(dict.fromkeys(v))


class AuditPolicy(_Strict):
    # How long audit-log entries are kept before the retention job removes them. The
    # floor is the legal minimum (CERT-In: a rolling 180 days) and cannot be lowered;
    # PCI DSS asks 12 months, HIPAA documentation 6 years, so the default is a year.
    retention_days: int = Field(default=365, ge=180, le=3650)


_MODELS: dict[str, type[_Strict]] = {
    "auth": AuthPolicy, "scan": ScanPolicy, "customer-defaults": CustomerDefaults, "audit": AuditPolicy,
}


# ── storage ─────────────────────────────────────────────────────────────────────

async def get_section(db: Any, tenant_id: uuid.UUID, section: str) -> _Strict:
    """The tenant's validated section, or its defaults. A stored value that no longer
    validates (it should not happen) falls back to the defaults rather than failing
    a sign-in or a scan."""
    model = _MODELS[section]
    row = (await db.execute(
        select(TenantSettings).where(TenantSettings.tenant_id == tenant_id)
    )).scalar_one_or_none()
    stored = getattr(row, _COLUMN[section], None) if row is not None else None
    try:
        return model.model_validate(stored or {})
    except Exception:  # noqa: BLE001 — see docstring
        return model()


async def put_section(db: Any, tenant_id: uuid.UUID, section: str, value: _Strict,
                      *, actor: str) -> _Strict:
    row = (await db.execute(
        select(TenantSettings).where(TenantSettings.tenant_id == tenant_id)
    )).scalar_one_or_none()
    if row is None:
        row = TenantSettings(tenant_id=tenant_id, auth_policy={}, scan_policy={}, customer_defaults={},
                             audit_policy={})
        db.add(row)
    setattr(row, _COLUMN[section], value.model_dump(mode="json"))
    row.updated_by = actor[:64]
    await db.flush()
    return value


# ── pure rules ──────────────────────────────────────────────────────────────────

def ip_allowed(allowlist: list[str], address: str | None) -> bool:
    """True when no allowlist is set, or `address` is inside it. An unparseable or
    missing address is NOT allowed once a list exists (fail closed)."""
    if not allowlist:
        return True
    try:
        ip = ipaddress.ip_address((address or "").strip())
    except ValueError:
        return False
    return any(ip.version == net.version and ip in net
               for net in (ipaddress.ip_network(n, strict=False) for n in allowlist))


def sign_in_allowed(policy: AuthPolicy, *, role: str, address: str | None) -> bool:
    """The network rule for a sign-in. Admins are always exempt: they are the way
    back in if the list is wrong. Customers are only held to it when the policy
    says so."""
    if role == "admin":
        return True
    if role == "client" and not policy.ip_allowlist_applies_to_portal:
        return True
    return ip_allowed(policy.ip_allowlist, address)


def mfa_required(policy: AuthPolicy, *, role: str) -> bool:
    return policy.mfa_required_for_customers if role == "client" else policy.mfa_required_for_operators


def session_limit_hours(policy: AuthPolicy, *, role: str) -> int | None:
    return policy.customer_session_max_hours if role == "client" else policy.operator_session_max_hours


def session_expired(policy: AuthPolicy, *, role: str, auth_time: datetime | None,
                    now: datetime | None = None) -> bool:
    """True when the absolute session limit has passed. A token that carries no
    sign-in time (issued before the limit existed) is treated as just signed in,
    so switching the limit on never mass-logs-out existing sessions at once."""
    limit = session_limit_hours(policy, role=role)
    if limit is None or auth_time is None:
        return False
    return (now or datetime.now(timezone.utc)) - auth_time > timedelta(hours=limit)


def active_blackout(policy: ScanPolicy, now: datetime | None = None) -> BlackoutWindow | None:
    """The first blackout window covering `now`, or None. Weekly windows are read in
    their own time zone (so DST shifts are honoured); a window may cross midnight."""
    now = now or datetime.now(timezone.utc)
    for window in policy.blackouts:
        if window.kind == "once":
            if window.starts_at <= now < window.ends_at:       # type: ignore[operator]
                return window
            continue
        local = now.astimezone(ZoneInfo(window.timezone))
        start = time(*map(int, window.start.split(":")))        # type: ignore[union-attr]
        end = time(*map(int, window.end.split(":")))            # type: ignore[union-attr]
        t, weekday = local.time(), local.weekday()
        if start < end:                                         # same-day window
            if weekday in window.days and start <= t < end:
                return window
        else:                                                   # crosses midnight
            if (weekday in window.days and t >= start) or ((weekday - 1) % 7 in window.days and t < end):
                return window
    return None


def merge_global_exclusions(job_excluded: list[str] | None, policy: ScanPolicy) -> list[str]:
    """The job's own exclusions plus the organisation's, de-duplicated, order kept."""
    return list(dict.fromkeys([*(job_excluded or []), *policy.global_exclusions]))


def entirely_excluded(targets: list[str] | None, exclusions: list[str]) -> bool:
    """True when EVERY requested target is an address or CIDR fully inside the
    exclusions. Anything else (ranges, hostnames) counts as not covered: the probe's
    scope guard still enforces the exclusions, this only spares an operator a scan
    that would silently do nothing."""
    if not targets or not exclusions:
        return False
    excluded = [ipaddress.ip_network(e, strict=False) for e in exclusions]
    for target in targets:
        try:
            net = ipaddress.ip_network(str(target).strip(), strict=False)
        except ValueError:
            return False
        if not any(net.version == e.version and net.subnet_of(e) for e in excluded):
            return False
    return True
