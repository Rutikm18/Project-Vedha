# Customer Portal — Design Spec (Platform Part 2)

**Status:** approved 2026-08-13 · **Stack:** FastAPI + SQLAlchemy/Postgres (Alembic) · Next.js App Router + TanStack Query + Tailwind v4 + JWT
**Related:** platform roadmap Part 2 (customer portal); reuses Part 1 posture analytics.

---

## 1. Goal

A customer-facing portal where a client organization sees **only their one assigned
engagement** — findings, posture, reports, scan history — and can **request** a scan
(operator approves). Clients **cannot**: create engagements, create/run scans directly,
manage probes/fleet, switch engagements, or see any operator UI. Customer logins are
**provisioned and managed by the operator** from the manager dashboard.

## 2. Non-negotiable principle

**Engagement isolation is a backend security boundary, not a UI filter.** Every client
request is authorized server-side against the user's bound engagement. A client-supplied
`engagement_id` is never trusted. The frontend hiding a control is never the control.

## 3. Isolation architecture (decision)

A dedicated **`/portal` surface** (own login + layout; clients never see manager chrome)
in the same Next app, behind **host-aware middleware** so it can be promoted to
`portal.<domain>` later with zero rework. Chosen for **cleanest separation at least infra**
(subdomain-ready). Rejected: a fully separate deploy now (more CI/infra, premature);
shared login + role redirect (client could glimpse operator chrome).

## 4. Data model (Alembic migrations)

- `UserRole` += **`client`**.
- `Engagement.assigned_agent_id` → FK `agents.id`, nullable (one agent serves an engagement).
- `User.client_engagement_id` → FK `engagements.id`, nullable; set **only** for `client`
  users → "one login = one engagement". (Multi-engagement join table deferred — YAGNI.)
- New **`ScanRequest`** (mirrors `ValidationRequest`/`ReviewStatus`):
  `id, tenant_id, engagement_id, requested_by (user_id), scan_type (ScanJobType subset),
  status (ReviewStatus: pending|approved|rejected), scan_job_id (nullable, set on approve),
  note, reviewed_by, reviewed_at, review_reason, requested_at`.

## 5. Auth & scoping (backend)

- Same JWT flow. Client tokens carry `role=client` and an **`aud` claim** (`portal` vs
  `manager`) — a portal token cannot call operator APIs even if a role check is ever missed.
- `CurrentUser` gains `client_engagement_id`.
- **`require_client`** dependency (role gate) + **`scoped_engagement`** dependency that
  resolves the client's bound engagement and **ignores/rejects any caller-supplied
  `engagement_id`**.
- **`client_scoped(query, current_user)`** — the single helper every `/portal` query MUST
  use, so isolation cannot be forgotten. A contract test asserts no portal route returns
  cross-engagement rows.
- RBAC hard-denies `client` from: engagement create, scan create/run, fleet/probe mgmt,
  agents, exploits, detection config, provisioning.

## 6. Backend API

**Client-scoped (`/portal/*`):** `GET /engagement · /findings · /findings/{id} · /posture ·
/reports · /reports/{id}/download · /scans` · `POST /scan-requests` (creates **pending
only**) · `GET /scan-requests`.
**Operator-side:** `GET/POST /engagements/{id}/scan-requests` (approve→creates `ScanJob` on
`assigned_agent_id`, links `scan_job_id`) · `POST/PATCH/DELETE /engagements/{id}/client-user`
(provision / reset-link / disable) · `PATCH /engagements/{id}/assign-agent`.

## 7. Client-safe serialization (data-exposure control)

Operator `FindingOut` leaks internal fields (`exploit_validated`, `detection_status`,
`needs_review`, `verification_rationale/confidence`, `resolution_miss_count`,
`detected_db_version`, raw `evidence`). Clients get a dedicated **`ClientFindingOut`
whitelist**: `id, title, description, severity, status, cvss_score, cve_ids, risk_score,
remediation, first_seen, evidence_summary (curated)`. **Never reuse `FindingOut`.**
Reports: clients receive only `review_status == approved` `LLMOutput`, with
`review_feedback`/`validation` stripped.

## 8. Frontend (`/portal/*`)

`login` (own branding) · `/portal` overview (engagement + posture + Request-scan) ·
`findings[/id]` · `reports` · `scans` (history + request status). Nav: **Overview ·
Findings · Posture · Reports · Scans**. No fleet, no create-engagement, no create-scan,
no engagement switcher. BFF proxy under `app/api/portal/*`.

## 9. Operator additions (manager dashboard)

Engagement detail → **Customer Access** panel: provision/reset/disable client login,
assign agent, and a **Scan-Request inbox** (approve/reject → runs on assigned agent).

## 10. Folded improvements (from code audit)

| Area | Improvement | Phase |
|---|---|---|
| Isolation | `scoped_engagement` forces bound engagement; reject caller `engagement_id` | 0 |
| Isolation | central `client_scoped()` helper + no-cross-engagement contract test | 0 |
| Defense | JWT `aud` claim (portal vs manager) | 0 |
| Exposure | `ClientFindingOut` whitelist; never reuse `FindingOut` | 2 |
| Exposure | reports gated to `approved`; strip internal review fields | 2 |
| Audit | audit-log client login / scan-request / report-download | 1 |
| Creds | one-time reset link + forced first-login rotation via `password_expires_at` | 1 |
| Abuse | rate-limit portal login + scan-request cooldown/dedupe | 1/4 |
| Cleanup | extract `_finding_views`/`_two_latest_completed_runs` from `analytics.py` to shared posture-queries module | 2 |
| UX | scan-request status/ETA + completion notify; empty/first-run states | 3/4 |

## 11. Roadmap

| Phase | Deliverable | Done-when |
|---|---|---|
| **0** | Data + auth foundation: migrations (client role, `assigned_agent_id`, `client_engagement_id`, `scan_requests`), `CurrentUser.client_engagement_id`, `require_client` + `scoped_engagement` + `client_scoped`, `aud` claim, RBAC denies | isolation + RBAC tests green |
| **1** | Operator provisioning + scan-request inbox (backend + manager UI) + audit + reset-link | operator mints a client login & approves a scan → ScanJob |
| **2** | Portal read surfaces: shell + login, Overview+Posture, Findings (`ClientFindingOut`), Reports (approved) | client sees only their data |
| **3** | Customer scan-request flow + scan history in portal | request → inbox → run, status visible |
| **4** | Hardening: isolation suite, login throttle, empty states, subdomain switch, responsive | — |

## 12. Testing strategy

- **Isolation (critical):** a `client` user gets 403/empty for any engagement that isn't
  theirs; caller-supplied `engagement_id` is ignored; no portal route returns cross-engagement rows.
- **RBAC:** `client` is 403 on engagement-create, scan-run, fleet, agents, exploits, provisioning.
- **Scan request:** `POST /portal/scan-requests` creates `pending` only, never a `ScanJob`;
  operator approve creates exactly one `ScanJob` on `assigned_agent_id`.
- **Serialization:** `ClientFindingOut` never contains internal fields (property-based field-set assertion).
- Prefer mocked/fixture DB per existing backend test patterns; no live infra.

## 13. Out of scope (now)

Multi-engagement-per-client, self-service scan execution, SSO/SAML, in-portal ticketing,
billing. All revisitable post-MVP.
