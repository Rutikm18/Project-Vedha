"""
test_engine_bridge_ingest_health.py — a zero-finding run must never be able to
LIE about why it is zero.

Every detection rule, CVE and posture alike, reads the Assets that the engine's
ingester builds. A fact the ingester rejects therefore reaches no rule at all —
it is not a degraded result, it is an absent one. ingest quarantines silently by
design (one corrupt line must not sink a 100k-record pass) and the bridge used to
drop that quarantine list on the floor, which made agent/manager shape drift look
exactly like a clean network: facts submitted, run COMPLETED, findings 0, nothing
logged.

That is the failure this file exists to prevent. It asserts the census the bridge
now returns, because the census is what the operator (and DetectionRun.stats)
reads to tell "checked and clean" from "understood nothing you sent".
"""
from __future__ import annotations

import pytest

from app.detection import engine_bridge

pytestmark = pytest.mark.skipif(
    not engine_bridge._ensure_importable(),
    reason="detection_engine not importable in this environment",
)

# The real wire shape: asdict(ScanResult) — scanner/target/timestamp/status are all
# REQUIRED by ingest. Two hosts, one of which is vulnerable (SMBv1 + signing off).
_TS = "2026-09-02T11:03:50.208953+00:00"
_GOOD = [
    {"scanner": "smb_scan", "target": "10.0.0.10", "timestamp": _TS, "port": 445,
     "proto": "tcp", "status": "open",
     "data": {"smbv1_enabled": True, "smb2_supported": True,
              "signing_required": False, "negotiated_dialect": "0x0311"}},
    {"scanner": "smb_scan", "target": "10.0.0.11", "timestamp": _TS, "port": 445,
     "proto": "tcp", "status": "open",
     "data": {"smbv1_enabled": False, "smb2_supported": True,
              "signing_required": True, "negotiated_dialect": "0x0311"}},
]


def test_healthy_facts_ingest_completely_and_detect():
    """Baseline: the shape the agent actually sends survives ingest and fires rules.
    If this breaks, the corpus/contract drifted — not the census."""
    _cve, posture, meta = engine_bridge.detect_all_from_facts_traced(_GOOD)
    census = meta["ingest"]
    assert census["submitted"] == 2
    assert census["ingested"] == 2
    assert census["quarantined"] == 0
    assert census["assets"] == 2
    assert posture, "SMBv1 + signing-off must produce posture findings"


def test_total_shape_drift_is_reported_not_silently_zero():
    """The regression. Drop the one field an agent rename could plausibly drop and
    the result is zero findings — the census is the ONLY thing that distinguishes
    this from a clean network, so it must say so precisely."""
    drifted = [{k: v for k, v in f.items() if k != "timestamp"} for f in _GOOD]
    _cve, posture, meta = engine_bridge.detect_all_from_facts_traced(drifted)
    census = meta["ingest"]
    assert posture == [], "sanity: drifted facts cannot fire rules"
    assert census["submitted"] == 2
    assert census["ingested"] == 0
    assert census["quarantined"] == 2, "the loss must be counted, not swallowed"
    assert census["assets"] == 0
    # The reason must name the offending field — that is what makes the log
    # actionable instead of just alarming.
    assert any("timestamp" in reason for reason in census["reasons"]), census["reasons"]


def test_partial_drift_still_detects_but_reports_the_loss():
    """A partly-bad batch must keep its good findings AND still admit what it lost.
    Silently detecting on 1 of 2 hosts is how a vulnerable host disappears."""
    partial = [_GOOD[0], {k: v for k, v in _GOOD[1].items() if k != "target"}]
    _cve, posture, meta = engine_bridge.detect_all_from_facts_traced(partial)
    census = meta["ingest"]
    assert posture, "the well-formed fact must still be detected on"
    assert census["ingested"] == 1
    assert census["quarantined"] == 1
    assert any("target" in reason for reason in census["reasons"]), census["reasons"]


def test_census_survives_an_engine_that_returns_no_ingest_result():
    """The census is best-effort by contract: an older engine returning no
    IngestResult must degrade to a zeroed census, never raise into detection."""
    census, rejected = engine_bridge._ingest_census(None, submitted=7)
    assert census == {"submitted": 7, "ingested": 0, "quarantined": 0,
                      "assets": 0, "reasons": {}}
    assert rejected == set(), "no verdict means nothing is known-bad"
