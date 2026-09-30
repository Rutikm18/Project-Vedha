"""
test_engine_bridge_posture.py — the posture/config-exposure track reaches Findings.

Before this wiring the manager ran only the CVE pipeline, so config weaknesses from
the VERIFIED scanners (SMBv1, RDP-without-NLA, weak TLS, exposed RPC) never became
Findings. This proves a posture finding now flows through create_findings_from_facts
into a Finding row carrying severity, risk_score, MITRE technique and remediation.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.detection import engine_bridge
from app.models.enums import FindingSeverity, FindingStatus
from app.services.finding_scan_provenance import (
    SCAN_PROVENANCE_KEY,
    record_scan_observation,
)


_POSTURE = {
    "finding_id": "abc123", "asset_ip": "10.0.0.5", "rule_id": "POSTURE-SMB-V1-ENABLED",
    "title": "SMBv1 enabled (wormable, deprecated)", "category": "misconfiguration",
    "severity": "critical", "state": "confirmed", "confidence": 90, "cwe": "CWE-477",
    "mitre": "T1210", "port": 445, "proto": "tcp",
    "evidence_refs": ["smb.jsonl:1"], "evidence": {"negotiated": "SMBv1"},
    "remediation": "Disable SMBv1.", "fp_notes": "needs a successful SMBv1 negotiate",
    "internet_facing": None, "auth_enforced": None, "risk_score": 90,
    "priority": "critical", "created_at": "2026-08-29T00:00:00Z", "scanner": "smb_scan",
}


@pytest.mark.asyncio
async def test_posture_finding_becomes_a_finding_row():
    engagement_id = uuid.uuid4()
    result = {"facts": [{"scanner": "smb_scan", "target": "10.0.0.5", "status": "open"}],
              "scanner_runs": [{"id": "smb_scan", "status": "completed"}]}

    added: list = []
    db = MagicMock()
    db.add = MagicMock(side_effect=lambda o: added.append(o))
    db.flush = AsyncMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one=lambda: 0))

    with patch.object(engine_bridge, "_vuln_db_meta", return_value=("v1", "t")), \
         patch.object(engine_bridge, "detect_all_from_facts_traced", return_value=([], [_POSTURE], {"coverage": {"rules_blind": 0}, "verdicts": {}})), \
         patch.object(engine_bridge, "_resolve_asset", new=AsyncMock(return_value=None)), \
         patch.object(engine_bridge, "_find_open_duplicate", new=AsyncMock(return_value=None)), \
         patch.object(engine_bridge, "_find_remediated_match", new=AsyncMock(return_value=None)), \
         patch.object(engine_bridge, "_persist_attack_paths", new=AsyncMock(return_value=0)), \
         patch.object(engine_bridge, "_stamp_verification", new=AsyncMock(return_value=None)), \
         patch.object(engine_bridge, "evaluate_resolutions", new=AsyncMock(return_value=0)):
        await engine_bridge.create_findings_from_facts(db, engagement_id, result)

    findings = [o for o in added if type(o).__name__ == "Finding"]
    assert len(findings) == 1
    f = findings[0]
    assert "SMBv1" in f.title
    assert f.severity == FindingSeverity.critical
    assert f.status == FindingStatus.confirmed          # validated scanner → confirmed
    assert f.mitre_techniques == ["T1210"]
    assert f.remediation == "Disable SMBv1."
    # The upstream 0-100 rule score is evidence only; Manager recomputes its
    # non-saturating 0-1000 score from severity, context, and evidence quality.
    assert 0.0 < float(f.risk_score) < 1000.0
    assert f.cve_ids is None                             # posture, not a CVE


@pytest.mark.asyncio
async def test_no_posture_no_finding():
    engagement_id = uuid.uuid4()
    result = {"facts": [{"scanner": "smb_scan", "target": "10.0.0.5", "status": "open"}],
              "scanner_runs": []}
    added: list = []
    db = MagicMock()
    db.add = MagicMock(side_effect=lambda o: added.append(o))
    db.flush = AsyncMock()
    db.execute = AsyncMock(return_value=MagicMock(scalar_one=lambda: 0))

    with patch.object(engine_bridge, "_vuln_db_meta", return_value=("v1", "t")), \
         patch.object(engine_bridge, "detect_all_from_facts_traced", return_value=([], [], {"coverage": {}, "verdicts": {}})), \
         patch.object(engine_bridge, "_persist_attack_paths", new=AsyncMock(return_value=0)), \
         patch.object(engine_bridge, "_stamp_verification", new=AsyncMock(return_value=None)), \
         patch.object(engine_bridge, "evaluate_resolutions", new=AsyncMock(return_value=0)):
        await engine_bridge.create_findings_from_facts(db, engagement_id, result)

    assert [o for o in added if type(o).__name__ == "Finding"] == []


@pytest.mark.asyncio
async def test_posture_reaffirmation_preserves_manager_scan_provenance():
    observed_at = datetime(2026, 9, 27, 8, 30, tzinfo=timezone.utc)
    previous_evidence = record_scan_observation(
        {"proof": "probe finding"},
        scan_result_id=uuid.uuid4(),
        scan_job_id=uuid.uuid4(),
        scan_type="smb_scan",
        source="probe",
        tool="smb_scan",
        recorded_at=observed_at,
        initial=True,
    )
    trusted_provenance = previous_evidence[SCAN_PROVENANCE_KEY]
    duplicate = SimpleNamespace(
        evidence=previous_evidence,
        last_seen=None,
        detection_run_id=None,
        resolution_miss_count=2,
        risk_score=None,
    )
    incoming = {
        **_POSTURE,
        SCAN_PROVENANCE_KEY: {
            "recorded_by": "scanner",
            "schema_version": 1,
            "initial": {"scan_result_id": str(uuid.uuid4())},
        },
    }
    touched: list = []
    db = MagicMock()

    with (
        patch.object(engine_bridge, "_resolve_asset", new=AsyncMock(return_value=None)),
        patch.object(
            engine_bridge,
            "_find_open_duplicate",
            new=AsyncMock(return_value=duplicate),
        ),
    ):
        created, reaffirmed = await engine_bridge._persist_posture_findings(
            db,
            uuid.uuid4(),
            uuid.uuid4(),
            observed_at,
            [incoming],
            touched,
            "db-v1",
        )

    assert created == 0
    assert reaffirmed == 1
    assert duplicate.evidence["title"] == _POSTURE["title"]
    assert duplicate.evidence[SCAN_PROVENANCE_KEY] == trusted_provenance
    assert duplicate.evidence[SCAN_PROVENANCE_KEY]["recorded_by"] == "vedha_manager"
