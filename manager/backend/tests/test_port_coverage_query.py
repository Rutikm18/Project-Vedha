"""
F2 — make "what was port 8443 on this host?" answerable.

The probe now records EVERY requested port's state, run-length encoded, on the
per-host scan_summary fact (see probe/tests/test_port_state_ranges.py):

    {"scanner": "port_scan", "target": "10.0.0.5", "status": "scan_summary",
     "data": {"port_states": {"closed": [[1,21],[23,442]],
                              "open": [[22,22],[443,443]],
                              "not_scanned": [[10000,65535]]}}}

That already reaches the manager and is already persisted inside
scan_results.facts — it simply was not queryable. No migration and no probe
change are needed here; this is the read side.

WHY THE FOUR-WAY ANSWER MATTERS
-------------------------------
`open` / `closed` / `filtered` / `not_scanned` are four different facts about
the world, and the last two are the ones that get conflated:

  * filtered    — probed, stayed silent. Evidence about the TARGET.
  * not_scanned — never probed (budget, cap, truncated sweep). Evidence about
                  the SCAN.

Reporting "not scanned" as "filtered" would claim a firewall that may not
exist, which is the false-negative class this whole workstream removes. And a
port absent from every range is `unknown` — not `closed`.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.services.port_coverage import (
    decode_port_states,
    port_state_at,
    summarize_coverage,
)

RANGES = {
    "open": [[22, 22], [443, 443]],
    "closed": [[1, 21], [23, 442]],
    "filtered": [[500, 510]],
    "not_scanned": [[1000, 65535]],
}


# ── the decoder ─────────────────────────────────────────────────────────────

class TestPortStateAt:
    @pytest.mark.parametrize("port,expected", [
        (22, "open"), (443, "open"),
        (1, "closed"), (21, "closed"), (23, "closed"), (442, "closed"),
        (500, "filtered"), (505, "filtered"), (510, "filtered"),
        (1000, "not_scanned"), (65535, "not_scanned"),
    ])
    def test_every_state_is_reported_exactly(self, port, expected):
        assert port_state_at(RANGES, port) == expected

    def test_a_port_in_no_range_is_unknown_not_closed(self):
        """Absence of evidence is not evidence of a closed port."""
        assert port_state_at(RANGES, 800) == "unknown"

    def test_boundaries_are_inclusive(self):
        assert port_state_at({"closed": [[10, 20]]}, 10) == "closed"
        assert port_state_at({"closed": [[10, 20]]}, 20) == "closed"
        assert port_state_at({"closed": [[10, 20]]}, 21) == "unknown"

    def test_empty_ranges_are_unknown(self):
        assert port_state_at({}, 443) == "unknown"
        assert port_state_at(None, 443) == "unknown"

    def test_malformed_spans_are_ignored_not_crashed(self):
        """Facts come off the wire; a bad span must not 500 the query."""
        bad = {"closed": [[10], "nope", [30, 20], None, [40, 45]]}
        assert port_state_at(bad, 42) == "closed"
        assert port_state_at(bad, 10) == "unknown"


class TestDecode:
    def test_expands_to_one_entry_per_port(self):
        expanded = decode_port_states({"open": [[22, 22]], "closed": [[80, 82]]})
        assert expanded == {22: "open", 80: "closed", 81: "closed", 82: "closed"}

    def test_a_full_sweep_expands_to_the_whole_space(self):
        expanded = decode_port_states({"closed": [[1, 65535]]})
        assert len(expanded) == 65535

    def test_decode_and_lookup_agree(self):
        expanded = decode_port_states(RANGES)
        for port in (1, 22, 442, 443, 505, 1000, 65535):
            assert expanded[port] == port_state_at(RANGES, port)


# ── the per-host rollup ─────────────────────────────────────────────────────

class TestCoverageSummary:
    def test_counts_each_state(self):
        summary = summarize_coverage(RANGES)
        assert summary["open"] == 2
        assert summary["closed"] == 21 + 420
        assert summary["filtered"] == 11
        assert summary["not_scanned"] == 64536

    def test_reports_what_share_was_actually_probed(self):
        """`not_scanned` is the number that says how much to trust the rest."""
        summary = summarize_coverage(RANGES)
        assert summary["probed"] == 2 + 441 + 11
        assert summary["total"] == summary["probed"] + 64536
        assert 0.0 < summary["probed_fraction"] < 0.01

    def test_a_complete_sweep_is_fully_probed(self):
        summary = summarize_coverage({"closed": [[1, 65535]]})
        assert summary["not_scanned"] == 0
        assert summary["probed_fraction"] == 1.0

    def test_nothing_measured_is_not_a_division_by_zero(self):
        summary = summarize_coverage({})
        assert summary["total"] == 0
        assert summary["probed_fraction"] == 0.0


# ── pulling it out of stored facts ──────────────────────────────────────────

def _facts():
    return [
        {"scanner": "port_scan", "target": "10.0.0.5", "port": 22,
         "status": "open"},
        {"scanner": "port_scan", "target": "10.0.0.5", "status": "scan_summary",
         "data": {"port_states": RANGES}},
        {"scanner": "port_scan", "target": "10.0.0.9", "status": "scan_summary",
         "data": {"port_states": {"open": [[80, 80]]}}},
    ]


class TestExtraction:
    def test_finds_the_ranges_for_one_host(self):
        from app.services.port_coverage import ranges_from_facts

        assert ranges_from_facts(_facts(), "10.0.0.5") == RANGES

    def test_a_host_with_no_summary_yields_nothing(self):
        from app.services.port_coverage import ranges_from_facts

        assert ranges_from_facts(_facts(), "10.0.0.77") == {}

    def test_ignores_facts_that_are_not_scan_summaries(self):
        from app.services.port_coverage import ranges_from_facts

        only_open = [f for f in _facts() if f["status"] == "open"]
        assert ranges_from_facts(only_open, "10.0.0.5") == {}

    def test_a_later_definitive_state_wins_and_extends_coverage(self):
        """A second summary for the same host (e.g. the port tail re-scanning
        a port the first pass also covered) must MERGE with, not replace,
        the earlier one: its new port (8443, previously not_scanned) is
        added, and its re-affirmed port (22) keeps agreeing, while every
        port the second summary never mentions keeps its first verdict."""
        from app.services.port_coverage import ranges_from_facts

        facts = _facts() + [
            {"scanner": "port_scan", "target": "10.0.0.5",
             "status": "scan_summary",
             "data": {"port_states": {"open": [[22, 22], [8443, 8443]]}}},
        ]
        result = ranges_from_facts(facts, "10.0.0.5")
        assert result == {
            "open": [[22, 22], [443, 443], [8443, 8443]],
            "closed": [[1, 21], [23, 442]],
            "filtered": [[500, 510]],
            # 8443 sat inside RANGES' [1000, 65535] not_scanned span; the
            # later definitive "open" for it splits that span around it.
            "not_scanned": [[1000, 8442], [8444, 65535]],
        }

    def test_two_summaries_with_disjoint_ports_both_survive_the_merge(self):
        """The realistic two-phase shape: a first-pass summary over the
        high-signal ports and a tail summary over the rest, with NO overlap
        in what each one even mentions."""
        from app.services.port_coverage import ranges_from_facts

        first_pass = {"open": [[22, 22]], "closed": [[80, 80]]}
        tail = {"closed": [[443, 443]], "not_scanned": [[8000, 8000]]}
        facts = [
            {"scanner": "port_scan", "target": "10.0.0.5",
             "status": "scan_summary", "data": {"port_states": first_pass}},
            {"scanner": "syn_scan", "target": "10.0.0.5",
             "status": "scan_summary", "data": {"port_states": tail}},
        ]

        assert ranges_from_facts(facts, "10.0.0.5") == {
            "open": [[22, 22]],
            "closed": [[80, 80], [443, 443]],
            "not_scanned": [[8000, 8000]],
        }

    def test_a_definitive_state_beats_not_scanned_regardless_of_fact_order(self):
        """A port the tail budget never reached (not_scanned) must not erase
        a definitive verdict the first pass already gave it — and the
        reverse must never invent not_scanned over a definitive answer."""
        from app.services.port_coverage import ranges_from_facts

        definitive_first = [
            {"scanner": "port_scan", "target": "10.0.0.5",
             "status": "scan_summary",
             "data": {"port_states": {"closed": [[443, 443]]}}},
            {"scanner": "syn_scan", "target": "10.0.0.5",
             "status": "scan_summary",
             "data": {"port_states": {"not_scanned": [[443, 443]]}}},
        ]
        assert ranges_from_facts(definitive_first, "10.0.0.5") == {
            "closed": [[443, 443]]}

        not_scanned_first = list(reversed(definitive_first))
        assert ranges_from_facts(not_scanned_first, "10.0.0.5") == {
            "closed": [[443, 443]]}


# ── the endpoint is wired and gated ─────────────────────────────────────────

class TestTheEndpoint:
    def test_it_is_registered_on_the_engagement_router(self):
        from app.routers.engagements import router

        paths = {r.path for r in router.routes}
        assert "/engagements/{engagement_id}/port-coverage" in paths

    def test_it_is_operator_gated_like_raw_facts(self):
        """Coverage reveals scanned topology, so it must not reach clients."""
        import inspect

        from app.routers import engagements

        src = inspect.getsource(engagements.port_coverage)
        assert 'require_role(["admin", "manager", "tester"])' in src

    def test_it_extracts_the_summary_in_sql_not_in_python(self):
        """A deep submission stores ~107 KB of facts per host. Loading a whole
        submission to read one object is exactly what raw-facts had to be
        rewritten to stop doing."""
        import inspect

        from app.routers import engagements

        src = inspect.getsource(engagements.port_coverage)
        assert "jsonb_array_elements" in src
        assert "scan_summary" in src
        # The row must come back already narrowed to the one host.
        assert "f->>'target'  = :host" in src

    def test_a_missing_host_is_a_404_not_an_empty_success(self):
        """An empty 200 would read as "every port unknown", which is a claim
        about the scan rather than an admission that none was found."""
        import inspect

        from app.routers import engagements

        src = inspect.getsource(engagements.port_coverage)
        assert "raise HTTPException(\n            404," in src


# ── F1: the endpoint must MERGE every scan_summary for the host, not pick one ─
#
# A two-phase deep scan emits two per-host scan_summary facts (first pass +
# tail, disjoint port ranges), routinely landing in the SAME scan_results row
# (one job, one submission, two facts for the host). A query that picks only
# one scan_summary fact-row silently drops whichever summary loses the
# ordering, even when both live in that one row.

def _user():
    return SimpleNamespace(tenant_id=uuid.uuid4(), user_id=uuid.uuid4(), role="admin")


class TestTheEndpointMergesEverySummaryForTheHost:
    @pytest.mark.asyncio
    async def test_two_disjoint_summaries_in_one_job_are_merged(self):
        """The realistic shape: one job, one scan_results row, two
        scan_summary facts for the same host (first pass + tail)."""
        from app.routers import engagements as eng

        engagement_id = uuid.uuid4()
        job_id = uuid.uuid4()
        t0 = datetime(2026, 1, 1, tzinfo=timezone.utc)
        facts = [
            {"scanner": "port_scan", "target": "10.0.0.5", "status": "scan_summary",
             "data": {"port_states": {"open": [[22, 22]], "closed": [[80, 80]]}}},
            {"scanner": "syn_scan", "target": "10.0.0.5", "status": "scan_summary",
             "data": {"port_states": {"closed": [[443, 443]],
                                      "not_scanned": [[8000, 8000]]}}},
        ]

        db = MagicMock()
        db.execute = AsyncMock(side_effect=[
            MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=engagement_id)),  # get_or_404
            MagicMock(first=lambda: SimpleNamespace(
                id=uuid.uuid4(), job_id=job_id, scan_type="vuln_scan",
                created_at=t0)),                                       # latest
            MagicMock(all=lambda: [SimpleNamespace(facts=facts, created_at=t0)]),  # job rows
        ])

        out = await eng.port_coverage(engagement_id, db, _user(), "10.0.0.5", None)

        assert out["port_states"] == {
            "open": [[22, 22]],
            "closed": [[80, 80], [443, 443]],
            "not_scanned": [[8000, 8000]],
        }
        assert out["coverage"]["open"] == 1

    @pytest.mark.asyncio
    async def test_summaries_split_across_the_jobs_rows_still_merge(self):
        """A job whose evidence was rescued from its chunk buffer (or
        resubmitted after a lease expiry) can land in more than one
        scan_results row under the SAME job_id — every row for that job must
        still be gathered, not just the row that happens to sort last."""
        from app.routers import engagements as eng

        engagement_id = uuid.uuid4()
        job_id = uuid.uuid4()
        t0 = datetime(2026, 1, 1, tzinfo=timezone.utc)
        t1 = datetime(2026, 1, 1, 0, 5, tzinfo=timezone.utc)
        first_pass_row = [
            {"scanner": "port_scan", "target": "10.0.0.5", "status": "scan_summary",
             "data": {"port_states": {"open": [[22, 22]], "closed": [[80, 80]]}}},
        ]
        tail_row = [
            {"scanner": "syn_scan", "target": "10.0.0.5", "status": "scan_summary",
             "data": {"port_states": {"closed": [[443, 443]],
                                      "not_scanned": [[8000, 8000]]}}},
        ]

        db = MagicMock()
        db.execute = AsyncMock(side_effect=[
            MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=engagement_id)),
            MagicMock(first=lambda: SimpleNamespace(
                id=uuid.uuid4(), job_id=job_id, scan_type="vuln_scan",
                created_at=t1)),
            MagicMock(all=lambda: [
                SimpleNamespace(facts=first_pass_row, created_at=t0),
                SimpleNamespace(facts=tail_row, created_at=t1),
            ]),
        ])

        out = await eng.port_coverage(engagement_id, db, _user(), "10.0.0.5", None)

        assert out["port_states"] == {
            "open": [[22, 22]],
            "closed": [[80, 80], [443, 443]],
            "not_scanned": [[8000, 8000]],
        }

    @pytest.mark.asyncio
    async def test_a_row_with_no_job_id_falls_back_to_that_row_alone(self):
        """Older submissions (or ones with no job_id) merge just their own
        row's summaries — there is no job to widen the lookup to."""
        from app.routers import engagements as eng

        engagement_id = uuid.uuid4()
        scan_result_id = uuid.uuid4()
        t0 = datetime(2026, 1, 1, tzinfo=timezone.utc)
        facts = [
            {"scanner": "port_scan", "target": "10.0.0.5", "status": "scan_summary",
             "data": {"port_states": {"open": [[22, 22]]}}},
        ]

        db = MagicMock()
        db.execute = AsyncMock(side_effect=[
            MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=engagement_id)),
            MagicMock(first=lambda: SimpleNamespace(
                id=scan_result_id, job_id=None, scan_type="vuln_scan",
                created_at=t0)),
            MagicMock(all=lambda: [SimpleNamespace(facts=facts, created_at=t0)]),
        ])

        out = await eng.port_coverage(engagement_id, db, _user(), "10.0.0.5", None)

        assert out["port_states"] == {"open": [[22, 22]]}

    @pytest.mark.asyncio
    async def test_an_older_scans_states_do_not_leak_into_the_current_view(self):
        """Only the most recent job's summaries are used — a single port
        query asks for one port and gets the merged map, not the union of
        every scan this engagement has ever run against the host."""
        from app.routers import engagements as eng

        engagement_id = uuid.uuid4()
        job_id = uuid.uuid4()
        t1 = datetime(2026, 1, 1, tzinfo=timezone.utc)
        current_row_facts = [
            {"scanner": "port_scan", "target": "10.0.0.5", "status": "scan_summary",
             "data": {"port_states": {"closed": [[22, 22]]}}},
        ]

        db = MagicMock()
        db.execute = AsyncMock(side_effect=[
            MagicMock(scalar_one_or_none=lambda: SimpleNamespace(id=engagement_id)),
            MagicMock(first=lambda: SimpleNamespace(
                id=uuid.uuid4(), job_id=job_id, scan_type="vuln_scan",
                created_at=t1)),
            # Only the CURRENT job's row(s) come back — an older scan's own
            # row, with port 22 reported `open`, is never queried at all.
            MagicMock(all=lambda: [SimpleNamespace(facts=current_row_facts, created_at=t1)]),
        ])

        out = await eng.port_coverage(engagement_id, db, _user(), "10.0.0.5", 22)

        assert out["state"] == "closed"
