"""findings gain a `content_overrides` JSONB column

Per-finding explanation, business impact, technical detail, evidence-as-facts and
compliance mapping are produced deterministically on read by the finding_content /
finding_compliance / evidence_summary services — no storage needed, and they stay
fresh as the knowledge base improves. What DOES need to be recorded is the
exception: AI-generated prose or an analyst's manual edit that should override the
deterministic text for a specific finding. That is what this column holds.

Nullable and defaulting to NULL: the overwhelming majority of findings use the pure
KB and store nothing here, so this adds no write cost to the detection path.

Revision ID: 0038
Revises: 0037
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0038"
down_revision: Union[str, None] = "0037"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "findings",
        sa.Column("content_overrides", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("findings", "content_overrides")
