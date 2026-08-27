"""Finding lifecycle audit trail — append-only per-finding event log.

One row per transition (detected, confirmed, remediated, accepted, reopened,
resolved, …) with the actor and the exact timestamp. Immutable: no updated_at.
Cascades with its parent finding. Indexed on (finding_id, occurred_at) so a
finding's timeline reads back in a single ordered scan.

Revision ID: 0033
Revises: 0032
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0033"
down_revision: Union[str, None] = "0032"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "finding_events",
        sa.Column("id", postgresql.UUID(as_uuid=True),
                  server_default=sa.text("gen_random_uuid()"), primary_key=True),
        sa.Column("finding_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("findings.id", ondelete="CASCADE"), nullable=False),
        sa.Column("event_type", sa.String(length=32), nullable=False),
        sa.Column("actor", sa.String(length=255), nullable=True),
        sa.Column("actor_type", sa.String(length=16), server_default="system", nullable=False),
        sa.Column("from_status", sa.String(length=16), nullable=True),
        sa.Column("to_status", sa.String(length=16), nullable=True),
        sa.Column("detail", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), server_default=sa.text("now()"),
                  nullable=False),
    )
    op.create_index("ix_finding_events_finding_id", "finding_events", ["finding_id"])
    op.create_index("ix_finding_events_event_type", "finding_events", ["event_type"])
    op.create_index("ix_finding_events_occurred_at", "finding_events", ["occurred_at"])
    # The timeline read: every event for one finding, oldest-first.
    op.create_index("ix_finding_events_finding_time", "finding_events",
                    ["finding_id", "occurred_at"])


def downgrade() -> None:
    op.drop_index("ix_finding_events_finding_time", table_name="finding_events")
    op.drop_index("ix_finding_events_occurred_at", table_name="finding_events")
    op.drop_index("ix_finding_events_event_type", table_name="finding_events")
    op.drop_index("ix_finding_events_finding_id", table_name="finding_events")
    op.drop_table("finding_events")
