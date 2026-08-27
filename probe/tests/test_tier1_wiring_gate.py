"""
test_tier1_wiring_gate.py — integration/accuracy gate for deep-scan capabilities.

Every deep-scan branch must be wired consistently across the orchestration layers,
or the capability silently never runs. This test codifies the invariants that were
checked by hand while building the Tier-1 catalog (SSH/SMB/LDAP/DNS/NFS/FTP/rsync/
VNC/IPMI/SMTP/MSRPC/printer), so a future half-wired branch fails CI instead of
shipping dark.

Invariants, per IT-profile deep branch:
  * has an entry in gates._BRANCH_PORT_TABLE;
  * TCP branches are routed in scan_funnel.DEFAULT_PORT_ROUTES AND have a funnel
    factory whose scanner exposes a name registered in asset._MERGE_DISPATCH;
  * UDP host-wide branches (snmp, ipmi) still have a merge handler.
"""

from __future__ import annotations

from workflow.gates import PROFILE_DEEP_BRANCHES, _BRANCH_PORT_TABLE
from workflow.asset import _MERGE_DISPATCH
from scanner.scan_funnel import DEFAULT_PORT_ROUTES, build_default_funnel
from scanner.scanner_base import ScopeGuard

# Branches handled host-wide over UDP (like SNMP) — intentionally NOT in the
# TCP funnel routing table.
_UDP_HOSTWIDE_BRANCHES = {"snmp", "ipmi"}

# Known pre-existing naming quirk: the AI scanner is the "mcp_ai" branch in the
# workflow/gates but routes as "ai" in the funnel. Documented here so the gate
# still verifies it is fully wired (under its funnel name) rather than papering
# over it.
_FUNNEL_ROUTE_ALIAS = {"mcp_ai": "ai"}


def _funnel():
    return build_default_funnel(ScopeGuard.from_list(["10.0.0.0/8"]))


def test_every_it_branch_has_port_table_entry():
    for b in PROFILE_DEEP_BRANCHES["it"]:
        assert b in _BRANCH_PORT_TABLE, f"branch '{b}' has no _BRANCH_PORT_TABLE entry"


def test_tcp_branches_are_fully_wired():
    funnel = _funnel()
    for b in PROFILE_DEEP_BRANCHES["it"] - _UDP_HOSTWIDE_BRANCHES:
        route = _FUNNEL_ROUTE_ALIAS.get(b, b)
        assert route in DEFAULT_PORT_ROUTES, f"branch '{b}' not in funnel routes"
        assert route in funnel.deep_scanner_factories, f"branch '{b}' has no funnel factory"
        scanner = funnel.deep_scanner_factories[route](sorted(_BRANCH_PORT_TABLE[b]))
        assert scanner.name in _MERGE_DISPATCH, (
            f"branch '{b}' scanner '{scanner.name}' has no asset merge handler")


def test_udp_hostwide_branches_have_merge_handlers():
    assert "snmp_scan" in _MERGE_DISPATCH
    assert "ipmi_scan" in _MERGE_DISPATCH


def test_new_tier1_branches_present():
    # Regression guard: the Tier-1 catalog built this session must stay wired.
    expected = {"ssh", "smb_enum", "ldap", "dns", "nfs", "ftp", "rsync",
                "vnc", "ipmi", "smtp", "msrpc", "printer"}
    assert expected <= PROFILE_DEEP_BRANCHES["it"], (
        f"missing Tier-1 branches: {expected - PROFILE_DEEP_BRANCHES['it']}")
