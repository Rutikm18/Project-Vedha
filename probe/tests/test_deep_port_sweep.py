"""
deep_port_sweep — the full-65,535-port use-case (the UI's Deep mode).

Aggressive (network_va deep) is the bounded enterprise set; scanning the whole
TCP space is this use-case. It used to be limited to 3 hosts because its tail
had to fit a fixed 2 h ceiling; the ceiling now grows with the sweep, so there
is no host cap unless an operator sets one (PROBE_DEEP_PORT_SWEEP_MAX_HOSTS).
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


def test_no_host_cap_by_default():
    assert "deep_port_sweep" not in _MAX_HOSTS_BY_SCAN_TYPE


def test_four_hosts_are_not_refused_by_a_cap():
    # A 1 s ceiling still refuses on time, but NOT with a host-cap message.
    r = _run(["10.77.0.1", "10.77.0.2", "10.77.0.3", "10.77.0.4"])
    assert "host(s); this job resolved" not in r.get("error", "")


def test_an_operator_cap_still_refuses_a_wider_scope(monkeypatch):
    monkeypatch.setitem(_MAX_HOSTS_BY_SCAN_TYPE, "deep_port_sweep", 3)
    r = _run(["10.77.0.1", "10.77.0.2", "10.77.0.3", "10.77.0.4"])
    assert r["error_code"] == "job_cannot_finish"
    assert "limited to 3 host(s)" in r["error"]
    assert "65,535" in r["error"]
    assert r["facts"] == []


def test_allow_infeasible_bypasses_an_operator_cap(monkeypatch):
    monkeypatch.setitem(_MAX_HOSTS_BY_SCAN_TYPE, "deep_port_sweep", 3)
    r = _run(["10.77.0.1", "10.77.0.2", "10.77.0.3", "10.77.0.4"],
             allow_infeasible=True)
    assert "limited to 3 host(s)" not in r.get("error", "")


def test_a_capped_sweep_is_sized_by_its_first_pass_not_65535():
    # Phased: admission prices the ~1,145-port first pass, not all 65,535.
    r = _run(["10.77.0.1", "10.77.0.2", "10.77.0.3"])
    assert r["run_stats"]["timing"]["estimate"]["scope"] == "first_pass"
    assert "65535" not in r["error"].replace(",", "")
