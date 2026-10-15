Title: fix(migrate): port migrations 0055–0058 so Alembic can locate the database's revisions

## What changed
- Adds migrations `0055_notification_rules`, `0056_sla_alerts`, `0057_tenant_settings` and `0058_user_mfa` to `manager/backend/alembic/versions/`, chained 0054 → 0055 → 0056 → 0057 → 0058 (single head, no missing parents; checked).
- Adds a `docs/STATUS.md` line and a `LEARNINGS.md` entry.

## Why
The database had revisions 0055–0058 applied from feature branches (notifications, SLA alerts, tenant settings, two-step sign-in), but `main` only carried migrations up to 0054. Alembic then refuses to run with "Can't locate revision", so the `migrate` service fails and the stack does not start. Porting the four files makes the recorded revisions resolvable again.

## Reviewer notes
- **The migrations are ported on their own.** The code that uses these tables lives on `claude/adoring-maxwell-uz71b2` and is not on `main`. On `main` the new tables and columns are unused until that work is merged; nothing reads them.
- **Rebuild the backend image after merging.** Migration files are baked into the image at build time (`COPY . .`), so an old `vedha-backend:local` keeps failing until it is rebuilt (`LEARNINGS.md` has the detail).
- Fresh databases will create the four tables up front; existing databases at 0058 need no change.
- I verified the revision chain only. I have not run these migrations against a database.

## Test plan
- [ ] `alembic heads` shows one head (`0058`)
- [ ] `make full` on a database stamped at 0058: the `migrate` service completes
- [ ] `alembic upgrade head` on an empty database completes
- [ ] backend test suite passes
