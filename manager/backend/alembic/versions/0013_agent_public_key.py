"""Add agents.public_key (Phase-4 X25519 identity for scope encryption).

The probe registers a base64-encoded X25519 public key so the manager can
encrypt engagement-scope payloads to it. The Agent model gained this column but
no migration was ever generated, so probe registration crashed with
`column agents.public_key does not exist` (HTTP 500) — no probe could connect.

Revision ID: 0013
Revises: 0012
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0013"
down_revision: Union[str, None] = "0012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("agents", sa.Column("public_key", sa.String(64), nullable=True))


def downgrade() -> None:
    op.drop_column("agents", "public_key")
