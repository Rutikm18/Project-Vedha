"""Fragile-asset guard: HSM / ATM / SWIFT / ICS hosts get only gentle scans unless overridden."""
from __future__ import annotations

import pytest

from app.intel.fragile import (
    FragileHost,
    fragile_exclusions,
    fragile_hosts,
    fragile_reasons,
    is_gentle,
)


def _tags(*pairs):
    return {"v": 1, "auto": [{"key": k, "value": v} for k, v in pairs], "manual": []}


def test_fragile_reasons():
    assert fragile_reasons({"sector_fn:hsm", "role:web"}) == ["sector_fn:hsm"]
    assert fragile_reasons({"role:ics"}) == ["role:ics"]
    assert fragile_reasons({"role:web"}) == []
    # operator marks any host fragile, or explicitly clears a heuristic one
    assert fragile_reasons({"scan_policy:fragile"}) == ["scan_policy:fragile"]
    assert fragile_reasons({"sector_fn:swift", "scan_policy:standard"}) == []


def test_fragile_hosts_from_asset_rows():
    rows = [("10.20.0.20", _tags(("sector_fn", "hsm"))),
            ("10.0.0.10", _tags(("role", "domain_controller"))),
            (None, _tags(("sector_fn", "atm"))),
            ("10.30.0.5", {"manual": [{"key": "scan_policy", "value": "fragile"}]})]
    hosts = fragile_hosts(rows)
    assert [h.ip for h in hosts] == ["10.20.0.20", "10.30.0.5"]


@pytest.mark.parametrize("scan_type,intensity,gentle", [
    ("passive_discovery", None, True),
    ("passive_discovery", "deep", True),
    ("discovery", "light", True),
    ("device_inventory", "light", True),
    ("discovery", "standard", False),
    ("discovery", None, False),          # unknown intensity fails closed
    ("network_va", "light", False),
    ("web_scan", "light", False),
    ("unknown_type", "light", False),
])
def test_is_gentle(scan_type, intensity, gentle):
    assert is_gentle(scan_type, intensity) is gentle


def test_exclusions_only_for_hosts_inside_the_job_scope():
    hosts = [FragileHost("10.20.0.20", ["sector_fn:hsm"]), FragileHost("192.168.9.9", ["role:ics"]),
             FragileHost("2001:db8::5", ["sector_fn:swift"])]
    plan = fragile_exclusions(hosts, job_scope=["10.20.0.0/24", "2001:db8::/64"])
    assert plan.cidrs == ["10.20.0.20/32", "2001:db8::5/128"]
    assert plan.fully_blocked is False
    assert [h["ip"] for h in plan.hosts] == ["10.20.0.20", "2001:db8::5"]


def test_job_that_targets_only_fragile_hosts_is_fully_blocked():
    hosts = [FragileHost("10.20.0.20", ["sector_fn:hsm"])]
    assert fragile_exclusions(hosts, job_scope=["10.20.0.20/32"]).fully_blocked is True
    assert fragile_exclusions(hosts, job_scope=["10.20.0.20"]).fully_blocked is True


def test_no_fragile_hosts_no_plan():
    plan = fragile_exclusions([], job_scope=["10.0.0.0/8"])
    assert plan.cidrs == [] and not plan.fully_blocked


# ── enforcement at enqueue ───────────────────────────────────────────────────

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

from fastapi import HTTPException

from app.models.audit_log import AuditLog
from app.models.enums import ScanJobType
from app.routers import agents as ag

HSM = FragileHost("10.20.0.20", ["sector_fn:hsm"])


def _db():
    eng = SimpleNamespace(id=uuid.uuid4(), rules_of_engagement=None, scope_cidrs=["10.0.0.0/8"],
                          excluded_cidrs=["10.99.0.0/16"])
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: eng))
    db.add = MagicMock()
    db.flush = AsyncMock()
    db.refresh = AsyncMock()
    db.commit = AsyncMock()
    return db


def _user(role="admin"):
    return SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4(), role=role)


def _job(db):
    return next(c.args[0] for c in db.add.call_args_list if not isinstance(c.args[0], AuditLog))


@pytest.fixture
def hsm(monkeypatch):
    monkeypatch.setattr("app.services.fragile_guard.load_fragile_hosts", AsyncMock(return_value=[HSM]))


@pytest.mark.asyncio
async def test_intrusive_job_excludes_fragile_host(hsm):
    db = _db()
    body = ag.EnqueueJobRequest(engagement_id=uuid.uuid4(), job_type=ScanJobType.discovery,
                                params={"targets": ["10.20.0.0/24"]}, intensity="deep")
    out = await ag.enqueue_agent_job(body, db, AsyncMock(), _user())
    params = _job(db).result
    assert params["_excluded_cidrs"] == ["10.99.0.0/16", "10.20.0.20/32"]
    assert out["fragile_excluded"] == [{"ip": "10.20.0.20", "reasons": ["sector_fn:hsm"]}]


@pytest.mark.asyncio
async def test_gentle_job_is_untouched(hsm):
    db = _db()
    body = ag.EnqueueJobRequest(engagement_id=uuid.uuid4(), job_type=ScanJobType.discovery,
                                params={"targets": ["10.20.0.0/24"]}, intensity="light")
    out = await ag.enqueue_agent_job(body, db, AsyncMock(), _user())
    assert _job(db).result["_excluded_cidrs"] == ["10.99.0.0/16"]
    assert out["fragile_excluded"] == []


@pytest.mark.asyncio
async def test_job_on_only_fragile_targets_is_refused(hsm):
    body = ag.EnqueueJobRequest(engagement_id=uuid.uuid4(), job_type=ScanJobType.discovery,
                                params={"targets": ["10.20.0.20"]}, intensity="standard")
    with pytest.raises(HTTPException) as exc:
        await ag.enqueue_agent_job(body, _db(), AsyncMock(), _user())
    assert exc.value.status_code == 422 and "fragile" in exc.value.detail


@pytest.mark.asyncio
async def test_override_needs_role_and_reason_and_is_audited(hsm):
    base = dict(engagement_id=uuid.uuid4(), job_type=ScanJobType.discovery,
                params={"targets": ["10.20.0.20"]}, intensity="deep", allow_fragile=True)
    with pytest.raises(HTTPException) as exc:
        await ag.enqueue_agent_job(ag.EnqueueJobRequest(**base, fragile_override_reason="approved CR-4411 window"),
                                   _db(), AsyncMock(), _user("tester"))
    assert exc.value.status_code == 403
    with pytest.raises(HTTPException) as exc:
        await ag.enqueue_agent_job(ag.EnqueueJobRequest(**base, fragile_override_reason="ok"),
                                   _db(), AsyncMock(), _user())
    assert exc.value.status_code == 422

    db = _db()
    out = await ag.enqueue_agent_job(
        ag.EnqueueJobRequest(**base, fragile_override_reason="Approved CR-4411, HSM vendor on site"),
        db, AsyncMock(), _user("manager"))
    assert out["fragile_override"] is True
    assert "10.20.0.20/32" not in _job(db).result["_excluded_cidrs"]
    audits = [c.args[0] for c in db.add.call_args_list if isinstance(c.args[0], AuditLog)]
    assert audits and audits[0].action == "scan.fragile_override"
    assert audits[0].detail["reason"].startswith("Approved CR-4411")


# ── manager-side scanners (Nuclei / Nessus) ──────────────────────────────────

from app.routers import vuln_scans as vs


def test_manager_scanner_filter_skips_fragile_and_override_is_audited():
    db = MagicMock()
    hosts = [HSM]
    body = vs.NucleiScanRequest()
    kept, skipped = vs._fragile_filter(db, uuid.uuid4(), ["10.0.0.1", "10.20.0.20"], hosts, body,
                                       _user(), scanner="nuclei")
    assert kept == ["10.0.0.1"] and skipped[0]["ip"] == "10.20.0.20"
    db.add.assert_not_called()

    with pytest.raises(HTTPException) as exc:
        vs._fragile_filter(db, uuid.uuid4(), ["10.20.0.20"], hosts, body, _user(), scanner="nuclei")
    assert exc.value.status_code == 422

    body = vs.NucleiScanRequest(allow_fragile=True, fragile_override_reason="CR-7781 approved by CISO")
    with pytest.raises(HTTPException) as exc:
        vs._fragile_filter(db, uuid.uuid4(), ["10.20.0.20"], hosts, body, _user("tester"), scanner="nuclei")
    assert exc.value.status_code == 403
    kept, skipped = vs._fragile_filter(db, uuid.uuid4(), ["10.20.0.20"], hosts, body, _user(), scanner="nuclei")
    assert kept == ["10.20.0.20"] and skipped == []
    assert db.add.call_args[0][0].action == "scan.fragile_override"
