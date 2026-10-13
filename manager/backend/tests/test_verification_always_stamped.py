"""Every finding carries a passive verification verdict.

Regression for "every finding shows Unverified": verification_enabled defaulted
to False and nothing set it, so no finding was ever stamped — including ones
whose evidence already said state=confirmed. Findings created outside a
detection run (service_vuln, imports, AD) and attack-path findings were never
stamped even with the flag on.
"""
from __future__ import annotations

import uuid
from types import SimpleNamespace

import pytest

from app.config import Settings
from app.detection import engine_bridge
from app.detection.verification import stamp_passive_verdict
from app.models.enums import FindingSeverity, FindingStatus
from app.models.finding import Finding
from app.services.finding_content import detection_method


def test_verification_enabled_by_default(monkeypatch):
    monkeypatch.delenv("VERIFICATION_ENABLED", raising=False)
    assert Settings().verification_enabled is True


def _finding(evidence):
    return SimpleNamespace(evidence=evidence, verification_state=None,
                           verification_confidence=None, verification_rationale=None,
                           needs_review=False, verification_method=None)


def test_stamp_confirmed_evidence():
    f = _finding({"state": "confirmed", "confidence": 85})
    stamp_passive_verdict(f)
    assert f.verification_state == "confirmed"
    assert f.verification_confidence == 85
    assert f.verification_method == "passive"


def test_stamp_never_overwrites_an_existing_verdict():
    f = _finding({"state": "confirmed", "confidence": 85})
    f.verification_state = "contradicted"
    stamp_passive_verdict(f)
    assert f.verification_state == "contradicted"


def test_stamp_tolerates_missing_evidence():
    f = _finding(None)
    stamp_passive_verdict(f)
    assert f.verification_state == "inferred"


def test_before_insert_hook_stamps_any_new_finding():
    """The mapper event stamps rows from every creation path, not just the engine."""
    from app.models.finding import _stamp_verdict_before_insert

    f = Finding(engagement_id=uuid.uuid4(), title="Weak SSH cryptographic algorithms offered",
                severity=FindingSeverity.medium, status=FindingStatus.open,
                evidence={"port": 22, "weak_algorithms": ["ssh-dss"]})
    _stamp_verdict_before_insert(None, None, f)
    assert f.verification_state == "inferred"


@pytest.mark.asyncio
async def test_attack_path_findings_join_touched(monkeypatch):
    """Attack-path rows must be handed to the verification stamp like CVE/posture rows."""
    monkeypatch.setattr(engine_bridge, "attack_path_findings", lambda facts, roles: [
        {"rule_id": "AP-1", "title": "NTLM relay path", "severity": FindingSeverity.high,
         "target": "10.0.0.5", "evidence": {"hosts": ["10.0.0.5"]}},
    ])

    async def _roles(db, eid):
        return {}

    async def _asset(db, eid, target, cache=None, identity=None):
        return SimpleNamespace(id=uuid.uuid4())

    async def _dup(*a, **k):
        return None

    monkeypatch.setattr(engine_bridge, "_engagement_device_roles", _roles)
    monkeypatch.setattr(engine_bridge, "_resolve_asset", _asset)
    monkeypatch.setattr(engine_bridge, "_find_open_duplicate", _dup)
    monkeypatch.setattr(engine_bridge, "_find_remediated_match", _dup)

    class _DB:
        def add(self, obj):
            pass

        async def flush(self):
            pass

    touched: list = []
    run = SimpleNamespace(id=uuid.uuid4())
    created = await engine_bridge._persist_attack_paths(
        _DB(), uuid.uuid4(), run, [], now=None, touched=touched)
    assert created == 1
    assert len(touched) == 1 and touched[0].title == "NTLM relay path"


# ── detection_method: an assessed finding always states HOW it was established ──

def _dm(**kw):
    base = dict(exploit_validated=False, verification_state=None, evidence={})
    base.update(kw)
    return detection_method(SimpleNamespace(**base))


def test_inferred_version_match_reads_as_version():
    assert _dm(verification_state="inferred",
               evidence={"match_basis": "range", "matched_version": "2017.75"}) == "version"


def test_inferred_banner_only_reads_as_banner():
    assert _dm(verification_state="inferred",
               evidence={"port": 80, "banner_first_line": "Server: thttpd"}) == "banner"


def test_inferred_other_reads_as_inference():
    assert _dm(verification_state="inferred", evidence={"correlation": True}) == "inference"


def test_unassessed_stays_unverified():
    assert _dm() is None
    assert _dm(verification_state="contradicted") is None
