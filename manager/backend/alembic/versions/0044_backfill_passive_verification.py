"""backfill the passive verification verdict on findings that never got one

`verification_enabled` defaulted to False and no deployment set it, so no
finding was ever stamped: every row carried verification_state=NULL and the
dashboard read "Unverified" — including findings whose evidence already said
state=confirmed. New rows are now stamped at insert; this fills the history.

A FROZEN copy of app.detection.verification.compute_verdict, in SQL, so the
migration means the same thing forever even if the Python rule evolves:

    confirmed     evidence.source_confidence = authoritative OR evidence.state = confirmed
    corroborated  evidence.confidence >= 70
    inferred      otherwise (missing confidence counts as 40)
    needs_review  evidence.state in (suspected, potential), not confirmed,
                  AND (kev OR priority in critical/high)

Only NULL rows are touched, so it is idempotent and never overwrites a verdict
an LLM, active-validation or analyst tier set. Downgrade is a no-op: the
stamped verdict is correct data, and NULL is exactly the bug being fixed.

Revision ID: 0044
Revises: 0043
"""
from typing import Sequence, Union

from alembic import op

revision: str = "0044"
down_revision: Union[str, None] = "0043"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        WITH v AS (
            SELECT id,
                   ev,
                   CASE WHEN jsonb_typeof(ev->'confidence') = 'number'
                        THEN GREATEST(0, LEAST(100, TRUNC((ev->>'confidence')::numeric)::int))
                        ELSE 40 END AS conf
            FROM (SELECT id,
                         CASE WHEN jsonb_typeof(evidence) = 'object'
                              THEN evidence ELSE '{}'::jsonb END AS ev
                  FROM findings
                  WHERE verification_state IS NULL) raw
        ), s AS (
            SELECT id, ev, conf,
                   CASE WHEN ev->>'source_confidence' = 'authoritative'
                          OR ev->>'state' = 'confirmed' THEN 'confirmed'
                        WHEN conf >= 70 THEN 'corroborated'
                        ELSE 'inferred' END AS vstate
            FROM v
        ), r AS (
            SELECT id, conf, vstate,
                   (ev->>'state' IN ('suspected', 'potential')
                    AND vstate <> 'confirmed'
                    AND (COALESCE(ev->>'kev', 'false') = 'true'
                         OR LOWER(COALESCE(ev->>'priority', '')) IN ('critical', 'high'))
                   ) IS TRUE AS review
            FROM s
        )
        UPDATE findings f
        SET verification_state = r.vstate,
            verification_confidence = r.conf,
            verification_method = 'passive',
            needs_review = r.review,
            verification_rationale =
                CASE r.vstate
                    WHEN 'confirmed' THEN 'authoritative/credentialed evidence'
                    WHEN 'corroborated' THEN 'network evidence, confidence ' || r.conf
                    ELSE 'weak/single-signal evidence, confidence ' || r.conf
                END
                || CASE WHEN r.review
                        THEN '; flagged for review (high-stakes + uncertain)' ELSE '' END
        FROM r
        WHERE f.id = r.id AND f.verification_state IS NULL
    """)


def downgrade() -> None:
    pass
