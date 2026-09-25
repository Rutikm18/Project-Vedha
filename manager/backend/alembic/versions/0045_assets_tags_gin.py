"""GIN index on assets.tags — tag filters stay fast on large estates

Asset tags (app/intel/tagging.py) are stored as {"v", "auto": [...], "manual": [...]}.
The asset list's ?tag=key:value filter is a JSONB containment test
(tags @> {"auto": [{"key": k, "value": v}]}), which jsonb_path_ops serves
directly and with a smaller index than the default operator class.

Revision ID: 0045
Revises: 0044
"""
from typing import Sequence, Union

from alembic import op

revision: str = "0045"
down_revision: Union[str, None] = "0044"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_assets_tags_gin "
        "ON assets USING gin (tags jsonb_path_ops)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_assets_tags_gin")
