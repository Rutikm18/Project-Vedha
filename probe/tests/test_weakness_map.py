"""
test_weakness_map.py — the weakness -> canonical-CVE bridge (cve/weakness_map.py).

This is the second correlation route (complementing the CPE version-range path):
the probe's detect stage concludes a weakness it DIRECTLY observed (SMBv1 enabled,
Terrapin-affected SSH, IPMI cipher-0), and this layer maps that weakness to the
named, globally-tracked CVE it is the precondition for — enriched with LIVE
CVSS/KEV/EPSS pulled from the same offline mirror. Tests pin: both fact shapes,
the data-gated discriminators (SSLv3->POODLE / SSLv2->DROWN), mirror enrichment +
exposure boost, graceful behaviour when a CVE is absent from the mirror, dedup,
and the coverage-gap report + CLI verbs.
"""

from __future__ import annotations

import json

import pytest

from cve.vulndb import VulnDB
from cve.weakness_map import (
    WEAKNESS_CVES, correlate_weaknesses, missing_from_mirror, _finding_view,
)
import cve.cli as cli


# ── a mirror carrying the canonical CVEs the map references ───────────────────
@pytest.fixture()
def db():
    d = VulnDB(":memory:", create=True)
    d.upsert_cve("CVE-2017-0144", 8.1, "HIGH", "", "EternalBlue", "2017", "2017")
    d.upsert_kev("CVE-2017-0144", "microsoft", "windows", "EternalBlue", "2022-03-25")
    d.upsert_epss("CVE-2017-0144", 0.97, 0.99)
    d.upsert_cve("CVE-2023-48795", 5.9, "MEDIUM", "", "Terrapin", "2023", "2023")
    d.upsert_cve("CVE-2014-3566", 3.4, "LOW", "", "POODLE", "2014", "2014")
    d.upsert_cve("CVE-2016-0800", 5.9, "MEDIUM", "", "DROWN", "2016", "2016")
    # CVE-2013-4786, CVE-2013-5211, CVE-2019-0708 deliberately absent -> gap tests.
    d.commit()
    return d


# ── fact builders (both shapes the correlator must accept) ────────────────────
def _wrapped(rule_id, target, port, data=None):
    """A detect-stage fact: ScanResult('findings', ..., data=Finding.to_dict())."""
    return {"scanner": "findings", "target": target, "port": port, "status": "observed",
            "data": {"type": "finding", "rule_id": rule_id, "target": target,
                     "port": port, "severity": "high", "data": data or {}}}


def _raw(rule_id, target, port, data=None):
    """A bare Finding dict (findings.py --json output)."""
    return {"type": "finding", "rule_id": rule_id, "target": target, "port": port,
            "severity": "high", "data": data or {}}


class TestFindingView:
    def test_wrapped_shape(self):
        v = _finding_view(_wrapped("SMB-V1-ENABLED", "10.0.0.5", 445))
        assert v and v["rule_id"] == "SMB-V1-ENABLED"

    def test_raw_shape(self):
        v = _finding_view(_raw("SMB-V1-ENABLED", "10.0.0.5", 445))
        assert v and v["rule_id"] == "SMB-V1-ENABLED"

    def test_non_finding_ignored(self):
        assert _finding_view({"scanner": "smb_scan", "data": {"smbv1_enabled": True}}) is None


class TestCorrelateWeaknesses:
    def test_smbv1_maps_to_eternalblue_with_live_enrichment(self, db):
        fnds = correlate_weaknesses([_wrapped("SMB-V1-ENABLED", "10.0.0.5", 445,
                                              {"smbv1_enabled": True})], db)
        assert len(fnds) == 1
        f = fnds[0]
        assert f.cve_id == "CVE-2017-0144"
        assert f.cvss_score == 8.1 and f.kev is True and f.epss == 0.97
        assert f.confidence == "medium"          # surface seen, patch level not
        assert f.source_scanner == "weakness_map"
        assert f.extra["weakness_rule_id"] == "SMB-V1-ENABLED"
        assert "EternalBlue" in f.evidence and "MS17-010" in f.evidence

    def test_exposure_boosts_risk(self, db):
        base = correlate_weaknesses([_raw("SMB-V1-ENABLED", "10.0.0.5", 445)], db)[0]
        boosted = correlate_weaknesses([_raw("SMB-V1-ENABLED", "10.0.0.5", 445)], db,
                                       exposed_targets={"10.0.0.5"})[0]
        assert boosted.risk_score > base.risk_score

    def test_terrapin_high_confidence(self, db):
        f = correlate_weaknesses([_raw("SSH-TERRAPIN", "10.0.0.9", 22)], db)[0]
        assert f.cve_id == "CVE-2023-48795" and f.confidence == "high"

    def test_obsolete_tls_sslv3_only_poodle(self, db):
        f = correlate_weaknesses(
            [_raw("TLS-OBSOLETE-PROTO", "10.0.0.7", 443,
                  {"accepted_versions": ["SSLV3", "TLSV1.2"]})], db)
        assert {x.cve_id for x in f} == {"CVE-2014-3566"}         # POODLE, not DROWN

    def test_obsolete_tls_sslv2_only_drown(self, db):
        f = correlate_weaknesses(
            [_raw("TLS-OBSOLETE-PROTO", "10.0.0.7", 443,
                  {"accepted_versions": ["SSLV2"]})], db)
        assert {x.cve_id for x in f} == {"CVE-2016-0800"}         # DROWN, not POODLE

    def test_obsolete_tls_both_when_both_offered(self, db):
        f = correlate_weaknesses(
            [_raw("TLS-OBSOLETE-PROTO", "10.0.0.7", 443,
                  {"accepted_versions": ["SSLV2", "SSLV3"]})], db)
        assert {x.cve_id for x in f} == {"CVE-2014-3566", "CVE-2016-0800"}

    def test_unmapped_rule_yields_nothing(self, db):
        assert correlate_weaknesses([_raw("WEB-MISSING-SECURITY-HEADERS", "1.1.1.1", 80)], db) == []

    def test_cve_absent_from_mirror_still_emitted_with_note(self, db):
        # IPMI-CIPHER-ZERO -> CVE-2013-4786, which is NOT in the fixture mirror.
        f = correlate_weaknesses([_raw("IPMI-CIPHER-ZERO", "10.0.0.3", 623)], db)[0]
        assert f.cve_id == "CVE-2013-4786"
        assert f.cvss_score is None and f.kev is False
        assert "not in the offline mirror" in f.evidence

    def test_no_db_degrades_gracefully(self):
        f = correlate_weaknesses([_raw("SMB-V1-ENABLED", "10.0.0.5", 445)], None)[0]
        assert f.cve_id == "CVE-2017-0144" and f.cvss_score is None

    def test_dedup_by_cve_target_port(self, db):
        facts = [_raw("SMB-V1-ENABLED", "10.0.0.5", 445),
                 _wrapped("SMB-V1-ENABLED", "10.0.0.5", 445, {"smbv1_enabled": True})]
        f = correlate_weaknesses(facts, db)
        assert len(f) == 1

    def test_sorted_by_risk_desc(self, db):
        facts = [_raw("SMB-V1-ENABLED", "10.0.0.5", 445),      # KEV+EPSS -> high
                 _raw("TLS-OBSOLETE-PROTO", "10.0.0.7", 443,
                      {"accepted_versions": ["SSLV3"]})]        # low CVSS -> low
        f = correlate_weaknesses(facts, db)
        assert [x.risk_score for x in f] == sorted((x.risk_score for x in f), reverse=True)

    def test_to_dict_shape_matches_cve_finding(self, db):
        d = correlate_weaknesses([_raw("SMB-V1-ENABLED", "10.0.0.5", 445)], db)[0].to_dict()
        assert d["type"] == "cve_finding" and d["cve_id"] == "CVE-2017-0144"


class TestMirrorGap:
    def test_missing_from_mirror_lists_absent_canonical_cves(self, db):
        missing = missing_from_mirror(db)
        # present in fixture -> not listed; absent -> listed.
        assert "CVE-2017-0144" not in missing
        assert "CVE-2013-4786" in missing and "CVE-2019-0708" in missing

    def test_every_mapping_has_at_least_one_cve(self):
        for rule_id, m in WEAKNESS_CVES.items():
            assert m.assocs, rule_id
            for a in m.assocs:
                assert a.cve_id.startswith("CVE-"), rule_id


class TestCliStatus:
    def _disk_db(self, tmp_path):
        p = tmp_path / "vuln.db"
        d = VulnDB(str(p), create=True)
        d.upsert_cve("CVE-2017-0144", 8.1, "HIGH", "", "EternalBlue", "2017", "2017")
        from datetime import datetime, timezone
        d.set_meta("last_ingest_utc",
                   datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
        d.commit(); d.close()
        return p

    def test_status_reports_counts_and_gaps(self, tmp_path, capsys):
        p = self._disk_db(tmp_path)
        rc = cli.main(["status", "--db", str(p)])
        assert rc == 0
        report = json.loads(capsys.readouterr().out)
        assert report["counts"]["cve"] == 1
        assert report["weakness_map_rules"] == len(WEAKNESS_CVES)
        # fresh stamp + gaps -> not healthy (missing canonical CVEs)
        assert report["stale"] is False
        assert "CVE-2013-4786" in report["weakness_map_missing_from_mirror"]
        assert report["healthy"] is False


class TestCliCorrelateMerges:
    def _disk_db(self, tmp_path):
        p = tmp_path / "vuln.db"
        d = VulnDB(str(p), create=True)
        d.upsert_cve("CVE-2017-0144", 8.1, "HIGH", "", "EternalBlue", "2017", "2017")
        d.upsert_kev("CVE-2017-0144", "microsoft", "windows", "EternalBlue", "2022-03-25")
        d.commit(); d.close()
        return p

    def test_correlate_includes_weakness_findings(self, tmp_path, capsys):
        p = self._disk_db(tmp_path)
        facts = tmp_path / "facts.jsonl"
        facts.write_text(json.dumps(_wrapped("SMB-V1-ENABLED", "10.0.0.5", 445,
                                             {"smbv1_enabled": True})) + "\n")
        out = tmp_path / "cve.jsonl"
        rc = cli.main(["correlate", "--db", str(p), "--facts", str(facts), "--out", str(out)])
        assert rc == 0
        lines = [json.loads(x) for x in out.read_text().splitlines() if x.strip()]
        assert any(l["cve_id"] == "CVE-2017-0144" for l in lines)

    def test_no_weakness_map_flag_disables_it(self, tmp_path):
        p = self._disk_db(tmp_path)
        facts = tmp_path / "facts.jsonl"
        facts.write_text(json.dumps(_wrapped("SMB-V1-ENABLED", "10.0.0.5", 445,
                                             {"smbv1_enabled": True})) + "\n")
        out = tmp_path / "cve.jsonl"
        cli.main(["correlate", "--db", str(p), "--facts", str(facts),
                  "--out", str(out), "--no-weakness-map"])
        lines = [json.loads(x) for x in out.read_text().splitlines() if x.strip()]
        assert not any(l["cve_id"] == "CVE-2017-0144" for l in lines)
