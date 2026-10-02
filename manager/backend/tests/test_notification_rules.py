"""Notification rules: persistence, the rule-aware dispatcher, and the real producers."""
from __future__ import annotations

import asyncio
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from app.models.enums import FindingSeverity
from app.models.notification_rule import NotificationRule
from app.services import notification_rules as nr
from app.services import notifications as nt

TENANT = uuid.uuid4()


class FakeDB:
    """Just enough of an AsyncSession for the rule service: stored NotificationRule rows."""

    def __init__(self, rows=None):
        self.rows: list[NotificationRule] = list(rows or [])
        self.added: list = []
        self.flushed = 0

    async def execute(self, _stmt):
        out = MagicMock()
        out.scalars = MagicMock(return_value=MagicMock(all=MagicMock(return_value=list(self.rows))))
        return out

    def add(self, obj):
        self.added.append(obj)
        if isinstance(obj, NotificationRule):
            self.rows.append(obj)

    async def flush(self):
        self.flushed += 1

    def begin_nested(self):
        class _Ctx:
            async def __aenter__(self_inner):
                return self_inner

            async def __aexit__(self_inner, *a):
                return False
        return _Ctx()


def run(coro):
    return asyncio.run(coro)


# ── catalogue + defaults ─────────────────────────────────────────────────────

def test_defaults_when_nothing_is_stored():
    rules = run(nr.effective_rules(FakeDB(), TENANT))
    assert [r["event"] for r in rules] == [e.key for e in nr.EVENTS]
    crit = next(r for r in rules if r["event"] == "critical_finding")
    assert crit["enabled"] is True and crit["channels"] == ["email", "slack"] and crit["is_custom"] is False
    assert next(r for r in rules if r["event"] == "finding_status_changed")["enabled"] is False


def test_only_events_something_emits_are_marked_connected():
    connected = {e.key for e in nr.EVENTS if e.connected}
    assert connected == {"critical_finding", "high_finding", "report_approved", "probe_enrolled"}


# ── saving ───────────────────────────────────────────────────────────────────

def test_save_creates_then_updates_one_row_per_event():
    db = FakeDB()
    out = run(nr.save_rules(db, TENANT, [{"event": "high_finding", "enabled": False, "channels": ["slack", "email"]}]))
    high = next(r for r in out if r["event"] == "high_finding")
    assert high == {**high, "enabled": False, "channels": ["email", "slack"], "is_custom": True}
    assert len(db.rows) == 1

    run(nr.save_rules(db, TENANT, [{"event": "high_finding", "enabled": True, "channels": ["slack"]}]))
    assert len(db.rows) == 1                       # updated, not duplicated
    assert db.rows[0].enabled is True and db.rows[0].channels == ["slack"]


def test_channels_are_deduplicated_and_ordered():
    db = FakeDB()
    run(nr.save_rules(db, TENANT, [{"event": "report_approved", "enabled": True, "channels": ["slack", "slack", "email"]}]))
    assert db.rows[0].channels == ["email", "slack"]


def test_unknown_event_or_channel_is_refused_and_nothing_is_stored():
    db = FakeDB()
    with pytest.raises(nr.RuleError, match="Unknown event"):
        run(nr.save_rules(db, TENANT, [
            {"event": "high_finding", "enabled": True, "channels": ["email"]},
            {"event": "made_up", "enabled": True, "channels": []},
        ]))
    with pytest.raises(nr.RuleError, match="Unknown channel"):
        run(nr.save_rules(db, TENANT, [{"event": "high_finding", "enabled": True, "channels": ["pager"]}]))
    assert db.rows == [] and db.flushed == 0       # validated up front: a bad request changes nothing


# ── dispatcher ───────────────────────────────────────────────────────────────

@pytest.fixture
def queued(monkeypatch):
    calls: list[dict] = []
    monkeypatch.setattr(nt, "enqueue_notification",
                        lambda db, tenant, subject, body, **kw: calls.append(
                            {"tenant": tenant, "subject": subject, "body": body, **kw}))
    return calls


def test_default_rule_routes_to_its_default_channels(queued):
    assert run(nr.notify_event(FakeDB(), TENANT, "critical_finding", "S", "B")) is True
    assert queued == [{"tenant": TENANT, "subject": "S", "body": "B", "channels": ["email", "slack"], "event": "critical_finding"}]


def test_a_disabled_rule_sends_nothing(queued):
    db = FakeDB([NotificationRule(tenant_id=TENANT, event_key="critical_finding", enabled=False, channels=["email"])])
    assert run(nr.notify_event(db, TENANT, "critical_finding", "S", "B")) is False
    assert queued == []


def test_an_enabled_rule_with_no_channels_sends_nothing(queued):
    db = FakeDB([NotificationRule(tenant_id=TENANT, event_key="probe_enrolled", enabled=True, channels=[])])
    assert run(nr.notify_event(db, TENANT, "probe_enrolled", "S", "B")) is False
    assert queued == []


def test_a_custom_rule_overrides_the_default_channels(queued):
    db = FakeDB([NotificationRule(tenant_id=TENANT, event_key="critical_finding", enabled=True, channels=["slack"])])
    run(nr.notify_event(db, TENANT, "critical_finding", "S", "B"))
    assert queued[0]["channels"] == ["slack"]


def test_an_unknown_event_is_ignored(queued):
    assert run(nr.notify_event(FakeDB(), TENANT, "nope", "S", "B")) is False
    assert queued == []


def test_safe_variant_never_raises_into_the_caller(monkeypatch):
    class Broken(FakeDB):
        def begin_nested(self):
            raise RuntimeError("db down")
    assert run(nr.notify_event_safe(Broken(), TENANT, "critical_finding", "S", "B")) is False

    async def boom(*a, **k):
        raise RuntimeError("enqueue failed")
    monkeypatch.setattr(nr, "notify_event", boom)
    assert run(nr.notify_event_safe(FakeDB(), TENANT, "critical_finding", "S", "B")) is False


# ── delivery routing ─────────────────────────────────────────────────────────

def _integration_rows():
    return [SimpleNamespace(kind="slack", config={}, secret_enc=None, enabled=True),
            SimpleNamespace(kind="email", config={}, secret_enc=None, enabled=True),
            SimpleNamespace(kind="jira", config={}, secret_enc=None, enabled=True)]


def _db_with(rows):
    db = MagicMock()
    r = MagicMock()
    r.scalars = MagicMock(return_value=MagicMock(all=MagicMock(return_value=rows)))
    db.execute = AsyncMock(return_value=r)
    return db


def test_delivery_is_limited_to_the_rules_channels():
    sent: list[str] = []
    senders = {k: (lambda c, s, subj, b, k=k: sent.append(k)) for k in ("slack", "email", "jira")}
    n = run(nt.notify_tenant(_db_with(_integration_rows()), TENANT, "S", "B", senders=senders, channels=["slack"]))
    assert n == 1 and sent == ["slack"]


def test_without_channels_every_enabled_integration_still_gets_it():
    # The integration "send test" path passes no channels.
    sent: list[str] = []
    senders = {k: (lambda c, s, subj, b, k=k: sent.append(k)) for k in ("slack", "email", "jira")}
    n = run(nt.notify_tenant(_db_with(_integration_rows()), TENANT, "S", "B", senders=senders))
    assert n == 3 and sorted(sent) == ["email", "jira", "slack"]


def test_enqueue_carries_channels_and_event_only_when_given(monkeypatch):
    payloads: list[dict] = []
    import app.workers.outbox as outbox
    monkeypatch.setattr(outbox, "enqueue", lambda db, topic, payload: payloads.append(payload))
    nt.enqueue_notification(MagicMock(), TENANT, "S", "B")
    nt.enqueue_notification(MagicMock(), TENANT, "S", "B", channels=["email"], event="probe_enrolled")
    assert "channels" not in payloads[0] and "event" not in payloads[0]
    assert payloads[1]["channels"] == ["email"] and payloads[1]["event"] == "probe_enrolled"


def test_the_outbox_handler_passes_the_rules_channels_through(monkeypatch):
    import contextlib
    import app.workers.outbox as outbox
    seen: dict = {}

    async def fake_notify(db, tenant_id, subject, body, **kw):
        seen.update(kw)
        return 1

    @contextlib.asynccontextmanager
    async def fake_session():
        db = MagicMock()
        db.commit = AsyncMock()
        yield db

    monkeypatch.setattr(nt, "notify_tenant", fake_notify)
    monkeypatch.setattr(outbox, "AsyncSessionLocal", fake_session)
    event = SimpleNamespace(id=1, payload={"tenant_id": str(TENANT), "subject": "S", "body": "B", "channels": ["email"]})
    run(outbox._handle_notify(event))
    assert seen == {"channels": ["email"]}


# ── API ──────────────────────────────────────────────────────────────────────

def _user():
    return SimpleNamespace(tenant_id=TENANT, user_id=uuid.uuid4(), role="admin")


def test_api_returns_the_catalogue_and_saves_with_an_audit_row():
    from app.routers import notification_rules as api
    db = FakeDB()
    got = run(api.list_rules(db, _user()))
    assert len(got) == len(nr.EVENTS)

    body = api.RulesIn(rules=[api.RuleIn(event="report_approved", enabled=False, channels=["email"])])
    out = run(api.put_rules(body, db, _user()))
    assert next(r for r in out if r["event"] == "report_approved")["enabled"] is False
    assert any(type(a).__name__ == "AuditLog" and a.action == "notification_rules.updated" for a in db.added)


def test_api_rejects_unknown_event_with_422():
    from app.routers import notification_rules as api
    body = api.RulesIn(rules=[api.RuleIn(event="made_up", enabled=True, channels=[])])
    with pytest.raises(HTTPException) as e:
        run(api.put_rules(body, FakeDB(), _user()))
    assert e.value.status_code == 422


def _as(role):
    from app.schemas.auth import CurrentUser
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=TENANT, role=role)


def test_writing_rules_needs_admin_or_manager():
    from app.routers import notification_rules as api
    check = api._WRITE.dependency
    assert run(check(_as("admin"))).role == "admin" and run(check(_as("manager"))).role == "manager"
    for role in ("tester", "analyst", "auditor", "client"):
        with pytest.raises(HTTPException) as e:
            run(check(_as(role)))
        assert e.value.status_code == 403


def test_customers_cannot_read_operator_notification_rules():
    from app.routers import notification_rules as api
    check = api._READ.dependency
    assert run(check(_as("analyst"))).role == "analyst"
    with pytest.raises(HTTPException) as e:
        run(check(_as("client")))
    assert e.value.status_code == 403


# ── producers ────────────────────────────────────────────────────────────────

def _spy(monkeypatch):
    calls: list[tuple] = []

    async def spy(db, tenant_id, event, subject, body):
        calls.append((event, subject, body))
        return True
    monkeypatch.setattr(nr, "notify_event_safe", spy)
    return calls


def _savepoint():
    class _Ctx:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False
    return _Ctx()


def _detection_db(opened, engagement):
    first, second = MagicMock(), MagicMock()
    first.all = MagicMock(return_value=opened)
    second.one_or_none = MagicMock(return_value=engagement)
    db = MagicMock()
    db.execute = AsyncMock(side_effect=[first, second])
    db.begin_nested = _savepoint
    return db


def test_detection_run_notifies_per_severity(monkeypatch):
    from app.detection.engine_bridge import _notify_new_findings
    calls = _spy(monkeypatch)
    opened = [(FindingSeverity.critical, "RCE in web"), (FindingSeverity.high, "Weak TLS"),
              (FindingSeverity.critical, "Default creds")]
    run(_notify_new_findings(_detection_db(opened, (TENANT, "Acme internal")), uuid.uuid4(), uuid.uuid4()))
    by_event = {c[0]: c for c in calls}
    assert set(by_event) == {"critical_finding", "high_finding"}
    assert "2 new Critical findings in Acme internal" in by_event["critical_finding"][1]
    assert "RCE in web" in by_event["critical_finding"][2] and "Default creds" in by_event["critical_finding"][2]
    assert "1 new High finding in Acme internal" in by_event["high_finding"][1]


def test_detection_run_with_no_critical_or_high_sends_nothing(monkeypatch):
    from app.detection.engine_bridge import _notify_new_findings
    calls = _spy(monkeypatch)
    db = MagicMock()
    empty = MagicMock()
    empty.all = MagicMock(return_value=[])
    db.execute = AsyncMock(return_value=empty)
    db.begin_nested = _savepoint
    run(_notify_new_findings(db, uuid.uuid4(), uuid.uuid4()))
    assert calls == [] and db.execute.await_count == 1


def test_detection_run_survives_a_notification_failure():
    from app.detection.engine_bridge import _notify_new_findings
    db = MagicMock()
    db.execute = AsyncMock(side_effect=RuntimeError("db gone"))
    db.begin_nested = _savepoint
    run(_notify_new_findings(db, uuid.uuid4(), uuid.uuid4()))      # must not raise


def test_many_findings_are_summarised(monkeypatch):
    from app.detection.engine_bridge import _notify_new_findings
    calls = _spy(monkeypatch)
    opened = [(FindingSeverity.high, f"Issue {i}") for i in range(8)]
    run(_notify_new_findings(_detection_db(opened, (TENANT, "Eng")), uuid.uuid4(), uuid.uuid4()))
    assert "…and 3 more" in calls[0][2] and "Issue 4" in calls[0][2] and "Issue 5" not in calls[0][2]


def test_approving_a_report_notifies(monkeypatch):
    from app.routers import ai_report
    calls: list[tuple] = []

    async def spy(db, tenant_id, event, subject, body):
        calls.append((event, subject))
        return True
    monkeypatch.setattr(ai_report, "notify_event_safe", spy)
    monkeypatch.setattr(ai_report, "get_or_404", AsyncMock(return_value=SimpleNamespace(name="Acme internal")))
    rows = [SimpleNamespace(id=uuid.uuid4()), SimpleNamespace(id=uuid.uuid4())]
    monkeypatch.setattr(ai_report, "_pending_outputs", AsyncMock(return_value=rows))
    db = MagicMock()
    db.flush = AsyncMock()
    out = run(ai_report.approve_report(uuid.uuid4(), SimpleNamespace(output_ids=None), db, _user()))
    assert out["approved"] == 2
    assert calls == [("report_approved", "Vedha: report approved for Acme internal")]


def test_enrolling_a_probe_notifies(monkeypatch):
    from datetime import datetime, timezone
    from app.routers import probe_enrollment as pe

    calls: list[tuple] = []

    async def spy(db, tenant_id, event, subject, body):
        calls.append((event, subject, body))
        return True
    monkeypatch.setattr(pe, "notify_event_safe", spy)

    none = MagicMock()
    none.scalar_one_or_none = MagicMock(return_value=None)       # no duplicate probe name
    db = MagicMock()
    db.execute = AsyncMock(return_value=none)
    db.flush = AsyncMock()
    site = SimpleNamespace(id=uuid.uuid4(), name="hq-site", location="Pune",
                           approved_capabilities=["tcp_connect"], authorized_cidrs=["10.0.0.0/24"])
    row = SimpleNamespace(
        id=uuid.uuid4(), reported_capabilities=["tcp_connect", "dns"], encryption_public_key="k",
        signing_public_key="s", signing_key_fingerprint="fp", agent_version="1", installer_version="1",
        build_digest="d", version=1)
    agent = run(pe._provision_agent_for_site(
        db, row=row, site=site, tenant_id=TENANT, probe_name="pune-probe-1", location=None,
        approved_by="admin", now=datetime.now(timezone.utc), auto=False))
    assert agent.name == "pune-probe-1"
    assert len(calls) == 1
    event, subject, body = calls[0]
    assert event == "probe_enrolled" and "pune-probe-1" in subject
    assert "hq-site" in body and "automatically" not in body


def test_auto_enrolled_probe_says_so(monkeypatch):
    from datetime import datetime, timezone
    from app.routers import probe_enrollment as pe
    bodies: list[str] = []

    async def spy(db, tenant_id, event, subject, body):
        bodies.append(body)
        return True
    monkeypatch.setattr(pe, "notify_event_safe", spy)
    none = MagicMock()
    none.scalar_one_or_none = MagicMock(return_value=None)
    db = MagicMock()
    db.execute = AsyncMock(return_value=none)
    db.flush = AsyncMock()
    site = SimpleNamespace(id=uuid.uuid4(), name="auto", location=None,
                           approved_capabilities=[], authorized_cidrs=[])
    row = SimpleNamespace(id=uuid.uuid4(), reported_capabilities=[], encryption_public_key="k",
                          signing_public_key="s", signing_key_fingerprint="fp", agent_version="1",
                          installer_version="1", build_digest="d", version=1)
    run(pe._provision_agent_for_site(db, row=row, site=site, tenant_id=TENANT, probe_name="p", location=None,
                                     approved_by="system", now=datetime.now(timezone.utc), auto=True))
    assert "automatically" in bodies[0]
