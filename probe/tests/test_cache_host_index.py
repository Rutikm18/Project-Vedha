"""
C4 — per-host cache lookup must not scan the whole cache.

THE COST THIS REMOVES
---------------------
`_commit_host` hands ONE host's evidence to the manager, and it found that
evidence by walking every entry in the cache:

    facts = [asdict(entry.result) for entry in cache._store.values()
             if getattr(entry.result, "target", None) == host]

It runs once per host, over a cache that grows with every host, so the whole
job is O(hosts x total_entries). Measured on this machine with 51 facts/host:

      50 hosts ( 2,550 entries) -> 0.4 ms/host
     200 hosts (10,200 entries) -> 0.7 ms/host
     500 hosts (25,500 entries) -> 1.9 ms/host
    1000 hosts (51,000 entries) -> 5.0 ms/host, 4.98 s total

Quadratic, and spent on the EVENT LOOP — `_scan_one_host_logged` awaits the
commit directly, so every other host's scan stalls behind it. At MAX_TARGETS
(4096) it is roughly 80 s of pure bookkeeping.

The cache is already keyed `(host, port, scanner)`, so the host is right there
in the key. A secondary index turns the lookup into O(that host's facts).

NOTE ON MEMORY: the sibling task assumed the cache also grew to gigabytes and
needed eviction. Measured, a realistic 25-open-port host costs ~60 KB, so 1000
hosts is ~60 MB — eviction is not warranted and would risk the final result,
which is still built from the whole cache. Only the lookup cost was real.
"""
from __future__ import annotations

import time

from scanner.scanner_base import ScanResult
from workflow.cache import WorkflowCache


def _fact(host: str, port: int, scanner: str = "port_scan") -> ScanResult:
    return ScanResult(scanner, host, port=port, proto="tcp", status="open",
                      data={"reason": "connect_success"})


def _fill(cache: WorkflowCache, hosts: int, facts_per_host: int = 51) -> list[str]:
    names = [f"10.{i // 65536}.{(i // 256) % 256}.{i % 256}" for i in range(hosts)]
    for host in names:
        for port in range(1, facts_per_host + 1):
            cache.put(_fact(host, port))
    return names


# ── correctness first: the index must agree with a full scan ────────────────

class TestTheIndexIsCorrect:
    def test_returns_exactly_that_host_s_entries(self):
        cache = WorkflowCache()
        _fill(cache, hosts=3, facts_per_host=4)
        entries = cache.all_entries_for_host("10.0.0.1")
        assert len(entries) == 4
        assert {e.host for e in entries} == {"10.0.0.1"}

    def test_agrees_with_an_exhaustive_scan(self):
        """The index is a shortcut, never a different answer."""
        cache = WorkflowCache()
        hosts = _fill(cache, hosts=5, facts_per_host=6)
        for host in hosts:
            indexed = sorted(
                (e.host, e.port, e.scanner) for e in cache.all_entries_for_host(host))
            scanned = sorted(
                (e.host, e.port, e.scanner)
                for (h, _, _), e in cache._store.items() if h == host)
            assert indexed == scanned, host

    def test_an_unknown_host_returns_empty(self):
        cache = WorkflowCache()
        _fill(cache, hosts=2, facts_per_host=2)
        assert cache.all_entries_for_host("192.168.99.99") == []

    def test_overwriting_a_key_does_not_duplicate_the_index_entry(self):
        """put() on the same (host, port, scanner) replaces, so must the index."""
        cache = WorkflowCache()
        cache.put(_fact("10.0.0.1", 80))
        cache.put(_fact("10.0.0.1", 80))
        assert len(cache.all_entries_for_host("10.0.0.1")) == 1
        assert len(cache._store) == 1

    def test_the_index_survives_a_jsonl_round_trip(self, tmp_path):
        """_load() populates _store directly — the index must be built there too."""
        path = tmp_path / "cache.jsonl"
        cache = WorkflowCache(path)
        _fill(cache, hosts=3, facts_per_host=4)
        cache.save()

        reloaded = WorkflowCache(path)
        assert len(reloaded.all_entries_for_host("10.0.0.1")) == 4
        assert len(reloaded._store) == 12

    def test_distinct_scanners_on_one_port_are_all_indexed(self):
        cache = WorkflowCache()
        cache.put(_fact("10.0.0.1", 443, scanner="port_scan"))
        cache.put(_fact("10.0.0.1", 443, scanner="service_banner"))
        cache.put(_fact("10.0.0.1", 443, scanner="tls_scan"))
        assert len(cache.all_entries_for_host("10.0.0.1")) == 3


# ── and it must actually be cheaper ─────────────────────────────────────────

def test_lookup_cost_does_not_grow_with_the_rest_of_the_cache():
    """The quadratic blow-up, pinned.

    Same per-host fact count, 20x the cache. A linear scan gets ~20x slower;
    an indexed lookup stays flat. The threshold is deliberately loose (4x) so
    this measures COMPLEXITY, not the speed of the machine running CI.
    """
    small = WorkflowCache()
    _fill(small, hosts=50)
    large = WorkflowCache()
    hosts = _fill(large, hosts=1000)

    def _timed(cache, host, reps=200):
        start = time.perf_counter()
        for _ in range(reps):
            cache.all_entries_for_host(host)
        return (time.perf_counter() - start) / reps

    small_cost = _timed(small, "10.0.0.1")
    large_cost = _timed(large, hosts[0])

    assert large_cost < small_cost * 4, (
        f"lookup scales with cache size: {small_cost * 1e6:.0f}us at 2,550 "
        f"entries vs {large_cost * 1e6:.0f}us at 51,000"
    )


def test_commit_host_uses_the_indexed_accessor():
    """Source-level: the engine re-implemented the scan inline rather than
    calling all_entries_for_host, so indexing the accessor alone fixes nothing.
    """
    import inspect

    from workflow import workflow_engine

    src = inspect.getsource(workflow_engine.run_engagement)
    assert "all_entries_for_host" in src, \
        "_commit_host must use the indexed accessor"
    assert "cache._store.values()" not in src, \
        "_commit_host still walks the whole cache"
