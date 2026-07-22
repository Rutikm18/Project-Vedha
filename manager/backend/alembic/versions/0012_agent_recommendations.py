"""Agentic AI advisor: agent_recommendations (recommend-only, human-approved).

Stores decisions/actions the Claude tool-use advisor proposes over an
engagement's real data (triage / next-action / attack-path). Every row is
"pending" until a human approves it — the agent never executes anything.

Revision ID: 0012
Revises: 0011
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0012"
down_revision: Union[str, None] = "0011"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "agent_recommendations",
        sa.Column("id", postgresql.UUID(as_uuid=True), server_default=sa.text("gen_random_uuid()"),
                  primary_key=True),
        sa.Column("engagement_id", postgresql.UUID(as_uuid=True),
                  sa.ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False),
        sa.Column("run_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("category", sa.String(32), nullable=False),
        sa.Column("target_type", sa.String(32), nullable=True),
        sa.Column("target_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("action", sa.String(64), nullable=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=True),
        sa.Column("confidence", sa.Numeric(4, 1), nullable=True),
        sa.Column("priority", sa.String(16), nullable=True),
        sa.Column("status", sa.String(16), nullable=False, server_default="pending"),
        sa.Column("evidence", postgresql.JSONB(), nullable=True),
        sa.Column("model", sa.String(64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
    )
    op.create_index("ix_agent_recommendations_engagement_id", "agent_recommendations", ["engagement_id"])
    op.create_index("ix_agent_recommendations_run_id", "agent_recommendations", ["run_id"])


def downgrade() -> None:
    op.drop_index("ix_agent_recommendations_run_id", table_name="agent_recommendations")
    op.drop_index("ix_agent_recommendations_engagement_id", table_name="agent_recommendations")
    op.drop_table("agent_recommendations")
