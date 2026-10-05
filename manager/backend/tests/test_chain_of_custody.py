"""
Gap #1 — chain of custody.

Every finding carried recorded evidence, but none carried an integrity digest:
the engagement report could never prove the displayed evidence was the evidence
captured. `normalize_evidence` therefore flagged `evidence_integrity_hash_absent`
on every artifact, and the "sha256_verified" column was always null. The fix
stamps a content digest plus capture identity (who/where/when) at every point a
finding is created, and the report verifies that digest over the OBSERVED
content — excluding the manager's own custody/provenance metadata, which is
stamped or advanced after the fact and must not invalidate the hash.

These tests pin that contract:
  * the digest covers observed content only, so advancing scan_provenance (the
    outbox worker linking a detection run) or re-stamping custody never breaks it;
  * a stamp made at create time verifies when the report reads it back;
  * tampering with the observed content is caught (mismatch, not silent);
  * every producer path (probe, manager scanner, external import, and the
    detection engine) leaves a verifiable hash where there was none.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.detection import engine_bridge as EB
from app.routers.ad import _ad_finding
from app.routers.vuln_scans import FindingImport, _import_finding, _nuclei_finding
from app.services.evidence_integrity import (
    CANONICAL_SHA256_BASIS,
    content_for_integrity,
    extract_integrity_content,
    item_content_sha256,
)
from app.services.finding_scan_provenance import (
    CUSTODY_CAPTURED_BY_MANAGER,
    CUSTODY_CAPTURED_BY_PROBE,
    SCAN_PROVENANCE_KEY,
    attach_detection_run_to_scan_findings,
    record_scan_observation,
    stamp_chain_of_custody,
)
from app.services.report_document import normalize_evidence

TS = datetime(2026, 10, 5, 12, 0, tzinfo=timezone.utc)

_INTEGRITY_GAPS = {
    "evidence_integrity_hash_absent",
    "evidence_integrity_hash_invalid",
    "evidence_integrity_hash_unverified",
    "evidence_integrity_hash_mismatch",
}


def _artifact_of(evidence):
    norm = normalize_evidence(evidence)
    assert norm.artifacts, "a stamped evidence dict must normalize to one artifact"
    return norm, norm.artifacts[0]


# ── the integrity primitive: observed content only ───────────────────────────

def test_content_for_integrity_strips_only_top_level_custody_keys():
    content = {
        "service": "telnet",
        "sha256": "deadbeef",
        "sha256_basis": CANONICAL_SHA256_BASIS,
        "captured_by": "x",
        "captured_at": "t",
        "source_host": "10.0.0.5",
        "scan_provenance": {"recorded_by": "vedha_manager"},
        "dedup_key": "exposed:23",
        # A nested field that happens to share a custody name is observed content.
        "nested": {"source_host": "keep-me", "sha256": "keep-me-too"},
    }
    stripped = content_for_integrity(content)
    assert stripped == {"service": "telnet", "nested": {"source_host": "keep-me", "sha256": "keep-me-too"}}
    # Non-mappings pass through unchanged.
    assert content_for_integrity("a string") == "a string"
    assert content_for_integrity(["a", "list"]) == ["a", "list"]


def test_extract_integrity_content_mirrors_report_content_choice():
    # When a content/output/value key is present, the digest covers THAT value,
    # matching what the report displays and hashes.
    assert extract_integrity_content({"output": "raw-banner", "sha256": "x"}) == "raw-banner"
    assert extract_integrity_content({"service": "telnet", "sha256": "x"}) == {"service": "telnet"}


# ── stamp → report round-trip ────────────────────────────────────────────────

def test_stamped_evidence_verifies_and_closes_the_integrity_gap():
    evidence = stamp_chain_of_custody(
        {"service": "telnet", "port": 23},
        source_host="10.0.0.5",
        captured_by=CUSTODY_CAPTURED_BY_PROBE,
        tool="nmap",
        captured_at=TS,
    )
    assert evidence["sha256_basis"] == CANONICAL_SHA256_BASIS
    norm, art = _artifact_of(evidence)
    assert art.sha256_verified is True
    assert art.captured_by == CUSTODY_CAPTURED_BY_PROBE
    assert art.source_host == "10.0.0.5"
    # The gap this whole change exists to close is gone, along with every other
    # integrity-hash gap.
    assert _INTEGRITY_GAPS.isdisjoint(norm.gaps), norm.gaps


def test_restamp_of_identical_content_is_a_stable_hash():
    first = stamp_chain_of_custody(
        {"service": "telnet", "port": 23}, source_host="10.0.0.5",
        captured_by=CUSTODY_CAPTURED_BY_PROBE, tool="nmap", captured_at=TS)
    later = stamp_chain_of_custody(
        {"service": "telnet", "port": 23}, source_host="10.0.0.5",
        captured_by=CUSTODY_CAPTURED_BY_PROBE, tool="nmap",
        captured_at=datetime(2027, 1, 1, tzinfo=timezone.utc))
    assert first["sha256"] == later["sha256"]
    # Different observed content is a different hash — the intended signal.
    changed = stamp_chain_of_custody(
        {"service": "telnet", "port": 24}, source_host="10.0.0.5",
        captured_by=CUSTODY_CAPTURED_BY_PROBE, tool="nmap", captured_at=TS)
    assert changed["sha256"] != first["sha256"]


def test_tampered_observed_content_is_caught_as_mismatch():
    evidence = stamp_chain_of_custody(
        {"service": "telnet", "port": 23}, source_host="10.0.0.5",
        captured_by=CUSTODY_CAPTURED_BY_PROBE, tool="nmap", captured_at=TS)
    tampered = {**evidence, "port": 24}
    norm, art = _artifact_of(tampered)
    assert art.sha256_verified is False
    assert "evidence_integrity_hash_mismatch" in norm.gaps


def test_unhashable_content_leaves_no_false_hash():
    # A set is not JSON-serializable; the canonical digest is unavailable, so the
    # stamp must leave no hash rather than a false one.
    evidence = stamp_chain_of_custody(
        {"service": "telnet", "weird": {1, 2, 3}}, source_host="10.0.0.5",
        captured_by=CUSTODY_CAPTURED_BY_PROBE, captured_at=TS)
    assert "sha256" not in evidence
    assert "sha256_basis" not in evidence


# ── custody survives the provenance lifecycle ────────────────────────────────

@pytest.mark.asyncio
async def test_detection_run_linking_does_not_break_the_hash():
    """The outbox worker fills scan_provenance.latest.detection_run_id AFTER the
    finding (and its hash) already exist. Because the digest excludes the
    provenance block, that legitimate mutation must keep verifying."""
    scan_result_id, run_id, eng_id = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
    evidence = record_scan_observation(
        {"service": "telnet", "port": 23},
        scan_result_id=scan_result_id, scan_job_id=uuid.uuid4(),
        scan_type="port_scan", source="probe", tool="nmap",
        recorded_at=TS, initial=True, source_host="10.0.0.5")
    assert _artifact_of(evidence)[1].sha256_verified is True

    finding = SimpleNamespace(evidence=evidence, initial_detection_run_id=None,
                              detection_run_id=None)

    class _Rows:
        def scalars(self_inner): return self_inner
        def all(self_inner): return [finding]

    db = MagicMock()
    db.execute = AsyncMock(return_value=_Rows())
    db.flush = AsyncMock()
    await attach_detection_run_to_scan_findings(db, eng_id, scan_result_id, run_id)

    assert finding.evidence[SCAN_PROVENANCE_KEY]["latest"]["detection_run_id"] == str(run_id)
    assert _artifact_of(finding.evidence)[1].sha256_verified is True


# ── every producer path leaves a verifiable hash ─────────────────────────────

def test_record_scan_observation_stamps_probe_custody():
    evidence = record_scan_observation(
        {"proof": "x"}, scan_result_id=uuid.uuid4(), scan_job_id=uuid.uuid4(),
        scan_type="tls_scan", source="probe", tool="testssl",
        recorded_at=TS, initial=True, source_host="10.0.0.9")
    norm, art = _artifact_of(evidence)
    assert art.sha256_verified is True
    assert art.captured_by == CUSTODY_CAPTURED_BY_PROBE
    assert art.source_host == "10.0.0.9"
    assert _INTEGRITY_GAPS.isdisjoint(norm.gaps), norm.gaps


@pytest.mark.parametrize("kind", ["nuclei", "import", "ad"])
def test_manager_side_scanners_stamp_manager_custody(kind):
    job_id, eng_id = uuid.uuid4(), uuid.uuid4()
    if kind == "nuclei":
        finding = _nuclei_finding(
            eng_id, {"title": "N", "severity": "high",
                     "evidence": {"x": 1}, "host": "10.0.0.7"},
            scan_job_id=job_id, recorded_at=TS)
        expect_host = "10.0.0.7"
    elif kind == "import":
        finding = _import_finding(
            eng_id, FindingImport(title="I", severity="medium", evidence={"x": 1}),
            scan_job_id=job_id, recorded_at=TS)
        expect_host = None
    else:
        finding = _ad_finding(
            eng_id, {"title": "A", "severity": "critical", "evidence": {"x": 1}},
            scan_job_id=job_id, recorded_at=TS, source_host="10.0.0.1")
        expect_host = "10.0.0.1"

    norm, art = _artifact_of(finding.evidence)
    assert art.sha256_verified is True
    assert art.captured_by == CUSTODY_CAPTURED_BY_MANAGER
    assert art.source_host == expect_host
    assert _INTEGRITY_GAPS.isdisjoint(norm.gaps), norm.gaps


def test_detection_engine_findings_are_stamped_for_the_manager():
    """CVE/posture/attack-path findings record lineage in DB columns, never an
    evidence provenance block, so they never pass through record_scan_observation.
    The run's custody pass must still leave each one a verifiable hash, with the
    manager as custodian and the rule's asset as the scanned host."""
    cve = SimpleNamespace(evidence={"cve_id": "CVE-2021-1", "asset_ip": "10.0.0.2",
                                    "scanner": "version_cpe"})
    posture = SimpleNamespace(evidence={"rule_id": "POSTURE-EXPOSED-CLEARTEXT",
                                        "asset_ip": "10.0.0.3", "port": 23})
    path = SimpleNamespace(evidence={"rule_id": "PATH-NTLM-RELAY", "correlation": True})
    EB._stamp_chain_of_custody([cve, posture, path], TS)

    for f in (cve, posture, path):
        norm, art = _artifact_of(f.evidence)
        assert art.sha256_verified is True, f.evidence
        assert art.captured_by == CUSTODY_CAPTURED_BY_MANAGER
        assert _INTEGRITY_GAPS.isdisjoint(norm.gaps), norm.gaps
    assert normalize_evidence(cve.evidence).artifacts[0].source_host == "10.0.0.2"
    assert normalize_evidence(posture.evidence).artifacts[0].source_host == "10.0.0.3"


def test_detection_custody_pass_never_raises_on_a_bad_finding():
    # A finding whose evidence is not a dict must not sink the run's custody pass.
    bad = SimpleNamespace(evidence=None)
    good = SimpleNamespace(evidence={"cve_id": "CVE-2021-2", "asset_ip": "10.0.0.4"})
    EB._stamp_chain_of_custody([bad, good], TS)
    assert normalize_evidence(good.evidence).artifacts[0].sha256_verified is True
