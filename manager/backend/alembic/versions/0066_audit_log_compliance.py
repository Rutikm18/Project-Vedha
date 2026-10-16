"""Audit log fit for compliance: tenant scope, outcome, request context, tamper evidence.

audit_logs gets what PCI DSS 10.2.2, NIST 800-53 AU-3, ISO 27001 A.8.15, SOC 2 CC7.2,
HIPAA 164.312(b) and CERT-In's logging directions all ask of an entry: who (actor and
type), what (action, resource, before/after), when (UTC), where from (source address,
user agent), the outcome, and a request identifier to tie the entry to other logs.
It also gets a tenant, so a tenant's own events can be read at all (before this, an
event was reachable only through an engagement, and tenant-level ones not at all).

Tamper evidence is enforced by the database, not by callers: a BEFORE INSERT trigger
chains each entry to the previous one in its tenant (sha256 over the previous hash and
the entry's fields) under an advisory lock, so every writer is chained and none can skip
it; a BEFORE UPDATE/DELETE/TRUNCATE trigger refuses any change. The only exception is
retention: a DELETE is allowed when the session sets vedha.audit_purge = 'on', which
only the retention job does, and a purge removes the oldest entries first so the chain
stays verifiable from the first remaining row.

This makes tampering detectable and accidental edits impossible. It does not stop a
database superuser who disables triggers: that needs the log held off-box, which is the
(not yet enabled) forwarding option.

Revision ID: 0066
Revises: 0065
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg

revision = "0066"
down_revision = "0065"
branch_labels = None
depends_on = None

_ZERO = "00000000-0000-0000-0000-000000000000"

_HASH_FN = """
CREATE OR REPLACE FUNCTION audit_row_hash(
    prev bytea, pos bigint, id uuid, tenant uuid, actor text, action text, outcome text,
    rtype text, rid uuid, eng uuid, ip text, ts timestamptz, detail jsonb, changes jsonb
) RETURNS bytea AS $$
    SELECT sha256(
        coalesce(prev, ''::bytea) || convert_to(concat_ws('|',
            pos::text, id::text, coalesce(tenant::text, ''), actor, action, outcome,
            coalesce(rtype, ''), coalesce(rid::text, ''), coalesce(eng::text, ''),
            coalesce(ip, ''), to_char(ts AT TIME ZONE 'UTC', 'YYYY-MM-DD"T"HH24:MI:SS.US'),
            coalesce(detail::text, ''), coalesce(changes::text, '')
        ), 'UTF8'))
$$ LANGUAGE sql IMMUTABLE;
"""

_CHAIN_FN = f"""
CREATE OR REPLACE FUNCTION audit_logs_chain() RETURNS trigger AS $$
DECLARE
    k uuid := coalesce(NEW.tenant_id, '{_ZERO}'::uuid);
    last_pos bigint;
    last_hash bytea;
BEGIN
    PERFORM pg_advisory_xact_lock(hashtextextended('vedha.audit:' || k::text, 0));
    SELECT chain_pos, row_hash INTO last_pos, last_hash
      FROM audit_logs WHERE chain_key = k ORDER BY chain_pos DESC LIMIT 1;
    NEW.chain_key := k;
    NEW.chain_pos := coalesce(last_pos, 0) + 1;
    NEW.prev_hash := last_hash;
    NEW.row_hash := audit_row_hash(
        last_hash, NEW.chain_pos, NEW.id, NEW.tenant_id, NEW.actor_id, NEW.action, NEW.outcome,
        NEW.resource_type, NEW.resource_id, NEW.engagement_id, NEW.ip_address, NEW.timestamp,
        NEW.detail, NEW.changes);
    RETURN NEW;
END $$ LANGUAGE plpgsql;
"""

_IMMUTABLE_FN = """
CREATE OR REPLACE FUNCTION audit_logs_immutable() RETURNS trigger AS $$
BEGIN
    IF TG_OP = 'DELETE' AND current_setting('vedha.audit_purge', true) = 'on' THEN
        RETURN OLD;
    END IF;
    RAISE EXCEPTION 'audit_logs is append-only: % is not allowed', TG_OP
        USING ERRCODE = 'insufficient_privilege';
END $$ LANGUAGE plpgsql;
"""

# Chain the rows that existed before this revision, oldest first, per tenant.
_BACKFILL_CHAIN = f"""
DO $$
DECLARE
    r record;
    cur_key uuid := NULL;
    pos bigint := 0;
    prev bytea := NULL;
    h bytea;
BEGIN
    FOR r IN
        SELECT * FROM audit_logs
        ORDER BY coalesce(tenant_id, '{_ZERO}'::uuid), "timestamp", id
    LOOP
        IF cur_key IS DISTINCT FROM coalesce(r.tenant_id, '{_ZERO}'::uuid) THEN
            cur_key := coalesce(r.tenant_id, '{_ZERO}'::uuid); pos := 0; prev := NULL;
        END IF;
        pos := pos + 1;
        h := audit_row_hash(prev, pos, r.id, r.tenant_id, r.actor_id, r.action, r.outcome,
                            r.resource_type, r.resource_id, r.engagement_id, r.ip_address,
                            r."timestamp", r.detail, r.changes);
        UPDATE audit_logs SET chain_key = cur_key, chain_pos = pos, prev_hash = prev, row_hash = h
         WHERE id = r.id;
        prev := h;
    END LOOP;
END $$;
"""


def upgrade():
    op.add_column("audit_logs", sa.Column("tenant_id", pg.UUID(as_uuid=True), nullable=True))
    op.add_column("audit_logs", sa.Column("outcome", sa.String(16), nullable=False, server_default="success"))
    op.add_column("audit_logs", sa.Column("actor_type", sa.String(16), nullable=True))
    op.add_column("audit_logs", sa.Column("actor_label", sa.String(255), nullable=True))
    op.add_column("audit_logs", sa.Column("request_id", sa.String(64), nullable=True))
    op.add_column("audit_logs", sa.Column("user_agent", sa.String(255), nullable=True))
    op.add_column("audit_logs", sa.Column("changes", pg.JSONB(), nullable=True))
    op.add_column("audit_logs", sa.Column("chain_key", pg.UUID(as_uuid=True), nullable=True))
    op.add_column("audit_logs", sa.Column("chain_pos", sa.BigInteger(), nullable=True))
    op.add_column("audit_logs", sa.Column("prev_hash", sa.LargeBinary(), nullable=True))
    op.add_column("audit_logs", sa.Column("row_hash", sa.LargeBinary(), nullable=True))

    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return

    # Give the existing events a tenant, so they become readable: through the
    # engagement when there is one, else through the acting user.
    op.execute("""
        UPDATE audit_logs a SET tenant_id = e.tenant_id
          FROM engagements e WHERE a.engagement_id = e.id AND a.tenant_id IS NULL
    """)
    op.execute("""
        UPDATE audit_logs a SET tenant_id = u.tenant_id
          FROM users u WHERE a.tenant_id IS NULL AND a.actor_id = u.id::text
    """)
    op.execute("""
        UPDATE audit_logs SET actor_type = CASE
            WHEN action LIKE 'portal.%' OR action LIKE 'client_user.%' THEN 'client'
            ELSE 'user' END
         WHERE actor_type IS NULL
    """)

    op.execute(_HASH_FN)
    op.execute(_BACKFILL_CHAIN)
    op.execute(_CHAIN_FN)
    op.execute(_IMMUTABLE_FN)

    op.create_index("ix_audit_logs_tenant_time", "audit_logs", ["tenant_id", sa.text("timestamp DESC")])
    op.create_index("ix_audit_logs_tenant_action", "audit_logs", ["tenant_id", "action"])
    op.create_index("uq_audit_logs_chain", "audit_logs", ["chain_key", "chain_pos"], unique=True)

    op.execute("CREATE TRIGGER audit_logs_chain_bi BEFORE INSERT ON audit_logs "
               "FOR EACH ROW EXECUTE FUNCTION audit_logs_chain()")
    op.execute("CREATE TRIGGER audit_logs_immutable_bud BEFORE UPDATE OR DELETE ON audit_logs "
               "FOR EACH ROW EXECUTE FUNCTION audit_logs_immutable()")
    op.execute("CREATE TRIGGER audit_logs_immutable_bt BEFORE TRUNCATE ON audit_logs "
               "FOR EACH STATEMENT EXECUTE FUNCTION audit_logs_immutable()")


def downgrade():
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("DROP TRIGGER IF EXISTS audit_logs_immutable_bt ON audit_logs")
        op.execute("DROP TRIGGER IF EXISTS audit_logs_immutable_bud ON audit_logs")
        op.execute("DROP TRIGGER IF EXISTS audit_logs_chain_bi ON audit_logs")
        op.drop_index("uq_audit_logs_chain", table_name="audit_logs")
        op.drop_index("ix_audit_logs_tenant_action", table_name="audit_logs")
        op.drop_index("ix_audit_logs_tenant_time", table_name="audit_logs")
        op.execute("DROP FUNCTION IF EXISTS audit_logs_immutable()")
        op.execute("DROP FUNCTION IF EXISTS audit_logs_chain()")
        op.execute("DROP FUNCTION IF EXISTS audit_row_hash(bytea, bigint, uuid, uuid, text, text, text, text, uuid, uuid, text, timestamptz, jsonb, jsonb)")
    for column in ("row_hash", "prev_hash", "chain_pos", "chain_key", "changes", "user_agent",
                   "request_id", "actor_label", "actor_type", "outcome", "tenant_id"):
        op.drop_column("audit_logs", column)
