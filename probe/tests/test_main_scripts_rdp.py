"""
test_main_scripts_rdp.py — Phase 18: protocol-level RDP confirmation + NLA detection.

Pure X.224 Connection-Request builder + Connection-Confirm parser (fixture bytes),
and the confirmed-RDP / NLA-off findings. No live network.
"""
from __future__ import annotations

import struct

from main_scripts import findings as F
from main_scripts import rdp_scanner as R


def _cc(neg_type: int | None, value: int = 0) -> bytes:
    """A TPKT + X.224 Connection Confirm, optionally carrying an rdpNeg PDU."""
    var = struct.pack("<BBHI", neg_type, 0x00, 0x0008, value) if neg_type else b""
    x224 = bytes([6 + len(var), 0xD0, 0x00, 0x00, 0x12, 0x34, 0x00]) + var
    return struct.pack("!BBH", 0x03, 0x00, 4 + len(x224)) + x224


# ── builder ──────────────────────────────────────────────────────────────────
def test_connection_request_is_valid_tpkt_and_requests_protocols():
    pkt = R.build_connection_request(R.PROTOCOL_SSL | R.PROTOCOL_HYBRID | R.PROTOCOL_HYBRID_EX)
    assert pkt[:2] == b"\x03\x00"                        # TPKT version + reserved
    assert struct.unpack("!H", pkt[2:4])[0] == len(pkt)  # TPKT length == packet length
    assert pkt[-8] == R._TYPE_NEG_REQ                    # rdpNegReq type
    assert struct.unpack("<I", pkt[-4:])[0] == 0x0B      # SSL|HYBRID|HYBRID_EX


# ── parser ───────────────────────────────────────────────────────────────────
def test_nla_when_hybrid_selected():
    r = R.parse_connection_confirm(_cc(R._TYPE_NEG_RSP, R.PROTOCOL_HYBRID))
    assert r["rdp_confirmed"] and r["nla"] is True and r["tls"] is True
    assert r["standard_rdp_security"] is False


def test_tls_only_is_not_nla():
    r = R.parse_connection_confirm(_cc(R._TYPE_NEG_RSP, R.PROTOCOL_SSL))
    assert r["tls"] is True and r["nla"] is False


def test_standard_rdp_security_no_nla():
    r = R.parse_connection_confirm(_cc(R._TYPE_NEG_RSP, R.PROTOCOL_RDP))
    assert r["standard_rdp_security"] is True and r["nla"] is False and r["tls"] is False


def test_negotiation_failure():
    r = R.parse_connection_confirm(_cc(R._TYPE_NEG_FAILURE, 0x00000002))
    assert r["rdp_confirmed"] and r["negotiation"] == "failure" and r["failure_code"] == 2


def test_cc_without_negotiation_is_standard_rdp():
    r = R.parse_connection_confirm(_cc(None))
    assert r["rdp_confirmed"] and r["standard_rdp_security"] is True and r["nla"] is False


def test_non_rdp_data_is_none():
    assert R.parse_connection_confirm(b"HTTP/1.1 200 OK\r\n\r\n") is None
    assert R.parse_connection_confirm(b"\x03\x00") is None


# ── findings ─────────────────────────────────────────────────────────────────
def _run(*facts):
    return F.run_findings(list(facts))


def test_confirmed_rdp_without_nla_is_high_finding():
    fs = _run({"scanner": "rdp_scan", "target": "t", "port": 3389, "status": "open",
               "data": {"rdp_confirmed": True, "nla": False, "tls": False,
                        "standard_rdp_security": True, "selected_protocol": 0}})
    ids = {f.rule_id for f in fs}
    assert "SVC-RDP-NO-NLA" in ids and "SVC-RDP-EXPOSED" in ids
    assert next(f for f in fs if f.rule_id == "SVC-RDP-NO-NLA").severity == F.SEV_HIGH


def test_confirmed_rdp_with_nla_has_no_nla_finding():
    fs = _run({"scanner": "rdp_scan", "target": "t", "port": 3389, "status": "open",
               "data": {"rdp_confirmed": True, "nla": True, "tls": True, "selected_protocol": 2}})
    ids = {f.rule_id for f in fs}
    assert "SVC-RDP-EXPOSED" in ids and "SVC-RDP-NO-NLA" not in ids


def test_confirmed_rdp_wins_dedup_over_port_hint():
    fs = _run(
        {"scanner": "port_scan", "target": "t", "port": 3389, "proto": "tcp", "status": "open"},
        {"scanner": "rdp_scan", "target": "t", "port": 3389, "status": "open",
         "data": {"rdp_confirmed": True, "nla": True, "tls": True, "selected_protocol": 2}},
    )
    rdp = [f for f in fs if f.rule_id == "SVC-RDP-EXPOSED"]
    assert len(rdp) == 1 and rdp[0].data.get("confirmed") is True   # confirmed, not port-hint
