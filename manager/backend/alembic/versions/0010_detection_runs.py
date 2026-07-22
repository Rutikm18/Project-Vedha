"""Temporal detection: detection_runs table + finding provenance columns.

Records each detection-engine execution (which facts, which vuln-DB snapshot,
what changed) and stamps findings with first_seen / last_seen / detection_run_id
so findings become a time series ("what changed since yesterday") and detection
can be re-run against a newer snapshot and diffed.

Revision ID: 0010
Revises: 0009
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0010"
down_revision: Union[str, None] = "0009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "detection_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"),
                  primary_key=True),
        sa.Column("engagement_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False),
        sa.Column("scan_result_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("trigger", sa.String(32), nullable=False, server_default="facts_ready"),
        sa.Column("status", sa.String(16), nullable=False, server_default="running"),
        sa.Column("vuln_db_version", sa.String(128), nullable=True),
        sa.Column("vuln_db_fetched_at", sa.String(64), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("facts_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("findings_new", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("findings_reaffirmed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("findings_current", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("stats", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_detection_runs_engagement_id", "detection_runs", ["engagement_id"])

    # Finding provenance / temporal columns.
    op.add_column("findings", sa.Column("first_seen", sa.DateTime(timezone=True), nullable=True))
    op.add_column("findings", sa.Column("last_seen", sa.DateTime(timezone=True), nullable=True))
    op.add_column("findings", sa.Column(
        "detection_run_id", postgresql.UUID(as_uuid=True),
        sa.ForeignKey("detection_runs.id", ondelete="SET NULL"), nullable=True,
    ))
    op.create_index("ix_findings_detection_run_id", "findings", ["detection_run_id"])

    # Backfill: existing findings get first_seen/last_seen from created_at so the
    # time series is continuous rather than starting null.
    op.execute("UPDATE findings SET first_seen = created_at, last_seen = created_at "
               "WHERE first_seen IS NULL")


def downgrade() -> None:
    op.drop_index("ix_findings_detection_run_id", table_name="findings")
    op.drop_column("findings", "detection_run_id")
    op.drop_column("findings", "last_seen")
    op.drop_column("findings", "first_seen")
    op.drop_index("ix_detection_runs_engagement_id", table_name="detection_runs")
    op.drop_table("detection_runs")
