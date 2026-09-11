"""
ScanSchedule: the table behind recurring rescans.

Shape decisions worth pinning, because each one is a support burden if wrong:

  * interval + next_run_at, NOT a cron expression. Cron costs a parser, a
    timezone story, and a class of "why did it not fire" questions, in exchange
    for calendar precision nobody asked for.
  * next_run_at is INDEXED — the worker's only question is "what is due now", and
    that must not scan every schedule in the system on every tick.
  * enabled, not deletion — pausing during a change freeze is routine, and
    deleting loses the configuration and its history.
  * created_by is SET NULL on user deletion: a schedule must keep running when
    the person who set it up leaves.
"""
from __future__ import annotations

from app.models.scan_schedule import ScanSchedule


class TestColumns:
    def test_has_every_required_column(self):
        cols = set(ScanSchedule.__table__.columns.keys())
        for c in ("id", "tenant_id", "engagement_id", "use_case_id", "intensity",
                  "interval_hours", "enabled", "last_run_at", "next_run_at",
                  "created_by", "created_at", "updated_at"):
            assert c in cols, c

    def test_next_run_at_is_indexed(self):
        """The worker's hot path."""
        col = ScanSchedule.__table__.columns["next_run_at"]
        assert col.index is True or any(
            "next_run_at" in i.columns for i in ScanSchedule.__table__.indexes)

    def test_next_run_at_is_not_nullable(self):
        """A schedule with no due time would never fire and never error."""
        assert ScanSchedule.__table__.columns["next_run_at"].nullable is False

    def test_last_run_at_is_nullable(self):
        """Null = never run yet, which is the state at creation."""
        assert ScanSchedule.__table__.columns["last_run_at"].nullable is True

    def test_timestamps_are_timezone_aware(self):
        for c in ("next_run_at", "last_run_at"):
            assert ScanSchedule.__table__.columns[c].type.timezone is True

    def test_enabled_defaults_to_true(self):
        assert ScanSchedule.__table__.columns["enabled"].server_default is not None


class TestRelationshipSafety:
    def test_created_by_survives_user_deletion(self):
        """SET NULL, not CASCADE — losing the author must not stop the schedule."""
        fks = list(ScanSchedule.__table__.columns["created_by"].foreign_keys)
        assert fks and fks[0].ondelete == "SET NULL"

    def test_engagement_deletion_removes_the_schedule(self):
        """CASCADE here IS right: a schedule for a deleted engagement has no
        target and would enqueue jobs forever."""
        fks = list(ScanSchedule.__table__.columns["engagement_id"].foreign_keys)
        assert fks and fks[0].ondelete == "CASCADE"

    def test_is_registered_in_the_model_aggregator(self):
        """An unregistered model is invisible to Alembic autogenerate."""
        import app.models as m
        assert hasattr(m, "ScanSchedule")
