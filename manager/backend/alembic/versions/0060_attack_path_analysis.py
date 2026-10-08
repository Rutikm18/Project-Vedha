"""Engagement-level attack-path analysis (attack-path plan P5)

* attack_path_analyses — one row per engagement holding the last computation's
  engagement-wide facts (choke points, minimum fix set, coverage, diagnostics) so
  they are stored once instead of on every path row (FM-26) and read instead of
  recomputed on every GET (FM-22).

Purely additive: nothing reads it until a recompute writes it.

Revision ID: 0060
Revises: 0059
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0060"
down_revision: Union[str, None] = "0059"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "attack_path_analyses",
        sa.Column("engagement_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("engagements.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("computed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("path_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("analysis", postgresql.JSONB(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("attack_path_analyses")
