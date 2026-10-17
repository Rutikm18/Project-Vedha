# Rolling out migrations 0066, 0067 and 0068, one phase at a time

Three Alembic revisions arrive together: the per-scan snapshot (0066), the compliance audit
log (0067) and the audit retention setting (0068). `alembic upgrade head` would apply all three
in **one transaction**, and the `migrate` service does exactly that on every `docker compose up`.
On a small database that is fine. On a large audit table it is not, because 0067 locks
`audit_logs` for the whole run. This runbook applies them one at a time, with a check and a way
back after each.

Every number below was measured on a rehearsal copy (section 8), not estimated, except where it
says so. Your hardware will differ: **rehearse on a restored backup of your own database first.**

## 1. At a glance

| Phase | Revision | What it changes | Measured (3M run-finding rows, 2M audit rows) | What waits while it runs | Rolling back |
|---|---|---|---|---|---|
| 1 | 0066 | 3 nullable columns on `detection_run_findings` (per-scan severity, risk score, status) | 1.2 s | Anything touching that table, for a moment. A long-running transaction makes the migration queue, and everything behind it queues too (section 3). | 0.9 s. Drops the snapshot values; compare falls back to "in both scans" for those findings. |
| 2 | **0067** | 11 columns on `audit_logs`; gives old entries a tenant; builds the tamper-evident hash chain; 3 indexes, 3 triggers, 3 functions | **320 to 360 s (about 3 minutes per million audit rows)**, 11 GB of WAL, table 5 times larger until cleaned up | **Every audit write, and every audit read, for the whole run.** Logins, scans, report exports and every other action that records an entry hang. | 0.9 s. Drops tenant scope, outcome, request context and the chain. Entries are kept; the next upgrade recomputes the chain. |
| 3 | 0068 | 1 JSONB column on `tenant_settings` (retention policy), default `{}` | 0.9 s | A moment | 0.9 s. Drops saved retention settings. |

Phases 1 and 3 are safe to run with the application up. **Phase 2 needs a maintenance window.**

## 2. Before you start

1. **Revision.** `alembic current` must say `0065`. If it says anything else, or a database ran an
   earlier build of this branch, go to section 7 first.
2. **Back up, and know how to restore.** `pg_dump` or a volume snapshot, taken after the
   application is quiet. Phase 2 can be undone with `alembic downgrade 0066` (section 5), but a
   backup is what protects you from a mistake around it.
3. **Size the window for phase 2.** `SELECT count(*) FROM audit_logs;` then budget about
   **3 minutes per million rows** for the migration, about **15 seconds per million** to clean up,
   and about **10 seconds per million** to verify. Fewer than about 50,000 rows is a matter of seconds,
   and then running all three together is reasonable (an estimate; the smallest rehearsal was 2M rows).
4. **Disk and WAL.** The migration rewrites every audit row several times. Measured at 2M rows:
   `audit_logs` grew from 550 MB to about 2.9 GB (including indexes) and 11 GB of WAL was
   written. Keep free disk above 6 times the table's size, and if you archive WAL or replicate,
   expect 11 GB per 2M audit rows to be shipped.
5. **Database role.** The role that runs migrations must own `audit_logs`,
   `detection_run_findings` and `tenant_settings`, and be allowed to create functions, triggers
   and indexes (the table owner can). PostgreSQL 11 or later is required (`sha256()`,
   `hashtextextended()`); production runs 16.
6. **Role settings that matter.**
   ```sql
   ALTER ROLE <migration_role> SET lock_timeout = '10s';     -- fail fast instead of queueing (section 3)
   ALTER ROLE <migration_role> SET statement_timeout = 0;    -- a timeout kills phase 2 part-way (safe, but wasted)
   ```
   Put them back with `ALTER ROLE <migration_role> RESET lock_timeout;` and `... RESET statement_timeout;`
   when you finish.
7. **Long transactions.** Look for anything open longer than a minute; it will block the
   migration's first lock:
   ```sql
   SELECT pid, now() - xact_start AS open_for, state, left(query, 80)
     FROM pg_stat_activity WHERE xact_start < now() - interval '1 minute' ORDER BY xact_start;
   ```
8. **The new backend image is built or pulled, but `api` and `worker` are still on the old one.**
   The migration files live inside the image.
9. **Define the compose command once** (the same one `deploy/aws/install.sh` uses):
   ```bash
   COMPOSE="docker compose --env-file $APP_DIR/.env -f $APP_DIR/manager/docker-compose.yml -f $APP_DIR/deploy/aws/docker-compose.prod.yml"
   ```
   Do not run a plain `$COMPOSE up -d` before the three phases are done: the `migrate` service would
   run all of them at once, in one transaction.

The commands below run Alembic in the one-shot `migrate` container, without starting anything it
depends on. They were **not run here** (no Docker in the rehearsal environment); the same Alembic
commands were run directly against Postgres 16.

## 3. Phase 1: 0066 (per-scan snapshot)

```bash
$COMPOSE run --rm --no-deps migrate alembic upgrade 0066
```

**Check**

```sql
SELECT column_name FROM information_schema.columns
 WHERE table_name = 'detection_run_findings' AND column_name IN ('severity', 'risk_score', 'status');  -- 3 rows
SELECT version_num FROM alembic_version;                                                               -- 0066
```

**If it waits and then fails with "canceling statement due to lock timeout":** a long transaction held
the table, and the 10 s `lock_timeout` did its job. The database is unchanged (still 0065, no partial
columns). Wait for or end that transaction, then run the same command again.

Why the timeout matters: with an open reader and no `lock_timeout`, the migration waits for the reader,
and a plain `SELECT` started 1.5 s after the migration queued waited **5.9 s** behind it. The migration
blocks everyone who arrives after it, not only itself.

**Roll back**

```bash
$COMPOSE run --rm --no-deps migrate alembic downgrade 0065
```

The old application keeps working with or without these columns.

## 4. Phase 2: 0067 (compliance audit log), in a maintenance window

### 4.1 Prepare

```bash
$COMPOSE stop api worker          # nothing should write audit entries while the table is locked
```
```sql
SELECT count(*) AS audit_rows, pg_size_pretty(pg_total_relation_size('audit_logs')) AS size FROM audit_logs;
```

Stopping the writers is not required for correctness: a blocked insert waits and then succeeds
(the rehearsal's writer lost nothing; its one stalled insert took 361.6 s). It is advisable because
requests that audit would otherwise hang until their own timeouts.

### 4.2 Apply

```bash
$COMPOSE run --rm --no-deps migrate alembic upgrade 0067
```

Where the time goes (2M rows, first run):

| Step | Seconds |
|---|---|
| Give old entries a tenant, through their engagement | 24 |
| Give old entries a tenant, through the acting user | 44 |
| Set `actor_type` on every entry | 77 |
| Build the hash chain, oldest first, per tenant | 197 |
| Build the three indexes | 20 |

All of it is one transaction. **A failure at any point leaves the database exactly at 0066**: tested
by killing it at 20 s with a `statement_timeout`; the audit table kept its original 9 columns and no
function or trigger remained. Fix the cause and run the same command again. The aborted attempt
leaves dead rows behind, so run `VACUUM audit_logs;` before retrying.

### 4.3 Check

```sql
SELECT version_num FROM alembic_version;                                           -- 0067
SELECT count(*) FROM audit_logs WHERE row_hash IS NULL;                            -- 0
SELECT chain_key, count(*), max(chain_pos) FROM audit_logs
 GROUP BY chain_key HAVING count(*) <> max(chain_pos);                             -- no rows: every chain is gapless
                                                                                    -- (right after the migration; once retention has purged old entries, positions no longer start at 1)
SELECT tgname FROM pg_trigger WHERE tgrelid = 'audit_logs'::regclass AND NOT tgisinternal;
                                                                                    -- audit_logs_chain_bi, audit_logs_immutable_bud, audit_logs_immutable_bt
```

Append-only is enforced (expect `audit_logs is append-only: UPDATE is not allowed`):

```sql
BEGIN; UPDATE audit_logs SET action = action WHERE id = (SELECT id FROM audit_logs LIMIT 1); ROLLBACK;
```

Then verify every chain with the application's own verifier (2M entries took 19.5 s):

```bash
$COMPOSE run --rm --no-deps -e PYTHONPATH=/app migrate python scripts/rehearsal/verify_chains.py
```

It prints `broken chains: 0` and exits 0. The same check is in the app: **Settings → Audit log** shows
the integrity result.

### 4.4 Clean up

0067 rewrites every row several times, so the table is several times larger than it needs to be
(550 MB became 2.7 GB, then 953 MB once cleaned):

```sql
VACUUM (FULL, ANALYZE) audit_logs;     -- 22 s at 2M rows; exclusive lock, so do it inside the window
```

Plain `VACUUM (ANALYZE) audit_logs;` (11 s) frees the dead rows for reuse but does not shrink the file.
The chains stay valid after `VACUUM FULL` (re-verified).

### 4.5 Start the new application

```bash
$COMPOSE up -d api worker
```

An application instance that has **not** been upgraded yet can keep writing audit entries after 0067:
they are chained under the platform chain (no tenant) and succeed. They will not show in a tenant's own
activity view until that instance is upgraded.

### 4.6 Roll back (only if you must)

```bash
$COMPOSE stop api worker
$COMPOSE run --rm --no-deps migrate alembic downgrade 0066     # 0.9 s
# then bring the previous application image back: the new one expects the new audit columns
```

What is lost: tenant scope, outcome, actor type and label, request id, user agent, the before/after
`changes`, and the whole hash chain. What is kept: every audit entry, in its original columns, and the
table becomes editable again. Running 0067 a second time rebuilds all of it (it took 320 s the second time).

## 5. Phase 3: 0068 (audit retention setting)

```bash
$COMPOSE run --rm --no-deps migrate alembic upgrade 0068
```

Check: `SELECT audit_policy FROM tenant_settings LIMIT 1;` returns `{}`; `alembic current` says `0068 (head)`.
Roll back with `alembic downgrade 0067`. Existing organisations keep the default retention (1 year, never
less than 180 days).

## 6. After all three

1. `$COMPOSE up -d` brings up the rest of the stack. The `migrate` service runs `alembic upgrade head`,
   which finds nothing to do, and then its usual admin seed step.
2. Run `python scripts/recompute_risk_scores.py --dry-run`, then without `--dry-run`, so the stored risk
   scores match the number the pages show.
3. Put the role settings back (`RESET lock_timeout`, `RESET statement_timeout`).
4. Smoke checks: sign in; open Settings → Audit log and see integrity verified; open a finding and its
   risk-score working; open Findings → Compare with two scans.

## 7. If a database already ran this branch's earlier numbering

Before the merge into main, these three migrations were numbered 0065, 0066 and 0067. Main then took
0065 for `agent_install_codes`, so they became 0066, 0067 and 0068. A database that applied the earlier
numbering has the right tables and columns but a `alembic_version` that points at the wrong revision.
**No such database is known**; this is only for one that turns up.

Find out what it has:

```sql
SELECT version_num FROM alembic_version;
SELECT (SELECT count(*) FROM information_schema.columns WHERE table_name='detection_run_findings'
          AND column_name IN ('severity','risk_score','status'))                                    AS snapshot_columns,   -- 3 = phase 1 applied
       (SELECT count(*) FROM information_schema.columns WHERE table_name='audit_logs'
          AND column_name='row_hash')                                                               AS audit_chain,        -- 1 = phase 2 applied
       (SELECT count(*) FROM information_schema.columns WHERE table_name='tenant_settings'
          AND column_name='audit_policy')                                                           AS audit_policy,       -- 1 = phase 3 applied
       (SELECT count(*) FROM information_schema.tables WHERE table_name='agent_install_codes')      AS install_codes;      -- 1 = main's 0065 applied
```

| Snapshot | Audit chain | Audit policy | Install codes | Do this |
|---|---|---|---|---|
| 3 | 1 | 1 | 1 | `alembic stamp 0068` |
| 3 | 1 | 0 | 1 | `alembic stamp 0067`, then `alembic upgrade 0068` |
| 3 | 0 | 0 | 1 | `alembic stamp 0066`, then phases 2 and 3 |
| 3 | 0 | 0 | 0 | `alembic stamp 0064`, `alembic upgrade 0065`, `alembic stamp 0066`, then phases 2 and 3 |

Rehearsed: a database with everything applied and `0067` in the version table fails `alembic upgrade head` with
`column "audit_policy" of relation "tenant_settings" already exists`; `alembic stamp 0068` fixes it and the
next `upgrade head` runs nothing. A database that stopped after the audit step took `stamp 0067` and then
`upgrade head` ran 0068. The last two rows were not run; they follow the same rule: stamp to the highest
revision whose objects all exist, then upgrade the rest.

## 8. What was rehearsed, and what was not

**Environment.** PostgreSQL 16.15 on 4 vCPU and 16 GB RAM, default settings (`shared_buffers` 128 MB,
`fsync` on), local disk. Alembic ran directly, not through Docker.

**Data** (`manager/backend/scripts/rehearsal/seed_pre_0066.sql`): 20 tenants, 400 engagements, 100,000
assets, 400,000 findings, 20,000 detection runs, 3,000,000 `detection_run_findings` rows (462 MB) and
2,000,000 audit rows (550 MB), 1.2 GB in all; a third of the audit rows reachable through an engagement,
most of the rest through the acting user, a tenth with neither.

**Done, with results above:** each phase up, down and up again; a long reader against phase 1 with and
without `lock_timeout`; phase 2 with a live writer (`audit_writer.py`); per-statement timings; WAL
volume; table growth and both kinds of `VACUUM`; chain verification of all 21 chains; append-only and the
purge switch; an unupgraded writer after 0067; rollback of 0067 and re-upgrade; failure injection
mid-0067; the earlier-numbering restamps (two of the four rows in section 7).

**Not done:**
- The `docker compose run` commands (no Docker here).
- Streaming replicas, WAL archiving or point-in-time recovery under 11 GB of WAL.
- Production hardware, a production-sized `shared_buffers`, or concurrent real traffic.
- Tables much larger than 2M audit rows. Time and WAL grew linearly across the two runs, so 10M rows
  would be roughly 30 minutes and 55 GB of WAL (an extrapolation). If your audit table is that large,
  the backfill can be rewritten as a single pass; ask for that before the window, not during it.

To repeat the rehearsal on a scratch database:

```bash
createdb vedha_rehearsal
cd manager/backend && DATABASE_URL=postgresql+asyncpg://.../vedha_rehearsal alembic upgrade 0065
psql -d vedha_rehearsal -f scripts/rehearsal/seed_pre_0066.sql                     # about 3 minutes
python scripts/rehearsal/audit_writer.py postgresql://.../vedha_rehearsal w.log old 900 &   # the stand-in application
DATABASE_URL=postgresql+asyncpg://.../vedha_rehearsal alembic upgrade 0066
DATABASE_URL=postgresql+asyncpg://.../vedha_rehearsal alembic upgrade 0067
DATABASE_URL=postgresql+asyncpg://.../vedha_rehearsal alembic upgrade 0068
```

Both the seed script and the writer refuse a database whose name does not contain `rehearsal`, `scratch`,
`copy` or `sandbox`, because they insert rows.
