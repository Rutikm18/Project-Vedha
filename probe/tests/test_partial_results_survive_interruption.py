"""
A host that FINISHED must keep its facts when the job is cut short.

Every stage stored its results in one go, after the whole stage's gather
returned. So when a job hit its runtime ceiling (or the lease was revoked) during
the port stage, `asyncio.wait_for` cancelled the gather and every completed
host's work went with it — the payload came back carrying discovery facts only.
That is the "aggressive scan broke and we lost everything" report: hosts 1..N had
genuinely been scanned, and none of it reached the manager.

`agent/engine.py` already builds its partial result from the WorkflowCache on
both the deadline and lease-lost paths. The cache just never received anything
until the stage ended. Delivering each host's results the moment that host
finishes is what makes those partial-result paths real.
"""
from __future__ import annotations

import asyncio

import pytest

from workflow.asset import Asset
from workflow.cache import WorkflowCache
from scanner.scanner_base import ScanResult, ScopeGuard

from workflow.workflow_engine import run_engagement

FAST = "10.0.0.1"       # finishes immediately
HUNG = "10.0.0.2"       # never returns — the job dies waiting for it
SCOPE = ScopeGuard.from_list(["10.0.0.0/24"])


def _stub(component_id, *, port=None, data=None, hang_on=()):
    class Scanner:
        name = component_id

        def __init__(self, *args, **kwargs):
            pass

        async def scan_target(self, host):
            if host in hang_on:
                await asyncio.Event().wait()          # never completes
            return [ScanResult(scanner=component_id, target=host, port=port,
                               proto="tcp" if port else None, status="open",
                               data=data or {})]
    return Scanner


def _run_until_cut_short(monkeypatch, *, hang_stage: str):
    """Run a two-host engagement where one host hangs, then cut the job off the
    way the runtime ceiling does. Returns the cache the engine was handed."""
    monkeypatch.setattr(
        "workflow.workflow_engine.HostDiscoveryScanner",
        _stub("host_discovery", data={"alive": True},
              hang_on=(HUNG,) if hang_stage == "host_discovery" else ()))
    monkeypatch.setattr(
        "workflow.workflow_engine.PortScanner",
        _stub("port_scan", port=445,
              hang_on=(HUNG,) if hang_stage == "port_scan" else ()))
    monkeypatch.setattr("workflow.workflow_engine.OSFingerprintScanner",
                        _stub("os_fingerprint"))

    cache = WorkflowCache()
    assets = {h: Asset(host=h, profile="it") for h in (FAST, HUNG)}

    async def _go():
        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(
                run_engagement([FAST, HUNG], SCOPE, stage_ceiling="port_scan",
                               port_override=[445], cache=cache, assets=assets,
                               host_concurrency=2),
                timeout=0.5)

    asyncio.run(_go())
    return cache


def _cached_scanners_for(cache, host):
    return {entry.result.scanner for entry in cache._store.values()
            if entry.result.target == host}


class TestFinishedHostsSurvive:
    def test_port_facts_of_a_finished_host_reach_the_cache(self, monkeypatch):
        cache = _run_until_cut_short(monkeypatch, hang_stage="port_scan")

        assert "port_scan" in _cached_scanners_for(cache, FAST), (
            "the finished host's port scan was discarded when the job was cut "
            "short — this is the data loss the partial-result path exists to "
            "prevent")

    def test_discovery_facts_of_a_finished_host_reach_the_cache(self, monkeypatch):
        cache = _run_until_cut_short(monkeypatch, hang_stage="host_discovery")

        assert "host_discovery" in _cached_scanners_for(cache, FAST)

    def test_the_hung_host_contributes_nothing(self, monkeypatch):
        """Honesty: an unfinished host must not appear to have been scanned."""
        cache = _run_until_cut_short(monkeypatch, hang_stage="port_scan")

        assert "port_scan" not in _cached_scanners_for(cache, HUNG)


class TestCompleteRunsAreUnchanged:
    def test_results_are_still_returned_and_stored_once(self, monkeypatch):
        monkeypatch.setattr("workflow.workflow_engine.HostDiscoveryScanner",
                            _stub("host_discovery", data={"alive": True}))
        monkeypatch.setattr("workflow.workflow_engine.PortScanner",
                            _stub("port_scan", port=445))
        monkeypatch.setattr("workflow.workflow_engine.OSFingerprintScanner",
                            _stub("os_fingerprint"))
        cache = WorkflowCache()

        assets = asyncio.run(run_engagement(
            [FAST, HUNG], SCOPE, stage_ceiling="port_scan",
            port_override=[445], cache=cache))

        for host in (FAST, HUNG):
            assert 445 in assets[host].open_ports_for_deep_scan()
        # One cache entry per (host, port, scanner) — delivering per host must
        # not double-store what the stage also stored at the end.
        port_entries = [e for e in cache._store.values()
                        if e.result.scanner == "port_scan"]
        assert len(port_entries) == 2
