"""
test_main_scripts_rdp.py — Phase 18: protocol-level RDP confirmation + NLA detection.

Pure X.224 Connection-Request builder + Connection-Confirm parser (fixture bytes),
and the confirmed-RDP / NLA-off findings. No live network.
"""
from __future__ import annotations

import json
import struct
import sys

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


def test_hybrid_ex_0x08_is_nla_over_tls():
    # MS-RDPBCGR: CredSSP/NLA is signalled by 0x08 too, not only 0x02. The old code
    # tested only 0x02 → 0x08 was mislabelled nla:false/tls:false (the inversion).
    r = R.parse_connection_confirm(_cc(R._TYPE_NEG_RSP, R.PROTOCOL_HYBRID_EX))
    assert r["nla"] is True and r["tls"] is True
    assert r["standard_rdp_security"] is False


def test_posture_map_matches_spec():
    # (nla, tls, standard) for each selectedProtocol value.
    m = lambda s: R._posture_from_selected(s, negotiation="response")
    assert (m(0x08)["nla"], m(0x08)["tls"]) == (True, True)
    assert (m(0x00)["nla"], m(0x00)["tls"], m(0x00)["standard_rdp_security"]) == (False, False, True)


# ── two-probe NLA-required posture ────────────────────────────────────────────
def test_nla_required_when_rdp_only_probe_refused(monkeypatch):
    # Probe A selects NLA; Probe B (standard-RDP only) is REFUSED → NLA required.
    def _probe(ip, port, timeout, requested_protocols=None):
        if requested_protocols == R.PROTOCOL_RDP:
            return {"rdp_confirmed": True, "negotiation": "failure", "failure_code": 5}
        return {"rdp_confirmed": True, "negotiation": "response", "selected_protocol": 8,
                "nla": True, "tls": True, "standard_rdp_security": False}
    monkeypatch.setattr(R, "probe_rdp", _probe)
    info = R.probe_rdp_posture("1.2.3.4", 3389, 1.0)
    assert info["nla"] is True and info["tls"] is True
    assert info["nla_required"] is True and "RDP_NEG_FAILURE" in info["nla_required_evidence"]


def test_nla_not_required_when_rdp_only_accepted(monkeypatch):
    def _probe(ip, port, timeout, requested_protocols=None):
        if requested_protocols == R.PROTOCOL_RDP:
            return {"rdp_confirmed": True, "negotiation": "response", "selected_protocol": 0,
                    "nla": False, "tls": False, "standard_rdp_security": True}
        return {"rdp_confirmed": True, "negotiation": "response", "selected_protocol": 0,
                "nla": False, "tls": False, "standard_rdp_security": True}
    monkeypatch.setattr(R, "probe_rdp", _probe)
    assert R.probe_rdp_posture("1.2.3.4", 3389, 1.0)["nla_required"] is False


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


# ── CLI wiring (regression: main() used args.target and mis-called
#    main_entrypoint, so `python -m ...rdp_scanner` AttributeError'd before it
#    ever probed. Drive the real main() end-to-end with the network stubbed.) ──
def test_main_cli_runs_and_writes_finding(tmp_path, monkeypatch):
    scope = tmp_path / "scope.txt"
    scope.write_text("127.0.0.1\n")
    out = tmp_path / "rdp.jsonl"

    # Stub the blocking handshake so the test never touches the network but the
    # full argparse -> expand_targets -> RDPScanner.run -> writer path executes.
    # The two-probe posture calls probe_rdp twice: default (learns selection) and
    # RDP-only (learns whether NLA is required) — model both.
    def _fake_probe(ip, port, timeout, requested_protocols=None):
        if requested_protocols == R.PROTOCOL_RDP:
            return {"rdp_confirmed": True, "negotiation": "failure", "failure_code": 5}
        return {"rdp_confirmed": True, "negotiation": "response", "selected_protocol": 2,
                "nla": True, "tls": True, "standard_rdp_security": False}
    monkeypatch.setattr(R, "probe_rdp", _fake_probe)
    monkeypatch.setattr(
        sys, "argv",
        ["rdp_scanner", "-t", "127.0.0.1", "-s", str(scope), "-o", str(out),
         "-p", "3389", "--timeout", "1"])

    R.main()   # must not raise (previously: AttributeError on args.target)

    lines = [json.loads(x) for x in out.read_text().splitlines() if x.strip()]
    rdp = [r for r in lines if r.get("scanner") == "rdp_scan" and r.get("port") == 3389]
    assert rdp, "main() produced no rdp_scan result for the stubbed open host"
    assert rdp[0]["status"] == "open" and rdp[0]["data"]["nla"] is True


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


def test_nla_required_rdp_is_low_severity_no_bluekeep_language():
    # FIX 5(a): a CONFIRMED NLA-required host is LOW, confirmed, and carries no
    # "BlueKeep class" port-based language.
    fs = _run({"scanner": "rdp_scan", "target": "t", "port": 3389, "status": "open",
               "data": {"rdp_confirmed": True, "nla": True, "tls": True,
                        "nla_required": True, "selected_protocol": 8}})
    exposed = next(f for f in fs if f.rule_id == "SVC-RDP-EXPOSED")
    assert exposed.severity == F.SEV_LOW
    assert exposed.data["confirmed"] is True and exposed.data["nla_required"] is True
    assert "BlueKeep" not in exposed.evidence
    assert "SVC-RDP-NO-NLA" not in {f.rule_id for f in fs}


def test_confirmed_rdp_wins_dedup_over_port_hint():
    fs = _run(
        {"scanner": "port_scan", "target": "t", "port": 3389, "proto": "tcp", "status": "open"},
        {"scanner": "rdp_scan", "target": "t", "port": 3389, "status": "open",
         "data": {"rdp_confirmed": True, "nla": True, "tls": True, "selected_protocol": 2}},
    )
    rdp = [f for f in fs if f.rule_id == "SVC-RDP-EXPOSED"]
    assert len(rdp) == 1 and rdp[0].data.get("confirmed") is True   # confirmed, not port-hint
