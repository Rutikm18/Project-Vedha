"""Add fenced execution attempts for agent-dispatched scan jobs.

Revision ID: 0017
Revises: 0016
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0017"
down_revision: Union[str, None] = "0016"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "scan_job_attempts",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("job_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("attempt_number", sa.Integer(), nullable=False),
        sa.Column("fence", sa.BigInteger(), nullable=False),
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(length=16), server_default="running", nullable=False),
        sa.Column("claimed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("heartbeat_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("lease_expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("result_checksum", sa.String(length=64), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint("attempt_number > 0", name="ck_scan_job_attempt_number_positive"),
        sa.CheckConstraint("fence > 0", name="ck_scan_job_attempt_fence_positive"),
        sa.CheckConstraint(
            "status IN ('running', 'succeeded', 'failed', 'expired', 'cancelled', 'stale')",
            name="ck_scan_job_attempt_status",
        ),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["job_id"], ["scan_jobs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("job_id", "attempt_number", name="uq_scan_job_attempt_number"),
        sa.UniqueConstraint("job_id", "fence", name="uq_scan_job_attempt_fence"),
    )
    op.create_index("ix_scan_job_attempts_job_id", "scan_job_attempts", ["job_id"])
    op.create_index("ix_scan_job_attempts_agent_id", "scan_job_attempts", ["agent_id"])
    op.create_index("ix_scan_job_attempts_lease_expires_at", "scan_job_attempts", ["lease_expires_at"])
    op.create_index(
        "uq_scan_job_attempts_one_running",
        "scan_job_attempts",
        ["job_id"],
        unique=True,
        postgresql_where=sa.text("status = 'running'"),
    )

    op.add_column("scan_jobs", sa.Column("current_attempt_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("scan_jobs", sa.Column("current_fence", sa.BigInteger(), server_default="0", nullable=False))
    op.add_column("scan_jobs", sa.Column("attempt_count", sa.Integer(), server_default="0", nullable=False))
    op.add_column("scan_jobs", sa.Column("max_attempts", sa.Integer(), server_default="3", nullable=False))
    op.create_index("ix_scan_jobs_current_attempt_id", "scan_jobs", ["current_attempt_id"])
    op.create_foreign_key(
        "fk_scan_jobs_current_attempt_id",
        "scan_jobs",
        "scan_job_attempts",
        ["current_attempt_id"],
        ["id"],
        ondelete="SET NULL",
        deferrable=True,
        initially="DEFERRED",
    )
    # A pre-fencing agent attempt cannot safely be adopted because no immutable
    # attempt/fence was issued to the running probe. Fail it for explicit
    # operator review instead of requeueing and risking concurrent network work.
    op.execute(sa.text("""
        UPDATE scan_jobs
        SET status = 'failed',
            completed_at = now(),
            lease_expires_at = NULL,
            result = COALESCE(result, '{}'::jsonb) ||
                '{"error":"legacy running probe attempt stopped during fencing migration; review before retry"}'::jsonb
        WHERE status = 'running' AND agent_id IS NOT NULL
    """))
    op.add_column("scan_results", sa.Column("attempt_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("scan_results", sa.Column("agent_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("scan_results", sa.Column("content_checksum", sa.String(length=64), nullable=True))
    op.add_column(
        "scan_results",
        sa.Column("validation_state", sa.String(length=16), server_default="accepted", nullable=False),
    )
    op.create_foreign_key(
        "fk_scan_results_attempt_id", "scan_results", "scan_job_attempts",
        ["attempt_id"], ["id"], ondelete="RESTRICT",
    )
    op.create_foreign_key(
        "fk_scan_results_agent_id", "scan_results", "agents",
        ["agent_id"], ["id"], ondelete="RESTRICT",
    )
    op.create_index("ix_scan_results_attempt_id", "scan_results", ["attempt_id"], unique=True)
    op.create_index("ix_scan_results_agent_id", "scan_results", ["agent_id"])


def downgrade() -> None:
    op.drop_index("ix_scan_results_agent_id", table_name="scan_results")
    op.drop_index("ix_scan_results_attempt_id", table_name="scan_results")
    op.drop_constraint("fk_scan_results_agent_id", "scan_results", type_="foreignkey")
    op.drop_constraint("fk_scan_results_attempt_id", "scan_results", type_="foreignkey")
    op.drop_column("scan_results", "validation_state")
    op.drop_column("scan_results", "content_checksum")
    op.drop_column("scan_results", "agent_id")
    op.drop_column("scan_results", "attempt_id")
    op.drop_constraint("fk_scan_jobs_current_attempt_id", "scan_jobs", type_="foreignkey")
    op.drop_index("ix_scan_jobs_current_attempt_id", table_name="scan_jobs")
    op.drop_column("scan_jobs", "max_attempts")
    op.drop_column("scan_jobs", "attempt_count")
    op.drop_column("scan_jobs", "current_fence")
    op.drop_column("scan_jobs", "current_attempt_id")
    op.drop_index("uq_scan_job_attempts_one_running", table_name="scan_job_attempts")
    op.drop_index("ix_scan_job_attempts_lease_expires_at", table_name="scan_job_attempts")
    op.drop_index("ix_scan_job_attempts_agent_id", table_name="scan_job_attempts")
    op.drop_index("ix_scan_job_attempts_job_id", table_name="scan_job_attempts")
    op.drop_table("scan_job_attempts")
