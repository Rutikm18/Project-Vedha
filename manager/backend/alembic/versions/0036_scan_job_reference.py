"""scan jobs get a human-readable reference (SCN-YYMMDD-XXXXXX)

A scan job could only be named by its UUID, and the UI showed eight hex
characters of it. That is not something a customer can read down a phone line,
quote in a ticket, or tell apart from a neighbouring job at a glance.

The reference is DERIVED from the row's own UUID and created_at (see
app/services/reference.py), so this backfill needs no counter and no sequence and
cannot race — every existing job gets exactly the reference it would have been
given at insert. It is then STORED, because once a customer has quoted a
reference it must not change if the algorithm is ever improved.

Nullable + unique: nullable so the backfill and the application write can land
independently on a live database, unique so a duplicate is a loud error rather
than two jobs quietly sharing a name.

Revision ID: 0036
Revises: 0035
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0036"
down_revision: Union[str, None] = "0035"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("scan_jobs", sa.Column("reference", sa.String(24), nullable=True))

    # Backfill in SQL so the migration does not depend on the application layer:
    # the same Crockford base32 alphabet, the same 32**6 fold of the UUID, and the
    # row's own created_at for the date part. Keep this in step with
    # app/services/reference.py if the scheme ever changes.
    # bit(128)::numeric is not supported by all Postgres versions (raises
    # CannotCoerceError). Since 32**6 = 2**30 and 2**64 % 2**30 = 0, only the
    # lower 64 bits matter: uuid.int % 2**30 == lower_64_bits & 0x3FFFFFFF.
    # bit(64)::bigint is universally supported; masking with 1073741823
    # (= 0x3FFFFFFF = 2**30 - 1) extracts the same 30 bits that the Python
    # suffix_for() function derives via uuid.int % 32**6.
    op.execute(
        r"""
        WITH encoded AS (
            SELECT
                j.id,
                'SCN-' || to_char(j.created_at AT TIME ZONE 'UTC', 'YYMMDD') || '-' ||
                string_agg(
                    substr(
                        '0123456789ABCDEFGHJKMNPQRSTVWXYZ',
                        (
                            (
                                (('x' || right(replace(j.id::text, '-', ''), 16))::bit(64)::bigint
                                 & 1073741823)
                                / power(32, g.i)::bigint
                            ) % 32 + 1
                        )::integer,
                        1
                    ),
                    '' ORDER BY g.i DESC
                ) AS reference
            FROM scan_jobs j
            CROSS JOIN generate_series(0, 5) AS g(i)
            WHERE j.reference IS NULL
            GROUP BY j.id, j.created_at
        )
        UPDATE scan_jobs SET reference = encoded.reference
        FROM encoded WHERE scan_jobs.id = encoded.id
        """
    )

    op.create_unique_constraint("uq_scan_jobs_reference", "scan_jobs", ["reference"])
    op.create_index("ix_scan_jobs_reference", "scan_jobs", ["reference"])


def downgrade() -> None:
    op.drop_index("ix_scan_jobs_reference", table_name="scan_jobs")
    op.drop_constraint("uq_scan_jobs_reference", "scan_jobs", type_="unique")
    op.drop_column("scan_jobs", "reference")
