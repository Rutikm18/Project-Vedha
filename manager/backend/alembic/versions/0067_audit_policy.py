"""Audit-log retention setting (tenant_settings.audit_policy).

Revision ID: 0067
Revises: 0066
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg

revision = "0067"
down_revision = "0066"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("tenant_settings", sa.Column(
        "audit_policy", pg.JSONB(), nullable=False, server_default=sa.text("'{}'::jsonb")))


def downgrade():
    op.drop_column("tenant_settings", "audit_policy")
