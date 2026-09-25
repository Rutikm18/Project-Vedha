"""Per-run finding membership — which findings each detection run touched

Run-level counts (new/reaffirmed/current) can't answer "what did scan X find" or
diff two scans. This records one row per (run, finding) with its outcome, written
in the same transaction as the finding writes.

Revision ID: 0047
Revises: 0046
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0047"
down_revision: Union[str, None] = "0046"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "detection_run_findings",
        sa.Column("run_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("detection_runs.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("finding_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("findings.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("outcome", sa.String(16), nullable=False),
    )
    op.create_index("ix_detection_run_findings_finding_id", "detection_run_findings", ["finding_id"])


def downgrade() -> None:
    op.drop_index("ix_detection_run_findings_finding_id", table_name="detection_run_findings")
    op.drop_table("detection_run_findings")
