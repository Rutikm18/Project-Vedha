"""
deep_port_sweep — the host-capped full-65,535-port use-case.

Aggressive (network_va deep) is now the bounded enterprise set; scanning the
whole TCP space is this separate use-case, limited to a few hosts so full-port
coverage never fans out across a subnet and blows the time ceiling.
"""
from __future__ import annotations

from agent import engine
from agent.engine import _MAX_HOSTS_BY_SCAN_TYPE, _FORCE_PORT_PROFILE, _PHASED_FULL_SCAN_TYPES


def _run(hosts, **extra):
    params = {"targets": list(hosts), "scope_cidrs": ["10.77.0.0/24"],
              "intensity": "deep", "max_runtime_seconds": 1}
    params.update(extra)
    return engine.run_scan("deep_port_sweep", params)


def test_it_forces_the_full_range_and_phases_it():
    assert _FORCE_PORT_PROFILE["deep_port_sweep"] == "full"
    assert "deep_port_sweep" in _PHASED_FULL_SCAN_TYPES


def test_capped_at_three_hosts():
    assert _MAX_HOSTS_BY_SCAN_TYPE["deep_port_sweep"] == 3


def test_four_hosts_is_refused_by_the_cap():
    r = _run(["10.77.0.1", "10.77.0.2", "10.77.0.3", "10.77.0.4"])
    assert r["error_code"] == "job_cannot_finish"
    assert "limited to 3 host(s)" in r["error"]
    assert "65,535" in r["error"]
    assert r["facts"] == []


def test_three_hosts_is_not_refused_by_the_cap():
    # A 1 s ceiling still refuses on time, but NOT with the host-cap message.
    r = _run(["10.77.0.1", "10.77.0.2", "10.77.0.3"])
    assert "limited to 3 host(s)" not in r.get("error", "")


def test_allow_infeasible_bypasses_the_cap():
    r = _run(["10.77.0.1", "10.77.0.2", "10.77.0.3", "10.77.0.4"],
             allow_infeasible=True)
    assert "limited to 3 host(s)" not in r.get("error", "")


def test_a_capped_sweep_is_sized_by_its_first_pass_not_65535():
    # Phased: admission prices the ~1,145-port first pass, not all 65,535.
    r = _run(["10.77.0.1", "10.77.0.2", "10.77.0.3"])
    assert r["run_stats"]["timing"]["estimate"]["scope"] == "first_pass"
    assert "65535" not in r["error"].replace(",", "")
