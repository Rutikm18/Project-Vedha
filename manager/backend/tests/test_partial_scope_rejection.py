"""
B1 — one out-of-scope identity must not destroy the whole result.

THE FAILURE THIS REMOVES
------------------------
validate_result_scope() is all-or-nothing: a single unparseable or out-of-scope
target anywhere in the payload returns 422 + permanent_rejection, and the probe
treats that as terminal (agent/transport.py maps 422 to PERMANENT_REJECTION and
quarantines the file). A 1000-host scan is discarded in full because of one bad
row, leaving only a `job.result_scope_rejected` log line.

The probability of that scales with host count and with breadth, so the widest,
longest, most expensive scans are the ones most likely to lose everything. The
run-scoped-fact fix (test_run_scoped_fact_scope.py) patched ONE emitter; this
changes the RULE.

WHY PARTIAL ACCEPTANCE IS NOT A WEAKENING
-----------------------------------------
The control exists so a probe cannot launder an out-of-scope host into the
inventory. Partitioning still drops every rejected identity — byte for byte the
same entries never reach the database. What changes is only that authorized
evidence stops being collateral damage. Detection is untouched:
validate_result_scope() keeps its exact semantics and every test in
test_run_scoped_fact_scope.py still pins it.

Fail-closed is preserved where it matters: if NOTHING survives the partition,
the result is still refused. An empty accepted result would be recorded as "we
scanned and found nothing", which is a worse lie than a rejection.
"""
from __future__ import annotations

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models.enums import ScanJobStatus
from app.services.job_result_service import (
    apply_scope_gate,
    partition_result_scope,
    process_job_result,
    validate_result_scope,
)

SCOPE = ["10.20.0.0/24"]


def _fact(target: str, scanner: str = "port_scan", **extra):
    return {"scanner": scanner, "target": target, "status": "open", **extra}


# ── the partition itself ────────────────────────────────────────────────────

class TestPartition:
    def test_keeps_authorized_facts_and_drops_the_rest(self):
        result = {"facts": [_fact("10.20.0.5"), _fact("8.8.8.8"),
                            _fact("10.20.0.6")]}
        kept, rejected = partition_result_scope(result, SCOPE)
        assert [f["target"] for f in kept["facts"]] == ["10.20.0.5", "10.20.0.6"]
        assert [r["value"] for r in rejected] == ["8.8.8.8"]

    def test_filters_hosts_and_findings_too(self):
        result = {
            "hosts": [{"ip": "10.20.0.5"}, {"ip": "203.0.113.1"}],
            "facts": [_fact("10.20.0.5")],
            "findings": [{"target": "10.20.0.5"}, {"target": "203.0.113.1"}],
        }
        kept, rejected = partition_result_scope(result, SCOPE)
        assert kept["hosts"] == [{"ip": "10.20.0.5"}]
        assert kept["findings"] == [{"target": "10.20.0.5"}]
        assert len(rejected) == 2

    def test_run_scoped_facts_are_kept_not_filtered(self):
        """They contribute NO identity, so they were never rejected.

        ipv6_discovery's target is an interface or the literal "auto". The
        exemption means it is not judged at all — dropping it would re-create
        the very data loss this module exists to stop, just more quietly.
        """
        result = {"facts": [_fact("auto", scanner="ipv6_discovery"),
                            _fact("10.20.0.5")]}
        kept, rejected = partition_result_scope(result, SCOPE)
        assert rejected == []
        assert len(kept["facts"]) == 2

    def test_entries_without_an_identity_key_are_kept(self):
        # A scan_summary fact carries no `target`; it is not a host claim.
        result = {"facts": [{"scanner": "port_scan", "status": "scan_summary"},
                            _fact("10.20.0.5")]}
        kept, rejected = partition_result_scope(result, SCOPE)
        assert rejected == [] and len(kept["facts"]) == 2

    def test_excluded_cidr_entries_are_dropped(self):
        result = {"facts": [_fact("10.20.0.9"), _fact("10.20.0.5")]}
        kept, rejected = partition_result_scope(result, SCOPE, ["10.20.0.9/32"])
        assert [f["target"] for f in kept["facts"]] == ["10.20.0.5"]
        assert [r["value"] for r in rejected] == ["10.20.0.9"]

    def test_hostname_identities_are_dropped_not_accepted(self):
        # Authorization is IP/CIDR-only. This is the probe/manager divergence
        # that silently destroyed results; it must drop the row, never pass it.
        result = {"facts": [_fact("evil.example.com"), _fact("10.20.0.5")]}
        kept, rejected = partition_result_scope(result, SCOPE)
        assert [f["target"] for f in kept["facts"]] == ["10.20.0.5"]
        assert [r["value"] for r in rejected] == ["evil.example.com"]

    def test_does_not_mutate_the_input(self):
        result = {"facts": [_fact("10.20.0.5"), _fact("8.8.8.8")]}
        before = [dict(f) for f in result["facts"]]
        partition_result_scope(result, SCOPE)
        assert result["facts"] == before

    def test_preserves_unrelated_top_level_keys(self):
        result = {"facts": [_fact("8.8.8.8")], "scan_type": "assessment",
                  "run_stats": {"host_count": 1}}
        kept, _ = partition_result_scope(result, SCOPE)
        assert kept["scan_type"] == "assessment"
        assert kept["run_stats"] == {"host_count": 1}

    def test_agrees_exactly_with_the_detector(self):
        """partition and validate must never disagree about what is authorized.

        Two implementations of one security rule is how a gate silently opens.
        """
        result = {
            "hosts": [{"ip": "10.20.0.1"}, {"ip": "1.1.1.1"}],
            "facts": [_fact("10.20.0.2"), _fact("nope"), _fact("10.20.0.9"),
                      _fact("auto", scanner="ipv6_discovery")],
            "findings": [{"target": "203.0.113.7"}],
        }
        _, rejected = partition_result_scope(result, SCOPE, ["10.20.0.9/32"])
        detected = validate_result_scope(result, SCOPE, ["10.20.0.9/32"])
        assert rejected == detected


# ── policy: what process_job_result does with a partition ───────────────────

def _job(scope=SCOPE, excluded=None):
    attempt_id = uuid.uuid4()
    row = SimpleNamespace(
        status=ScanJobStatus.running,
        current_attempt_id=attempt_id,
        current_fence=5,
        engagement_id=uuid.uuid4(),
        result={"_scope_cidrs": scope, "_excluded_cidrs": excluded or []},
    )
    db = MagicMock()
    attempt = SimpleNamespace(status="running", result_checksum=None)
    db.execute = AsyncMock(side_effect=[
        MagicMock(scalar_one_or_none=lambda: row),
        MagicMock(scalar_one_or_none=lambda: attempt),
    ])
    db.flush = AsyncMock()
    return db, row, attempt_id


class TestPolicy:
    """The decision itself, kept DB-free.

    apply_scope_gate() is pure precisely so this security policy can be pinned
    without mocking the whole ingest pipeline behind it — the same reason
    scan_health and doctor keep their logic separate from their IO.
    """

    def test_one_bad_identity_no_longer_discards_the_good_evidence(self):
        """The headline: a scan survives one unparseable row."""
        good = [_fact(f"10.20.0.{n}") for n in range(1, 20)]
        kept, rejected, refusal = apply_scope_gate(
            {"facts": [*good, _fact("not-an-ip")]}, SCOPE)
        assert refusal is None
        assert len(rejected) == 1
        assert len(kept["facts"]) == 19

    def test_a_wholly_out_of_scope_result_is_still_refused(self):
        """Fail-closed is preserved: nothing survived, so nothing is accepted."""
        _, _, refusal = apply_scope_gate(
            {"facts": [_fact("10.20.0.9")]}, SCOPE, ["10.20.0.9/32"])
        assert refusal is not None
        assert refusal["status_code"] == 422
        assert refusal["permanent_rejection"] is True
        assert refusal["ok"] is False

    def test_an_all_rejected_payload_of_many_rows_is_also_refused(self):
        _, _, refusal = apply_scope_gate(
            {"facts": [_fact("8.8.8.8"), _fact("1.1.1.1")],
             "hosts": [{"ip": "9.9.9.9"}]}, SCOPE)
        assert refusal is not None and refusal["status_code"] == 422

    def test_a_clean_result_is_passed_through_untouched(self):
        payload = {"facts": [_fact("10.20.0.5")]}
        kept, rejected, refusal = apply_scope_gate(payload, SCOPE)
        assert refusal is None and rejected == []
        assert "scope_rejected" not in kept

    def test_a_partial_acceptance_records_the_rejection_in_the_payload(self):
        """Persisted with the result so a finding can be raised from it."""
        kept, _, _ = apply_scope_gate(
            {"facts": [_fact("10.20.0.5"), _fact("8.8.8.8")]}, SCOPE)
        assert kept["scope_rejected"]["count"] == 1
        assert kept["scope_rejected"]["surviving_entries"] == 1
        assert kept["scope_rejected"]["sample"][0]["value"] == "8.8.8.8"

    def test_the_rejection_sample_is_bounded(self):
        """A pathological payload must not write 50,000 rows into the result."""
        noisy = {"facts": [_fact(f"8.8.8.{n}") for n in range(60)]
                          + [_fact("10.20.0.5")]}
        kept, rejected, refusal = apply_scope_gate(noisy, SCOPE)
        assert refusal is None
        assert len(rejected) == 60
        assert len(kept["scope_rejected"]["sample"]) == 10
        assert kept["scope_rejected"]["count"] == 60


class TestPolicyReachesTheIngestPath:
    @pytest.mark.asyncio
    async def test_a_wholly_out_of_scope_result_still_422s_end_to_end(self):
        """The pre-existing security test's scenario, unchanged."""
        db, row, attempt_id = _job(excluded=["10.20.0.9/32"])
        summary = await process_job_result(
            db, uuid.uuid4(), uuid.uuid4(), True,
            {"facts": [_fact("10.20.0.9")]}, None, attempt_id, 5,
        )
        assert summary["ok"] is False
        assert summary["status_code"] == 422
        assert summary["permanent_rejection"] is True
        assert row.status == ScanJobStatus.running
        db.add.assert_not_called()

    def test_the_result_path_uses_the_gate_and_reports_what_it_dropped(self):
        """Source-level, matching test_result_chunk_merge's approach: the wiring
        is what regresses, and there is no DB fixture to drive it end to end."""
        import inspect

        src = inspect.getsource(process_job_result)
        assert "apply_scope_gate" in src
        assert "validate_result_scope(" not in src, \
            "the all-or-nothing gate must not come back"
        assert "scope_rejected_count" in src, \
            "a silent partial acceptance hides a scope divergence"


# ── the finding raised from a partial acceptance ────────────────────────────

class TestScopeRejectionFinding:
    """Ingesting the authorized part is right; doing it silently is not.

    A partial acceptance means something asked this probe to report a host the
    engagement did not authorize. That needs a human, so it gets a finding.
    """

    @pytest.mark.asyncio
    async def test_a_partial_acceptance_raises_one_finding(self):
        from app.discovery import finding_translator as ft

        db = MagicMock()
        db.flush = AsyncMock()
        db.execute = AsyncMock(
            return_value=MagicMock(scalar_one_or_none=lambda: None))

        kept, _, _ = apply_scope_gate(
            {"facts": [_fact("10.20.0.5"), _fact("8.8.8.8")],
             "scan_type": "assessment"}, SCOPE)
        created = await ft.create_scope_rejection_finding(
            db, uuid.uuid4(), kept)

        assert created == 1
        finding = db.add.call_args[0][0]
        assert finding.title == ft._SCOPE_REJECTED_TITLE
        assert "8.8.8.8" in finding.description
        assert finding.evidence["scope_rejected"]["count"] == 1

    @pytest.mark.asyncio
    async def test_it_is_medium_not_low(self):
        """An authorization-boundary event, not a scan-quality one."""
        from app.models.enums import FindingSeverity
        from app.discovery import finding_translator as ft

        db = MagicMock()
        db.flush = AsyncMock()
        db.execute = AsyncMock(
            return_value=MagicMock(scalar_one_or_none=lambda: None))
        kept, _, _ = apply_scope_gate(
            {"facts": [_fact("10.20.0.5"), _fact("8.8.8.8")]}, SCOPE)

        await ft.create_scope_rejection_finding(db, uuid.uuid4(), kept)
        assert db.add.call_args[0][0].severity == FindingSeverity.medium

    @pytest.mark.asyncio
    async def test_a_clean_result_raises_nothing(self):
        from app.discovery import finding_translator as ft

        db = MagicMock()
        kept, _, _ = apply_scope_gate({"facts": [_fact("10.20.0.5")]}, SCOPE)
        assert await ft.create_scope_rejection_finding(db, uuid.uuid4(), kept) == 0
        db.add.assert_not_called()

    @pytest.mark.asyncio
    async def test_a_chronic_divergence_refreshes_instead_of_piling_up(self):
        from app.discovery import finding_translator as ft

        existing = SimpleNamespace(evidence=None, description=None, last_seen=None)
        db = MagicMock()
        db.flush = AsyncMock()
        db.execute = AsyncMock(
            return_value=MagicMock(scalar_one_or_none=lambda: existing))
        kept, _, _ = apply_scope_gate(
            {"facts": [_fact("10.20.0.5"), _fact("8.8.8.8")]}, SCOPE)

        assert await ft.create_scope_rejection_finding(db, uuid.uuid4(), kept) == 0
        db.add.assert_not_called()
        assert existing.evidence["scope_rejected"]["count"] == 1
        assert existing.last_seen is not None
