"""
T1.4 (probe half) — hours of port-sweep evidence must survive a killed process.

`_commit_host` only ran at the END of the deep-scan stage. Every stage before
it — discovery, the port sweep, OS fingerprint, banners — reached the manager
only through the job's FINAL submission. A wide scan spends its hours in the
port stage, so the most expensive evidence was the least protected: if the
process died there (OOM on a 65,535-port sweep, container evicted) or the
submission was fenced out, the manager held nothing and the operator saw a
failed job that apparently scanned nothing.

Worse, a job whose stage ceiling stops before deep_scan — `discovery`,
`port_scan`, `service_fingerprint`, which is most jobs — returned early and
committed NOTHING, ever.

Commits now happen at every stage boundary, marked `complete=False` so the
manager's resume list still only skips genuinely finished hosts (see
manager/tests/test_partial_chunk_commits.py for that half). The commit at a
job's own ceiling IS final, so those are marked complete.
"""
from __future__ import annotations

import asyncio

import pytest

from scanner.scanner_base import ScopeGuard
from workflow import workflow_engine as we


class _Recorder:
    """Stands in for the probe's chunk sink."""

    def __init__(self):
        self.calls: list[tuple[str, bool, int]] = []

    async def __call__(self, host, facts, *, complete=True):
        self.calls.append((host, complete, len(facts)))

    @property
    def hosts(self) -> set[str]:
        return {h for h, _, _ in self.calls}

    def completeness_for(self, host: str) -> list[bool]:
        return [c for h, c, _ in self.calls if h == host]


@pytest.fixture
def scope():
    return ScopeGuard.from_list(["10.99.0.0/24"], strict=True)


async def _run(scope, sink, *, stage_ceiling):
    """Drive run_engagement against unreachable hosts.

    Nothing answers, so every stage completes instantly — but the COMMIT
    contract is what is under test, and it does not depend on any host
    replying.
    """
    return await we.run_engagement(
        ["10.99.0.1", "10.99.0.2"], scope,
        profile="it", rate=5000, concurrency=20, timeout=0.01,
        disc_timeout=0.01, retries=0,
        stage_ceiling=stage_ceiling,
        on_host_complete=sink,
    )


class TestEveryCeilingDeliversSomething:
    @pytest.mark.asyncio
    async def test_a_host_discovery_job_commits(self, scope):
        """Previously returned early and committed nothing at all."""
        sink = _Recorder()
        await _run(scope, sink, stage_ceiling="host_discovery")
        assert sink.calls, "a host_discovery job delivered no chunk"

    @pytest.mark.asyncio
    async def test_a_port_scan_job_commits(self, scope):
        sink = _Recorder()
        await _run(scope, sink, stage_ceiling="port_scan")
        assert sink.calls, "a port_scan job delivered no chunk"

    @pytest.mark.asyncio
    async def test_a_service_fingerprint_job_commits(self, scope):
        sink = _Recorder()
        await _run(scope, sink, stage_ceiling="service_banner")
        assert sink.calls, "a service_fingerprint job delivered no chunk"

    @pytest.mark.asyncio
    async def test_a_full_assessment_still_commits(self, scope):
        sink = _Recorder()
        await _run(scope, sink, stage_ceiling="deep_scan")
        assert sink.calls


async def _run_local(sink, *, stage_ceiling):
    """A REACHABLE host, so the pipeline actually advances past discovery.

    Two closed ports keep it fast; the commit contract does not depend on
    finding anything open.
    """
    return await we.run_engagement(
        ["127.0.0.1"], ScopeGuard.from_list(["127.0.0.0/8"], strict=True),
        profile="it", rate=5000, concurrency=20, timeout=0.05,
        disc_timeout=0.2, retries=0, port_override=[7, 9],
        stage_ceiling=stage_ceiling, on_host_complete=sink,
    )


class TestCompletenessIsHonest:
    @pytest.mark.asyncio
    async def test_the_commit_at_a_job_s_own_ceiling_is_final(self):
        """A port_scan job that reaches the port stage IS done with that host.
        Marking it partial would make every retry rescan the whole estate."""
        sink = _Recorder()
        await _run_local(sink, stage_ceiling="port_scan")
        assert sink.completeness_for("127.0.0.1")[-1] is True, sink.calls

    @pytest.mark.asyncio
    async def test_intermediate_commits_are_marked_partial(self):
        """The safety property: mid-pipeline evidence must never suppress a
        rescan. If an early commit claimed completeness, a probe killed in the
        port stage would resume having skipped everything it had discovered."""
        sink = _Recorder()
        await _run_local(sink, stage_ceiling="service_banner")
        flags = sink.completeness_for("127.0.0.1")
        assert len(flags) > 1, f"expected several boundaries, got {sink.calls}"
        assert all(f is False for f in flags[:-1]), flags
        assert flags[-1] is True, flags

    @pytest.mark.asyncio
    async def test_evidence_grows_across_the_boundaries(self):
        """Each commit carries strictly more than the last, which is why the
        manager replaces rather than appends."""
        sink = _Recorder()
        await _run_local(sink, stage_ceiling="service_banner")
        counts = [n for h, _, n in sink.calls if h == "127.0.0.1"]
        assert counts == sorted(counts) and counts[0] < counts[-1], counts

    @pytest.mark.asyncio
    async def test_a_host_that_never_answered_is_never_marked_complete(self, scope):
        """Liveness is classified `uncertain` on purpose — a host can come back
        between attempts — so a retry must be free to re-check it."""
        sink = _Recorder()
        await _run(scope, sink, stage_ceiling="port_scan")
        assert sink.calls, "the dead host's evidence was not delivered at all"
        assert all(c is False for _, c, _ in sink.calls), sink.calls


class TestTheCommitContract:
    @pytest.mark.asyncio
    async def test_a_sink_failure_never_fails_the_scan(self, scope):
        """The buffer is an optimisation; the final submission is the
        authoritative delivery."""
        async def _explode(host, facts, *, complete=True):
            raise RuntimeError("manager unreachable")

        assets = await _run(scope, _explode, stage_ceiling="deep_scan")
        assert assets, "a failing chunk sink took the scan down with it"

    @pytest.mark.asyncio
    async def test_no_sink_is_supported(self, scope):
        """Standalone runs and managers without the endpoint pass None."""
        assets = await we.run_engagement(
            ["10.99.0.1"], scope, profile="it", rate=5000, concurrency=20,
            timeout=0.01, disc_timeout=0.01, retries=0,
            stage_ceiling="port_scan", on_host_complete=None)
        assert assets

    @pytest.mark.asyncio
    async def test_a_sink_that_does_not_accept_complete_still_works(self, scope):
        """Backwards compatible: the kwarg must be optional at the call site,
        so an older sink signature is not a crash."""
        seen = []

        async def _legacy(host, facts):
            seen.append(host)

        await _run(scope, _legacy, stage_ceiling="port_scan")
        assert seen, "a legacy two-argument sink was never called"


def test_the_engine_commits_at_every_ceiling():
    """Source-level: each early return must deliver before it returns, or the
    bounded-ceiling job types silently go back to committing nothing."""
    import inspect

    src = inspect.getsource(we.run_engagement)
    # Each `return assets` that ends a bounded run is preceded by a commit.
    returns = [line for line in src.splitlines() if "return assets" in line]
    assert len(returns) >= 3, "expected the bounded-ceiling early returns"
    assert src.count("_commit_stage(") >= 3, \
        "a stage ceiling returns without committing its evidence"
