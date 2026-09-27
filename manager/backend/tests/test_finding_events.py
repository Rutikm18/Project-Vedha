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
        initial_detection_run_id=None,
        resolved_at=None, resolution_method=None, resolution_run_id=None,
        reopened_count=0, resolution_miss_count=0,
        cvss_score=None, risk_score=None, remediation=None,
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

    def test_detected_detail_uses_initial_run_not_latest_touch_run(self):
        initial_run_id = uuid.uuid4()
        latest_run_id = uuid.uuid4()
        event = svc.synthesize_events(
            _finding(
                initial_detection_run_id=initial_run_id,
                detection_run_id=latest_run_id,
            )
        )[0]

        assert event["detail"]["initial_detection_run_id"] == str(initial_run_id)
        assert "detection_run_id" not in event["detail"]

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

        await patch_finding(
            finding.id,
            FindingPatch(status=FindingStatus.confirmed, action_reason="Validated against scan evidence"),
            db,
            user,
        )

        assert finding.status == FindingStatus.confirmed
        assert any(getattr(r, "event_type", None) == "confirmed" for r in added)
        ev = next(r for r in added if r.event_type == "confirmed")
        assert ev.from_status == "open" and ev.to_status == "confirmed"
        assert ev.actor == str(user.user_id)
        assert ev.detail == {
            "origin": "manager",
            "reason": "Validated against scan evidence",
        }
        assert ev.actor_type == "manager"

    @pytest.mark.asyncio
    async def test_manual_remediation_sets_close_metadata_and_audits_reason(self):
        from app.routers.findings import patch_finding
        from app.schemas.finding import FindingPatch

        finding = _finding()
        added = []
        db = MagicMock()
        db.execute = AsyncMock(return_value=MagicMock(scalar_one_or_none=lambda: finding))
        db.flush = AsyncMock()
        db.refresh = AsyncMock()
        db.add = MagicMock(side_effect=lambda row: added.append(row))
        user = SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4())

        await patch_finding(
            finding.id,
            FindingPatch(
                status=FindingStatus.remediated,
                action_reason="Patched the service and the follow-up scan passed",
            ),
            db,
            user,
        )

        assert finding.status == FindingStatus.remediated
        assert finding.resolution_method == "manual"
        assert finding.resolved_at is not None
        event = next(row for row in added if row.event_type == "remediated")
        assert event.detail == {
            "origin": "manager",
            "reason": "Patched the service and the follow-up scan passed",
            "resolution_method": "manual",
        }

    @pytest.mark.asyncio
    async def test_structured_closure_packet_is_stored_on_immutable_event(self):
        from app.routers.findings import patch_finding
        from app.schemas.finding import FindingPatch

        finding = _finding()
        added = []
        db = MagicMock()
        db.execute = AsyncMock(
            return_value=MagicMock(scalar_one_or_none=lambda: finding)
        )
        db.flush = AsyncMock()
        db.refresh = AsyncMock()
        db.add = MagicMock(side_effect=lambda row: added.append(row))
        user = SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4())
        before = {
            "label": "Before fix",
            "content": "TLS 1.0 accepted",
            "evidence_type": "retest",
            "tool": "testssl",
            "captured_at": "2026-08-28T12:00:00Z",
            "captured_by": "tester@example.test",
            "sha256": "a" * 64,
        }
        after = {
            **before,
            "label": "After fix",
            "content": "TLS 1.0 rejected",
            "captured_at": "2026-08-28T12:30:00Z",
            "sha256": "b" * 64,
        }

        await patch_finding(
            finding.id,
            FindingPatch(
                status=FindingStatus.remediated,
                closure={
                    "reason": "Authorized retest confirms the fix",
                    "reviewed_by": "reviewer@example.test",
                    "retest": {
                        "passed": True,
                        "requested_at": "2026-08-28T11:50:00Z",
                        "started_at": "2026-08-28T12:00:00Z",
                        "completed_at": "2026-08-28T12:35:00Z",
                        "verified_at": "2026-08-28T12:45:00Z",
                        "tested_by": "tester@example.test",
                        "verified_by": "verifier@example.test",
                        "scope": {"asset_ids": ["asset-1"]},
                        "vantage_point": "external-probe-1",
                        "authentication_context": "unauthenticated",
                        "method": "authorized protocol negotiation",
                        "tool_configuration": {"profile": "tls"},
                        "expected_result": "TLS 1.0 is rejected",
                        "actual_result": "TLS 1.0 was rejected",
                        "coverage_comparison": {"before": 1, "after": 0},
                        "change_reference": "CHG-2026-0828",
                        "residual_risk": "TLS 1.2 remains enabled by design",
                        "before_evidence": [before],
                        "after_evidence": [after],
                    },
                },
            ),
            db,
            user,
        )

        event = next(row for row in added if row.event_type == "remediated")
        assert event.detail["reason"] == "Authorized retest confirms the fix"
        assert event.detail["reviewed_by"] == "reviewer@example.test"
        assert event.detail["before_evidence"][0]["content"] == "TLS 1.0 accepted"
        assert event.detail["post_fix_evidence"][0]["content"] == "TLS 1.0 rejected"
        assert event.detail["retest"]["passed"] is True
        assert event.detail["retest"]["verified_by"] == "verifier@example.test"

        # Supplying optional proof after a legacy close must append it rather
        # than accepting the packet and silently dropping the validated data.
        await patch_finding(
            finding.id,
            FindingPatch(
                status=FindingStatus.remediated,
                closure={
                    "reason": event.detail["reason"],
                    "reviewed_by": event.detail["reviewed_by"],
                    "retest": event.detail["retest"],
                },
            ),
            db,
            user,
        )
        remediation_events = [
            row
            for row in added
            if getattr(row, "event_type", None) == "remediated"
        ]
        assert len(remediation_events) == 2
        assert remediation_events[-1].detail["retest"]["passed"] is True

    @pytest.mark.asyncio
    async def test_action_tracking_is_recorded_and_audited(self):
        from app.routers.findings import patch_finding
        from app.schemas.finding import FindingPatch

        finding = _finding()
        added = []
        db = MagicMock()
        db.execute = AsyncMock(
            return_value=MagicMock(scalar_one_or_none=lambda: finding)
        )
        db.flush = AsyncMock()
        db.refresh = AsyncMock()
        db.add = MagicMock(side_effect=lambda row: added.append(row))
        user = SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4())

        await patch_finding(
            finding.id,
            FindingPatch(
                action_tracking={
                    "non_closure_reason": "Waiting for the maintenance window",
                    "planned_closure_at": "2026-09-15T22:00:00+05:30",
                    "action_reference": "CHG-2026-0915",
                }
            ),
            db,
            user,
        )

        tracking = finding.evidence["action_tracking"]
        assert tracking["non_closure_reason"] == (
            "Waiting for the maintenance window"
        )
        assert tracking["recorded_at"].endswith("+00:00")
        event = next(
            row for row in added if row.event_type == "action_tracking_updated"
        )
        assert event.actor == str(user.user_id)
        assert event.detail["action_tracking"]["action_reference"] == (
            "CHG-2026-0915"
        )

    @pytest.mark.asyncio
    async def test_remediation_text_records_editor_and_exact_update_time(self):
        from app.routers.findings import patch_finding
        from app.schemas.finding import FindingPatch

        finding = _finding()
        db = MagicMock()
        db.execute = AsyncMock(
            return_value=MagicMock(scalar_one_or_none=lambda: finding)
        )
        db.flush = AsyncMock()
        db.refresh = AsyncMock()
        db.add = MagicMock()
        user = SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4())

        await patch_finding(
            finding.id,
            FindingPatch(remediation="Apply the vendor-supported update."),
            db,
            user,
        )

        assert finding.remediation == "Apply the vendor-supported update."
        assert finding.remediation_updated_by == str(user.user_id)
        assert finding.remediation_updated_at.tzinfo is timezone.utc

        recorded_at = finding.remediation_updated_at
        await patch_finding(
            finding.id,
            FindingPatch(remediation="Apply the vendor-supported update."),
            db,
            user,
        )
        assert finding.remediation_updated_at is recorded_at
