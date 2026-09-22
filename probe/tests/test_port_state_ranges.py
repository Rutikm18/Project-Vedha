"""
F1/F3 — report every port's state, not just the open ones.

WHAT IS MISSING TODAY
---------------------
`_retain_result` keeps an observation only if the port is OPEN (or the operator
passed --report-closed). Everything else is tallied into a counter and dropped:

    "open": 3, "closed": 65000, "filtered": 510

So a result can say 65,000 ports were closed but not WHICH, and nothing
distinguishes "closed" from "filtered" from "never reached" for any specific
port. An operator asking "was 8443 closed or filtered on this host?" cannot be
answered from the evidence, only re-scanned for.

The obvious fix — keep every observation — is the one that was deliberately
removed: it cost 47 MB per host, and the port stage scans every live host at
once (measured 4.7 GB at 100 hosts, which the OS answers with a kill).

WHY RANGES
----------
The information an operator needs is the STATE PER PORT, not a ScanResult
object per port. A byte per port is 64 KB for the whole TCP space — about
1,000x cheaper than the objects — and run-length encoding collapses it to a
handful of ranges, because port states cluster hard:

    closed:   [[1,21],[23,79],[81,442],[444,65535]]

Same information, four entries instead of 65,535. That is what makes "all the
data" affordable to hold, to submit, and to store.
"""
from __future__ import annotations

import pytest

from scanner.port_scanner import ScanMetrics


def _metrics(requested: set[int] | None = None) -> ScanMetrics:
    ports = requested if requested is not None else set(range(1, 11))
    return ScanMetrics(target="10.0.0.1", vantage="probe-1",
                       ports_requested=len(ports), requested_ports=set(ports))


def _observe(metrics: ScanMetrics, states: dict[int, str]) -> None:
    for port, state in states.items():
        metrics.note_state(port, state)


# ── run-length encoding ─────────────────────────────────────────────────────

class TestEncoding:
    def test_consecutive_ports_collapse_into_one_range(self):
        m = _metrics()
        _observe(m, {p: "closed" for p in range(1, 11)})
        assert m.state_ranges()["closed"] == [[1, 10]]

    def test_a_gap_splits_the_range(self):
        m = _metrics()
        _observe(m, {p: "closed" for p in (1, 2, 3, 7, 8)})
        assert m.state_ranges()["closed"] == [[1, 3], [7, 8]]

    def test_a_single_port_is_its_own_range(self):
        m = _metrics()
        _observe(m, {5: "filtered"})
        assert m.state_ranges()["filtered"] == [[5, 5]]

    def test_states_are_reported_separately(self):
        m = _metrics()
        _observe(m, {1: "closed", 2: "closed", 3: "filtered", 4: "open"})
        ranges = m.state_ranges()
        assert ranges["closed"] == [[1, 2]]
        assert ranges["filtered"] == [[3, 3]]
        assert ranges["open"] == [[4, 4]]

    def test_a_state_nothing_matched_is_absent(self):
        m = _metrics()
        _observe(m, {1: "closed"})
        assert "unreachable" not in m.state_ranges()

    def test_nothing_requested_and_nothing_observed_yields_nothing(self):
        assert _metrics(set()).state_ranges() == {}

    def test_requested_but_nothing_observed_is_all_not_scanned(self):
        """A sweep that never ran is not a sweep that found nothing."""
        assert _metrics(set(range(1, 11))).state_ranges() == {
            "not_scanned": [[1, 10]]}


# ── the honest part: ports never reached ────────────────────────────────────

class TestNotScanned:
    def test_requested_but_unobserved_ports_are_reported_not_scanned(self):
        """The distinction the budget work depends on: a port the clock never
        reached is NOT evidence of a firewall."""
        m = _metrics(set(range(1, 11)))
        _observe(m, {p: "closed" for p in range(1, 6)})
        assert m.state_ranges()["not_scanned"] == [[6, 10]]

    def test_a_complete_sweep_reports_nothing_not_scanned(self):
        m = _metrics(set(range(1, 11)))
        _observe(m, {p: "closed" for p in range(1, 11)})
        assert "not_scanned" not in m.state_ranges()

    def test_not_scanned_is_never_conflated_with_filtered(self):
        m = _metrics(set(range(1, 11)))
        _observe(m, {p: "filtered" for p in range(1, 4)})
        ranges = m.state_ranges()
        assert ranges["filtered"] == [[1, 3]]
        assert ranges["not_scanned"] == [[4, 10]]


# ── round trip: the encoding must lose nothing ──────────────────────────────

def _expand(ranges: dict[str, list[list[int]]]) -> dict[int, str]:
    out: dict[int, str] = {}
    for state, spans in ranges.items():
        for low, high in spans:
            for port in range(low, high + 1):
                out[port] = state
    return out


class TestRoundTrip:
    def test_a_realistic_host_reconstructs_exactly(self):
        requested = set(range(1, 1001))
        original = {p: "closed" for p in requested}
        for p in (22, 80, 443, 3306):
            original[p] = "open"
        for p in range(600, 650):
            original[p] = "filtered"

        m = _metrics(requested)
        _observe(m, original)
        assert _expand(m.state_ranges()) == original

    def test_the_whole_tcp_space_reconstructs_exactly(self):
        """65,535 ports in and 65,535 ports out, via a handful of ranges."""
        requested = set(range(1, 65536))
        original = {p: "closed" for p in requested}
        for p in (22, 443, 8443, 49152):
            original[p] = "open"
        for p in range(30000, 30500):
            original[p] = "filtered"

        m = _metrics(requested)
        _observe(m, original)
        ranges = m.state_ranges()
        assert _expand(ranges) == original
        # The point of the exercise: a handful of entries, not 65,535.
        assert sum(len(v) for v in ranges.values()) < 20

    @pytest.mark.parametrize("seed", [1, 7, 42])
    def test_arbitrary_state_patterns_round_trip(self, seed):
        import random

        rng = random.Random(seed)
        requested = set(range(1, 501))
        states = ("open", "closed", "filtered", "unreachable")
        original = {p: rng.choice(states) for p in requested}

        m = _metrics(requested)
        _observe(m, original)
        assert _expand(m.state_ranges()) == original


# ── cost ────────────────────────────────────────────────────────────────────

def test_a_full_sweep_costs_a_byte_per_port_not_an_object():
    """The constraint that killed the obvious implementation: holding every
    observation cost 47 MB/host. A byte per port is 64 KB."""
    import sys

    m = _metrics(set(range(1, 65536)))
    _observe(m, {p: "closed" for p in range(1, 65536)})
    assert sys.getsizeof(m._port_state) < 200_000


def test_the_summary_carries_the_ranges():
    m = _metrics(set(range(1, 11)))
    _observe(m, {1: "open", 2: "closed"})
    summary = m.summary()
    assert "port_states" in summary
    assert summary["port_states"]["open"] == [[1, 1]]
