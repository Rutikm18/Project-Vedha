"""
Gate 6 (credentialed collection) ran one host at a time.

The last sequential stage in the pipeline, and the same defect class the banner
stage had — but a worse one to leave, because a credentialed collection is the
slowest per-host work the probe does. An SSH collection is a TCP connect, a
key exchange, host-key verification, auth, then a series of command round
trips; a Windows collection is an SMB session setup plus DCE/RPC binds. All of
it is latency, none of it is this host's CPU, so it overlaps almost perfectly.

    for host in live_hosts:              # 200 Windows hosts x ~4 s
        ...                              # = 13 minutes of mostly waiting
        results = await _run_inventory(...)

Bounded by `host_concurrency` like every other per-host stage, and here the
bound does real work rather than just matching a convention: these collectors
are BLOCKING clients (paramiko, impacket) driven through the default executor,
which is min(32, cpu+4) threads. That is the exact pool os_fingerprint was
found saturating, and a credentialed collection occupies a thread far longer
than an ICMP echo does.

ORDER IS NOT PART OF THE CONTRACT. `cred_collected` guarding a second pass IS.
"""
from __future__ import annotations

import asyncio
import time

import pytest

from scanner.scanner_base import ScanResult, ScopeGuard
from workflow import workflow_engine as we

SCOPE = ScopeGuard.from_list(["10.89.0.0/24"], strict=True)
HOSTS = [f"10.89.0.{n}" for n in range(1, 9)]
SSH_CREDS = {"user": "svc", "password": "x"}


class _SlowCollector:
    """A credentialed collector that takes a fixed time per host.

    Not a BaseScanner: the real ones expose .run(targets, writer) only.
    """

    delay = 0.12
    seen: list[str] = []

    def __init__(self, *a, **kw):
        pass

    async def run(self, targets, sink):
        for host in targets:
            _SlowCollector.seen.append(host)
            await asyncio.sleep(self.delay)
            sink.write(ScanResult("ssh_inventory", host, status="observed",
                                  data={"os": "linux"}))


class _Instant:
    """Stands in for the stages that are not under test — on an unprivileged
    dev box ICMP falls back to paths slow enough to dominate the measurement."""

    name = "stub"

    def __init__(self, *a, **kw):
        pass

    async def scan_target(self, host):
        return []


@pytest.fixture
def slow_ssh(monkeypatch):
    _SlowCollector.seen = []
    monkeypatch.setattr(we, "SSHCollector", _SlowCollector)
    for name in ("HostDiscoveryScanner", "OSFingerprintScanner",
                 "PortScanner", "SynScanner", "ServiceBannerScanner"):
        monkeypatch.setattr(we, name, _Instant)
    return _SlowCollector


def _seeded(hosts):
    """Hosts already known alive — Gate 6 requires last_seen_alive."""
    assets = {}
    for host in hosts:
        asset = we.Asset(host=host, profile="it")
        asset.merge_result(we.ScanResult(
            "host_discovery", host, status="observed", data={"alive": True}))
        assets[host] = asset
    return assets


async def _run(hosts=None, *, assets=None, **kw):
    hosts = list(hosts or HOSTS)
    return await we.run_engagement(
        hosts, SCOPE, profile="it", rate=100_000, concurrency=50,
        timeout=0.01, disc_timeout=0.01, retries=0,
        assets=_seeded(hosts) if assets is None else assets,
        ssh_creds=SSH_CREDS, port_override=[80], **kw)


class TestTheStageOverlapsHosts:
    @pytest.mark.asyncio
    async def test_eight_hosts_do_not_cost_eight_sequential_collections(self, slow_ssh):
        """The defect in one number: 8 hosts x 0.12 s was 0.96 s serial."""
        started = time.monotonic()
        await _run()
        elapsed = time.monotonic() - started

        assert set(slow_ssh.seen) == set(HOSTS), "not every host was collected"
        assert elapsed < 0.7, (
            f"gate 6 took {elapsed:.2f}s for {len(HOSTS)} hosts — "
            f"still running them one at a time"
        )

    @pytest.mark.asyncio
    async def test_every_host_is_still_visited_exactly_once(self, slow_ssh):
        await _run()
        assert sorted(slow_ssh.seen) == sorted(HOSTS)

    @pytest.mark.asyncio
    async def test_the_fan_out_is_bounded(self, slow_ssh):
        """These collectors are BLOCKING clients on the shared default
        executor. Unbounded fan-out starves every other stage of a thread."""
        live = 0
        peak = 0

        class _Counting(_SlowCollector):
            async def run(self, targets, sink):
                nonlocal live, peak
                live += 1
                peak = max(peak, live)
                try:
                    await super().run(targets, sink)
                finally:
                    live -= 1

        import unittest.mock as m
        with m.patch.object(we, "SSHCollector", _Counting):
            await _run(host_concurrency=3)
        assert peak <= 3, f"{peak} collections in flight against a limit of 3"


class TestTheContractIsUnchanged:
    @pytest.mark.asyncio
    async def test_a_host_never_seen_alive_is_skipped(self, slow_ssh):
        assets = {h: we.Asset(host=h, profile="it") for h in HOSTS[:3]}
        await _run(HOSTS[:3], assets=assets)
        assert slow_ssh.seen == [], "collected from a host never seen alive"

    @pytest.mark.asyncio
    async def test_no_creds_means_no_collection(self, slow_ssh):
        await we.run_engagement(
            HOSTS[:3], SCOPE, profile="it", rate=100_000, concurrency=10,
            timeout=0.01, disc_timeout=0.01, retries=0,
            assets=_seeded(HOSTS[:3]), port_override=[80])
        assert slow_ssh.seen == []

    @pytest.mark.asyncio
    async def test_a_second_pass_does_not_recollect(self, slow_ssh):
        """`cred_collected` is the guard; concurrency must not bypass it."""
        assets = _seeded(HOSTS[:2])
        for _ in range(2):
            await _run(HOSTS[:2], assets=assets)
        assert len(slow_ssh.seen) == 2, slow_ssh.seen

    @pytest.mark.asyncio
    async def test_one_host_failing_does_not_abort_its_peers(self, slow_ssh):
        class _Exploding(_SlowCollector):
            async def run(self, targets, sink):
                if targets and targets[0] == HOSTS[0]:
                    raise RuntimeError("ssh collection blew up")
                await super().run(targets, sink)

        import unittest.mock as m
        with m.patch.object(we, "SSHCollector", _Exploding):
            await _run()
        assert set(slow_ssh.seen) == set(HOSTS[1:]), \
            "a single host's failure took the stage down"
