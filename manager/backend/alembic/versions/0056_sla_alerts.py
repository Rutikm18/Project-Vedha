"""SLA alerts: remember which SLA transitions were already announced

* sla_alerts — one row per (finding, state). The SLA watcher inserts the row
  before it notifies, so each transition into "at_risk" or "breached" is announced
  once, whichever worker sees it first.

Revision ID: 0056
Revises: 0055
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0056"
down_revision: Union[str, None] = "0055"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "sla_alerts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("finding_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("findings.id", ondelete="CASCADE"), nullable=False),
        sa.Column("state", sa.String(16), nullable=False),
        sa.Column("notified_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("now()")),
        sa.UniqueConstraint("finding_id", "state", name="uq_sla_alert_finding_state"),
    )
    op.create_index("ix_sla_alerts_finding_id", "sla_alerts", ["finding_id"])


def downgrade() -> None:
    op.drop_index("ix_sla_alerts_finding_id", table_name="sla_alerts")
    op.drop_table("sla_alerts")
