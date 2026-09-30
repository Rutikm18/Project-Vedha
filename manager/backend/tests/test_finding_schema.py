from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.models.enums import FindingStatus
from app.schemas.finding import FindingPatch, FindingSummary
from app.services.evidence_integrity import (
    CANONICAL_SHA256_BASIS,
    canonical_content_sha256,
)


NOW = datetime(2026, 9, 27, 8, 0, tzinfo=timezone.utc)


def _closure_packet(**over):
    before_content = "TLS 1.0 accepted"
    after_content = "TLS 1.0 rejected"
    before_artifact = {
        "label": "Authorized retest output",
        "content": before_content,
        "evidence_type": "retest",
        "tool": "testssl",
        "captured_at": (NOW + timedelta(minutes=5)).isoformat(),
        "captured_by": "tester@example.test",
        "source_host": "probe-01",
        "sha256": canonical_content_sha256(before_content),
        "sha256_basis": CANONICAL_SHA256_BASIS,
    }
    after_artifact = {
        **before_artifact,
        "content": after_content,
        "captured_at": (NOW + timedelta(minutes=30)).isoformat(),
        "sha256": canonical_content_sha256(after_content),
    }
    packet = {
        "reason": "Authorized retest confirms the fix",
        "reviewed_by": "reviewer@example.test",
        "retest": {
            "passed": True,
            "requested_at": NOW.isoformat(),
            "started_at": (NOW + timedelta(minutes=10)).isoformat(),
            "completed_at": (NOW + timedelta(minutes=40)).isoformat(),
            "verified_at": (NOW + timedelta(minutes=50)).isoformat(),
            "tested_by": "tester@example.test",
            "verified_by": "verifier@example.test",
            "scope": {"asset_ids": ["asset-1"]},
            "vantage_point": "external-probe-1",
            "authentication_context": "unauthenticated",
            "method": "authorized protocol negotiation",
            "tool_configuration": {"minimum_protocol": "TLS1.0"},
            "expected_result": "TLS 1.0 is rejected",
            "actual_result": "TLS 1.0 was rejected",
            "coverage_comparison": {"before": 1, "after": 0},
            "change_reference": "CHG-2026-0927",
            "residual_risk": "TLS 1.2 remains enabled by design",
            "before_evidence": [before_artifact],
            "after_evidence": [after_artifact],
        },
    }
    packet.update(over)
    return packet


def test_finding_patch_accepts_documented_maximum_risk_score():
    patch = FindingPatch(risk_score=Decimal("1000"))

    assert patch.risk_score == Decimal("1000")


def test_finding_patch_rejects_risk_score_above_scale():
    with pytest.raises(ValidationError):
        FindingPatch(risk_score=Decimal("1000.01"))


def test_finding_patch_accepts_complete_timezone_aware_closure_packet():
    patch = FindingPatch(
        status=FindingStatus.remediated,
        closure=_closure_packet(),
    )

    assert patch.closure is not None
    assert patch.closure.retest.passed is True
    assert patch.closure.retest.before_evidence[0].tool == "testssl"


@pytest.mark.parametrize(
    "mutate",
    [
        lambda packet: packet["retest"].update(passed=False),
        lambda packet: packet["retest"].update(before_evidence=[]),
        lambda packet: packet["retest"]["after_evidence"][0].update(
            sha256="not-a-hash"
        ),
        lambda packet: packet["retest"]["after_evidence"][0].update(
            sha256="0" * 64
        ),
        lambda packet: packet["retest"]["after_evidence"][0].update(
            tool="unrelated-scanner"
        ),
        lambda packet: packet["retest"]["after_evidence"][0].update(
            captured_at=(NOW + timedelta(hours=2)).isoformat()
        ),
        lambda packet: packet["retest"].update(
            verified_at=(NOW - timedelta(minutes=1)).isoformat()
        ),
    ],
)
def test_finding_patch_rejects_incomplete_or_failed_closure_packet(mutate):
    packet = _closure_packet()
    mutate(packet)

    with pytest.raises(ValidationError):
        FindingPatch(status=FindingStatus.remediated, closure=packet)


def test_closure_packet_cannot_be_attached_to_non_remediated_transition():
    with pytest.raises(ValidationError):
        FindingPatch(status=FindingStatus.accepted, closure=_closure_packet())


def test_action_tracking_requires_timezone_aware_planned_closure():
    patch = FindingPatch(
        action_tracking={
            "non_closure_reason": "Waiting for the maintenance window",
            "planned_closure_at": "2026-10-05T22:00:00+05:30",
            "action_reference": "CHG-2026-1005",
        }
    )
    assert patch.action_tracking is not None
    assert patch.action_tracking.planned_closure_at.utcoffset() is not None

    with pytest.raises(ValidationError):
        FindingPatch(
            action_tracking={
                "non_closure_reason": "Waiting for the maintenance window",
                "planned_closure_at": "2026-10-05T22:00:00",
            }
        )


def test_finding_summary_exposes_full_open_severity_breakdown():
    summary = FindingSummary(
        total=12,
        open_total=8,
        critical_open=1,
        high_open=2,
        medium_open=3,
        low_open=1,
        info_open=1,
        validated=4,
        blind=2,
        average_risk=475,
    )

    assert (
        summary.critical_open
        + summary.high_open
        + summary.medium_open
        + summary.low_open
        + summary.info_open
    ) == summary.open_total
