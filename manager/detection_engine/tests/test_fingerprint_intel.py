"""
test_fingerprint_intel.py — TLS fingerprint IOC matching (fingerprint_intel.py).

Covers: a seeded JARM C2 match, JA4S/JA4X matches via a registry, the all-zero /
absent no-op, exact-match-only (no substring), and the end-to-end posture wiring
(SUSPECTED state, threat_intel category, NO_MATCH trace when clean).
"""
from __future__ import annotations

import fingerprint_intel as FI
from models import Asset, Fact, SourceConfidence
from posture_rules import detect_posture_traced

# the seeded Cobalt Strike default JARM
_CS_JARM = "07d14d16d21d21d07c42d41d00041d24a458a375eef0c576d23a7bab9a9fb1"


def _tls_fp_fact(data: dict, scanner="tls_fingerprint", port=443) -> Fact:
    return Fact(scanner=scanner, target="10.0.0.7", timestamp="2026-09-01T00:00:00Z",
                port=port, proto="tcp", status="open", data=data, evidence=None,
                error=None, source_confidence=SourceConfidence.inferred,
                source_file="c.jsonl", source_line=1)


def _asset(*facts):
    a = Asset(ip="10.0.0.7")
    for f in facts:
        a.add_fact(f)
    return a


def test_jarm_c2_match():
    m = FI.match_fact_data({"tls_fingerprint": _CS_JARM})
    assert len(m) == 1 and m[0]["kind"] == "JARM" and "Cobalt Strike" in m[0]["label"]


def test_all_zero_jarm_is_no_match():
    assert FI.match_fact_data({"tls_fingerprint": "0" * 62}) == []


def test_unknown_fingerprint_clean():
    assert FI.match_fact_data({"tls_fingerprint": "deadbeef" * 7}) == []


def test_case_insensitive_match():
    assert FI.match_fact_data({"tls_fingerprint": _CS_JARM.upper()})


def test_exact_match_only_no_substring():
    # a superstring of a known fingerprint must NOT match
    assert FI.match_fact_data({"tls_fingerprint": _CS_JARM + "ff"}) == []


def test_external_feed_merges_and_matches(tmp_path, monkeypatch):
    feed = tmp_path / FI._FEED_NAME
    feed.write_text('{"ja4s": {"t130200_1301_abc123def456": "Example C2 server-hello"},'
                    ' "ja4x": {"aa11_bb22_cc33": "Example tooling cert"}}')
    monkeypatch.setenv("VEDHA_INTEL_DIR", str(tmp_path))
    reg = FI.load_registry()
    assert reg["ja4s"]["t130200_1301_abc123def456"] == "Example C2 server-hello"
    m = FI.match_fact_data({"ja4s": "t130200_1301_abc123def456",
                            "certificate": {"ja4x": "aa11_bb22_cc33"}})
    kinds = {x["kind"] for x in m}
    assert kinds == {"JA4S", "JA4X"}


def test_bad_feed_fails_open(tmp_path, monkeypatch):
    (tmp_path / FI._FEED_NAME).write_text("{not valid json")
    monkeypatch.setenv("VEDHA_INTEL_DIR", str(tmp_path))
    reg = FI.load_registry()               # must not raise
    assert _CS_JARM in reg["jarm"]         # seeds still present


def test_posture_wiring_suspected_and_traced():
    findings, traces = detect_posture_traced(_asset(
        _tls_fp_fact({"tls_fingerprint": _CS_JARM, "ja4s": None})))
    hits = [f for f in findings if f.rule_id == FI.RULE_ID]
    assert len(hits) == 1
    f = hits[0]
    assert f.state == "suspected"           # IOC match is a lead, never proof
    assert f.category == "threat_intel"
    assert f.severity == "high"
    assert f.evidence["label"].startswith("Cobalt Strike")


def test_posture_wiring_clean_tls_reports_no_match():
    findings, traces = detect_posture_traced(_asset(
        _tls_fp_fact({"tls_fingerprint": "a" * 62})))
    assert not [f for f in findings if f.rule_id == FI.RULE_ID]
    fi_traces = [t for t in traces if t.rule_id == FI.RULE_ID]
    assert fi_traces and any(t.outcome == "no_match" for t in fi_traces)
