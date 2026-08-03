# Probe Pre-Authorized Enrollment Token — Design Spec

**Date:** 2026-08-04
**Status:** Approved for implementation
**Author:** brainstorming session (Rutik + Claude)

## Goal

Remove the one manual step that blocks unattended probe onboarding: today a
probe self-enrolls but then **blocks waiting for an operator to type a
`user_code` at `/fleet/enroll`**. Replace that human step with a
**pre-authorized, Site-bound enrollment token** so the install one-liner is
fully automated, while keeping every security property of the current
device-code flow.

Target install command (AWS testing manager, http):

```bash
curl --proto '=https' --tlsv1.2 -fsS https://downloads.vedha.example/probe/install.sh \
  | sudo sh -s -- --manager http://13.127.147.205:18080 \
      --enroll-token vet_xxx --insecure
```

Then: probe auto-enrolls → appears **online** in the fleet → operator **assigns
an engagement to the connected probe and creates a job** → probe auto-polls and
runs. (Assignment stays manual by design — the operator's decision.)

## Relationship to prior specs

- **Builds on** `2026-08-02-probe-enrollment-foundation-design.md` (the
  `/probe-enrollment` device-code flow that is **implemented in code**:
  proof-of-possession signing, refresh secrets, signed Site policy).
- **Supersedes the enrollment-token portion** of
  `2026-08-02-probe-fleet-automation-design.md`. That spec proposed a
  *per-engagement* `venr_` token. The operator model has since changed to
  **connect-first, assign-engagement-second**, which a per-engagement token
  cannot express. This spec's token is **Site-bound** (a reusable appliance
  identity), not engagement-bound. The job-queue/priority phases of the fleet
  spec are unaffected.

## Why Site-bound (the key decision)

In the current flow, operator approval is **not** a bare yes/no — it is where
the probe is bound to a **Site policy**: `authorized_cidrs`,
`approved_capabilities`, and `max_targets` / `max_job_seconds` / `max_rate_pps`
budgets (`probe_enrollment.py:approve_enrollment`). Naive auto-approval would
produce **un-scoped probes**. Binding the enrollment token to a pre-existing
`ProbeSite` means auto-enrolled probes inherit that Site's bounded policy with
zero human input — the same guarantee, no typing.

## Architecture

### A. Manager — Site-bound enrollment tokens

**New model** `ProbeEnrollmentToken` (`app/models/probe_enrollment.py`),
migration `0019`, mirroring the `PersonalAccessToken` security shape:

| Column | Notes |
|---|---|
| `id` | uuid pk |
| `tenant_id` | FK tenants, cascade |
| `site_id` | FK probe_sites, **restrict** — the bound policy |
| `token_hash` | SHA-256 only; raw token shown once |
| `token_prefix` | `vet_` + first chars, for display/lookup |
| `name` | operator label |
| `max_uses` / `uses` | default single-use (`max_uses=1`) |
| `expires_at` | short TTL (default 60 min, ≤ 24h) |
| `revoked_at`, `created_by`, timestamps | lifecycle |

**New routes** on the existing `/probe-enrollment` router (admin/manager RBAC):

- `POST /probe-enrollment/enroll-tokens` → body `{name, site_id, expires_in_minutes?, max_uses?}` → returns `{token: "vet_…", token_prefix, expires_at}` **once**.
- `GET /probe-enrollment/enroll-tokens` → list (no secrets).
- `DELETE /probe-enrollment/enroll-tokens/{id}` → revoke.

**Auto-approve inside `create_enrollment_request`**: `EnrollmentCreate` gains an
optional `enroll_token`. When present and valid (not expired/revoked, uses
remaining), the manager, in the same transaction:
1. loads the token's Site,
2. runs the **existing** agent-creation logic from `approve_enrollment`
   (dedupe name via a derived name, bind Site policy, create `Agent`
   `lifecycle_status="provisioning"`),
3. sets the request to state `approved` with an `activation_challenge`,
4. increments `token.uses`,
5. writes an `AuditLog` `probe.enrollment.approved` with `detail.auto=true`.

The response omits the human `user_code` fields when auto-approved (probe never
prints an approval prompt). All downstream steps — poll → sign challenge →
`activate` → device token + refresh secret + signed policy — are **unchanged**.
The manual `user_code` path remains fully intact as the fallback.

### B. Probe — pass the token, skip the wait

- **`install.sh`**: accept `--enroll-token <vet_…>` (→ `PROBE_ENROLL_TOKEN`) and
  `--insecure` (→ `PROBE_ALLOW_INSECURE=true`, relaxes the https guard so the
  http testing manager is accepted; production still requires https unless the
  flag is explicitly set). Token is passed to the container via env, never argv
  of the long-running process.
- **`transport.create_enrollment_request`**: include `enroll_token` in the POST
  body when `PROBE_ENROLL_TOKEN` is set.
- **`agent._enroll_device`**: if the create response returns state `approved`
  (auto), skip printing the `user_code`/verification prompt and go straight into
  the existing poll→activate path. No new state machine — just a branch on the
  create response.

### C. Assignment (no code change, documented)

Operator assigns engagement to the online probe, then creates the job; the probe
daemon auto-claims via the existing `GET /agents/{id}/jobs`. Documented in the
probe runbook section, not implemented here.

## Data flow

```
operator: POST /probe-enrollment/enroll-tokens {site_id} ──► vet_xxx (shown once)
                                                                │
install.sh --manager <url> --enroll-token vet_xxx --insecure    │
   probe boots, builds device identity                          │
   POST /probe-enrollment/requests { …keys…, enroll_token } ────► validate+consume token
                                                                  create Agent bound to Site
        ◄──── { request_id, device_secret, state:"approved", activation_challenge }
   sign(challenge) → POST …/activate ─────────────────────────► verify PoP → device token
        ◄──── access_token + refresh_secret + signed policy
   POST /agents/register / heartbeat ─────────────────────────► ONLINE in fleet
   ── operator assigns engagement + creates job ──
   GET /agents/{id}/jobs (poll) ──────────────────────────────► scan → results → findings
```

## Error handling & security invariants

- **Un-scoped probe impossible** — token → Site → policy; no token param can
  widen scope.
- **Token is low-value if leaked** — single-use by default, ≤24h TTL, hashed at
  rest, revocable, rate-limited (reuse the existing `_rate_limit`), audited.
- **Invalid/expired/revoked/exhausted token** → fall back to the manual
  `user_code` path (request created `awaiting_approval`), never a hard failure,
  so a bad token degrades to "needs approval" rather than bricking install.
- **Key dedupe preserved** — the existing 409 on an already-enrolled
  `signing_key_fingerprint` still applies before token logic.
- **`--insecure` is explicit** — http is only accepted when the operator opts in;
  the production https guard is unchanged by default.

## Testing (TDD)

**Manager** (`tests/test_probe_enrollment.py`):
- mint token (admin/manager only; tester forbidden),
- auto-approve: create request with valid token → state `approved`, Agent bound
  to Site, token `uses` incremented,
- single-use exhaustion → second use rejected → falls back to `awaiting_approval`,
- expired / revoked token → fallback,
- capability subset still enforced against the Site.

**Probe** (`probe/tests/`):
- `create_enrollment_request` includes `enroll_token` when env set,
- `_enroll_device` takes the activate branch (no prompt) on `approved` create
  response,
- unchanged manual path still prints prompt when no token.

**Install** (`probe/tests/` contract test): `--insecure` allows http manager;
without it, http non-local still refused; `--enroll-token` sets env, absent from
persisted process argv.

## Out of scope (YAGNI)

Job priority / dashboard queue control (owned by the fleet-automation spec),
inline Site creation from token params (Site must pre-exist), OS-keychain secret
storage, engagement-bound tokens.
