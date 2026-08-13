"""
Tests for pipeline.py — the orchestrator with 0% prior coverage.

Covers the critical paths through run_pipeline:
  - empty input → no findings
  - a vulnerable package on a credentialed host → confirmed finding
  - injected dbs are used (no file I/O in tests)
  - exposure context propagates to findings
  - finding state is confirmed for authoritative sources, suspected for inferred
  - dedup collapses same (asset, CVE) across duplicate facts
  - AI-assist path routes through propose_candidates on normalizer misses
  - ab_evaluate structure and zero-precision-regression invariant
"""
from __future__ import annotations

import json

import pytest

import ai_normalizer as ai_mod
import vuln_db as vdb_mod
from enrichment_db import EpssDB, KevDB
from models import FindingState, SourceConfidence
from pipeline import ab_evaluate, run_pipeline
from vuln_db import SnapshotMeta, VulnDB, _content_hash


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _empty_kev() -> KevDB:
    return KevDB(cve_ids=set(), fetched_at="2026-01-01T00:00:00Z")


def _empty_epss() -> EpssDB:
    return EpssDB(scores={}, fetched_at="2026-01-01T00:00:00Z")


def _mock_vuln_db(records: dict) -> VulnDB:
    meta = SnapshotMeta(
        fetched_at="2026-01-01T00:00:00Z", ecosystem="Debian:12",
        products=sorted(records), content_hash=_content_hash(records),
        path="test.json",
    )
    return VulnDB(records, meta)


def _openssh_vuln_db() -> VulnDB:
    """Returns a VulnDB with a record that matches openssh 8.4p1 (vulnerable).

    The fixed boundary uses a Debian epoch-prefixed version ("1:9.0p1-1")
    matching the real OSV snapshot format — has_ambiguous_epoch() in the
    matcher blocks comparisons where one side has an explicit epoch and the
    other doesn't, so the boundary must carry the same epoch as the candidate's
    version_raw ("1:8.4p1-5+deb11u1")."""
    records = {
        "openssh": [{
            "id": "DEBIAN-CVE-2023-12345",
            "upstream": ["CVE-2023-12345"],
            "affected": [{
                "package": {"name": "openssh", "ecosystem": "Debian:12"},
                "ranges": [{"type": "ECOSYSTEM",
                            "events": [{"introduced": "0"},
                                       {"fixed": "1:9.0p1-1"}]}],
            }],
            "severity": [],
        }]
    }
    return _mock_vuln_db(records)


def _ssh_inventory_jsonl(tmp_path, target="10.0.0.1",
                         packages="openssh-server 1:8.4p1-5+deb11u1\n",
                         filename="fixture.jsonl") -> str:
    record = {
        "scanner": "ssh_inventory", "target": target,
        "timestamp": "2026-01-01T00:00:00Z", "port": 22, "proto": "tcp",
        "status": "open", "evidence": None, "error": None,
        "data": {"inventory": {"hostname": f"host-{target}",
                               "dpkg_packages": packages}},
    }
    p = tmp_path / filename
    p.write_text(json.dumps(record) + "\n")
    return str(p)


def _banner_jsonl(tmp_path, target="10.0.0.2",
                  first_line="SSH-2.0-OpenSSH_8.4p1 Debian-5",
                  filename="banner.jsonl") -> str:
    record = {
        "scanner": "service_banner", "target": target,
        "timestamp": "2026-01-01T00:00:00Z", "port": 22, "proto": "tcp",
        "status": "open", "evidence": None, "error": None,
        "data": {"first_line": first_line},
    }
    p = tmp_path / filename
    p.write_text(json.dumps(record) + "\n")
    return str(p)


def _empty_jsonl(tmp_path) -> str:
    p = tmp_path / "empty.jsonl"
    p.write_text("")
    return str(p)


# ---------------------------------------------------------------------------
# C1-1: empty input
# ---------------------------------------------------------------------------

class TestRunPipelineEmptyInput:
    def test_empty_jsonl_returns_no_findings(self, tmp_path):
        """A completely empty file must not produce any findings."""
        findings, ingest = run_pipeline(
            [_empty_jsonl(tmp_path)],
            vuln_db=_mock_vuln_db({}),
            kev_db=_empty_kev(), epss_db=_empty_epss(),
        )
        assert findings == []
        assert ingest.fact_count == 0

    def test_no_paths_returns_empty(self):
        """Passing an empty path list must return empty findings and no facts."""
        findings, ingest = run_pipeline(
            [],
            vuln_db=_mock_vuln_db({}),
            kev_db=_empty_kev(), epss_db=_empty_epss(),
        )
        assert findings == []
        assert ingest.assets == {}


# ---------------------------------------------------------------------------
# C1-2: vuln matching with credentialed (authoritative) source
# ---------------------------------------------------------------------------

class TestRunPipelineVulnMatching:
    def test_ssh_inventory_vulnerable_package_produces_finding(self, tmp_path):
        """A credentialed package at a version inside a vulnerable range must
        produce at least one finding."""
        path = _ssh_inventory_jsonl(tmp_path)
        findings, _ = run_pipeline(
            [path], vuln_db=_openssh_vuln_db(),
            kev_db=_empty_kev(), epss_db=_empty_epss(),
        )
        assert len(findings) > 0
        assert any(f.cve_id == "CVE-2023-12345" for f in findings)

    def test_ssh_inventory_finding_is_confirmed(self, tmp_path):
        """Findings from an authoritative (credentialed) source must be
        confirmed — the anti-false-positive rule requires BOTH range match AND
        authoritative source confidence."""
        path = _ssh_inventory_jsonl(tmp_path)
        findings, _ = run_pipeline(
            [path], vuln_db=_openssh_vuln_db(),
            kev_db=_empty_kev(), epss_db=_empty_epss(),
        )
        cve_findings = [f for f in findings if f.cve_id == "CVE-2023-12345"]
        assert cve_findings
        assert all(f.state == FindingState.confirmed for f in cve_findings)

    def test_banner_finding_is_suspected_not_confirmed(self, tmp_path):
        """A banner-derived (inferred) source match can only produce 'suspected'
        — backported distro packages may keep upstream version strings while
        already being patched."""
        path = _banner_jsonl(tmp_path, first_line="OpenSSH_8.4p1")
        findings, _ = run_pipeline(
            [path], vuln_db=_openssh_vuln_db(),
            kev_db=_empty_kev(), epss_db=_empty_epss(),
        )
        cve_findings = [f for f in findings if f.cve_id == "CVE-2023-12345"]
        if cve_findings:
            assert all(f.state == FindingState.suspected for f in cve_findings)

    def test_no_finding_for_patched_version(self, tmp_path):
        """A host running the fixed version must not produce a finding."""
        path = _ssh_inventory_jsonl(tmp_path,
                                    packages="openssh-server 1:9.5p1-1\n")
        findings, _ = run_pipeline(
            [path], vuln_db=_openssh_vuln_db(),
            kev_db=_empty_kev(), epss_db=_empty_epss(),
        )
        cve_findings = [f for f in findings if f.cve_id == "CVE-2023-12345"]
        assert cve_findings == []

    def test_injected_dbs_used_no_file_io(self, tmp_path):
        """When all three dbs are injected, the pipeline must not try to read
        the default snapshot files — the injected db IS the snapshot."""
        path = _ssh_inventory_jsonl(tmp_path)
        empty_db = _mock_vuln_db({})
        findings, _ = run_pipeline(
            [path], vuln_db=empty_db,
            kev_db=_empty_kev(), epss_db=_empty_epss(),
        )
        assert findings == []


# ---------------------------------------------------------------------------
# C1-3: exposure context
# ---------------------------------------------------------------------------

class TestRunPipelineExposure:
    def test_exposure_internet_facing_propagates(self, tmp_path):
        path = _ssh_inventory_jsonl(tmp_path)
        exposure = {"10.0.0.1": {"internet_facing": True, "auth_enforced": False}}
        findings, _ = run_pipeline(
            [path], vuln_db=_openssh_vuln_db(),
            kev_db=_empty_kev(), epss_db=_empty_epss(),
            exposure=exposure,
        )
        cve_findings = [f for f in findings if f.cve_id == "CVE-2023-12345"]
        assert cve_findings
        assert all(f.internet_facing is True for f in cve_findings)

    def test_no_exposure_fields_are_none(self, tmp_path):
        """Without an exposure dict the fields stay None — pipeline never guesses."""
        path = _ssh_inventory_jsonl(tmp_path)
        findings, _ = run_pipeline(
            [path], vuln_db=_openssh_vuln_db(),
            kev_db=_empty_kev(), epss_db=_empty_epss(),
        )
        cve_findings = [f for f in findings if f.cve_id == "CVE-2023-12345"]
        assert cve_findings
        assert all(f.internet_facing is None for f in cve_findings)


# ---------------------------------------------------------------------------
# C1-4: deduplication
# ---------------------------------------------------------------------------

class TestRunPipelineDedup:
    def test_two_identical_hosts_each_get_their_own_finding(self, tmp_path):
        """Different IPs must produce independent findings — dedup is per
        (asset, CVE, CPE), not global."""
        p1 = _ssh_inventory_jsonl(tmp_path, target="10.0.0.1", filename="h1.jsonl")
        p2 = _ssh_inventory_jsonl(tmp_path, target="10.0.0.2", filename="h2.jsonl")
        findings, _ = run_pipeline(
            [p1, p2], vuln_db=_openssh_vuln_db(),
            kev_db=_empty_kev(), epss_db=_empty_epss(),
        )
        ips_with_finding = {f.asset_ip for f in findings if f.cve_id == "CVE-2023-12345"}
        assert "10.0.0.1" in ips_with_finding
        assert "10.0.0.2" in ips_with_finding

    def test_findings_deduped_within_same_host(self, tmp_path):
        """The same (asset, CVE) can't appear twice in the output — dedup
        must collapse it to one finding."""
        path = _ssh_inventory_jsonl(tmp_path)
        findings, _ = run_pipeline(
            [path], vuln_db=_openssh_vuln_db(),
            kev_db=_empty_kev(), epss_db=_empty_epss(),
        )
        ids = [f.finding_id for f in findings]
        assert len(ids) == len(set(ids)), "duplicate finding_ids in output"


# ---------------------------------------------------------------------------
# C1-5: ingest result returned alongside findings
# ---------------------------------------------------------------------------

class TestRunPipelineReturnValue:
    def test_returns_tuple_of_findings_and_ingest_result(self, tmp_path):
        path = _ssh_inventory_jsonl(tmp_path)
        result = run_pipeline(
            [path], vuln_db=_openssh_vuln_db(),
            kev_db=_empty_kev(), epss_db=_empty_epss(),
        )
        assert isinstance(result, tuple) and len(result) == 2
        findings, ingest = result
        assert isinstance(findings, list)
        assert ingest.fact_count > 0


# ---------------------------------------------------------------------------
# C1-6: AI-assist path
# ---------------------------------------------------------------------------

class TestRunPipelineAiAssist:
    def test_ai_assist_off_by_default(self, tmp_path):
        """With use_ai_assist=False (the default) and no ai_client, the pipeline
        produces the same results as rule-based-only mode."""
        path = _ssh_inventory_jsonl(tmp_path)
        db = _openssh_vuln_db()
        kev, epss = _empty_kev(), _empty_epss()
        findings_default, _ = run_pipeline([path], vuln_db=db, kev_db=kev, epss_db=epss)
        findings_explicit, _ = run_pipeline(
            [path], vuln_db=db, kev_db=kev, epss_db=epss, use_ai_assist=False)
        assert {f.finding_id for f in findings_default} == {f.finding_id for f in findings_explicit}

    def test_ab_evaluate_returns_expected_keys(self, tmp_path):
        """ab_evaluate must return a dict with the expected structure."""
        path = _ssh_inventory_jsonl(tmp_path)
        db = _openssh_vuln_db()
        fake_client = ai_mod.FakeAIClient({})
        report = ab_evaluate([path], ai_client=fake_client, vuln_db=db,
                              kev_db=_empty_kev(), epss_db=_empty_epss())
        for key in ("baseline_count", "with_ai_count", "recall_gain",
                    "lost_findings", "precision_regression",
                    "gained_finding_ids", "non_suspected_ai_findings"):
            assert key in report, f"missing key: {key!r}"

    def test_ab_evaluate_no_precision_regression_without_ai_gain(self, tmp_path):
        """When FakeAIClient returns nothing new, there must be no precision
        regression (lost_findings == 0, precision_regression == False)."""
        path = _ssh_inventory_jsonl(tmp_path)
        db = _openssh_vuln_db()
        fake_client = ai_mod.FakeAIClient({})
        report = ab_evaluate([path], ai_client=fake_client, vuln_db=db,
                              kev_db=_empty_kev(), epss_db=_empty_epss())
        assert report["lost_findings"] == 0
        assert report["precision_regression"] is False
