"""
Detection engine test suite — unit tests for the core detection/correlation
pipeline modules. Covers: models, ingest, cvss, matcher, correlate, verifier,
cpe_normalizer, enrichment, vuln_db, consistency, and pipeline integration.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from models import (
    Asset, Fact, Finding, FindingState, SourceConfidence, make_finding_id,
)
from ingest import ingest_file, ingest_files, IngestResult, _validate, _classify_confidence, _is_ip
from cvss import base_score, parse_vector, _roundup
from matcher import _version_in_ranges, _safe_compare, match_candidate
from correlate import dedup_findings, suppress_negated, correlate_smb_patch, _product_from_cpe
from verifier import classify_tier, deception_score, verify, EvidenceTier
from enrichment import _compute_priority, enrich_finding
from enrichment_db import KevDB, EpssDB
from consistency import wilson_ci, aggregate, FindingConsistency, ConsistencyReport
from cpe_normalizer import (
    CPECandidate, normalize, normalize_banner, normalize_web, normalize_db,
    clean_debian_version, clean_rpm_version, all_osv_source_packages,
)
from vuln_db import VulnDB, SnapshotMeta, _content_hash


def _fact(scanner="service_banner", target="10.0.0.1", port=22,
          data=None, source_confidence=SourceConfidence.inferred,
          source_file="test.jsonl", source_line=1, **kw):
    return Fact(
        scanner=scanner, target=target, timestamp=kw.get("timestamp", "2026-01-01T00:00:00Z"),
        port=port, proto=kw.get("proto", "tcp"), status=kw.get("status", "open"),
        data=data or {}, evidence=kw.get("evidence"), error=kw.get("error"),
        source_confidence=source_confidence,
        source_file=source_file, source_line=source_line,
    )


def _candidate(version="1.0", lookup_key="openssh", vendor="openbsd",
               product="openssh", source_confidence=SourceConfidence.inferred,
               basis="banner", source_ref="test.jsonl:1", ai_assisted=False):
    return CPECandidate(
        vendor=vendor, product=product,
        version_raw=version, version_normalized=version,
        confidence="high", source_confidence=source_confidence,
        basis=basis, source_ref=source_ref,
        lookup_key=lookup_key, ai_assisted=ai_assisted,
    )


def _finding(cve_id="CVE-2023-0001", asset_ip="10.0.0.1",
             cpe="cpe:2.3:a:vendor:product:1.0:*:*:*:*:*:*:*",
             state=FindingState.suspected,
             source_confidence=SourceConfidence.inferred,
             evidence_refs=None, notes=None, **kw):
    return Finding(
        finding_id=kw.get("finding_id", make_finding_id(asset_ip, cve_id, cpe)),
        asset_ip=asset_ip, cpe=cpe, cve_id=cve_id,
        match_basis=kw.get("match_basis", "range"),
        state=state, source_confidence=source_confidence,
        evidence_refs=evidence_refs or ["test.jsonl:1"],
        db_snapshot_hash=kw.get("db_snapshot_hash", "abc123"),
        created_at=kw.get("created_at", datetime.now(timezone.utc).isoformat()),
        matched_version=kw.get("matched_version", "1.0"),
        ai_assisted=kw.get("ai_assisted", False),
        notes=notes or [],
    )


def _mock_vuln_db(records=None):
    if records is None:
        records = {}
    meta = SnapshotMeta(
        fetched_at="2026-01-01T00:00:00Z", ecosystem="Debian:12",
        products=list(records.keys()), content_hash=_content_hash(records),
        path="test.json",
    )
    return VulnDB(records, meta)


def _mock_kev_db(cve_ids=None):
    return KevDB(cve_ids=cve_ids or set(), fetched_at="2026-01-01T00:00:00Z")


def _mock_epss_db(scores=None):
    return EpssDB(scores=scores or {}, fetched_at="2026-01-01T00:00:00Z")


# ═══════════════════════════════════════════════════════════════════════════
# models.py
# ═══════════════════════════════════════════════════════════════════════════

class TestMakeFindingId:
    def test_deterministic(self):
        a = make_finding_id("10.0.0.1", "CVE-2023-0001", "cpe:2.3:a:v:p:1.0")
        b = make_finding_id("10.0.0.1", "CVE-2023-0001", "cpe:2.3:a:v:p:1.0")
        assert a == b

    def test_different_inputs_different_ids(self):
        a = make_finding_id("10.0.0.1", "CVE-2023-0001", "cpe:a")
        b = make_finding_id("10.0.0.2", "CVE-2023-0001", "cpe:a")
        assert a != b

    def test_length_16(self):
        assert len(make_finding_id("1.2.3.4", "CVE-1", "cpe:x")) == 16


class TestFindingPostInit:
    def test_refuses_zero_evidence_refs(self):
        with pytest.raises(ValueError, match="zero evidence_refs"):
            Finding(
                finding_id="test", asset_ip="10.0.0.1", cpe="cpe:a",
                cve_id="CVE-1", match_basis="range", state=FindingState.suspected,
                source_confidence=SourceConfidence.inferred, evidence_refs=[],
                db_snapshot_hash="x", created_at="2026-01-01", matched_version="1.0",
            )

    def test_accepts_nonempty_evidence_refs(self):
        f = _finding(evidence_refs=["a.jsonl:1"])
        assert f.evidence_refs == ["a.jsonl:1"]


class TestAsset:
    def test_add_fact_updates_first_last_seen(self):
        a = Asset(ip="10.0.0.1")
        a.add_fact(_fact(timestamp="2026-01-01T00:00:00Z"))
        a.add_fact(_fact(timestamp="2026-06-01T00:00:00Z"))
        assert a.first_seen == "2026-01-01T00:00:00Z"
        assert a.last_seen == "2026-06-01T00:00:00Z"

    def test_facts_by_scanner(self):
        a = Asset(ip="10.0.0.1")
        a.add_fact(_fact(scanner="tls_scan"))
        a.add_fact(_fact(scanner="web_scan"))
        a.add_fact(_fact(scanner="tls_scan"))
        assert len(a.facts_by_scanner("tls_scan")) == 2

    def test_open_ports(self):
        a = Asset(ip="10.0.0.1")
        a.add_fact(_fact(port=22, status="open"))
        a.add_fact(_fact(port=80, status="closed"))
        a.add_fact(_fact(port=443, status="open"))
        assert a.open_ports() == [22, 443]

    def test_as_of_cutoff(self):
        a = Asset(ip="10.0.0.1")
        a.add_fact(_fact(timestamp="2026-01-01T00:00:00Z"))
        a.add_fact(_fact(timestamp="2026-06-01T00:00:00Z"))
        snap = a.as_of("2026-03-01T00:00:00Z")
        assert len(snap.facts) == 1

    def test_add_alias(self):
        a = Asset(ip="10.0.0.1")
        a.add_alias("web01.example.com")
        a.add_alias(None)
        a.add_alias("")
        assert "web01.example.com" in a.aliases
        assert len(a.aliases) == 1


class TestFindingToDict:
    def test_enums_serialized_to_values(self):
        f = _finding()
        d = f.to_dict()
        assert d["state"] == "suspected"
        assert d["source_confidence"] == "inferred"


class TestFactRef:
    def test_ref_format(self):
        f = _fact(source_file="scan.jsonl", source_line=42)
        assert f.ref() == "scan.jsonl:42"


# ═══════════════════════════════════════════════════════════════════════════
# ingest.py
# ═══════════════════════════════════════════════════════════════════════════

class TestIngestValidation:
    def test_valid_record(self):
        assert _validate({"scanner": "s", "target": "1.2.3.4", "timestamp": "t", "status": "open"}) is None

    def test_missing_required_field(self):
        r = _validate({"scanner": "s", "target": "1.2.3.4"})
        assert r is not None and "missing" in r

    def test_non_dict_record(self):
        assert _validate("not a dict") is not None

    def test_empty_target(self):
        assert _validate({"scanner": "s", "target": "", "timestamp": "t", "status": "open"}) is not None

    def test_port_not_int(self):
        assert _validate({"scanner": "s", "target": "1.2.3.4", "timestamp": "t", "status": "open", "port": "abc"}) is not None


class TestClassifyConfidence:
    def test_authoritative_scanners(self):
        assert _classify_confidence("ssh_inventory") == SourceConfidence.authoritative
        assert _classify_confidence("windows_inventory") == SourceConfidence.authoritative

    def test_inferred_scanners(self):
        assert _classify_confidence("service_banner") == SourceConfidence.inferred
        assert _classify_confidence("tls_scan") == SourceConfidence.inferred


class TestIsIp:
    def test_valid_ipv4(self):
        assert _is_ip("10.0.0.1") is True

    def test_hostname(self):
        assert _is_ip("web01.example.com") is False


class TestIngestFile:
    def test_valid_jsonl(self, tmp_path):
        p = tmp_path / "test.jsonl"
        p.write_text(json.dumps({
            "scanner": "service_banner", "target": "10.0.0.1",
            "timestamp": "2026-01-01T00:00:00Z", "status": "open", "port": 22,
        }) + "\n")
        result = ingest_file(str(p))
        assert result.fact_count == 1
        assert "10.0.0.1" in result.assets

    def test_quarantines_malformed(self, tmp_path):
        p = tmp_path / "bad.jsonl"
        p.write_text("not-json\n")
        result = ingest_file(str(p))
        assert len(result.quarantined) == 1
        assert result.fact_count == 0

    def test_empty_file(self, tmp_path):
        p = tmp_path / "empty.jsonl"
        p.write_text("")
        result = ingest_file(str(p))
        assert result.fact_count == 0
        assert len(result.quarantined) == 0

    def test_multi_file_accumulation(self, tmp_path):
        for i in range(3):
            p = tmp_path / f"f{i}.jsonl"
            p.write_text(json.dumps({
                "scanner": "s", "target": "10.0.0.1",
                "timestamp": "2026-01-01T00:00:00Z", "status": "open",
            }) + "\n")
        result = ingest_files([str(tmp_path / f"f{i}.jsonl") for i in range(3)])
        assert result.fact_count == 3

    def test_authoritative_scanner_creates_authoritative_fact(self, tmp_path):
        p = tmp_path / "inv.jsonl"
        p.write_text(json.dumps({
            "scanner": "ssh_inventory", "target": "10.0.0.1",
            "timestamp": "2026-01-01T00:00:00Z", "status": "open",
        }) + "\n")
        result = ingest_file(str(p))
        fact = result.assets["10.0.0.1"].facts[0]
        assert fact.source_confidence == SourceConfidence.authoritative

    def test_hostname_target_not_ip_keyed(self, tmp_path):
        p = tmp_path / "host.jsonl"
        p.write_text(json.dumps({
            "scanner": "s", "target": "web01.example.com",
            "timestamp": "2026-01-01T00:00:00Z", "status": "open",
        }) + "\n")
        result = ingest_file(str(p))
        assert "web01.example.com" in result.assets
        assert result.assets["web01.example.com"].is_ip_keyed is False


# ═══════════════════════════════════════════════════════════════════════════
# cvss.py
# ═══════════════════════════════════════════════════════════════════════════

class TestCvss:
    @pytest.mark.parametrize("vector,expected", [
        ("AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", 9.8),
        ("AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H", 10.0),
        ("AV:L/AC:H/PR:H/UI:R/S:U/C:N/I:N/A:N", 0.0),
    ])
    def test_known_vectors(self, vector, expected):
        score = base_score(vector)
        assert score is not None
        assert abs(score - expected) < 0.1

    def test_returns_none_for_v2_vector(self):
        assert base_score("AV:N/AC:L/Au:N/C:P/I:P/A:P") is None

    def test_returns_none_for_malformed(self):
        assert base_score("") is None
        assert base_score("gibberish") is None

    def test_parse_vector(self):
        m = parse_vector("AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H")
        assert m["AV"] == "N"
        assert m["S"] == "U"

    def test_roundup_exact_boundary(self):
        assert _roundup(7.0) == 7.0
        assert _roundup(7.01) == 7.1


# ═══════════════════════════════════════════════════════════════════════════
# matcher.py
# ═══════════════════════════════════════════════════════════════════════════

class TestVersionInRanges:
    def test_introduced_fixed(self):
        ranges = [{"type": "ECOSYSTEM", "events": [
            {"introduced": "1.0"}, {"fixed": "2.0"}
        ]}]
        matched, desc = _version_in_ranges("1.5", ranges)
        assert matched is True
        assert "1.0" in desc and "2.0" in desc

    def test_version_before_introduced(self):
        ranges = [{"type": "ECOSYSTEM", "events": [
            {"introduced": "2.0"}, {"fixed": "3.0"}
        ]}]
        matched, _ = _version_in_ranges("1.0", ranges)
        assert matched is False

    def test_version_at_fixed(self):
        ranges = [{"type": "ECOSYSTEM", "events": [
            {"introduced": "1.0"}, {"fixed": "2.0"}
        ]}]
        matched, _ = _version_in_ranges("2.0", ranges)
        assert matched is False

    def test_last_affected(self):
        ranges = [{"type": "ECOSYSTEM", "events": [
            {"introduced": "1.0"}, {"last_affected": "2.0"}
        ]}]
        matched, desc = _version_in_ranges("2.0", ranges)
        assert matched is True
        assert "2.0" in desc

    def test_unbounded_introduced(self):
        ranges = [{"type": "ECOSYSTEM", "events": [
            {"introduced": "1.0"}
        ]}]
        matched, desc = _version_in_ranges("99.0", ranges)
        assert matched is True
        assert "unbounded" in desc

    def test_ignores_unknown_type(self):
        ranges = [{"type": "GIT", "events": [
            {"introduced": "1.0"}, {"fixed": "2.0"}
        ]}]
        matched, _ = _version_in_ranges("1.5", ranges)
        assert matched is False

    def test_semver_type_included(self):
        ranges = [{"type": "SEMVER", "events": [
            {"introduced": "1.0.0"}, {"fixed": "2.0.0"}
        ]}]
        matched, _ = _version_in_ranges("1.5.0", ranges)
        assert matched is True

    def test_no_match_returns_false_none(self):
        ranges = [{"type": "ECOSYSTEM", "events": [
            {"introduced": "5.0"}, {"fixed": "6.0"}
        ]}]
        matched, desc = _version_in_ranges("1.0", ranges)
        assert matched is False
        assert desc is None

    def test_empty_ranges(self):
        matched, desc = _version_in_ranges("1.0", [])
        assert matched is False
        assert desc is None

    def test_regression_sequence(self):
        ranges = [{"type": "ECOSYSTEM", "events": [
            {"introduced": "1.0"}, {"fixed": "2.0"},
            {"introduced": "3.0"}, {"fixed": "4.0"},
        ]}]
        matched, _ = _version_in_ranges("1.5", ranges)
        assert matched is True
        matched2, _ = _version_in_ranges("2.5", ranges)
        assert matched2 is False
        matched3, _ = _version_in_ranges("3.5", ranges)
        assert matched3 is True


class TestMatchCandidate:
    def test_no_version_returns_empty(self):
        c = _candidate(version="")
        c.version_raw = None
        c.version_normalized = None
        db = _mock_vuln_db()
        assert match_candidate("10.0.0.1", c, db) == []

    def test_unknown_product_returns_empty(self):
        c = _candidate(lookup_key="nonexistent_product")
        db = _mock_vuln_db()
        assert match_candidate("10.0.0.1", c, db) == []

    def test_match_produces_finding(self):
        records = {"openssh": [{
            "id": "OSV-1", "upstream": ["CVE-2023-0001"],
            "affected": [{"package": {"name": "openssh"}, "ranges": [
                {"type": "ECOSYSTEM", "events": [
                    {"introduced": "1.0"}, {"fixed": "9.0"}
                ]}
            ]}]
        }]}
        db = _mock_vuln_db(records)
        c = _candidate(version="8.0", lookup_key="openssh")
        findings = match_candidate("10.0.0.1", c, db)
        assert len(findings) == 1
        assert findings[0].cve_id == "CVE-2023-0001"
        assert findings[0].state == FindingState.suspected

    def test_authoritative_source_confirms(self):
        records = {"openssh": [{
            "id": "OSV-1", "upstream": ["CVE-2023-0001"],
            "affected": [{"package": {"name": "openssh"}, "ranges": [
                {"type": "ECOSYSTEM", "events": [
                    {"introduced": "1.0"}, {"fixed": "9.0"}
                ]}
            ]}]
        }]}
        db = _mock_vuln_db(records)
        c = _candidate(version="8.0", lookup_key="openssh",
                        source_confidence=SourceConfidence.authoritative)
        findings = match_candidate("10.0.0.1", c, db)
        assert findings[0].state == FindingState.confirmed

    def test_inferred_match_has_backport_note(self):
        records = {"nginx": [{
            "id": "OSV-2", "upstream": ["CVE-2023-0002"],
            "affected": [{"package": {"name": "nginx"}, "ranges": [
                {"type": "ECOSYSTEM", "events": [
                    {"introduced": "1.0"}, {"fixed": "2.0"}
                ]}
            ]}]
        }]}
        db = _mock_vuln_db(records)
        c = _candidate(version="1.5", lookup_key="nginx", product="nginx")
        findings = match_candidate("10.0.0.1", c, db)
        assert any("backport-possible" in n for n in findings[0].notes)

    def test_no_match_returns_empty(self):
        records = {"nginx": [{
            "id": "OSV-3", "upstream": ["CVE-2023-0003"],
            "affected": [{"package": {"name": "nginx"}, "ranges": [
                {"type": "ECOSYSTEM", "events": [
                    {"introduced": "5.0"}, {"fixed": "6.0"}
                ]}
            ]}]
        }]}
        db = _mock_vuln_db(records)
        c = _candidate(version="1.0", lookup_key="nginx", product="nginx")
        findings = match_candidate("10.0.0.1", c, db)
        assert findings == []

    def test_ai_assisted_carried_through(self):
        records = {"openssh": [{
            "id": "OSV-1", "upstream": ["CVE-2023-0001"],
            "affected": [{"package": {"name": "openssh"}, "ranges": [
                {"type": "ECOSYSTEM", "events": [
                    {"introduced": "1.0"}, {"fixed": "9.0"}
                ]}
            ]}]
        }]}
        db = _mock_vuln_db(records)
        c = _candidate(version="8.0", lookup_key="openssh", ai_assisted=True)
        findings = match_candidate("10.0.0.1", c, db)
        assert findings[0].ai_assisted is True
        assert any("AI-assisted" in n for n in findings[0].notes)


# ═══════════════════════════════════════════════════════════════════════════
# correlate.py
# ═══════════════════════════════════════════════════════════════════════════

class TestDedupFindings:
    def test_merges_same_id(self):
        fid = make_finding_id("10.0.0.1", "CVE-1", "cpe:a")
        f1 = _finding(finding_id=fid, evidence_refs=["a.jsonl:1"], notes=["x"])
        f2 = _finding(finding_id=fid, evidence_refs=["b.jsonl:2"], notes=["y"])
        merged = dedup_findings([f1, f2])
        assert len(merged) == 1
        assert "b.jsonl:2" in merged[0].evidence_refs
        assert "y" in merged[0].notes

    def test_authoritative_upgrades_state(self):
        fid = make_finding_id("10.0.0.1", "CVE-1", "cpe:a")
        f1 = _finding(finding_id=fid, state=FindingState.suspected,
                       source_confidence=SourceConfidence.inferred)
        f2 = _finding(finding_id=fid, state=FindingState.confirmed,
                       source_confidence=SourceConfidence.authoritative)
        merged = dedup_findings([f1, f2])
        assert merged[0].state == FindingState.confirmed
        assert merged[0].source_confidence == SourceConfidence.authoritative

    def test_different_ids_preserved(self):
        findings = [_finding(cve_id=f"CVE-{i}") for i in range(3)]
        merged = dedup_findings(findings)
        assert len(merged) == 3

    def test_evidence_refs_dedup_preserving_order(self):
        fid = make_finding_id("10.0.0.1", "CVE-1", "cpe:a")
        f1 = _finding(finding_id=fid, evidence_refs=["a:1", "b:2"], notes=[])
        f2 = _finding(finding_id=fid, evidence_refs=["a:1", "c:3"], notes=[])
        merged = dedup_findings([f1, f2])
        assert merged[0].evidence_refs == ["a:1", "b:2", "c:3"]


class TestSuppressNegated:
    def test_suppresses_inferred_when_authoritative_contradicts(self):
        f = _finding(state=FindingState.suspected,
                     source_confidence=SourceConfidence.inferred,
                     matched_version="1.0", cve_id="CVE-1",
                     cpe="cpe:2.3:a:vendor:product:1.0:*:*:*:*:*:*:*")
        auth_cand = _candidate(version="2.0", vendor="vendor", product="product",
                               source_confidence=SourceConfidence.authoritative)
        out = suppress_negated([f], {"10.0.0.1": [auth_cand]})
        assert len(out) == 0

    def test_keeps_authoritative_finding(self):
        f = _finding(state=FindingState.confirmed,
                     source_confidence=SourceConfidence.authoritative,
                     matched_version="1.0")
        out = suppress_negated([f], {})
        assert len(out) == 1

    def test_keeps_inferred_when_no_authoritative(self):
        f = _finding(state=FindingState.suspected,
                     source_confidence=SourceConfidence.inferred,
                     matched_version="1.0")
        out = suppress_negated([f], {"10.0.0.1": []})
        assert len(out) == 1

    def test_keeps_inferred_when_auth_version_lower(self):
        f = _finding(state=FindingState.suspected,
                     source_confidence=SourceConfidence.inferred,
                     matched_version="3.0",
                     cpe="cpe:2.3:a:vendor:product:3.0:*:*:*:*:*:*:*")
        auth_cand = _candidate(version="2.0", vendor="vendor", product="product",
                               source_confidence=SourceConfidence.authoritative)
        out = suppress_negated([f], {"10.0.0.1": [auth_cand]})
        assert len(out) == 1


class TestProductFromCpe:
    def test_extracts_product(self):
        assert _product_from_cpe("cpe:2.3:a:vendor:product:1.0:*:*:*:*:*:*:*") == "product"

    def test_short_cpe_returns_cpe(self):
        assert _product_from_cpe("cpe:2.3:a") == "cpe:2.3:a"


class TestCorrelateSmbPatch:
    def test_no_smb_facts_returns_none(self):
        a = Asset(ip="10.0.0.1")
        assert correlate_smb_patch(a) is None

    def test_smbv1_without_hotfix_data_returns_none(self):
        a = Asset(ip="10.0.0.1")
        a.add_fact(_fact(scanner="smb_scan", data={"smbv1_enabled": True}))
        assert correlate_smb_patch(a) is None

    def test_smbv1_with_missing_hotfixes_returns_finding(self):
        a = Asset(ip="10.0.0.1")
        a.add_fact(_fact(scanner="smb_scan", data={"smbv1_enabled": True}))
        a.add_fact(_fact(scanner="windows_inventory", data={
            "inventory": {"hotfixes": "KB123456 KB789012"}
        }))
        result = correlate_smb_patch(a)
        assert result is not None
        assert result.cve_id == "CVE-2017-0144"
        assert result.state == FindingState.suspected
        assert result.match_basis == "composite"

    def test_smbv1_with_patched_host_returns_none(self):
        a = Asset(ip="10.0.0.1")
        a.add_fact(_fact(scanner="smb_scan", data={"smbv1_enabled": True}))
        a.add_fact(_fact(scanner="windows_inventory", data={
            "inventory": {"hotfixes": "KB4012212 KB4012213 KB4012214 KB4012215 KB4012216 KB4012217 KB4012598"}
        }))
        assert correlate_smb_patch(a) is None


# ═══════════════════════════════════════════════════════════════════════════
# verifier.py
# ═══════════════════════════════════════════════════════════════════════════

class TestClassifyTier:
    def test_authoritative_tier4(self):
        f = _finding(source_confidence=SourceConfidence.authoritative)
        assert classify_tier(f) == EvidenceTier.authoritative_credentialed

    def test_protocol_scanner_tier3(self):
        f = _finding(source_confidence=SourceConfidence.inferred,
                     notes=["db_scan engine=mysql"])
        assert classify_tier(f) == EvidenceTier.protocol_confirmed

    def test_multi_signal_tier2(self):
        f = _finding(source_confidence=SourceConfidence.inferred,
                     evidence_refs=["a:1", "b:2"])
        assert classify_tier(f) == EvidenceTier.multi_signal_corroborated

    def test_single_banner_tier1(self):
        f = _finding(source_confidence=SourceConfidence.inferred,
                     evidence_refs=["a:1"])
        assert classify_tier(f) == EvidenceTier.single_banner_inferred


class TestDeceptionScore:
    def test_low_product_count(self):
        assert deception_score(3, False) == 0.0

    def test_moderate_product_count(self):
        assert 0.0 < deception_score(6, False) <= 0.5

    def test_high_product_count(self):
        assert deception_score(8, False) >= 0.5

    def test_contradictory_os(self):
        score = deception_score(2, True)
        assert score == 0.4

    def test_combined_high(self):
        assert deception_score(8, True) >= 0.9

    def test_capped_at_1(self):
        assert deception_score(20, True) <= 1.0


class TestVerify:
    def test_authoritative_tier_base_95(self):
        f = _finding(source_confidence=SourceConfidence.authoritative)
        result = verify(f)
        assert result.confidence == 95

    def test_protocol_tier_base_85(self):
        f = _finding(source_confidence=SourceConfidence.inferred,
                     notes=["db_scan engine=mysql"])
        result = verify(f)
        assert result.confidence == 85

    def test_backport_penalty(self):
        f = _finding(source_confidence=SourceConfidence.inferred,
                     notes=["version-inferred, backport-possible"],
                     evidence_refs=["a:1"])
        result = verify(f)
        assert result.confidence == 30  # 50 base - 20 backport

    def test_ai_cap_at_60(self):
        f = _finding(source_confidence=SourceConfidence.authoritative, ai_assisted=True)
        result = verify(f)
        assert result.confidence == 60

    def test_ai_no_cap_if_already_below(self):
        f = _finding(source_confidence=SourceConfidence.inferred,
                     notes=["version-inferred, backport-possible"],
                     evidence_refs=["a:1"], ai_assisted=True)
        result = verify(f)
        assert result.confidence == 30  # 50 base - 20 backport, ai cap at 60 but 30 < 60

    def test_filtered_port_penalty(self):
        f = _finding(source_confidence=SourceConfidence.authoritative)
        result = verify(f, reachability="filtered")
        assert result.confidence == 80  # 95 - 15

    def test_auth_enforced_penalty(self):
        f = _finding(source_confidence=SourceConfidence.authoritative)
        f.auth_enforced = True
        result = verify(f)
        assert result.confidence == 85  # 95 - 10

    def test_deception_high_penalty(self):
        f = _finding(source_confidence=SourceConfidence.authoritative)
        result = verify(f, deception=0.5)
        assert result.confidence == 70  # 95 - 25

    def test_deception_moderate_penalty(self):
        f = _finding(source_confidence=SourceConfidence.authoritative)
        result = verify(f, deception=0.25)
        assert result.confidence == 85  # 95 - 10

    def test_state_downgrade_below_40(self):
        f = _finding(state=FindingState.suspected,
                     source_confidence=SourceConfidence.inferred,
                     notes=["version-inferred, backport-possible"],
                     evidence_refs=["a:1"])
        result = verify(f)
        assert result.state == FindingState.potential  # 50 - 20 = 30 < 40

    def test_confirmed_never_downgraded(self):
        f = _finding(state=FindingState.confirmed,
                     source_confidence=SourceConfidence.authoritative)
        result = verify(f, deception=0.9)
        assert result.state == FindingState.confirmed

    def test_checks_dict_populated(self):
        f = _finding(source_confidence=SourceConfidence.inferred,
                     notes=["version-inferred, backport-possible"],
                     evidence_refs=["a:1"])
        result = verify(f)
        assert "evidence_tier" in result.checks
        assert "backport_possible" in result.checks
        assert result.evidence_reason is not None

    def test_confidence_clamped_at_zero(self):
        f = _finding(state=FindingState.suspected,
                     source_confidence=SourceConfidence.inferred,
                     notes=["version-inferred, backport-possible"],
                     evidence_refs=["a:1"])
        result = verify(f, reachability="filtered", deception=0.5)
        # 50 - 20 backport - 15 filtered - 25 deception = -10 -> clamp to 0
        assert result.confidence == 0


# ═══════════════════════════════════════════════════════════════════════════
# enrichment.py + enrichment_db.py
# ═══════════════════════════════════════════════════════════════════════════

class TestComputePriority:
    def test_kev_unauth_reachable_critical(self):
        f = _finding()
        f.kev = True
        f.internet_facing = True
        f.auth_enforced = False
        tier, reason = _compute_priority(f)
        assert tier == "critical"
        assert "KEV" in reason

    def test_kev_alone_critical(self):
        f = _finding()
        f.kev = True
        tier, reason = _compute_priority(f)
        assert tier == "critical"

    def test_high_epss_critical(self):
        f = _finding()
        f.epss_score = 0.6
        tier, reason = _compute_priority(f)
        assert tier == "critical"
        assert "EPSS" in reason

    def test_elevated_epss_high(self):
        f = _finding()
        f.epss_score = 0.15
        f.cvss_score = 9.0
        tier, _ = _compute_priority(f)
        assert tier == "high"

    def test_cvss_critical(self):
        f = _finding()
        f.cvss_score = 9.5
        tier, _ = _compute_priority(f)
        assert tier == "critical"

    def test_cvss_high(self):
        f = _finding()
        f.cvss_score = 7.5
        tier, _ = _compute_priority(f)
        assert tier == "high"

    def test_cvss_medium(self):
        f = _finding()
        f.cvss_score = 5.5
        tier, _ = _compute_priority(f)
        assert tier == "medium"

    def test_cvss_low(self):
        f = _finding()
        f.cvss_score = 2.0
        tier, _ = _compute_priority(f)
        assert tier == "low"

    def test_unknown_tier(self):
        f = _finding()
        tier, _ = _compute_priority(f)
        assert tier == "unknown"


class TestEnrichFinding:
    def test_enriches_cvss_from_vuln_db(self):
        records = {"nginx": [{
            "id": "OSV-1", "upstream": ["CVE-2023-0001"],
            "severity": [{"type": "CVSS_V3", "score": "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"}]
        }]}
        db = _mock_vuln_db(records)
        kev = _mock_kev_db()
        epss = _mock_epss_db()
        f = _finding(cve_id="CVE-2023-0001")
        result = enrich_finding(f, db, kev, epss)
        assert result.cvss_vector is not None
        assert result.cvss_score is not None
        assert result.priority is not None

    def test_enriches_kev(self):
        db = _mock_vuln_db()
        kev = _mock_kev_db(cve_ids={"CVE-2023-0001"})
        epss = _mock_epss_db()
        f = _finding(cve_id="CVE-2023-0001")
        result = enrich_finding(f, db, kev, epss)
        assert result.kev is True

    def test_enriches_epss(self):
        db = _mock_vuln_db()
        kev = _mock_kev_db()
        epss = _mock_epss_db(scores={"CVE-2023-0001": {"epss": 0.5, "percentile": 0.9}})
        f = _finding(cve_id="CVE-2023-0001")
        result = enrich_finding(f, db, kev, epss)
        assert result.epss_score == 0.5

    def test_no_data_still_sets_priority(self):
        db = _mock_vuln_db()
        kev = _mock_kev_db()
        epss = _mock_epss_db()
        f = _finding(cve_id="CVE-9999-0001")
        result = enrich_finding(f, db, kev, epss)
        assert result.priority == "unknown"

    def test_idempotent(self):
        db = _mock_vuln_db()
        kev = _mock_kev_db()
        epss = _mock_epss_db()
        f = _finding()
        r1 = enrich_finding(f, db, kev, epss)
        r2 = enrich_finding(r1, db, kev, epss)
        assert r1.cvss_score == r2.cvss_score
        assert r1.kev == r2.kev
        assert r1.epss_score == r2.epss_score
        assert r1.priority == r2.priority


class TestKevDb:
    def test_is_kev(self):
        db = _mock_kev_db(cve_ids={"CVE-2023-0001"})
        assert db.is_kev("CVE-2023-0001") is True
        assert db.is_kev("CVE-9999-9999") is False

    def test_case_insensitive(self):
        db = _mock_kev_db(cve_ids={"CVE-2023-0001"})
        assert db.is_kev("cve-2023-0001") is True


class TestEpssDb:
    def test_get_existing(self):
        db = _mock_epss_db(scores={"CVE-2023-0001": {"epss": 0.5, "percentile": 0.9}})
        assert db.get("CVE-2023-0001")["epss"] == 0.5

    def test_get_missing(self):
        db = _mock_epss_db()
        assert db.get("CVE-9999-9999") is None

    def test_case_insensitive(self):
        db = _mock_epss_db(scores={"CVE-2023-0001": {"epss": 0.3, "percentile": 0.7}})
        assert db.get("cve-2023-0001") is not None


# ═══════════════════════════════════════════════════════════════════════════
# vuln_db.py
# ═══════════════════════════════════════════════════════════════════════════

class TestVulnDB:
    def test_lookup_existing(self):
        records = {"nginx": [{"id": "OSV-1"}]}
        db = _mock_vuln_db(records)
        assert len(db.lookup("nginx")) == 1

    def test_lookup_missing_returns_empty(self):
        db = _mock_vuln_db({})
        assert db.lookup("nonexistent") == []

    def test_covers(self):
        db = _mock_vuln_db({"nginx": []})
        assert db.covers("nginx") is True
        assert db.covers("apache") is False

    def test_cvss_vector_index(self):
        records = {"openssh": [{
            "id": "OSV-1", "upstream": ["CVE-2023-0001"],
            "severity": [{"type": "CVSS_V3", "score": "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"}]
        }]}
        db = _mock_vuln_db(records)
        assert db.get_cvss_vector("CVE-2023-0001") == "AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"

    def test_cvss_vector_missing(self):
        db = _mock_vuln_db({"x": []})
        assert db.get_cvss_vector("CVE-9999-9999") is None

    def test_known_products_sorted(self):
        db = _mock_vuln_db({"zlib": [], "apache2": [], "nginx": []})
        assert db.known_products() == ["apache2", "nginx", "zlib"]

    def test_content_hash_deterministic(self):
        r = {"a": [{"id": "1"}]}
        assert _content_hash(r) == _content_hash(r)


# ═══════════════════════════════════════════════════════════════════════════
# cpe_normalizer.py
# ═══════════════════════════════════════════════════════════════════════════

class TestCPECandidateCpe23:
    def test_cpe23_format(self):
        c = _candidate()
        assert c.cpe23() == f"cpe:2.3:a:{c.vendor}:{c.product}:{c.version_raw}:*:*:*:*:*:*:*"


class TestNormalizeBanner:
    def test_ssh_banner(self):
        fact = _fact(scanner="service_banner", data={"first_line": "SSH-2.0-OpenSSH_8.9p1"})
        candidates = normalize_banner(fact)
        assert any(c.product == "openssh" for c in candidates)

    def test_empty_banner(self):
        fact = _fact(scanner="service_banner", data={})
        candidates = normalize_banner(fact)
        assert candidates == []


class TestNormalizeWeb:
    def test_server_header(self):
        fact = _fact(scanner="web_scan", data={"server": "nginx/1.25.3"})
        candidates = normalize_web(fact)
        assert any(c.product == "nginx" for c in candidates)


class TestNormalizeDb:
    def test_mysql_mariadb_engine_without_mariadb_suffix_returns_empty(self):
        fact = _fact(scanner="db_scan", data={"engine": "mysql/mariadb", "server_version": "8.0.35"})
        candidates = normalize_db(fact)
        assert candidates == []

    def test_mysql_mariadb_engine_with_mariadb_suffix(self):
        fact = _fact(scanner="db_scan", data={"engine": "mysql/mariadb", "server_version": "10.11.6-MariaDB"})
        candidates = normalize_db(fact)
        assert any(c.product == "mysql" for c in candidates)
        assert candidates[0].confidence == "high"

    def test_postgresql(self):
        fact = _fact(scanner="db_scan", data={"engine": "postgresql", "server_version": "15.4"})
        candidates = normalize_db(fact)
        assert any(c.product == "postgresql" for c in candidates)

    def test_unknown_engine(self):
        fact = _fact(scanner="db_scan", data={"engine": "oracle"})
        assert normalize_db(fact) == []

    def test_no_version_confidence_low(self):
        fact = _fact(scanner="db_scan", data={"engine": "postgresql"})
        candidates = normalize_db(fact)
        assert len(candidates) == 1
        assert candidates[0].confidence == "low"


class TestNormalize:
    def test_dispatches_banner(self):
        fact = _fact(scanner="service_banner", data={"first_line": "SSH-2.0-OpenSSH_8.9p1"})
        candidates = normalize(fact)
        assert len(candidates) > 0

    def test_unknown_scanner_returns_empty(self):
        fact = _fact(scanner="unknown_scanner")
        assert normalize(fact) == []


class TestCleanDebianVersion:
    def test_strips_revision(self):
        upstream, epoch = clean_debian_version("1.25.3-1")
        assert upstream == "1.25.3"
        assert epoch is None

    def test_strips_epoch(self):
        upstream, epoch = clean_debian_version("1:3.9p1-1")
        assert upstream == "3.9p1"
        assert epoch == "1"

    def test_no_revision(self):
        upstream, epoch = clean_debian_version("1.25.3")
        assert upstream == "1.25.3"
        assert epoch is None


class TestCleanRpmVersion:
    def test_strips_release(self):
        assert clean_rpm_version("1.25.3-1.el8") == "1.25.3"


class TestAllOsvSourcePackages:
    def test_returns_list(self):
        pkgs = all_osv_source_packages()
        assert isinstance(pkgs, list)
        assert len(pkgs) > 0

    def test_sorted(self):
        pkgs = all_osv_source_packages()
        assert pkgs == sorted(pkgs)


# ═══════════════════════════════════════════════════════════════════════════
# consistency.py
# ═══════════════════════════════════════════════════════════════════════════

class TestWilsonCi:
    def test_perfect_appearance(self):
        lo, hi = wilson_ci(30, 30)
        assert lo > 80  # Wilson CI lower bound for 30/30

    def test_zero_appearances(self):
        lo, hi = wilson_ci(0, 10)
        assert lo == 0.0

    def test_all_appearances(self):
        lo, hi = wilson_ci(10, 10)
        assert hi >= 90.0

    def test_zero_n(self):
        lo, hi = wilson_ci(0, 0)
        assert lo == 0.0
        assert hi == 0.0


class TestFindingConsistency:
    def test_rate(self):
        fc = FindingConsistency(
            finding_id="fid", cve_id="CVE-1", asset_ip="10.0.0.1",
            appearances=27, runs=30, exemplar=_finding())
        assert abs(fc.rate - 0.9) < 0.01

    def test_classification_stable(self):
        fc = FindingConsistency(
            finding_id="fid", cve_id="CVE-1", asset_ip="10.0.0.1",
            appearances=30, runs=30, exemplar=_finding())
        assert fc.classification == "stable"

    def test_classification_mostly_stable(self):
        fc = FindingConsistency(
            finding_id="fid", cve_id="CVE-1", asset_ip="10.0.0.1",
            appearances=27, runs=30, exemplar=_finding())
        assert fc.classification == "mostly-stable"

    def test_classification_intermittent(self):
        fc = FindingConsistency(
            finding_id="fid", cve_id="CVE-1", asset_ip="10.0.0.1",
            appearances=15, runs=30, exemplar=_finding())
        assert fc.classification == "intermittent"


class TestAggregate:
    def test_single_run(self):
        f = _finding(cve_id="CVE-1")
        report = aggregate([[f]])
        assert len(report.findings) == 1
        assert report.findings[0].appearances == 1
        assert report.findings[0].runs == 1

    def test_multi_run_stable(self):
        f1 = _finding(cve_id="CVE-1")
        f2 = _finding(cve_id="CVE-1")
        report = aggregate([[f1], [f2]])
        stable = report.stable
        assert len(stable) == 1

    def test_multi_run_intermittent(self):
        f1 = _finding(cve_id="CVE-1")
        report = aggregate([[f1], []])
        intermittent = report.intermittent
        assert len(intermittent) == 1

    def test_dedup_within_run(self):
        fid = make_finding_id("10.0.0.1", "CVE-1", "cpe:a")
        f1 = _finding(finding_id=fid, cve_id="CVE-1")
        f2 = _finding(finding_id=fid, cve_id="CVE-1")
        report = aggregate([[f1, f2]])
        assert report.findings[0].appearances == 1  # counted once per run
