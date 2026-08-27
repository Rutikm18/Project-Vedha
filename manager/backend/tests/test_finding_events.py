"""
test_finding_events.py — the finding lifecycle audit trail.

The synthesis half is PURE (no DB): it derives DETECTED / RE-OBSERVED / RESOLVED /
REOPENED / terminal-state events from a finding's own columns. The merge half
proves stored audit rows supersede the synthesized ones. The endpoint test wires
the two through the router with a mocked session (no Postgres), and the write-path
tests prove a status patch / reopen appends the right immutable event.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.enums import FindingSeverity, FindingStatus
from app.services import finding_events as svc


NOW = datetime(2026, 8, 27, 14, 0, 0, tzinfo=timezone.utc)


def _finding(**over):
    base = dict(
        id=uuid.uuid4(), created_at=NOW, updated_at=NOW, first_seen=NOW,
        last_seen=NOW, severity=FindingSeverity.high, status=FindingStatus.open,
        evidence={}, detection_run_id=None, detected_db_version=None,
        resolved_at=None, resolution_method=None, resolution_run_id=None,
        reopened_count=0,
    )
    base.update(over)
    return SimpleNamespace(**base)


def _types(events):
    return [e["event_type"] for e in events]


# ── synthesis (pure) ──────────────────────────────────────────────────────────
class TestSynthesize:
    def test_genesis_detected_from_first_seen(self):
        evs = svc.synthesize_events(_finding())
        assert evs[0]["event_type"] == "detected"
        assert evs[0]["occurred_at"] == NOW
        assert evs[0]["to_status"] == "open"

    def test_detected_actor_labels_network_va_campaign(self):
        f = _finding(evidence={"source": "network-VA campaign"})
        assert svc.synthesize_events(f)[0]["actor"] == "network-VA campaign"

    def test_detected_actor_falls_back_to_detection_engine(self):
        f = _finding(evidence={}, detection_run_id=uuid.uuid4())
        assert svc.synthesize_events(f)[0]["actor"] == "detection-engine"

    def test_reobserved_when_last_seen_advances(self):
        f = _finding(last_seen=NOW + timedelta(hours=2))
        assert "reaffirmed" in _types(svc.synthesize_events(f))

    def test_no_reobserved_when_last_seen_equals_genesis(self):
        assert "reaffirmed" not in _types(svc.synthesize_events(_finding()))

    def test_auto_resolution_event(self):
        f = _finding(status=FindingStatus.remediated, resolved_at=NOW + timedelta(days=1),
                     resolution_method="auto", resolution_run_id=uuid.uuid4())
        resolved = next(e for e in svc.synthesize_events(f) if e["event_type"] == "resolved")
        assert resolved["actor"] == "auto-resolution" and resolved["actor_type"] == "system"
        assert resolved["detail"]["run_id"]

    def test_manual_remediation_event(self):
        f = _finding(status=FindingStatus.remediated, resolved_at=NOW + timedelta(days=1),
                     resolution_method="manual")
        assert "remediated" in _types(svc.synthesize_events(f))

    def test_reopened_inferred_from_count(self):
        f = _finding(reopened_count=1, status=FindingStatus.open,
                     evidence={"reopened_by": "u-42"})
        ev = next(e for e in svc.synthesize_events(f) if e["event_type"] == "reopened")
        assert ev["actor"] == "u-42" and ev["detail"]["approx"] is True

    def test_terminal_confirmed_state_emitted(self):
        assert "confirmed" in _types(svc.synthesize_events(_finding(status=FindingStatus.confirmed)))

    def test_terminal_false_positive_state_emitted(self):
        assert "false_positive" in _types(svc.synthesize_events(_finding(status=FindingStatus.fp)))


# ── merge ─────────────────────────────────────────────────────────────────────
class TestMerge:
    def _synth(self, etype, when):
        return {"id": None, "event_type": etype, "actor": "system", "actor_type": "system",
                "from_status": None, "to_status": None, "detail": None,
                "occurred_at": when, "synthesized": True}

    def _stored(self, etype, when, actor="u-1"):
        return {"id": uuid.uuid4(), "event_type": etype, "actor": actor, "actor_type": "user",
                "from_status": None, "to_status": None, "detail": None,
                "occurred_at": when, "synthesized": False}

    def test_stored_supersedes_synthesized_same_type(self):
        merged = svc.merge_timeline(
            [self._stored("resolved", NOW)],
            [self._synth("resolved", NOW), self._synth("detected", NOW - timedelta(days=1))],
        )
        resolved = [e for e in merged if e["event_type"] == "resolved"]
        assert len(resolved) == 1 and resolved[0]["synthesized"] is False

    def test_sorted_oldest_first(self):
        merged = svc.merge_timeline(
            [self._stored("confirmed", NOW)],
            [self._synth("detected", NOW - timedelta(days=2))],
        )
        assert _types(merged) == ["detected", "confirmed"]

    def test_labels_attached(self):
        merged = svc.merge_timeline([], [self._synth("detected", NOW)])
        assert merged[0]["label"] == "DETECTED"


# ── status -> event-type mapping ──────────────────────────────────────────────
class TestEventTypeForStatus:
    @pytest.mark.parametrize("status,expected", [
        (FindingStatus.confirmed, "confirmed"),
        (FindingStatus.remediated, "remediated"),
        (FindingStatus.accepted, "accepted"),
        (FindingStatus.fp, "false_positive"),
        (FindingStatus.open, "reopened"),
    ])
    def test_maps_status_to_specific_event(self, status, expected):
        assert svc.event_type_for_status(status) == expected


# ── endpoint ──────────────────────────────────────────────────────────────────
class TestTimelineEndpoint:
    @pytest.mark.asyncio
    async def test_returns_synthesized_timeline(self):
        from app.routers.findings import finding_timeline
        finding = _finding()
        # first execute() -> tenant finding; second -> stored events (none)
        tenant_res = MagicMock(scalar_one_or_none=lambda: finding)
        events_res = MagicMock()
        events_res.scalars.return_value.all.return_value = []
        db = MagicMock()
        db.execute = AsyncMock(side_effect=[tenant_res, events_res])
        user = SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4())

        result = await finding_timeline(finding.id, db, user)

        assert result.finding_id == finding.id
        assert result.events[0].event_type == "detected"
        assert result.events[0].label == "DETECTED"


# ── write path (status patch appends an audit event) ──────────────────────────
class TestPatchAudits:
    @pytest.mark.asyncio
    async def test_status_change_records_event(self):
        from app.routers.findings import patch_finding
        from app.schemas.finding import FindingPatch

        finding = _finding(status=FindingStatus.open, cvss_score=None, risk_score=None,
                           remediation=None, cve_ids=None, asset_id=None,
                           engagement_id=uuid.uuid4(), title="t", description=None,
                           cvss_vector=None, epss_score=None, exploitable=False,
                           exploit_validated=False, mitre_techniques=None,
                           detection_status=None, verification_state=None,
                           verification_confidence=None, verification_rationale=None,
                           needs_review=False)
        added = []
        db = MagicMock()
        db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: finding))
        db.flush = AsyncMock()
        db.refresh = AsyncMock()
        db.add = MagicMock(side_effect=lambda row: added.append(row))
        user = SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4())

        await patch_finding(finding.id, FindingPatch(status=FindingStatus.confirmed), db, user)

        assert finding.status == FindingStatus.confirmed
        assert any(getattr(r, "event_type", None) == "confirmed" for r in added)
        ev = next(r for r in added if r.event_type == "confirmed")
        assert ev.from_status == "open" and ev.to_status == "confirmed"
        assert ev.actor == str(user.user_id)
