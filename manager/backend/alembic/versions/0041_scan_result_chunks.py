"""per-host evidence buffer for running jobs

A job's facts reached the manager exactly once, at the end. A probe that died
mid-scan — OOM-killed on a deep sweep, container evicted, host rebooted — took
every host it had already finished with it; the lease expired, the retry started
from zero, and three attempts later the job failed having scanned the same hosts
three times and reported none of them.

A chunk is one HOST's facts, committed as soon as that host is done. It is a
BUFFER, not a second result path: the job still completes with one scan_results
row (the final submission merged with any chunk it does not cover), so detection,
coverage and campaign progress are unchanged. If the job dies instead, the
reaper promotes the chunks into a scan_results row so the evidence survives.

UNIQUE (job_id, host) because a later attempt that rescans a host REPLACES its
evidence — two attempts must not leave two opinions about the same host.

Revision ID: 0041
Revises: 0040
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0041"
down_revision: Union[str, None] = "0040"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "scan_result_chunks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("engagement_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("engagements.id", ondelete="CASCADE"),
                  nullable=False),
        sa.Column("job_id", postgresql.UUID(as_uuid=True), nullable=False),
        # NOT unique, unlike scan_results.attempt_id: one attempt commits many hosts.
        sa.Column("attempt_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("agents.id", ondelete="RESTRICT"), nullable=True),
        sa.Column("host", sa.String(255), nullable=False),
        sa.Column("scan_type", sa.String(64), nullable=True),
        sa.Column("content_checksum", sa.String(64), nullable=True),
        sa.Column("fact_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("facts", postgresql.JSONB(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.UniqueConstraint("job_id", "host", name="uq_result_chunk_job_host"),
    )
    op.create_index("ix_scan_result_chunks_engagement_id",
                    "scan_result_chunks", ["engagement_id"])
    # The hot read: "what has this job already committed" — the merge on final
    # submission, the promotion on failure, and the probe's resume query.
    op.create_index("ix_scan_result_chunks_job_id",
                    "scan_result_chunks", ["job_id"])
    op.create_index("ix_scan_result_chunks_attempt_id",
                    "scan_result_chunks", ["attempt_id"])
    op.create_index("ix_scan_result_chunks_agent_id",
                    "scan_result_chunks", ["agent_id"])


def downgrade() -> None:
    op.drop_index("ix_scan_result_chunks_agent_id", table_name="scan_result_chunks")
    op.drop_index("ix_scan_result_chunks_attempt_id", table_name="scan_result_chunks")
    op.drop_index("ix_scan_result_chunks_job_id", table_name="scan_result_chunks")
    op.drop_index("ix_scan_result_chunks_engagement_id", table_name="scan_result_chunks")
    op.drop_table("scan_result_chunks")
