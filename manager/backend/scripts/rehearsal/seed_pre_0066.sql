-- Synthetic data at the shape of revision 0065 (before migrations 0066-0068), for a migration
-- rehearsal on a SCRATCH database. It INSERTS rows, so it refuses to run anywhere whose name
-- does not say it is disposable. Scale it with psql -v, for example:
--
--   createdb vedha_rehearsal && DATABASE_URL=postgresql+asyncpg://.../vedha_rehearsal alembic upgrade 0065
--   psql -d vedha_rehearsal -v tenants=20 -v eng_per_tenant=20 -v assets_per_eng=250 \
--        -v findings_per_asset=4 -v runs_per_eng=50 -v links_per_run=150 -v audit_rows=2000000 \
--        -f seed_pre_0066.sql
--
-- The defaults above give 400k findings, 3M run-finding links and 2M audit rows (about 1.2 GB,
-- 3 minutes to seed). See docs/operations/migrations-0066-0068-rollout.md.
\set ON_ERROR_STOP on
DO $$ BEGIN
    IF current_database() !~* '(rehears|scratch|copy|sandbox)' THEN
        RAISE EXCEPTION 'refusing to seed %: the database name must contain rehearsal, scratch, copy or sandbox', current_database();
    END IF;
END $$;
\if :{?tenants} \else \set tenants 20 \endif
\if :{?eng_per_tenant} \else \set eng_per_tenant 20 \endif
\if :{?assets_per_eng} \else \set assets_per_eng 250 \endif
\if :{?findings_per_asset} \else \set findings_per_asset 4 \endif
\if :{?runs_per_eng} \else \set runs_per_eng 50 \endif
\if :{?links_per_run} \else \set links_per_run 150 \endif
\if :{?audit_rows} \else \set audit_rows 2000000 \endif
\timing on

INSERT INTO tenants (id, name, plan, created_at, is_active)
SELECT gen_random_uuid(), 'Tenant ' || g, 'enterprise', now() - interval '400 days', true
  FROM generate_series(1, :tenants) g;

INSERT INTO tenant_settings (tenant_id, auth_policy, scan_policy, customer_defaults, updated_by, updated_at)
SELECT id, '{}', '{}', '{}', 'seed', now() FROM tenants;

INSERT INTO users (id, tenant_id, email, hashed_password, role)
SELECT gen_random_uuid(), t.id, 'user' || g || '@t' || t.rn || '.example.test', 'x', 'analyst'
  FROM (SELECT id, row_number() OVER () rn FROM tenants) t, generate_series(1, 10) g;

INSERT INTO engagements (id, tenant_id, name, status)
SELECT gen_random_uuid(), t.id, 'Engagement ' || g, 'active'
  FROM tenants t, generate_series(1, :eng_per_tenant) g;

INSERT INTO assets (id, engagement_id, ip_address, hostname, asset_type, criticality)
SELECT gen_random_uuid(), e.id, '10.' || (g / 65536) % 256 || '.' || (g / 256) % 256 || '.' || g % 256,
       'host-' || g, 'server', (ARRAY['critical','high','medium','low'])[1 + g % 4]::assetcriticality
  FROM engagements e, generate_series(1, :assets_per_eng) g;

INSERT INTO findings (id, engagement_id, asset_id, title, severity, status, risk_score, first_seen, last_seen)
SELECT gen_random_uuid(), a.engagement_id, a.id, 'Finding ' || f,
       (ARRAY['critical','high','medium','low','info'])[1 + f % 5]::findingseverity,
       (ARRAY['open','confirmed','remediated'])[1 + f % 3]::findingstatus,
       (f * 37 % 1000) / 10.0, now() - interval '30 days', now()
  FROM assets a, generate_series(1, :findings_per_asset) f;

INSERT INTO detection_runs (id, engagement_id, trigger, status, started_at, finished_at, created_at, updated_at)
SELECT gen_random_uuid(), e.id, 'scan', 'completed', now() - (g || ' hours')::interval,
       now() - (g || ' hours')::interval + interval '10 minutes', now(), now()
  FROM engagements e, generate_series(1, :runs_per_eng) g;

INSERT INTO detection_run_findings (run_id, finding_id, outcome)
SELECT r.id, f.id, (ARRAY['new','reaffirmed','reaffirmed'])[1 + (random() * 2)::int]
  FROM detection_runs r
  CROSS JOIN LATERAL (SELECT id FROM findings WHERE engagement_id = r.engagement_id
                       ORDER BY random() LIMIT :links_per_run) f;

-- Audit trail: a third reachable through an engagement, most of the rest through the
-- acting user, a tenth with neither (anonymous / system) so it lands in the unscoped chain.
WITH eng AS (SELECT array_agg(id) ids, count(*) n FROM engagements),
     usr AS (SELECT array_agg(id) ids, count(*) n FROM users)
INSERT INTO audit_logs (id, actor_id, engagement_id, action, resource_type, resource_id, detail, ip_address, "timestamp")
SELECT gen_random_uuid(),
       CASE WHEN g % 10 = 0 THEN (ARRAY['anonymous','system'])[1 + g % 2]
            ELSE (usr.ids[1 + (random() * (usr.n - 1))::int])::text END,
       CASE WHEN g % 3 = 0 THEN eng.ids[1 + (random() * (eng.n - 1))::int] END,
       (ARRAY['finding.updated','scan.launched','auth.login','report.exported','integration.updated'])[1 + g % 5],
       'finding', gen_random_uuid(), jsonb_build_object('n', g, 'note', 'seeded'),
       '203.0.113.' || g % 250,
       now() - ((g % 365) || ' days')::interval - ((g % 86400) || ' seconds')::interval
  FROM generate_series(1, :audit_rows) g, eng, usr;

ANALYZE;
\timing off
SELECT 'tenants' t, count(*) FROM tenants UNION ALL SELECT 'users', count(*) FROM users
UNION ALL SELECT 'engagements', count(*) FROM engagements UNION ALL SELECT 'assets', count(*) FROM assets
UNION ALL SELECT 'findings', count(*) FROM findings UNION ALL SELECT 'detection_runs', count(*) FROM detection_runs
UNION ALL SELECT 'detection_run_findings', count(*) FROM detection_run_findings
UNION ALL SELECT 'audit_logs', count(*) FROM audit_logs;
SELECT pg_size_pretty(pg_database_size(current_database())) AS database_size,
       pg_size_pretty(pg_total_relation_size('audit_logs')) AS audit_logs_size,
       pg_size_pretty(pg_total_relation_size('detection_run_findings')) AS run_findings_size;
