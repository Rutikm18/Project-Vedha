"""
The banner stage ran one host at a time.

Every other per-host stage fans out — host_discovery and os_fingerprint through
_gather_per_host, the deep branches through a host_slots semaphore. Gate 4 was
a plain loop:

    for host in hosts:
        ...
        results = await _scan_one(banner, host)

So on a 1,000-host estate the stage cost the SUM of every host's banner grabs
while the other host slots sat idle. Each host is mostly waiting on remote
services to speak first, which is exactly the shape that overlaps well.

The fan-out is bounded by the same `host_concurrency` the deep stage uses, and
for the same reason its docstring gives: this multiplies total in-flight work,
and `concurrency` already bounds sockets WITHIN one scanner. A banner grab also
opens a socket per open port, so an unbounded fan-out here would be the widest
burst in the pipeline.

ORDER IS NOT PART OF THE CONTRACT, CACHE-GUARDING IS. The pass runs a second
time after the port tail and must still probe only what the tail newly opened.
"""
from __future__ import annotations

import asyncio
import time

import pytest

from scanner.scanner_base import ScopeGuard
from workflow import workflow_engine as we

SCOPE = ScopeGuard.from_list(["10.88.0.0/24"], strict=True)
HOSTS = [f"10.88.0.{n}" for n in range(1, 9)]


class _SlowBanner:
    """A banner scanner that takes a fixed time per host."""

    name = "service_banner"
    delay = 0.12
    seen: list[str] = []

    def __init__(self, *a, **kw):
        pass

    async def scan_target(self, host):
        _SlowBanner.seen.append(host)
        await asyncio.sleep(self.delay)
        # A real result, so the cache is actually populated — a scanner that
        # returns nothing can never be cache-guarded on a second pass.
        return [we.ScanResult("service_banner", host, port=80, proto="tcp",
                              status="observed", data={"product": "nginx"})]


class _Instant:
    """Stands in for the stages that are not under test.

    host_discovery and os_fingerprint both do ICMP, which on an unprivileged
    dev box falls back to paths slow enough to dominate — and neither has
    anything to do with whether the BANNER stage overlaps its hosts.
    """

    name = "stub"

    def __init__(self, *a, **kw):
        pass

    async def scan_target(self, host):
        return []


@pytest.fixture
def slow_banner(monkeypatch):
    _SlowBanner.seen = []
    monkeypatch.setattr(we, "ServiceBannerScanner", _SlowBanner)
    monkeypatch.setattr(we, "HostDiscoveryScanner", _Instant)
    monkeypatch.setattr(we, "OSFingerprintScanner", _Instant)
    monkeypatch.setattr(we, "PortScanner", _Instant)
    monkeypatch.setattr(we, "SynScanner", _Instant)
    return _SlowBanner


def _seeded(hosts):
    """Hosts already known alive with one open port, so the banner stage runs."""
    assets = {}
    for host in hosts:
        asset = we.Asset(host=host, profile="it")
        asset.merge_result(we.ScanResult(
            "host_discovery", host, status="observed", data={"alive": True}))
        asset.merge_result(we.ScanResult(
            "port_scan", host, port=80, proto="tcp", status="open", data={}))
        assets[host] = asset
    return assets


async def _run(hosts=None, **kw):
    hosts = list(hosts or HOSTS)
    return await we.run_engagement(
        hosts, SCOPE, profile="it", rate=100_000, concurrency=50,
        timeout=0.01, disc_timeout=0.01, retries=0,
        assets=_seeded(hosts), stage_ceiling="service_banner",
        port_override=[80], **kw)


class TestTheStageOverlapsHosts:
    @pytest.mark.asyncio
    async def test_eight_hosts_do_not_cost_eight_sequential_grabs(self, slow_banner):
        """The defect in one number: 8 hosts x 0.12 s was 0.96 s serial."""
        started = time.monotonic()
        await _run()
        elapsed = time.monotonic() - started

        assert set(slow_banner.seen) == set(HOSTS), "not every host was bannered"
        assert elapsed < 0.7, (
            f"banner stage took {elapsed:.2f}s for {len(HOSTS)} hosts — "
            f"still running them one at a time"
        )

    @pytest.mark.asyncio
    async def test_every_host_is_still_visited_exactly_once(self, slow_banner):
        await _run()
        assert sorted(slow_banner.seen) == sorted(HOSTS)

    @pytest.mark.asyncio
    async def test_the_fan_out_is_bounded(self, slow_banner):
        """Unbounded would be the widest burst in the pipeline: a banner grab
        opens a socket per OPEN port, across every host at once."""
        live = 0
        peak = 0

        class _Counting(_SlowBanner):
            async def scan_target(self, host):
                nonlocal live, peak
                live += 1
                peak = max(peak, live)
                try:
                    return await super().scan_target(host)
                finally:
                    live -= 1

        import unittest.mock as m
        with m.patch.object(we, "ServiceBannerScanner", _Counting):
            await _run(host_concurrency=3)
        assert peak <= 3, f"{peak} banner grabs in flight against a limit of 3"


class TestTheContractIsUnchanged:
    @pytest.mark.asyncio
    async def test_a_host_with_no_open_ports_is_skipped(self, slow_banner):
        assets = {}
        for host in HOSTS[:3]:
            asset = we.Asset(host=host, profile="it")
            asset.merge_result(we.ScanResult(
                "host_discovery", host, status="observed", data={"alive": True}))
            assets[host] = asset
        await we.run_engagement(
            HOSTS[:3], SCOPE, profile="it", rate=100_000, concurrency=10,
            timeout=0.01, disc_timeout=0.01, retries=0, assets=assets,
            stage_ceiling="service_banner", port_override=[80])
        assert slow_banner.seen == [], "bannered a host with nothing open"

    @pytest.mark.asyncio
    async def test_a_second_pass_reprobes_nothing_already_cached(self, slow_banner):
        """The tail re-runs this pass; cache-guarding is what stops it from
        re-grabbing every banner on the estate."""
        cache = we.WorkflowCache()
        assets = _seeded(HOSTS[:2])

        for _ in range(2):
            await we.run_engagement(
                HOSTS[:2], SCOPE, profile="it", rate=100_000, concurrency=10,
                timeout=0.01, disc_timeout=0.01, retries=0,
                assets=assets, cache=cache,
                stage_ceiling="service_banner", port_override=[80])

        # Second run adds nothing: the banner facts are cached per (host, port).
        assert len(slow_banner.seen) == 2, slow_banner.seen

    @pytest.mark.asyncio
    async def test_one_host_failing_does_not_abort_its_peers(self, slow_banner):
        class _Exploding(_SlowBanner):
            async def scan_target(self, host):
                if host == HOSTS[0]:
                    raise RuntimeError("banner grab blew up")
                return await super().scan_target(host)

        import unittest.mock as m
        with m.patch.object(we, "ServiceBannerScanner", _Exploding):
            assets = await _run()
        assert assets, "a single host's failure took the stage down"
