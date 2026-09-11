"""recurring scan schedules

Vedha could only be told "scan now". Every run started from scratch and nothing
re-checked an estate on its own — the difference between an assessment tool and a
monitoring product: exposure that appears on a Tuesday stays invisible until
someone remembers to look.

Deliberately an interval + next_run_at rather than a cron expression. Cron buys
calendar precision nobody asked for and costs a parser, a timezone story, and a
whole class of "why did it not fire" questions. A plain next_run_at column also
makes "what is due" one indexed query instead of evaluating every schedule on
every worker tick.

Revision ID: 0040
Revises: 0039
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0040"
down_revision: Union[str, None] = "0039"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "scan_schedules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
        sa.Column("engagement_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False),
        sa.Column("use_case_id", sa.String(64), nullable=False),
        sa.Column("intensity", sa.Integer(), nullable=False, server_default="2"),
        sa.Column("interval_hours", sa.Integer(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("last_run_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("next_run_at", sa.DateTime(timezone=True), nullable=False),
        # SET NULL, not CASCADE: a schedule must keep running when the person who
        # created it leaves the company.
        sa.Column("created_by", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True),
                  server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_scan_schedules_tenant_id", "scan_schedules", ["tenant_id"])
    op.create_index("ix_scan_schedules_engagement_id", "scan_schedules", ["engagement_id"])
    # The worker's hot path: "which schedules are due now".
    op.create_index("ix_scan_schedules_next_run_at", "scan_schedules", ["next_run_at"])


def downgrade() -> None:
    op.drop_index("ix_scan_schedules_next_run_at", table_name="scan_schedules")
    op.drop_index("ix_scan_schedules_engagement_id", table_name="scan_schedules")
    op.drop_index("ix_scan_schedules_tenant_id", table_name="scan_schedules")
    op.drop_table("scan_schedules")
