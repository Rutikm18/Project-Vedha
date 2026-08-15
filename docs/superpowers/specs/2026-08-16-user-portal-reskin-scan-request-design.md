# Spec 1 — User Portal: reskin + comprehensive dashboard + rich scan request

**Date:** 2026-08-16
**Status:** in implementation
**Branch:** `feat/user-portal-reskin-scan-request`

Part 2 of the platform roadmap already shipped a working (but plain) customer
portal. This spec rebrands it to the **User Portal**, reskins it onto the main
dashboard's *console* design system, adds a comprehensive in-portal dashboard,
and upgrades the scan request from a single hardcoded `vuln_scan` button to a
real form (type + specific targets-in-scope + intensity) feeding a queue.

Deferred to their own specs: **incident IDs (`VDH-####`) + open/closed lifecycle
platform-wide** (Spec 2), and **Slack/Jira/email integrations** (Spec 3).

## Decisions (locked with the user)

- **Label** becomes "User Portal"; route stays `/portal`, cookie stays
  `vedha_portal_token` (subdomain-ready) — no needless churn.
- **Scan types in the request dropdown:** all active `ScanJobType`s incl.
  offensive (discovery, vuln_scan, exploit, ad_enum, lateral, cloud_scan,
  detection). Operator approval is the safety gate on every request.
- **Targets:** the user requests **specific hosts / sub-ranges within the
  engagement's allowed scope**. Backend re-validates every target ⊆
  `scope_cidrs` and ∉ `excluded_cidrs`, rejecting anything outside (422).
- **Intensity:** Light / Normal / Thorough → `light` / `standard` / `deep`.
- **Dashboard widgets:** posture scorecard + KPIs; severity + open/closed
  trends; scan queue + recent scans; SLA + top open incidents.
- **Theme:** reuse the console design system (theme tokens, `.console-scope`,
  `.panel`, light/dark) — not the current hardcoded light-only slate/indigo.

## System-design invariants

1. **Authorization double-gate, single source of truth.** A customer can never
   cause a scan outside their engagement scope. Enforced twice — request-time
   (portal route, fast 422) and dispatch-time (`agents.py`, authoritative) —
   both calling the same pure `validate_targets_in_scope`. Scope is read
   server-side from the engagement, never trusted from the request body.
2. **Read-scoping choke point** stays `client_scoped` / `assert_client`.
3. **Whitelist serializers** (`ClientFindingOut`) are never widened.
4. **Contract parity** — the portal's scan-type/intensity vocabulary is a
   subset of what the probe accepts (parity test).

## Backend changes (`manager/backend`)

1. **`app/services/scope_targets.py`** — extract the target-⊆-scope logic
   currently private in `agents.py::_job_reachability_scope` into a pure,
   unit-tested `validate_targets_in_scope(targets, scope_cidrs, excluded_cidrs)`.
   `agents.py` reuses it (no behavior change).
2. **`ScanRequest`** gains `targets: JSONB` and `intensity: str|None`
   (migration, nullable/defaulted — backwards compatible).
3. **`ScanRequestCreate`** widens to all `ScanJobType`s + `targets[]` +
   `intensity`. `POST /portal/scan-requests` validates type, intensity, and
   every target ⊆ scope (422 naming the offender). Queue cap raised from
   1-pending to ≤5-pending (409 past that) so requests queue, not block.
4. **`build_scan_job`** writes `targets` + `intensity` into `job.result` so the
   existing dispatch-time validation + probe consume them.
5. **`GET /portal/summary`** (posture + KPI counts + open/closed + queue state)
   and **`GET /portal/trends`** (severity breakdown + open-vs-closed over time),
   both `client_scoped`, reusing `services/posture`.
6. **Cleanups:** remove dead `resolve_scope`/`scoped_engagement`/`ScopedEngagement`
   (#4); collapse a scan request that already has a linked job so the scans list
   doesn't double-count it (#5).

## Frontend changes (`manager/frontend`)

1. **`PortalShell`** mirroring `PageShell`'s console chrome (theme toggle, UTC/
   session chrome, `.console-scope`) with limited nav (Dashboard, Findings,
   Scans, Reports) + portal auth. Extract shared visual chrome so the two shells
   don't cosmetically diverge.
2. **Reskin every portal page** onto theme tokens + `.panel` (removes the
   hardcoded light-only slate/indigo; gains dark mode). Reskin the operator
   `customer-access` page for consistency.
3. **Comprehensive dashboard** over `/portal/summary` + `/portal/trends`,
   reusing `PostureScorecard`, `SlaStatus`, `DashboardCharts` patterns.
4. **Rich scan-request form** — type dropdown (all active types), targets input
   validated against the shown allowed scope (per-target inline error),
   intensity Light/Normal/Thorough, note → queue.
5. **Scans page** becomes a real queue view.

## Test strategy

- **Unit (pure):** `validate_targets_in_scope` (in/out of scope, excluded,
  malformed, empty scope → deny-all, v4/v6); `build_scan_job` param plumbing.
- **Integration (route):** `POST /portal/scan-requests` — in-scope 201,
  out-of-scope 422, cross-engagement target 422 (IDOR), bad intensity 422,
  6th pending 409.
- **Scoping:** every `/portal/*` returns only the caller's engagement.
- **Contract/parity:** portal vocab ⊆ probe-accepted codes.
- **Frontend:** tsc + eslint clean; form disables until ≥1 valid target;
  422 target error rendered inline; widgets render loading/empty/error.
