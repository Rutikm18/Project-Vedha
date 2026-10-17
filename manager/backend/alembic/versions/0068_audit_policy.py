"""Audit-log retention setting (tenant_settings.audit_policy).

Revision ID: 0068
Revises: 0067
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg

revision = "0068"
down_revision = "0067"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("tenant_settings", sa.Column(
        "audit_policy", pg.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")))


def downgrade():
    op.drop_column("tenant_settings", "audit_policy")
