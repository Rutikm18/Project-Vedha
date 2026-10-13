"""The producers added after the first four events: SLA watch, status change, coverage gap."""
from __future__ import annotations

import asyncio
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

from app.models.enums import FindingSeverity, FindingStatus
from app.services import notification_rules as nr
from app.workers import sla_watch

TENANT = uuid.uuid4()


def run(c):
    return asyncio.run(c)


def _savepoint():
    class _C:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False
    return _C()


# ── SLA message ──────────────────────────────────────────────────────────────

def test_sla_message_orders_by_urgency_and_caps_the_list():
    items = [{"title": f"F{i}", "severity": "high", "hours_remaining": float(i)} for i in range(14)]
    subject, body = sla_watch._message("at_risk", items)
    assert subject == "Vedha: 14 findings at risk of missing the remediation SLA"
    assert body.index("F0") < body.index("F1") < body.index("F9") and "F10" not in body
    assert body.endswith("…and 4 more")


def test_sla_message_for_breached_shows_how_overdue():
    subject, body = sla_watch._message("breached", [{"title": "RCE", "severity": "critical", "hours_remaining": -30.4}])
    assert subject == "Vedha: 1 finding breached the remediation SLA"
    assert "[critical] RCE, 30 h overdue" in body


def test_sla_watcher_is_off_when_the_interval_is_zero(monkeypatch):
    monkeypatch.setattr(sla_watch, "get_settings", lambda: SimpleNamespace(sla_watch_interval_seconds=0))
    run(sla_watch.run_sla_watch(asyncio.Event()))      # returns immediately, does not loop


# ── coverage gap ─────────────────────────────────────────────────────────────

def _db(engagement):
    res = MagicMock()
    res.one_or_none = MagicMock(return_value=engagement)
    db = MagicMock()
    db.execute = AsyncMock(return_value=res)
    db.begin_nested = _savepoint
    return db


def _spy(monkeypatch):
    calls = []

    async def spy(db, tenant_id, event, subject, body):
        calls.append((event, subject, body))
        return True
    monkeypatch.setattr(nr, "notify_event_safe", spy)
    return calls


def test_rejected_facts_raise_a_coverage_gap(monkeypatch):
    from app.detection.engine_bridge import _notify_coverage_gap
    calls = _spy(monkeypatch)
    census = {"submitted": 10, "ingested": 6, "quarantined": 4, "reasons": {"missing timestamp": 3, "bad port": 1}}
    run(_notify_coverage_gap(_db((TENANT, "Acme")), uuid.uuid4(), census))
    event, subject, body = calls[0]
    assert event == "coverage_gap" and "Acme" in subject
    assert "10 facts" in body and "4 could not be understood" in body and "missing timestamp (3)" in body


def test_a_clean_ingest_is_silent(monkeypatch):
    from app.detection.engine_bridge import _notify_coverage_gap
    calls = _spy(monkeypatch)
    run(_notify_coverage_gap(_db((TENANT, "Acme")), uuid.uuid4(), {"submitted": 5, "ingested": 5, "quarantined": 0}))
    run(_notify_coverage_gap(_db((TENANT, "Acme")), uuid.uuid4(), None))
    run(_notify_coverage_gap(_db((TENANT, "Acme")), uuid.uuid4(), "garbage"))
    assert calls == []


def test_coverage_gap_never_raises(monkeypatch):
    from app.detection.engine_bridge import _notify_coverage_gap
    db = MagicMock()
    db.execute = AsyncMock(side_effect=RuntimeError("db gone"))
    db.begin_nested = _savepoint
    run(_notify_coverage_gap(db, uuid.uuid4(), {"quarantined": 2}))


# ── status change ────────────────────────────────────────────────────────────

def test_a_status_change_notifies_without_being_able_to_fail_the_change(monkeypatch):
    from app.schemas.finding import FindingPatch
    from app.services import finding_workflow as fw

    calls = []

    async def spy(db, tenant_id, event, subject, body):
        calls.append((event, subject, body))
        return True
    monkeypatch.setattr(fw, "notify_event_safe", spy)
    monkeypatch.setattr(fw.finding_events, "record_event", AsyncMock())
    monkeypatch.setattr(fw, "record_audit", MagicMock())

    finding = SimpleNamespace(
        id=uuid.uuid4(), engagement_id=uuid.uuid4(), title="Weak\nTLS " + "x" * 400,
        status=FindingStatus.open, severity=FindingSeverity.high, cvss_score=None, risk_score=None,
        remediation=None, asset_id=None, resolved_at=None, resolution_method=None, resolution_run_id=None,
        reopened_count=0, assigned_to=None, evidence=None)
    db = MagicMock()
    db.flush = AsyncMock()
    db.refresh = AsyncMock()
    body = FindingPatch(status=FindingStatus.confirmed, action_reason="triaged by analyst")
    run(fw.patch_finding(db, finding, body, tenant_id=TENANT, actor_id=uuid.uuid4(),
                         actor_type="user", origin="test"))
    event, subject, text = calls[0]
    assert event == "finding_status_changed" and subject == "Vedha: finding moved from open to confirmed"
    assert "\n" not in text.split("Reason")[0] and "triaged by analyst" in text and len(text) < 700


def test_no_status_change_means_no_notification(monkeypatch):
    from app.schemas.finding import FindingPatch
    from app.services import finding_workflow as fw
    calls = []
    monkeypatch.setattr(fw, "notify_event_safe", AsyncMock(side_effect=lambda *a: calls.append(a)))
    monkeypatch.setattr(fw.finding_events, "record_event", AsyncMock())
    monkeypatch.setattr(fw, "record_audit", MagicMock())
    finding = SimpleNamespace(
        id=uuid.uuid4(), engagement_id=uuid.uuid4(), title="t", status=FindingStatus.open,
        severity=FindingSeverity.low, cvss_score=None, risk_score=None, remediation=None, asset_id=None,
        resolved_at=None, resolution_method=None, resolution_run_id=None, reopened_count=0,
        assigned_to=None, evidence=None)
    db = MagicMock()
    db.flush = AsyncMock()
    db.refresh = AsyncMock()
    run(fw.patch_finding(db, finding, FindingPatch(status=FindingStatus.open), tenant_id=TENANT,
                         actor_id=uuid.uuid4(), actor_type="user", origin="test"))
    assert calls == []
