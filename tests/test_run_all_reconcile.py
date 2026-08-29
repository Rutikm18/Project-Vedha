"""
test_run_all_reconcile.py — cross-cutting: run_all and scan_funnel must derive the
canonical open-TCP set from ONE reconciler, so the two pipelines can never disagree.

run_all imports scan_funnel.reconcile_ports directly (not a copy), and extracts
EPM-advertised dynamic ports with the same rule the funnel uses. These pure helpers
are tested here; the subprocess stages are exercised in the live integration run.
"""
from __future__ import annotations

import inspect

from main_scripts.run_all import _advertised_dynamic_ports, _open_tcp_ports
from main_scripts import run_all
from main_scripts.scan_funnel import reconcile_ports


def test_run_all_runs_rdp_scanner_stage():
    # run_all must invoke the CONFIRMING rdp_scanner on 3389 so findings get the
    # X.224-confirmed fact (which wins dedup over the stale port-based RDP finding).
    src = inspect.getsource(run_all)
    assert '"rdp_scanner"' in src or "'rdp_scanner'" in src
    assert "3389 in open_tcp" in src


def test_run_all_imports_the_shared_reconciler_not_a_copy():
    # run_all must use scan_funnel.reconcile_ports (one source of truth), never a
    # re-implemented union — otherwise the two pipelines could silently diverge.
    src = inspect.getsource(run_all)
    assert "from main_scripts.scan_funnel import reconcile_ports" in src
    assert "def reconcile_ports" not in src        # no local re-implementation


def test_advertised_dynamic_ports_extraction():
    msrpc = [{"scanner": "msrpc_scan",
              "data": {"dynamic_tcp_ports": [49668, 49664]}},
             {"scanner": "msrpc_scan", "data": {"dynamic_tcp_ports": []}}]
    assert _advertised_dynamic_ports(msrpc) == [49664, 49668]


def test_reconcile_matches_between_pipelines_when_epm_unreachable():
    # Ground truth 192.168.1.77: EPM advertises dynamic ports but they are firewall
    # -blocked → confirmed 0 → canonical == the port-scan open set. Both pipelines
    # feed the SAME reconcile_ports, so both produce this identical set.
    port_scan_open = [135, 445, 2179, 3389, 7680]
    confirmed_dyn: list[int] = []                 # none reachable from this vantage
    canonical = reconcile_ports(port_scan_open, confirmed_dyn)
    assert canonical == [135, 445, 2179, 3389, 7680]


def test_reconcile_folds_in_only_reachable_dynamic_ports():
    port_scan_open = [135, 445, 3389]
    confirmed_dyn = [49664]                        # advertised 49664/49668, only 49664 reachable
    assert reconcile_ports(port_scan_open, confirmed_dyn) == [135, 445, 3389, 49664]


def test_open_tcp_ports_ignores_non_open_and_udp():
    recs = [{"proto": "tcp", "status": "open", "port": 445},
            {"proto": "tcp", "status": "closed", "port": 25},
            {"proto": "udp", "status": "open", "port": 161},
            {"proto": "tcp", "status": "open", "port": 135}]
    assert _open_tcp_ports(recs) == [135, 445]
