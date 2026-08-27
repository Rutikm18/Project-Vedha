"""
test_online.py — the OPT-IN live enrichment layer (cve/online.py).

Every test injects a fake `get` returning canned feed bytes, so nothing here
touches the network. Pins the module's contract: NVD parsing, Vulners
exploit-detection, fail-open on every error, gap-fill vs cross-check semantics,
per-CVE caching, and the offline-first invariant (a failed/absent lookup leaves
the offline finding exactly as produced).
"""

from __future__ import annotations

import json

import pytest

from cve.correlator import CVEFinding, risk_band, risk_score
from cve.online import (
    OnlineResult, enrich_findings, lookup_nvd, lookup_vulners,
)
import cve.cli as cli


# ── fakes ─────────────────────────────────────────────────────────────────────
def _nvd_bytes(cve_id="CVE-2013-4786", score=7.8, sev="HIGH",
               refs=("https://example.test/a",)):
    return json.dumps({
        "vulnerabilities": [{"cve": {
            "id": cve_id,
            "published": "2013-07-08T22:55:03.100",
            "metrics": {"cvssMetricV31": [{"cvssData": {
                "baseScore": score, "baseSeverity": sev,
                "vectorString": "CVSS:3.1/AV:N"}}]},
            "references": [{"url": u} for u in refs],
        }}]
    }).encode()


def _nvd_empty():
    return json.dumps({"vulnerabilities": []}).encode()


def _vulners_bytes(cve_id, *, exploit):
    refs = {"exploitdb": ["EDB-123"]} if exploit else {"nvd": ["x"]}
    return json.dumps({
        "result": "OK",
        "data": {"documents": {cve_id: {"references": refs}}},
    }).encode()


def _get_returning(payload):
    """A fake transport that ignores its args and returns fixed bytes."""
    def _get(url, *, params=None, headers=None, timeout=30.0):
        return payload
    return _get


def _get_raising(exc=ConnectionError("no egress")):
    def _get(url, *, params=None, headers=None, timeout=30.0):
        raise exc
    return _get


def _finding(cve_id="CVE-2013-4786", cvss=None, evidence="weakness observed."):
    """A CVEFinding as the offline pass would emit it — CVSS None models a mirror gap."""
    return CVEFinding(
        cve_id=cve_id, target="10.0.0.3", port=623, matched_cpe=None,
        product=None, version=None, cvss_score=cvss,
        cvss_severity=("HIGH" if cvss else None), kev=False, kev_date=None,
        epss=None, epss_percentile=None, confidence="medium",
        risk_score=risk_score(cvss, False, None, False),
        risk_band=risk_band(risk_score(cvss, False, None, False)),
        evidence=evidence, source_scanner="weakness_map")


# ── lookup_nvd ────────────────────────────────────────────────────────────────
class TestLookupNvd:
    def test_parses_score_severity_refs(self):
        r = lookup_nvd("CVE-2013-4786", get=_get_returning(_nvd_bytes()))
        assert isinstance(r, OnlineResult)
        assert r.cvss_score == 7.8 and r.cvss_severity == "HIGH"
        assert r.published.startswith("2013-07-08")
        assert r.references == ["https://example.test/a"]
        assert r.error is None

    def test_empty_result_is_none(self):
        assert lookup_nvd("CVE-0000-0000", get=_get_returning(_nvd_empty())) is None

    def test_network_error_is_fail_open(self):
        r = lookup_nvd("CVE-2013-4786", get=_get_raising())
        # fail-open: an OnlineResult carrying the error, never a raise
        assert r is not None and r.error and r.cvss_score is None

    def test_garbage_json_is_fail_open(self):
        r = lookup_nvd("CVE-2013-4786", get=_get_returning(b"not json"))
        assert r is not None and r.error


# ── lookup_vulners ────────────────────────────────────────────────────────────
class TestLookupVulners:
    def test_no_key_returns_none(self):
        assert lookup_vulners("CVE-1", api_key=None, get=_get_returning(b"{}")) is None

    def test_exploit_present_is_true(self):
        g = _get_returning(_vulners_bytes("CVE-2013-4786", exploit=True))
        assert lookup_vulners("CVE-2013-4786", api_key="k", get=g) is True

    def test_no_exploit_is_false(self):
        g = _get_returning(_vulners_bytes("CVE-2013-4786", exploit=False))
        assert lookup_vulners("CVE-2013-4786", api_key="k", get=g) is False

    def test_error_is_none(self):
        assert lookup_vulners("CVE-1", api_key="k", get=_get_raising()) is None


# ── enrich_findings ───────────────────────────────────────────────────────────
class TestEnrichFindings:
    def test_gap_fill_sets_cvss_and_recomputes_risk(self):
        f = _finding(cvss=None)
        before = f.risk_score
        enrich_findings([f], get=_get_returning(_nvd_bytes(score=7.8)),
                        sleep=lambda _s: None)
        assert f.cvss_score == 7.8
        assert f.risk_score > before                 # gap-fill raised the score
        assert "Live NVD lookup supplied CVSS 7.8" in f.evidence
        assert f.extra["online"]["filled_cvss"] is True

    def test_only_missing_skips_already_scored(self):
        f = _finding(cvss=6.5)
        calls = {"n": 0}

        def _get(url, *, params=None, headers=None, timeout=30.0):
            calls["n"] += 1
            return _nvd_bytes(score=9.9)
        enrich_findings([f], get=_get, sleep=lambda _s: None)     # only_missing=True
        assert calls["n"] == 0                        # never queried
        assert f.cvss_score == 6.5 and "online" not in f.extra

    def test_online_all_cross_checks_and_annotates_mismatch(self):
        f = _finding(cvss=5.0)
        enrich_findings([f], get=_get_returning(_nvd_bytes(score=9.8)),
                        only_missing=False, sleep=lambda _s: None)
        # mirror value is NOT overwritten — only annotated
        assert f.cvss_score == 5.0
        assert "differs from the mirror" in f.evidence
        assert f.extra["online"]["cvss_mismatch"] is True

    def test_vulners_exploit_flags_finding(self):
        f = _finding(cvss=None)

        def _get(url, *, params=None, headers=None, timeout=30.0):
            if "vulners" in url:
                return _vulners_bytes("CVE-2013-4786", exploit=True)
            return _nvd_bytes()
        enrich_findings([f], vulners_key="k", get=_get, sleep=lambda _s: None)
        assert "PUBLIC EXPLOIT" in f.evidence
        assert f.extra["online"]["exploit_available"] is True

    def test_caches_per_cve_id(self):
        # two findings, same CVE on different targets -> one NVD request
        f1, f2 = _finding(), _finding()
        f2.target = "10.0.0.9"
        calls = {"n": 0}

        def _get(url, *, params=None, headers=None, timeout=30.0):
            calls["n"] += 1
            return _nvd_bytes()
        enrich_findings([f1, f2], get=_get, sleep=lambda _s: None)
        assert calls["n"] == 1

    def test_fail_open_leaves_offline_result_untouched(self):
        f = _finding(cvss=None, evidence="offline evidence.")
        enrich_findings([f], get=_get_raising(), sleep=lambda _s: None)
        assert f.cvss_score is None
        assert f.evidence == "offline evidence."
        assert "online" not in f.extra


# ── CLI wiring ────────────────────────────────────────────────────────────────
class TestCliOnlineFlag:
    def _facts(self, tmp_path):
        # a weakness fact whose canonical CVE (CVE-2013-4786) is absent from the mirror
        p = tmp_path / "facts.jsonl"
        p.write_text(json.dumps({
            "type": "finding", "rule_id": "IPMI-CIPHER-ZERO", "target": "10.0.0.3",
            "port": 623, "severity": "high", "data": {}}) + "\n")
        return p

    def _db(self, tmp_path):
        from cve.vulndb import VulnDB
        p = tmp_path / "vuln.db"
        d = VulnDB(str(p), create=True)
        d.commit(); d.close()
        return p

    def test_online_flag_invokes_enrichment(self, tmp_path, monkeypatch):
        called = {"hit": False}

        def _fake_enrich(findings, **kw):
            called["hit"] = True
            return findings
        monkeypatch.setattr(cli, "enrich_findings", _fake_enrich)
        out = tmp_path / "cve.jsonl"
        rc = cli.main(["correlate", "--db", str(self._db(tmp_path)),
                       "--facts", str(self._facts(tmp_path)),
                       "--out", str(out), "--online"])
        assert rc == 0 and called["hit"] is True

    def test_no_online_flag_skips_enrichment(self, tmp_path, monkeypatch):
        called = {"hit": False}
        monkeypatch.setattr(cli, "enrich_findings",
                            lambda findings, **kw: called.__setitem__("hit", True))
        out = tmp_path / "cve.jsonl"
        cli.main(["correlate", "--db", str(self._db(tmp_path)),
                  "--facts", str(self._facts(tmp_path)), "--out", str(out)])
        assert called["hit"] is False
