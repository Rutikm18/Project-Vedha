"""User.portal_password_enc — encrypted, operator-recoverable customer portal password.

Adds a nullable column holding the client login's temp password encrypted at rest
(Fernet, keyed off jwt_secret). Auth still uses the bcrypt hash; this is a separate
recoverable copy so an operator can re-reveal a customer's credential.

Revision ID: 0029
Revises: 0028
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0029"
down_revision: Union[str, None] = "0028"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("portal_password_enc", sa.String(length=512), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "portal_password_enc")
