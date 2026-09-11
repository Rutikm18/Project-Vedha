"""
Finding ownership + explicit close time.

The mobilization gap: SLA windows existed, remediation recipes existed, but
nothing recorded WHO owns a finding or WHEN it actually closed. Without an owner
a report is a list of problems with no path to anyone's queue; without a close
timestamp there is no MTTR.

Scope correction found while implementing: only `assigned_to` is actually new.
`resolved_at`, `resolution_method` and `resolution_run_id` ALREADY exist (the
coverage-gated auto-resolver writes them), as do first_seen/last_seen. So MTTR
needs no schema work at all — it was a computation gap, not a data gap. The tests
below still assert the resolution columns, deliberately: the metrics service is
built on them, and if they ever disappear MTTR should fail loudly here rather
than silently become uncomputable.
"""
from __future__ import annotations

from app.models.finding import Finding


class TestOwnershipColumns:
    def test_assigned_to_exists(self):
        assert "assigned_to" in Finding.__table__.columns

    def test_resolved_at_exists(self):
        assert "resolved_at" in Finding.__table__.columns

    def test_assigned_to_is_nullable(self):
        """Unassigned is the normal state — most findings never get an owner."""
        assert Finding.__table__.columns["assigned_to"].nullable is True

    def test_resolved_at_is_nullable(self):
        """Null means still open; it is the presence of a value that means closed."""
        assert Finding.__table__.columns["resolved_at"].nullable is True

    def test_assigned_to_is_indexed(self):
        """'What is on my plate' is a per-owner query and must not table-scan."""
        col = Finding.__table__.columns["assigned_to"]
        assert col.index is True or any(
            "assigned_to" in idx.columns for idx in Finding.__table__.indexes)

    def test_resolved_at_is_timezone_aware(self):
        """Naive timestamps would make MTTR wrong by the UTC offset."""
        assert Finding.__table__.columns["resolved_at"].type.timezone is True


class TestMttrInputsAlreadyExist:
    """Guards the assumption the metrics service is built on — if these ever go
    away, MTTR silently becomes uncomputable rather than obviously broken."""

    def test_first_seen_exists(self):
        assert "first_seen" in Finding.__table__.columns

    def test_last_seen_exists(self):
        assert "last_seen" in Finding.__table__.columns
