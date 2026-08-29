"""
test_os_fusion.py — FIX 3(a): cross-scanner OS identification with calibrated,
multi-signal confidence. An exact NTLM build corroborated by an SMB2 Windows
handshake and a hostname must be near-certain (>=0.95); a lone TTL guess stays a
hint (~0.5). Detection-as-code: every confidence tier is asserted with its inputs.
"""
from __future__ import annotations

from scanner import findings as F


def _os(*facts):
    out = [f for f in F.run_findings(list(facts)) if f.rule_id == "ASSET-OS-IDENTIFIED"]
    return out[0] if out else None


def test_build_smb2_hostname_is_high_confidence():
    osf = _os({"scanner": "smb_scan", "target": "192.168.1.77", "port": 445,
               "status": "open",
               "data": {"smb2_supported": True, "os_build": 26100,
                        "os_release": "Windows 11 24H2", "target_name": "DESKTOP-34M18MB"}})
    assert osf is not None
    assert osf.data["os_release"] == "Windows 11 24H2"
    assert osf.data["confidence"] >= 0.95
    assert osf.data["hostname"] == "DESKTOP-34M18MB"
    assert osf.confidence == F.CONF_HIGH and osf.severity == F.SEV_INFO


def test_build_only_is_strong_but_not_certain():
    osf = _os({"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
               "data": {"os_build": 19045, "os_release": "Windows 10 22H2"}})
    assert osf.data["confidence"] == 0.90 and osf.data["os_release"] == "Windows 10 22H2"


def test_ttl_only_stays_a_hint():
    osf = _os({"scanner": "os_fingerprint", "target": "t", "status": "open",
               "data": {"os_guess": "Linux/Unix/macOS", "confidence": 0.5}})
    assert osf.data["confidence"] == 0.5 and osf.data["method"] == "ttl_only"
    assert osf.confidence == F.CONF_LOW


def test_smb2_plus_p0f_stack_is_medium():
    osf = _os({"scanner": "smb_scan", "target": "t", "port": 445, "status": "open",
               "data": {"smb2_supported": True}},
              {"scanner": "os_fingerprint", "target": "t", "status": "open",
               "data": {"os_guess": "Windows",
                        "stack_guess": "Windows (NT 6.2+ — 8/10/11, Server 2012+)"}})
    assert osf.data["confidence"] == 0.80 and "Windows" in osf.data["os_release"]


def test_no_os_signal_yields_no_finding():
    assert _os({"scanner": "port_scan", "target": "t", "port": 80, "proto": "tcp",
                "status": "open"}) is None
