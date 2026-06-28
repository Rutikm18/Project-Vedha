"""P3: composite indexes for the hot aggregate + poll query paths.

The dashboard's /engagements/overview groups findings by
(engagement_id, severity, status); the agent poll filters scan_jobs by
(agent_id, status). The existing single-column indexes don't serve these
multi-column predicates well — a composite index lets Postgres satisfy them
with one index scan instead of a filter over a broader index.

Revision ID: 0007
Revises: 0006
"""
from typing import Sequence, Union

from alembic import op

revision: str = "0007"
down_revision: Union[str, None] = "0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Serves: SELECT ... WHERE engagement_id IN (...) GROUP BY engagement_id, severity, status
    op.create_index(
        "ix_findings_eng_sev_status", "findings",
        ["engagement_id", "severity", "status"], unique=False,
    )
    # Serves: SELECT ... WHERE agent_id = ? AND status = 'pending'  (the poll)
    op.create_index(
        "ix_scan_jobs_agent_status", "scan_jobs",
        ["agent_id", "status"], unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_scan_jobs_agent_status", table_name="scan_jobs")
    op.drop_index("ix_findings_eng_sev_status", table_name="findings")
