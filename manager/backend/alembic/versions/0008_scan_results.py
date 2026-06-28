"""P3-#10: append-only scan_results table (raw facts).

Decouples the (large) raw facts payload from scan_jobs so jobs stay lean and
detection can be re-run against an updated vuln DB without re-scanning.

Revision ID: 0008
Revises: 0007
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0008"
down_revision: Union[str, None] = "0007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "scan_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"),
                  primary_key=True),
        sa.Column("engagement_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False),
        sa.Column("job_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("scan_type", sa.String(64), nullable=True),
        sa.Column("fact_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("facts", postgresql.JSONB(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_scan_results_engagement_id", "scan_results", ["engagement_id"])
    op.create_index("ix_scan_results_job_id", "scan_results", ["job_id"])


def downgrade() -> None:
    op.drop_index("ix_scan_results_job_id", table_name="scan_results")
    op.drop_index("ix_scan_results_engagement_id", table_name="scan_results")
    op.drop_table("scan_results")
