"""
test_reference.py — the human-readable reference scheme.

A scan job could only be named by its UUID, shown in the UI as eight hex
characters. The properties that matter for something a customer reads down a
phone line and types back are pinned here: it survives transcription, it never
changes once issued, and the migration's SQL backfill agrees with the
application, so historical and new jobs follow one rule.
"""
from __future__ import annotations

import decimal
import uuid
from datetime import datetime, timezone
from decimal import Decimal

import pytest

from app.models.scan_job import ScanJob, _stamp_reference
from app.services import reference as R


def _at(y=2026, m=9, d=2):
    return datetime(y, m, d, 12, 0, tzinfo=timezone.utc)


class TestShape:
    def test_reads_as_prefix_date_code(self):
        ref = R.scan_job_reference(uuid.uuid4(), _at())
        prefix, date, suffix = ref.split("-")
        assert prefix == "SCN"
        assert date == "260902"
        assert len(suffix) == 6

    def test_uses_the_rows_own_date_not_today(self):
        """A backfilled reference must match what the row would have been given
        when it was created."""
        assert "-240115-" in R.scan_job_reference(uuid.uuid4(), _at(2024, 1, 15))

    def test_naive_created_at_is_treated_as_utc(self):
        naive = datetime(2026, 9, 2, 12, 0)
        assert "-260902-" in R.scan_job_reference(uuid.uuid4(), naive)

    def test_an_unknown_prefix_is_refused(self):
        with pytest.raises(ValueError):
            R.make_reference("XXX", uuid.uuid4())


class TestSurvivesBeingReadAloud:
    """The whole point of the scheme: a human relays it."""

    def test_the_confusable_letters_are_absent(self):
        # I/L/O/U never appear, so they cannot be misread as 1/1/0/V.
        for _ in range(2000):
            suffix = R.suffix_for(uuid.uuid4())
            assert not (set(suffix) & set("ILOU")), suffix

    def test_typed_back_lowercase_still_resolves(self):
        ref = R.scan_job_reference(uuid.uuid4(), _at())
        assert R.normalize(ref.lower()) == ref

    def test_o_for_zero_and_l_for_one_resolve(self):
        assert R.normalize("SCN-260902-7K3MQO") == "SCN-260902-7K3MQ0"
        assert R.normalize("SCN-260902-7K3MQL") == "SCN-260902-7K3MQ1"

    def test_stray_spaces_are_tolerated(self):
        assert R.normalize(" scn-260902-7k3mqp ") == "SCN-260902-7K3MQP"

    def test_only_the_suffix_is_alias_folded(self):
        """The prefix and date are literal — folding them would corrupt a date."""
        assert R.normalize("SCN-260901-ABCDEF") == "SCN-260901-ABCDEF"


class TestTellingThemApart:
    def test_a_reference_is_distinguishable_from_a_uuid(self):
        ref = R.scan_job_reference(uuid.uuid4(), _at())
        assert R.is_reference(ref) is True
        assert R.is_reference(str(uuid.uuid4())) is False
        assert R.is_reference("") is False
        assert R.is_reference("SCN-260902-TOOLONGX") is False

    def test_an_unregistered_prefix_is_not_ours(self):
        assert R.is_reference("ZZZ-260902-ABCDEF") is False


class TestStability:
    def test_the_same_row_always_gets_the_same_reference(self):
        """It is quoted in tickets — it must not move."""
        u, when = uuid.uuid4(), _at()
        assert R.scan_job_reference(u, when) == R.scan_job_reference(u, when)

    def test_different_rows_get_different_references(self):
        seen = {R.suffix_for(uuid.uuid4()) for _ in range(20_000)}
        # 32**6 space; a handful of collisions in 20k would still be tolerable,
        # but anything worse means the fold is clustering.
        assert len(seen) >= 19_990, f"only {len(seen)} distinct suffixes in 20000"


class TestStamping:
    def test_every_insert_gets_one(self):
        job = ScanJob()
        _stamp_reference(None, None, job)
        assert job.id is not None
        assert R.is_reference(job.reference)

    def test_an_explicit_reference_is_never_overwritten(self):
        job = ScanJob(reference="SCN-000000-KEEPME")
        _stamp_reference(None, None, job)
        assert job.reference == "SCN-000000-KEEPME"

    def test_the_reference_matches_the_row_id(self):
        job = ScanJob()
        _stamp_reference(None, None, job)
        assert job.reference.endswith(R.suffix_for(job.id))


def test_the_migration_backfill_agrees_with_the_application():
    """Migration 0036 backfills in SQL so it needs no application layer. If the
    two derivations ever diverge, historical jobs and new jobs carry references
    built by different rules — and nobody would notice until a customer quoted
    one that did not exist."""
    decimal.getcontext().prec = 60          # UUID ints are 39 digits
    alphabet = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

    def as_sql_does(u: uuid.UUID) -> str:
        n = Decimal(u.int) % Decimal(32 ** 6)
        return "".join(alphabet[int(n / Decimal(32 ** i)) % 32] for i in range(5, -1, -1))

    for _ in range(5_000):
        u = uuid.uuid4()
        assert as_sql_does(u) == R.suffix_for(u), u
