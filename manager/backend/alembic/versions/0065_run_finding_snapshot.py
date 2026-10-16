"""Per-scan snapshot of a finding's severity, risk score and status.

A finding is one mutable row, so a scan-to-scan diff could say a finding was in both
scans but not that its severity or score changed between them. These nullable columns
record the finding as each scan saw it. Rows written before this revision stay NULL and
compare shows presence only for them.

Revision ID: 0065
Revises: 0064
"""

from alembic import op
import sqlalchemy as sa

revision = "0065"
down_revision = "0064"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("detection_run_findings", sa.Column("severity", sa.String(16), nullable=True))
    op.add_column("detection_run_findings", sa.Column("risk_score", sa.Numeric(6, 2), nullable=True))
    op.add_column("detection_run_findings", sa.Column("status", sa.String(16), nullable=True))


def downgrade():
    op.drop_column("detection_run_findings", "status")
    op.drop_column("detection_run_findings", "risk_score")
    op.drop_column("detection_run_findings", "severity")
