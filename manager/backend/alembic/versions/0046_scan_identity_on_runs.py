"""Scan identity as queryable columns — use-case + intensity on jobs, job_id on runs

Findings are labelled and filtered by the scan that produced them. That needs the
scan's use-case and intensity as columns (they lived only inside scan_jobs.result
JSON) and a direct run→job link (it was run→scan_result→job). Additive + backfilled.

Revision ID: 0046
Revises: 0045
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0046"
down_revision: Union[str, None] = "0045"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("scan_jobs", sa.Column("use_case_id", sa.String(64), nullable=True))
    op.add_column("scan_jobs", sa.Column("intensity", sa.String(16), nullable=True))
    op.add_column(
        "detection_runs",
        sa.Column("job_id", postgresql.UUID(as_uuid=True), nullable=True),
    )
    op.create_index("ix_detection_runs_job_id", "detection_runs", ["job_id"])

    # Backfill run→job from the scan_result the run processed.
    op.execute(
        "UPDATE detection_runs r SET job_id = s.job_id "
        "FROM scan_results s WHERE r.scan_result_id = s.id AND r.job_id IS NULL"
    )
    # Backfill use-case / intensity best-effort from the result JSON (enqueue
    # params or the probe result blob), tolerating both shapes.
    op.execute(
        "UPDATE scan_jobs SET use_case_id = COALESCE(result->>'use_case_id', use_case_id) "
        "WHERE result ? 'use_case_id'"
    )
    op.execute(
        "UPDATE scan_jobs SET intensity = COALESCE("
        "result->>'intensity', result->'params'->>'intensity', intensity) "
        "WHERE (result ? 'intensity') OR (result->'params' ? 'intensity')"
    )


def downgrade() -> None:
    op.drop_index("ix_detection_runs_job_id", table_name="detection_runs")
    op.drop_column("detection_runs", "job_id")
    op.drop_column("scan_jobs", "intensity")
    op.drop_column("scan_jobs", "use_case_id")
