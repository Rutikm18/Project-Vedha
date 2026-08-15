"""Client portal slug — the customer's stable 'user as domain' handle.

Adds users.portal_slug: a URL-safe per-customer identifier auto-generated when a
client login is provisioned. Today it brands the shared portal; once a wildcard
domain exists it becomes the customer's subdomain (<slug>.portal.<domain>).
Unique per tenant so two customers never collide on a handle/subdomain.

Revision ID: 0026
Revises: 0025
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0026"
down_revision: Union[str, None] = "0025"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("portal_slug", sa.String(length=63), nullable=True))
    op.create_unique_constraint(
        "uq_user_tenant_portal_slug", "users", ["tenant_id", "portal_slug"]
    )


def downgrade() -> None:
    op.drop_constraint("uq_user_tenant_portal_slug", "users", type_="unique")
    op.drop_column("users", "portal_slug")
