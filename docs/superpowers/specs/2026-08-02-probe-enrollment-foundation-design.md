# Vedha Probe — Enrollment Foundation (Slice 1) Design

**Date:** 2026-08-02
**Status:** Approved design, ready for implementation planning
**Author:** Design session (Rutik + Claude)

---

## 1. Context and scope

The "redesign the Probe into a production-grade autonomous agent" request spans ~7
independent subsystems (installer, unified CLI, cross-platform config/filesystem,
enrollment/auth, native service management, sync, self-healing). That is far too
large for a single implementation. It is decomposed into four sequential slices,
each with its own spec → plan → build cycle:

- **Slice 1 — Enrollment foundation (THIS SPEC):** one cross-platform `config.json`,
  auto-created directory tree, and `probe install --manager <url> --name <name>`
  performing enroll → auto-minted-and-encrypted PAT → identity → register → ready.
- **Slice 2 — Unified CLI + lifecycle:** `start/stop/restart/status/logs/config/jobs/
  engagements`, startup-validation checklist surfaced to operators, structured
  logging, and the Problem/Cause/Impact/Fix error format everywhere.
- **Slice 3 — Native service:** systemd / launchd / Windows Service generation,
  install/uninstall, auto-start on reboot, restart-on-failure.
- **Slice 4 — Sync & self-healing hardening:** incremental engagement/job delta sync,
  local engagement/job DB, PAT rotation on expiry, corrupted-state recovery,
  version/update checks, and manager-side incremental sync + metrics endpoints.

### 1.1 What already exists (reused unchanged or minimally extended)

This is **not** a greenfield build. The runtime engine already implements much of
the target behavior; the gap is the operator-experience layer.

| Capability | Existing location |
|---|---|
| WebSocket push + auto-reconnect (exp. backoff 1→60s) | `probe/agent/agent.py::_run_ws_push_loop` |
| Concurrent HTTP-poll fallback | `probe/agent/agent.py::_ws_http_poll_fallback` |
| Offline spool + idempotent retry | `probe/agent/result_spool.py` |
| X25519 identity generation + persistence | `probe/agent/scope_crypt.py`, state file |
| Register / resume without operator interaction | `probe/agent/agent.py::_obtain_identity` |
| Hardware-binding gate (dev/prod) | `probe/agent/hw_bind.py` |
| License gate (dev/prod) | `probe/agent/license.py` |
| Heartbeat (HTTP + WS) | `probe/agent/transport.py`, `agent.py` |
| PAT model, scopes, issuance | manager `app/auth/pat.py`, `POST /auth/pat` |
| Config w/ 0600 perms + atomic writes | `probe/agent/cli.py::ConfigStore` (CLI only) |
| Idempotent probe registration | manager `app/routers/agents.py::register_agent` |

**Baseline test status at design time:** probe 410/410, frontend 82/82 (green).

### 1.2 Problems Slice 1 solves

1. Two disjoint config systems: `probe.env` (env vars, hardcoded `/var/lib/vedha-probe`)
   for the daemon and `~/.config/vedha/probe-cli.json` for the CLI.
2. No auto-PAT bootstrap — operator manually creates and pastes a PAT.
3. Hardcoded Linux paths that break on macOS/Windows.
4. PAT stored in plaintext (0600, but not encrypted at rest).
5. No single, obvious `probe install` entry point.

---

## 2. Design decisions (locked)

| Decision | Choice | Rationale |
|---|---|---|
| Starting slice | Enrollment foundation | Delivers the headline two-input install; everything else builds on the config layer. |
| Trust model | Shared secret (per-tenant **enrollment token**), hardened | Operator input stays at manager-URL + name. Engineered defensively (below). |
| Secret delivery | Manager-generated one-line install command carrying the token as a flag/env var | Industry standard (CrowdStrike CID, SentinelOne site token, Datadog API key, Elastic enrollment token, Nessus linking key). **No Docker dependency.** |
| `/agents/register` gate | Scope-based (`probe:register`), not role-based | Probe PATs stay minimally privileged (`role="agent"`). One-line change to the register dependency. |
| Pending / offline install behavior | Install the service, poll in background, transition to Ready automatically | Operator runs one command and walks away; survives a temporarily unreachable manager. |
| PAT at rest | Envelope encryption, headless-safe, auto-selected KEK backend | Works on servers/containers where OS keychains are unavailable. |
| Env-var coexistence | `config.json` is authoritative but env vars override it | Keeps the existing Docker/compose deployment path working. |

### 2.1 Residual risk (shared-secret model)

A leaked enrollment token lets an actor who can also reach the manager mint probe
PATs **for that one tenant** until the token is rotated. Mitigations (per-tenant
scoping, HMAC proof-of-possession, replay window, audit logging, optional
source-CIDR allowlist, 90-day PAT TTL) reduce but do not eliminate this. This is
the accepted trade-off of the chosen model and must be documented in operator docs.

---

## 3. Module architecture

New package `probe/agent/bootstrap/`. Each module has one responsibility and is
injectable for tests (dependency injection over import-time globals).

| Module | Responsibility | Depends on |
|---|---|---|
| `platform_paths.py` | Resolve OS-specific dirs (config/state/cache/logs/results/jobs/spool/certs/updates); create with correct perms; root/non-root aware | stdlib |
| `config.py` | Load/save/validate the single `config.json`; layer env-var overrides; migrate legacy `probe.env` + `probe-cli.json` | `platform_paths` |
| `secret_store.py` | Encrypt/decrypt PAT at rest; pluggable KEK backend | `platform_paths`, `hw_bind` |
| `enrollment.py` | Client half of the enroll protocol: build HMAC-signed request, poll, receive PAT | `transport`, `config`, `secret_store` |
| `preflight.py` | Startup validation checklist (DNS/TCP/TLS/auth/PAT/identity/config/fs-perms/state/spool/disk/time) → PASS/WARN/FAIL | `transport`, `platform_paths` |
| `installer.py` | Orchestrate `probe install`: paths → config → identity → enroll → store → register → service handoff | all of the above |

`transport.py`, `hw_bind.py`, `license.py`, `result_spool.py`, `scope_crypt.py`,
`engine.py`, `use_cases.py` are reused. `agent.py::main()` is refactored to consume
`config.py` instead of reading `os.environ` directly — but env-var overrides still
flow **through** `config.py`, so container deployments are unaffected. `config.py`
becomes the single place that reads the environment.

---

## 4. Enrollment protocol (hardened shared-secret)

### 4.1 Manager side — new `POST /agents/enroll` (unauthenticated, rate-limited)

- A **per-tenant enrollment token** is created/rotated by an admin in the Manager UI
  and stored **hashed** (never plaintext) with a `key_id`. Manager maps
  `token → tenant`.
- Request body (canonicalized for signing):
  `{ name, fingerprint, public_key, capabilities, network_segments, nonce, timestamp }`
- Header: `X-Vedha-Enroll-Auth: <key_id>:<HMAC-SHA256(token, canonical_body)>`
  (proof-of-possession; the raw token is never sent on the wire).
- Manager verifies:
  1. `key_id` resolves to a live (non-revoked) enrollment token.
  2. HMAC matches.
  3. `timestamp` skew ≤ 60s.
  4. `nonce` not previously seen (replay protection; short-TTL nonce cache).
  5. (optional) source IP ∈ the token's CIDR allowlist.
- On success, **auto-approve**: mint a probe-scoped PAT via
  `build_personal_access_token(tenant_id=<resolved>, user_id=<tenant enrollment
  service user>, name=<probe name>, role="agent", scopes=DEFAULT_PROBE_CLI_SCOPES,
  expires_in_days=90)`, associate it with the probe `fingerprint`, and return
  `{ pat, poll_ok: true }`.
- Every enroll (success and failure) is audit-logged: source IP, fingerprint,
  tenant, key_id, outcome.

**Supporting manager changes:**
- **Enrollment service user per tenant:** PATs are bound to `(tenant_id, user_id)`.
  A non-login system principal owns probe PATs so audit trails and revocation stay
  surgical (rather than overloading a human admin's user_id).
- **Scope-based register gate:** relax `app/routers/agents.py::register_agent` so a
  credential carrying the `probe:register` scope is accepted regardless of `role`
  (today it requires `role in {admin, manager}`). Probe PATs then use `role="agent"`.
- **New model + migration:** `enrollment_token` table (`id/key_id`, `tenant_id`,
  `token_hash`, `name`, `cidr_allowlist`, `created_at`, `revoked_at`) and, if needed,
  a `fingerprint` column on `personal_access_token` / `agent`.

### 4.2 Probe side (`enrollment.py`)

- Token resolution order: `--enroll-token` flag → `VEDHA_ENROLL_TOKEN` env → optional
  baked file (for pre-provisioned images).
- Build the canonical body, compute HMAC, POST `/agents/enroll` over HTTPS
  (HTTP allowed only for a local/dev manager).
- On success: hand the PAT to `secret_store` for encrypted persistence, then proceed
  to `/agents/register` with the PAT.
- On manager-unreachable: return a "pending" result so `installer.py` can install the
  service and retry in the background (see §7).

### 4.3 Operator-facing delivery

Manager UI "Probes → Add Probe" generates a one-line install command, e.g.:

```bash
curl -fsSL https://<manager>/install.sh | sudo VEDHA_ENROLL_TOKEN=vent_… sh -s -- --name branch-office-01
```

which ultimately runs `probe install --manager https://<manager> --name
branch-office-01` with the token supplied via env. The operator's mental model
remains "manager + name"; the token is pre-filled in the copied command.

---

## 5. Cross-platform paths (`platform_paths.py`)

| Purpose | Linux (root) | macOS | Windows |
|---|---|---|---|
| config | `/etc/vedha/` | `~/Library/Application Support/Vedha/` | `C:\ProgramData\Vedha\` |
| state, cache, logs, results, jobs, spool, certs, updates | `/var/lib/vedha-probe/<sub>` | `~/Library/Application Support/Vedha/<sub>` | `C:\ProgramData\Vedha\<sub>` |

- OS detected via `sys.platform`; **never** hardcode a single OS's paths.
- Root/non-root aware: unprivileged installs fall back to user-writable bases
  (`$XDG_CONFIG_HOME`, `$XDG_STATE_HOME`, `~/.local/…`) so `probe install` works in
  dev without sudo.
- Permissions: config dir `0700`; secret files (`certs/pat.enc`, KEK material) `0600`.
- Directory tree is created idempotently on every run; recreated if missing
  (foundation for Slice 4 self-healing).

---

## 6. Configuration (`config.py`)

- Single `config.json`:
  ```json
  {
    "manager_url": "...", "probe_name": "...", "probe_id": "...",
    "capabilities": ["..."], "network_segments": ["..."],
    "tls": { "verify": true, "ca_bundle": null, "client_cert": null, "client_key": null },
    "retry": { "base_seconds": 5, "max_seconds": 60, "schedule": [5,10,20,40,60] },
    "runtime": { "heartbeat": 30, "poll": 10, "job_limit": 1,
                 "max_targets": 4096, "max_job_seconds": 7200 },
    "version": "2.0.0"
  }
  ```
- **PAT is NOT stored here** — it lives encrypted in `certs/pat.enc` (§7).
- **Precedence (highest → lowest):** CLI flag → env var → `config.json` → built-in
  default. Every existing `probe.env` variable therefore still overrides, which is
  what keeps Docker/compose working. `config.py` is the only reader of `os.environ`.
- **Migration:** on first run, if legacy `probe.env` and/or `probe-cli.json` exist,
  import their values into `config.json` (one-time, logged); originals are left
  intact for rollback.
- Writes are atomic (temp-file + `replace`) with restrictive perms, matching the
  existing `ConfigStore` pattern.

---

## 7. PAT encryption at rest (`secret_store.py`)

Envelope encryption: the PAT is sealed with AES-GCM under a random data key; the
data key is wrapped by the best available KEK backend, auto-selected (overridable):

1. **env-provided KEK** (`VEDHA_SECRET_KEY`) — k8s / secrets-manager deploys.
2. **OS keychain** (macOS Keychain / Windows DPAPI / Linux Secret Service) — desktop.
3. **hw-bound KEK** (derived via existing `hw_bind`) — bare-metal / VM; ties
   ciphertext to the machine.
4. **key-file KEK** (random 0600 file in `certs/`) — portable headless / container
   fallback.

**Container recreation gotcha:** the KEK/salt lives in the **persisted state volume**
(the same volume already mounted for state/spool), so ciphertext still decrypts after
a container is recreated; the key does not depend on unstable container "hardware".

---

## 8. `probe install` flow (`installer.py`)

```
probe install --manager <url> --name <name>
 1. preflight (DNS, TCP, TLS)          → fail fast with an actionable error
 2. resolve paths + create dir tree
 3. load-or-generate X25519 identity
 4. write config.json (no secret yet)
 5. enroll (HMAC-signed)
       success           → encrypt + store PAT
       manager unreachable → install service anyway; it retries enroll in the
                             background with capped backoff; install exits with
                             "enrollment pending — service will finish when reachable"
 6. register (/agents/register with PAT) → persist agent_id into config.json
 7. install native service (Slice 3; Slice 1 provides a supervised local fallback)
 8. print a structured readiness summary
```

- **Idempotent + re-entrant:** re-running `install` reuses identity and PAT and never
  creates duplicate agents (manager register is already idempotent by tenant+name).
- Every step emits the structured `Loading… / Done` log line (spec §14 of the request).
- Every failure uses the **Problem / Cause / Impact / Suggested Fix / Docs** format
  (spec §15 of the request).

---

## 9. Preflight and logging

- `preflight.py` returns a list of `{name, status: PASS|WARN|FAIL, detail}` covering:
  manager reachable, DNS resolution, TCP connectivity, TLS, authentication, PAT,
  identity, configuration, filesystem permissions, state dir, spool dir, disk space,
  time synchronization. Reused by `probe install` (step 1) and, in Slice 2, by
  `probe doctor`.
- Logging: structured JSON to `logs/`, human-readable to console, replacing the
  scattered `say()` calls. (Full rollout is Slice 2; Slice 1 introduces the logger
  and uses it in the bootstrap package.)

---

## 10. Testing strategy (TDD — red-green before implementation)

**Unit:**
- `platform_paths`: per-OS resolution via monkeypatched `sys.platform`; root vs
  non-root fallback; perms.
- `config`: precedence (flag > env > file > default); migration from `probe.env` and
  `probe-cli.json`; atomic write; schema validation.
- `secret_store`: encrypt→decrypt round-trip for each KEK backend; wrong-key failure;
  perms.
- `enrollment`: canonicalization + HMAC; tamper → reject; timestamp skew → reject;
  replayed nonce → reject; unreachable-manager → pending.
- `preflight`: each check's PASS/WARN/FAIL mapping.

**Integration:**
- Fake-manager: enroll → register → ready happy path.
- Manager-unreachable → install-service-and-poll offline path.

**Manager-side:**
- `POST /agents/enroll`: HMAC verify, replay reject, per-tenant scoping, audit-log
  entry, PAT scopes/TTL, source-CIDR allowlist.
- Scope-based register gate: `probe:register` PAT accepted; role no longer required.
- Migration test for the new `enrollment_token` table + service user.

**Constraint:** the existing probe suite (410) and frontend suite (82) must remain
green; new modules must not regress the current daemon path.

---

## 11. Out of scope for Slice 1 (deferred to later slices)

- Renamed lifecycle commands `start/stop/restart/status/logs/update/config/jobs`
  (Slice 2).
- Native service unit generation for systemd/launchd/Windows (Slice 3) — Slice 1
  ships a supervised local fallback only.
- Incremental engagement/job delta sync, PAT rotation, version/update checks,
  manager metrics endpoints (Slice 4).
