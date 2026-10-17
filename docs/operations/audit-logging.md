# Audit logging

What the platform records about its own use, how it is protected, who can read it, and how long it is kept.
This describes behaviour as built; it is not a statement that any organisation is compliant with a standard.

## What an entry carries

| Field | Answers |
| --- | --- |
| `timestamp` (UTC) | When |
| `actor_id`, `actor_type`, `actor_label` | Who: an id, a kind (`user`, `client`, `agent`, `system`, `anonymous`) and the identity (email) as it was at the time, so an entry still reads correctly after an account is renamed or removed |
| `action`, `resource_type`, `resource_id`, `engagement_id` | What, and to what |
| `outcome` | `success`, `failure` (it was attempted and did not work) or `denied` (it was refused) |
| `ip_address`, `user_agent`, `request_id` | Where from, and the handle that ties the entry to the request's other logs |
| `detail`, `changes` | Context, and `{field: {before, after}}` for a change |
| `tenant_id` | Whose; every entry belongs to one organisation |
| `chain_pos`, `prev_hash`, `row_hash` | Tamper evidence (below) |

Source address, user agent, request id, tenant and the authenticated actor are bound once per request
(`app/audit_middleware.py`) and filled in by `record_audit`, so a call site only states what is specific to the event.

## Events recorded

| Category | Events |
| --- | --- |
| Sign-in and sessions | `auth.login.success`, `auth.login.failure` (with the reason), `auth.login.locked`, `auth.logout`, `auth.mfa.challenge_failed`, `auth.mfa.*` (enabled, disabled, recovery codes, admin reset), `auth.api_key.created`, `auth.api_key.revoked` |
| Access control | `access.denied` (a role-restricted endpoint refused the caller), `user.activated`, `user.deactivated`, `client_user.*`, `entitlement.*`, `agent.*` |
| Findings | `finding.updated`, `finding.reopened`, `finding.compliance_brief` |
| Scanning | `scan_job.*`, `scan_request.*`, `scan_schedule.*`, overrides, probe enrolment |
| Remediation, reports | fix plans, deadline extensions, AI report sections |
| Configuration | `org_settings.<section>.updated` (with before and after), integrations, notification rules, SLA policy, intelligence bundles |
| Audit log | `audit.exported`, `audit.retention_purged` |

Events on a path that raises (a failed sign-in, a refused request) are written in their own transaction so they survive the
request's rollback (`record_audit_independent`). Everything else joins the request's transaction: the entry commits with the
change, or neither does.

Not recorded today: views of findings or reports, and refusals other than role checks (for example an ownership check inside
a handler). Operator user creation and role changes have no endpoint yet; when they do they must call `record_audit`.

## Tamper evidence

* A database trigger (`audit_logs_chain`, migration 0067) chains each entry to the previous one in its organisation:
  `row_hash = sha256(previous hash || the entry's fields)`, under an advisory lock, so every writer is chained and none can skip it.
* A second trigger refuses `UPDATE`, `DELETE` and `TRUNCATE`. The one exception is the retention job, which sets
  `vedha.audit_purge` for its own transaction.
* `GET /audit-logs/integrity` recomputes every hash and reports the first entry that was changed, is missing, or breaks the chain.
* A purge removes the oldest entries only, so the chain stays verifiable from the first remaining entry.

This makes tampering detectable and accidental edits impossible. It does **not** stop someone with database superuser access
from disabling the triggers and rewriting the chain end to end. Closing that gap needs the log held off the system that produced
it (forwarding to a SIEM or write-once storage), which is not enabled yet.

## Retention

Per organisation, `PUT /org-settings/audit {"retention_days": n}`: default 365, minimum 180 (CERT-In's rolling six months;
it cannot be lowered), maximum 3,650. A daily worker (`app/workers/audit_retention.py`, interval
`AUDIT_RETENTION_INTERVAL_SECONDS`) removes entries older than the period and records what it removed.
Other regimes ask for more: PCI DSS 10.5.1 twelve months (three immediately available), HIPAA six years for related
documentation. Set the period to what your own obligations require.

## Who can read it

* **Operator administrators** (`admin`): everything, with filters, CSV and JSON export (`/audit-logs`, `/audit-logs/export`).
  Exports are uncapped up to 100,000 entries and are themselves recorded.
* **Customers**: `GET /portal/audit-log`, limited to customer-visible actions in their own engagement and the sign-ins of their own
  users. Vedha staff appear as "Vedha analyst"; no operator address, user agent, request id, detail or change set is returned.
* Other operator roles (including `auditor`) cannot read it.

## Upgrade notes

* Migration 0067 gives existing entries a tenant (through their engagement, else their acting user) and chains them oldest first.
  Entries whose tenant cannot be found stay in the platform chain and are visible to no organisation.
* Run the migration with a database role that may create triggers and functions.
* **Migration 0067 locks `audit_logs` for its whole run**: about 1.5 minutes per million entries, with every audit
  write and read waiting. Apply it in a maintenance window, one phase at a time, following
  [migrations-0066-0068-rollout.md](migrations-0066-0068-rollout.md) (measured timings, checks and rollback for each phase).
