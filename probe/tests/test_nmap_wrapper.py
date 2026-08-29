"""
test_nmap_wrapper.py — the "nmap returned 0 while native scanners saw ports" bug.

Root cause: the port-scanning profiles omitted -Pn, so nmap ran host discovery
first and a firewalled Windows host (blocks ICMP/probes) was marked 'down' and
never port-scanned. -Pn (treat as up, skip discovery) aligns nmap with the native
scanners, which always scan regardless of liveness. Also guards the parser: open
ports are emitted, filtered ports are not mislabelled open.
"""
from __future__ import annotations

from main_scripts.nmap_wrapper import _parse_nmap_xml, PROFILES

_OPEN_XML = """<?xml version="1.0"?><!DOCTYPE nmaprun>
<nmaprun><host><status state="up" reason="user-set"/>
<address addr="192.168.1.77" addrtype="ipv4"/><ports>
<port protocol="tcp" portid="445"><state state="open"/>
  <service name="microsoft-ds" product="Windows" version="10"/></port>
<port protocol="tcp" portid="3389"><state state="open"/>
  <service name="ms-wbt-server"/></port>
</ports></host></nmaprun>"""


def test_port_scan_profiles_carry_pn():
    for p in ("version", "os", "smb", "fast"):
        assert "-Pn" in PROFILES[p], f"{p} profile must skip host discovery (-Pn)"
    # discovery's whole job is to decide liveness — it must NOT assume up.
    assert "-Pn" not in PROFILES["discovery"]


def test_open_ports_are_emitted():
    res = _parse_nmap_xml(_OPEN_XML, "version")
    assert {r.port for r in res if r.status == "open"} == {445, 3389}


def test_filtered_ports_not_emitted_as_open():
    xml = _OPEN_XML.replace('state="open"', 'state="filtered"')
    res = _parse_nmap_xml(xml, "version")
    assert not any(r.status == "open" for r in res)
