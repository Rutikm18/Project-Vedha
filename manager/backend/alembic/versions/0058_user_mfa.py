"""User MFA (TOTP): encrypted secret, replay guard, hashed recovery codes

* users.mfa_secret_enc — the TOTP shared secret, encrypted at rest (Fernet).
* users.mfa_last_step — the last accepted 30-second step; a code is never accepted twice.
* users.mfa_enabled_at — when MFA was turned on.
* users.mfa_recovery_hashes — keyed hashes of the unused one-time recovery codes.

`users.mfa_enabled` already exists (it was never used); every existing user keeps
it false, so nothing changes until someone enrols or a policy requires it.

Revision ID: 0058
Revises: 0057
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0058"
down_revision: Union[str, None] = "0057"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("mfa_secret_enc", sa.String(512), nullable=True))
    op.add_column("users", sa.Column("mfa_last_step", sa.BigInteger(), nullable=True))
    op.add_column("users", sa.Column("mfa_enabled_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("users", sa.Column(
        "mfa_recovery_hashes", postgresql.JSONB(), nullable=False, server_default=sa.text("'[]'::jsonb"),
    ))


def downgrade() -> None:
    op.drop_column("users", "mfa_recovery_hashes")
    op.drop_column("users", "mfa_enabled_at")
    op.drop_column("users", "mfa_last_step")
    op.drop_column("users", "mfa_secret_enc")
