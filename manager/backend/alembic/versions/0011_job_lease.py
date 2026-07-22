"""Job leasing: scan_jobs.lease_expires_at for the dead-probe reaper.

A claimed (running) job carries a lease renewed on each probe heartbeat; the
reaper requeues running jobs whose lease has expired, so a probe that dies
mid-scan doesn't leave the job stuck 'running' forever.

Revision ID: 0011
Revises: 0010
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0011"
down_revision: Union[str, None] = "0010"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "scan_jobs",
        sa.Column("lease_expires_at", sa.DateTime(timezone=True), nullable=True),
    )
    # Partial index on the reaper's hot predicate: only running jobs with a lease.
    op.create_index(
        "ix_scan_jobs_lease_expires_at", "scan_jobs", ["lease_expires_at"],
        postgresql_where=sa.text("lease_expires_at IS NOT NULL"),
    )


def downgrade() -> None:
    op.drop_index("ix_scan_jobs_lease_expires_at", table_name="scan_jobs")
    op.drop_column("scan_jobs", "lease_expires_at")
