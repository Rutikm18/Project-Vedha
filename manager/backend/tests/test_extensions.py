"""test_extensions.py — customer deadline-extension requests with operator approval."""
from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from app.models.audit_log import AuditLog
from app.models.deadline_extension import DeadlineExtensionRequest
from app.models.enums import FindingSeverity, FindingStatus
from app.models.finding_event import FindingEvent
from app.routers import extensions as ext_router
from app.routers import portal
from app.schemas.auth import CurrentUser
from app.schemas.extension import ExtensionCreate, ExtensionDecision
from app.services import extensions as ext

NOW = datetime.now(timezone.utc)


def _scalar(v):
    r = MagicMock()
    r.scalar_one_or_none = MagicMock(return_value=v)
    return r


def _scalars(vals):
    r = MagicMock()
    r.scalars = MagicMock(return_value=MagicMock(all=MagicMock(return_value=list(vals))))
    return r


class _DB:
    def __init__(self, results=()):
        self.results = list(results)
        self.added = []

    async def execute(self, *a, **k):
        return self.results.pop(0) if self.results else _scalar(None)

    def add(self, obj):
        self.added.append(obj)

    async def flush(self):
        pass

    def of(self, cls):
        return [o for o in self.added if isinstance(o, cls)]


def _eng():
    return SimpleNamespace(id=uuid.uuid4(), tenant_id=uuid.uuid4(), rules_of_engagement={})


def _finding(eng, severity="medium", status=FindingStatus.open, evidence=None, age_h=10):
    t = NOW - timedelta(hours=age_h)
    return SimpleNamespace(id=uuid.uuid4(), engagement_id=eng.id, title="t", severity=FindingSeverity(severity),
                           status=status, first_seen=t, created_at=t, due_at=None, due_at_source=None,
                           evidence=evidence or {})


def _client(eng):
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=eng.tenant_id, role="client",
                       client_engagement_id=eng.id)


def _operator(eng):
    return CurrentUser(user_id=uuid.uuid4(), tenant_id=eng.tenant_id, role="manager")


def _create(db, eng, f, **kw):
    args = dict(engagement=eng, user=_client(eng), subject_type="finding", finding_id=f.id, fix_key=None,
                requested_due_at=NOW + timedelta(days=60), reason="Waiting for the vendor patch release",
                compensating_control=None)
    args.update(kw)
    return asyncio.run(ext.create_request(db, **args))


# finding lookup, tenant SLA policy (windows_for), pending check
def _finding_results(f, pending=None):
    return [_scalar(f), _scalar(None), _scalar(pending)]


class TestCreate:
    def test_finding_request_snapshots_and_logs(self):
        eng = _eng()
        f = _finding(eng)
        db = _DB(_finding_results(f))
        req = _create(db, eng, f)
        assert req.status == "pending" and req.member_finding_ids == [f.id]
        assert req.current_due_at is not None
        [ev] = db.of(FindingEvent)
        assert ev.event_type == "extension_requested" and ev.actor_type == "customer"
        assert ev.detail["reason"].startswith("Waiting")
        assert db.of(AuditLog)[0].action == "remediation.extension_requested"

    def test_date_must_be_later_than_current_due(self):
        eng = _eng()
        f = _finding(eng)
        with pytest.raises(HTTPException) as e:
            _create(_DB(_finding_results(f)), eng, f, requested_due_at=NOW + timedelta(hours=1))
        assert e.value.status_code == 422

    @pytest.mark.parametrize("severity,evidence", [("critical", {}), ("high", {}), ("medium", {"kev": True})])
    def test_compensating_control_required_for_serious(self, severity, evidence):
        eng = _eng()
        f = _finding(eng, severity=severity, evidence=evidence)
        with pytest.raises(HTTPException) as e:
            _create(_DB(_finding_results(f)), eng, f)
        assert e.value.status_code == 422 and "compensating" in e.value.detail

    def test_compensating_control_satisfies(self):
        eng = _eng()
        f = _finding(eng, severity="critical")
        req = _create(_DB(_finding_results(f)), eng, f, compensating_control="Port 445 blocked at the edge")
        assert req.compensating_control == "Port 445 blocked at the edge"

    def test_one_pending_per_subject(self):
        eng = _eng()
        f = _finding(eng)
        with pytest.raises(HTTPException) as e:
            _create(_DB(_finding_results(f, pending=uuid.uuid4())), eng, f)
        assert e.value.status_code == 409

    def test_finding_outside_engagement_is_404(self):
        eng = _eng()
        with pytest.raises(HTTPException) as e:
            _create(_DB([_scalar(None)]), eng, _finding(eng))
        assert e.value.status_code == 404

    def test_closed_finding_is_409(self):
        eng = _eng()
        f = _finding(eng, status=FindingStatus.remediated)
        with pytest.raises(HTTPException) as e:
            _create(_DB([_scalar(f)]), eng, f)
        assert e.value.status_code == 409

    def test_bundle_request_snapshots_open_members(self, monkeypatch):
        eng = _eng()
        a, b = _finding(eng), _finding(eng)
        due = NOW + timedelta(days=5)

        async def fake_bundles(db, engagement, tenant_id):
            return {"bundles": [{"fix_key": "abcdef123456", "open_finding_ids": [str(a.id), str(b.id)],
                                 "due_at": due}],
                    "items": [(a, None, {}), (b, None, {})], "sla_source": "default"}

        monkeypatch.setattr(ext.remediation_service, "engagement_bundles", fake_bundles)
        db = _DB([_scalar(None)])                   # pending check
        req = _create(db, eng, a, subject_type="bundle", finding_id=None, fix_key="abcdef123456")
        assert set(req.member_finding_ids) == {a.id, b.id}
        assert req.current_due_at == due
        assert len(db.of(FindingEvent)) == 2


class TestSchema:
    def test_bundle_needs_fix_key(self):
        with pytest.raises(ValidationError):
            ExtensionCreate(subject_type="bundle", requested_due_at=NOW, reason="x" * 20)

    def test_naive_date_rejected(self):
        with pytest.raises(ValidationError):
            ExtensionCreate(subject_type="finding", finding_id=uuid.uuid4(),
                            requested_due_at=datetime(2027, 1, 1), reason="x" * 20)

    def test_note_required(self):
        with pytest.raises(ValidationError):
            ExtensionDecision(note="")


def _pending(eng, members, requested=None):
    return DeadlineExtensionRequest(
        id=uuid.uuid4(), tenant_id=eng.tenant_id, engagement_id=eng.id, subject_type="finding",
        finding_id=members[0].id, member_finding_ids=[m.id for m in members],
        current_due_at=NOW + timedelta(days=1), requested_due_at=requested or NOW + timedelta(days=30),
        reason="vendor patch pending", status="pending", requested_by=uuid.uuid4(), requested_at=NOW)


class TestDecide:
    def test_approve_moves_open_members_only(self):
        eng = _eng()
        open_f, closed_f = _finding(eng), _finding(eng, status=FindingStatus.remediated)
        req = _pending(eng, [open_f, closed_f])
        db = _DB([_scalars([open_f, closed_f])])
        asyncio.run(ext.decide(db, request=req, operator=_operator(eng), approve=True, note="Approved"))
        assert req.status == "approved" and req.decided_due_at == req.requested_due_at
        assert open_f.due_at == req.requested_due_at and open_f.due_at_source == "extension"
        assert closed_f.due_at is None
        assert {e.event_type for e in db.of(FindingEvent)} == {"extension_approved"}

    def test_approve_with_different_date(self):
        eng = _eng()
        f = _finding(eng)
        req = _pending(eng, [f])
        granted = NOW + timedelta(days=14)
        asyncio.run(ext.decide(_DB([_scalars([f])]), request=req, operator=_operator(eng), approve=True,
                               note="Two weeks only", due_at=granted))
        assert f.due_at == granted and req.decided_due_at == granted

    def test_reject_leaves_due(self):
        eng = _eng()
        f = _finding(eng)
        req = _pending(eng, [f])
        db = _DB([_scalars([f])])
        asyncio.run(ext.decide(db, request=req, operator=_operator(eng), approve=False, note="No"))
        assert req.status == "rejected" and f.due_at is None
        assert db.of(FindingEvent)[0].event_type == "extension_rejected"

    def test_only_pending(self):
        eng = _eng()
        req = _pending(eng, [_finding(eng)])
        req.status = "approved"
        with pytest.raises(HTTPException) as e:
            asyncio.run(ext.decide(_DB(), request=req, operator=_operator(eng), approve=False, note="No"))
        assert e.value.status_code == 409

    def test_withdraw(self):
        eng = _eng()
        f = _finding(eng)
        req = _pending(eng, [f])
        db = _DB([_scalars([f])])
        asyncio.run(ext.withdraw(db, request=req, user=_client(eng)))
        assert req.status == "withdrawn"
        assert db.of(FindingEvent)[0].event_type == "extension_withdrawn"
        with pytest.raises(HTTPException):
            asyncio.run(ext.withdraw(_DB(), request=req, user=_client(eng)))


class TestRoutes:
    def test_operator_cannot_decide_other_tenant(self):
        eng = _eng()
        with pytest.raises(HTTPException) as e:
            asyncio.run(ext_router.approve_extension(uuid.uuid4(), ExtensionDecision(note="Looks fine"),
                                                     _DB([_scalar(None)]), _operator(eng)))
        assert e.value.status_code == 404

    def test_portal_withdraw_other_engagement_is_404(self):
        eng = _eng()
        with pytest.raises(HTTPException) as e:
            asyncio.run(portal.portal_withdraw_extension(uuid.uuid4(), _client(eng), _DB([_scalar(None)])))
        assert e.value.status_code == 404

    def test_portal_create_round_trip(self):
        eng = _eng()
        f = _finding(eng)
        db = _DB([_scalar(eng)] + _finding_results(f))
        body = ExtensionCreate(subject_type="finding", finding_id=f.id,
                               requested_due_at=NOW + timedelta(days=40), reason="Change freeze until month end")
        out = asyncio.run(portal.portal_request_extension(body, _client(eng), db))
        assert out["status"] == "pending" and out["fix_ref"] is None
