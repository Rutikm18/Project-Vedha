"""
test_risk_port_coverage.py — the collection half of the exposed-service rules.

THE INVARIANT: every port the manager's risk catalog (port_intel.py) can raise a
finding on must be SCANNED by a network_va. The exposed-service detector reads the
OPEN-PORT SET, so a port nobody probed is indistinguishable from a port that was
closed — the rule is dead code and the host looks clean.

This was a real, total blind spot: the IT catalog swept 40 ports, the risk catalog
named 85, and 55 were never probed — including EVERY backdoor/C2 port. A HIGH
severity rule (POSTURE-EXPOSED-BACKDOOR) could not fire on a default scan no matter
what was listening on 4444.

Same governed-data discipline as scanner_registry.VERIFIED ↔ posture_rules
.VALIDATED_SCANNERS: two lists in two packages that must agree, with a test that
fails loudly when they don't.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

from workflow.gates import (
    IT_PORTS, PROFILE_DEEP_BRANCHES, VA_RISK_PORTS, _BRANCH_PORT_TABLE,
)
from workflow.workflow_engine import _port_candidates

_ENGINE = Path(__file__).resolve().parents[2] / "manager" / "detection_engine"
_CATEGORIES = ("_BACKDOOR", "_CONTAINER", "_DATASTORE", "_DATABASE",
               "_CLEARTEXT", "_REMOTE", "_ADMIN_UI")


def _port_intel():
    if not _ENGINE.exists():
        pytest.skip(f"manager detection_engine not present at {_ENGINE}")
    if str(_ENGINE) not in sys.path:
        sys.path.insert(0, str(_ENGINE))
    import port_intel
    return port_intel


def _risk_ports() -> dict[int, str]:
    pi = _port_intel()
    out: dict[int, str] = {}
    for name in _CATEGORIES:
        for port in getattr(pi, name):
            out.setdefault(port, name[1:].lower())
    return out


def _swept_by_network_va() -> set[int]:
    """Exactly what a default network_va puts on the wire: the profile catalog
    plus every allowed branch's port table (this is _port_candidates itself, not a
    re-derivation, so the test cannot drift from the engine)."""
    return set(_port_candidates("it", None))


def test_network_va_scans_every_port_the_risk_catalog_knows():
    risk = _risk_ports()
    swept = _swept_by_network_va()
    missing = sorted(p for p in risk if p not in swept)
    detail = ", ".join(f"{p} ({risk[p]})" for p in missing[:24])
    assert not missing, (
        f"{len(missing)} port(s) in manager port_intel are NEVER scanned by a "
        f"network_va, so their exposed-service rules can never fire: {detail}"
        "\nAdd them to workflow.gates.VA_RISK_PORTS.")


def test_every_backdoor_port_is_swept():
    """Called out separately: these carry the highest severity and were 100%
    unscanned before VA_RISK_PORTS existed."""
    pi = _port_intel()
    swept = _swept_by_network_va()
    missing = sorted(p for p in pi._BACKDOOR if p not in swept)
    assert not missing, f"unscanned backdoor/C2 ports: {missing}"


def test_va_risk_ports_are_all_actually_in_the_risk_catalog():
    """Reverse direction: VA_RISK_PORTS must not accumulate ports the manager has
    no rule for — that is scan cost buying nothing."""
    risk = _risk_ports()
    stray = sorted(p for p in VA_RISK_PORTS if p not in risk)
    assert not stray, (
        f"VA_RISK_PORTS contains {stray}, which manager port_intel does not "
        "classify — either add a rule for them or drop them from the sweep.")


def test_va_risk_ports_has_no_duplicates_and_is_valid():
    assert len(VA_RISK_PORTS) == len(set(VA_RISK_PORTS)), "duplicate in VA_RISK_PORTS"
    assert all(0 < p < 65536 for p in VA_RISK_PORTS)


def test_it_ports_is_the_union_and_stays_sorted_unique():
    assert IT_PORTS == sorted(set(IT_PORTS))
    assert set(VA_RISK_PORTS) <= set(IT_PORTS)


def test_sweep_stays_within_a_sane_budget():
    """A connect scan is one socket per port per host, so this list is a cost as
    well as a coverage decision. Guard against it quietly becoming a full sweep."""
    swept = _swept_by_network_va()
    assert 90 <= len(swept) <= 400, (
        f"network_va now sweeps {len(swept)} ports — if that is intended, update "
        "this budget deliberately rather than letting it drift.")


def test_branch_tables_still_contribute():
    """The sweep is profile catalog UNION the TCP branch tables; a regression that
    dropped the branch half would silently stop deep scanners from ever being
    eligible. Datagram branches are excluded ON PURPOSE — snmp/ipmi probe UDP and
    gate on liveness, so putting 161 in a TCP connect sweep would just buy a
    guaranteed-closed result."""
    from workflow.branches import BRANCH_BY_NAME

    swept = _swept_by_network_va()
    for branch in PROFILE_DEEP_BRANCHES["it"]:
        spec = BRANCH_BY_NAME.get(branch)
        if spec is not None and spec.datagram:
            continue
        ports = set(_BRANCH_PORT_TABLE.get(branch, ()))
        if ports:
            assert ports <= swept, f"{branch}'s ports are not all swept: {sorted(ports - swept)}"


def test_datagram_branch_ports_are_not_in_the_tcp_sweep():
    """The complement of the rule above, pinned so a future edit cannot quietly
    add UDP-only ports to the TCP connect scan."""
    from workflow.branches import BRANCHES

    swept = _swept_by_network_va()
    assert 161 not in swept, "SNMP's UDP port must not be TCP-swept"
    for spec in BRANCHES:
        if spec.datagram and spec.branch == "snmp":
            assert not (set(spec.ports) & swept)


@pytest.mark.parametrize("port,what", [
    (4444, "Metasploit/Meterpreter default handler"),
    (31337, "Back Orifice"),
    (12345, "NetBus"),
    (6667, "IRC botnet C2"),
    (2323, "Mirai telnet"),
    (5555, "Android ADB"),
    (2379, "etcd client"),
    (9092, "Kafka"),
    (6000, "X11"),
    (514, "rsh / syslog"),
])
def test_named_high_value_ports_are_scanned(port, what):
    assert port in _swept_by_network_va(), f"{port} ({what}) is not scanned"
