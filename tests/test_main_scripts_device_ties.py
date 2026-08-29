"""
test_main_scripts_device_ties.py — Phase 23: device classification never resolves
a score tie arbitrarily; it reports an explicit ambiguous verdict.
"""
from __future__ import annotations

from main_scripts import device_classifier as dc


def test_workstation_server_tie_is_ambiguous():
    # FIX 5(b): SMB(445)/RDP(3389) are Windows-baseline, NOT server signals, so they
    # no longer manufacture a workstation/server tie. A GENUINE tie still reports
    # ambiguous: 445+3389 give workstation 2, a real server role port (SMTP 25,
    # weight 2) gives server 2 -> an honest 2-vs-2 tie.
    r = dc.classify_device(open_tcp_ports=[445, 3389, 25])
    assert r["device_type"] == "ambiguous"
    assert set(r["signals"]["tie"]) == {dc.WORKSTATION, dc.SERVER}
    assert r["confidence"] <= 0.5


def test_clear_winner_is_not_ambiguous():
    r = dc.classify_device(open_tcp_ports=[9100])          # raw print, weight 3
    assert r["device_type"] == dc.PRINTER
    assert "tie" not in r["signals"]


def test_domain_controller_breaks_the_tie():
    # kerberos(88)=server+3 dominates the workstation/server split from 445/3389.
    r = dc.classify_device(open_tcp_ports=[88, 445, 3389])
    assert r["device_type"] == dc.SERVER


def test_empty_is_unknown_not_ambiguous():
    r = dc.classify_device(open_tcp_ports=[])
    assert r["device_type"] == dc.UNKNOWN
