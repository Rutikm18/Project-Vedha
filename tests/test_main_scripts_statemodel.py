"""
test_main_scripts_statemodel.py — Phase 1: the normalized ScanResult state model.

Verifies network-state semantics are FIRST-CLASS fields (not buried in `data`),
that the canonical state vocabulary is shared, and that the `data`->first-class
bridge is non-destructive and backward compatible.
"""
from __future__ import annotations

import json

from main_scripts import scanner_base as sb
from main_scripts.scanner_base import ScanResult


def test_canonical_states_are_the_six_documented_states():
    assert sb.CANONICAL_STATES == {
        sb.OPEN, sb.CLOSED, sb.FILTERED, sb.OPEN_FILTERED, sb.UNREACHABLE, sb.ERROR}
    # wire-compatible values preserved
    assert sb.OPEN == "open" and sb.OPEN_FILTERED == "open|filtered"


def test_state_and_reason_are_separate_first_class_fields():
    r = ScanResult("port_scan", "10.0.0.5", port=22, proto="tcp",
                   status=sb.OPEN, reason="connect_success", rtt_ms=1.4, family="ipv4")
    assert r.status == "open" and r.reason == "connect_success"
    assert r.rtt_ms == 1.4 and r.family == "ipv4"


def test_semantics_in_data_are_promoted_to_first_class_non_destructively():
    # Existing scanners still write these into `data`; __post_init__ promotes them.
    r = ScanResult("port_scan", "t", port=80, proto="tcp", status="open",
                   data={"reason": "connect_success", "rtt_ms": 2.1,
                         "confidence": 0.9, "family": "ipv4", "errno": 0})
    assert r.reason == "connect_success" and r.rtt_ms == 2.1
    assert r.confidence == 0.9 and r.family == "ipv4"
    # data is left intact (non-destructive bridge)
    assert r.data["reason"] == "connect_success"


def test_explicit_first_class_value_wins_over_data():
    r = ScanResult("port_scan", "t", port=80, status="open",
                   reason="explicit", data={"reason": "from_data"})
    assert r.reason == "explicit"


def test_to_json_exposes_promoted_fields_and_round_trips():
    r = ScanResult("udp_scan", "t", port=161, proto="udp",
                   status=sb.OPEN_FILTERED, reason="no_response", vantage="probe-1")
    d = json.loads(r.to_json())
    assert d["status"] == "open|filtered"
    assert d["reason"] == "no_response" and d["vantage"] == "probe-1"
    for k in ("confidence", "family", "src_ip", "interface", "attempts", "rtt_ms", "errno"):
        assert k in d   # first-class, present even when null


def test_backward_compatible_old_style_construction_still_works():
    # The pre-Phase-1 call shape (no state-semantic kwargs) must be unaffected.
    r = ScanResult("smb_scan", "t", port=445, proto="tcp", status="open",
                   data={"smbv1_enabled": True}, evidence="negotiate ok")
    assert r.status == "open" and r.evidence == "negotiate ok"
    assert r.reason is None and r.data["smbv1_enabled"] is True
