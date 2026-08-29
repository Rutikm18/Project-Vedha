"""
test_engine_bridge_posture.py — the posture/config-exposure track reaches Findings.

Before this wiring the manager ran only the CVE pipeline, so config weaknesses from
the VERIFIED scanners (SMBv1, RDP-without-NLA, weak TLS, exposed RPC) never became
Findings. This proves a posture finding now flows through create_findings_from_facts
into a Finding row carrying severity, risk_score, MITRE technique and remediation.
"""
from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.detection import engine_bridge
from app.models.enums import FindingSeverity, FindingStatus


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
         patch.object(engine_bridge, "detect_all_from_facts", return_value=([], [_POSTURE])), \
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
    assert float(f.risk_score) == 90.0
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
         patch.object(engine_bridge, "detect_all_from_facts", return_value=([], [])), \
         patch.object(engine_bridge, "_persist_attack_paths", new=AsyncMock(return_value=0)), \
         patch.object(engine_bridge, "_stamp_verification", new=AsyncMock(return_value=None)), \
         patch.object(engine_bridge, "evaluate_resolutions", new=AsyncMock(return_value=0)):
        await engine_bridge.create_findings_from_facts(db, engagement_id, result)

    assert [o for o in added if type(o).__name__ == "Finding"] == []
