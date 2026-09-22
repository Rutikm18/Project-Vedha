"""
Stages that offload blocking work must be bounded by HOST slots, not sockets.

THE INCONSISTENCY
-----------------
`concurrency` bounds sockets WITHIN one scanner. `host_concurrency` bounds how
many HOSTS run a stage at once. The port stage and the deep stage learned that
distinction the hard way and say so:

    # HOST slots, not the socket budget. `concurrency` bounds sockets WITHIN a
    # scanner; using it here also started that many hosts at once, so on a /24
    # every live host swept in lockstep and none finished early.

os_fingerprint never got the same treatment — it still fans out to
`concurrency` hosts, which is up to 500 at the aggressive envelope.

WHY IT MATTERS MORE THERE THAN ANYWHERE ELSE
--------------------------------------------
OSFingerprintScanner.scan_target makes THREE run_in_executor(None, ...) calls
per host — SMB2 negotiate, ICMP echo TTL, ICMP timestamp — on the DEFAULT
thread pool, which is min(32, cpu+4) threads (14 on this machine). 500 hosts
therefore queue ~1,500 blocking tasks against ~14 workers.

That failure is already documented in this codebase, in _recheck_alive:

    "every scanner offloads its blocking socket work to the default thread
     pool, and during the datagram tail that pool is saturated. A heartbeat
     that needs a worker thread just queues behind the very scanners it is
     supposed to be watching, and silently stops heartbeating. That is exactly
     what happened: one beat got through, then nothing."

host_discovery is deliberately left wide: one cheap probe per host is the
stage where broad fan-out is the point, and the rate limiter still bounds the
packets it emits.
"""
from __future__ import annotations

import asyncio
import inspect

import pytest

from scanner.scanner_base import ScanResult, ScopeGuard
from workflow import workflow_engine as we

SCOPE = ScopeGuard.from_list(["10.66.0.0/16"], strict=True)


class _Instant:
    name = "stub"

    def __init__(self, *a, **kw):
        pass

    async def scan_target(self, host):
        return []


class _CountingOS:
    """Records how many OS fingerprints are in flight at once."""

    name = "os_fingerprint"
    live = 0
    peak = 0

    def __init__(self, *a, **kw):
        pass

    async def scan_target(self, host):
        _CountingOS.live += 1
        _CountingOS.peak = max(_CountingOS.peak, _CountingOS.live)
        try:
            await asyncio.sleep(0.01)
            return []
        finally:
            _CountingOS.live -= 1


def _hosts(n: int) -> list[str]:
    return [f"10.66.{i // 256}.{i % 256}" for i in range(1, n + 1)]


def _seeded(hosts):
    assets = {}
    for host in hosts:
        asset = we.Asset(host=host, profile="it")
        asset.merge_result(ScanResult("host_discovery", host, status="observed",
                                      data={"alive": True}))
        asset.merge_result(ScanResult("port_scan", host, port=80, proto="tcp",
                                      status="open", data={}))
        assets[host] = asset
    return assets


@pytest.fixture
def stubbed(monkeypatch):
    _CountingOS.live = _CountingOS.peak = 0
    monkeypatch.setattr(we, "HostDiscoveryScanner", _Instant)
    monkeypatch.setattr(we, "PortScanner", _Instant)
    monkeypatch.setattr(we, "SynScanner", _Instant)
    monkeypatch.setattr(we, "ServiceBannerScanner", _Instant)
    monkeypatch.setattr(we, "OSFingerprintScanner", _CountingOS)
    return _CountingOS


async def _run(hosts, **kw):
    return await we.run_engagement(
        hosts, SCOPE, profile="it", rate=100_000, concurrency=200,
        timeout=0.01, disc_timeout=0.01, retries=0, assets=_seeded(hosts),
        stage_ceiling="service_banner", port_override=[80], **kw)


class TestOsFingerprintIsBoundedByHostSlots:
    @pytest.mark.asyncio
    async def test_it_does_not_start_every_host_at_once(self, stubbed):
        """With concurrency=200 and 60 hosts, the old code ran all 60."""
        await _run(_hosts(60), host_concurrency=8)
        assert stubbed.peak <= 8, (
            f"{stubbed.peak} OS fingerprints in flight against a host limit "
            f"of 8 — the stage is still sized by the socket budget"
        )

    @pytest.mark.asyncio
    async def test_it_honours_an_explicit_host_concurrency(self, stubbed):
        await _run(_hosts(40), host_concurrency=3)
        assert stubbed.peak <= 3, stubbed.peak

    @pytest.mark.asyncio
    async def test_every_host_is_still_fingerprinted(self, stubbed):
        """Bounding the fan-out must not drop hosts."""
        seen = []

        class _Recording(_CountingOS):
            async def scan_target(self, host):
                seen.append(host)
                return await super().scan_target(host)

        import unittest.mock as m
        hosts = _hosts(20)
        with m.patch.object(we, "OSFingerprintScanner", _Recording):
            await _run(hosts, host_concurrency=4)
        assert sorted(seen) == sorted(hosts)

    @pytest.mark.asyncio
    async def test_it_stays_under_the_default_thread_pool(self, stubbed):
        """The real ceiling: scan_target makes three run_in_executor calls on
        the DEFAULT pool, which is min(32, cpu+4). Queueing hundreds of hosts
        against ~14 workers is the saturation _recheck_alive documents."""
        import os

        pool = min(32, (os.cpu_count() or 1) + 4)
        await _run(_hosts(50))          # default host_concurrency
        assert stubbed.peak <= pool, (
            f"{stubbed.peak} hosts fingerprinting at once against a "
            f"{pool}-thread default executor"
        )


class TestThePolicyIsConsistent:
    def test_every_per_host_stage_uses_host_slots(self):
        """host_discovery is the one deliberate exception — one cheap probe
        per host is exactly where wide fan-out is the point, and the rate
        limiter still bounds what it emits."""
        src = inspect.getsource(we.run_engagement)
        by_socket = src.count("max_in_flight=concurrency")
        assert by_socket == 1, (
            f"{by_socket} stages still size their HOST fan-out by the socket "
            f"budget; only host_discovery should"
        )

    def test_os_fingerprint_is_not_the_exception(self):
        src = inspect.getsource(we.run_engagement)
        osfp = src.split("Gate 4b", 1)[1].split("Gate 4:", 1)[0]
        assert "max_in_flight=host_concurrency" in osfp
        assert "max_in_flight=concurrency" not in osfp

    def test_gate_6_is_not_the_exception(self):
        """The last stage to be a plain `for host in live_hosts` loop. It bounds
        with a semaphore rather than _gather_per_host because the collectors are
        not BaseScanners — they expose .run(targets, writer), not .scan_target()
        — but the BOUND is the same host_concurrency. Behaviour is covered by
        tests/test_gate6_concurrency.py; this pins the policy."""
        src = inspect.getsource(we.run_engagement)
        gate6 = src.split("Gate 6:", 1)[1]
        assert "Semaphore(max(1, host_concurrency))" in gate6
        assert "asyncio.gather" in gate6
        assert "for host in live_hosts:" not in gate6, \
            "gate 6 is sequential again"
