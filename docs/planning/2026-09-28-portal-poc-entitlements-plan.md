# Customer portal — POC / licence entitlements, scan policy, agent IP protection

Date: 2026-09-28 · Branch: `feat/portal-poc-entitlements`

## What was asked

1. Portal offers **stealth and normal** scanning only; **aggressive is blocked**.
2. A **scan quota** per customer, set by the operator; the customer dashboard shows
   how many scans they have left.
3. An operator **configuration section** per customer: **POC** (with a POC duration)
   or **full use** (with a licence term). The login and credentials are issued
   and shown once the configuration exists.
4. Research on **protecting manager + agent code** when the agent is installed in a
   customer environment.
5. Fix bugs across the customer portal and improve its design.

## Ground truth (what the code does today)

| Fact | Where |
|---|---|
| Portal has TWO scan paths: request→operator approval, and direct launch | `portal.py::create_scan_request`, `portal.py::portal_workspace_scan_launch` |
| "stealth/normal/aggressive" are UI aliases for probe presets `light/standard/deep` | `agents.py::_INTENSITY_ALIASES` |
| A job with no intensity gets the **use-case default** — `uc_full_port_audit` and `uc_deep_port_sweep` default to `deep` | `agents._USE_CASES`, `probe/agent/use_cases.py` |
| Probe honours raw tuning overrides `rate/concurrency/timeout/retries/disc_timeout/max_host_seconds` in params — an "aggressive" scan can be rebuilt without saying `deep` | `probe/agent/engine.py::_tuning_from_params` |
| `require_client` re-reads the user from the DB on **every** portal request | `auth/portal_scope.py` — the natural place for an expiry gate |
| Sealed probe: license pubkey, HW fingerprint and `LICENSE_ENFORCED` are **runtime env vars** | `probe/agent/license.py`, `probe/Dockerfile.sealed` |
| Default installer runs `vedha-agent:local` (the plaintext image), not the sealed one | `probe/install.sh:206` |

## Decisions (defaults I chose — change any of them)

- **Where the entitlement lives:** a new `customer_entitlements` table, 1:1 with the
  engagement (the portal login is already 1:1 with the engagement).
- **Plan types:** `poc` (start + duration in days → `expires_at`) and `licensed`
  (licence term start/end + a generated licence key `VDH-XXXX-XXXX-XXXX-XXXX`).
- **What counts as a scan:** one portal scan launch, or one scan request. It is
  **refunded** if the operator rejects the request, or if the customer cancels the
  job before the probe picks it up. Operator-launched scans never count.
- **Race safety:** quota is consumed under `SELECT … FOR UPDATE` on the entitlement row,
  so two parallel launches cannot both take the last scan.
- **On expiry:** the portal becomes **read-only** (findings, reports and remediation stay
  visible; every scan path returns 403 with the reason). The operator can still
  disable the login entirely (that already exists). Read-only, not locked out, so
  the customer can see *why* and the POC findings keep selling.
- **No entitlement configured** → the portal cannot scan at all ("ask your security
  team to activate your plan"). Existing customers without a row: the migration
  creates a `licensed`, unlimited, non-expiring row so nothing breaks on deploy.
- **Aggressive block is server-side and unconditional for the portal**, not just a UI
  hide: effective intensity (explicit, else the use-case default) must be
  `light` or `standard`; `deep` → 403. Raw tuning overrides are stripped from portal
  jobs. The two deep-only use cases are removed from the portal catalogue.

## Plan — priority ordered

### P0-1 · Portal scan policy: block aggressive (backend)  ✅ first
- `services/portal_scan_policy.py` (pure, unit-tested): `PORTAL_ALLOWED_INTENSITIES`,
  `effective_intensity()`, `assert_portal_intensity()`, `strip_tuning_overrides()`.
- Apply in `create_scan_request` and `portal_workspace_scan_launch`; filter
  `deep`-default use cases out of both portal catalogues.
- Schema: `ScanRequestCreate.intensity` → `light|standard|stealth|normal`.

### P0-2 · Entitlements model + enforcement (backend)
- Migration `0049_customer_entitlements` + backfill (unlimited licensed for existing).
- `services/entitlements.py`: `status_of()` (active / expired / not_started /
  unconfigured / exhausted), `consume_scan()` (row lock), `refund_scan()`.
- Enforced on both portal scan paths; refund on reject and on pending-cancel.
- Portal: `GET /portal/entitlement` (plan, scans used/left, days left, state).

### P0-3 · Operator configuration API
- `GET/PUT /engagements/{id}/entitlement` (admin/manager, audited): plan type, POC
  days / licence dates, scan quota, notes; licence key generated on first `licensed`.
- `POST …/entitlement/adjust` to add scans or extend days (audited delta).

### P1-1 · Operator UI — Customers → Configuration
- Per-customer panel on `/customers`: POC vs Full, duration / term, quota,
  licence key, usage bar, then the credentials block (email, reveal, reset).

### P1-2 · Portal UI
- Dashboard usage card: "7 of 10 scans left · POC ends in 9 days".
- Scan page: intensity dial shows Stealth + Normal only on the portal; launch
  disabled with the reason when quota is exhausted or the plan has expired.
- Global banner when expired / near expiry (≤ 3 days) / ≤ 1 scan left.

### P2 · Agent code protection (research + the concrete fixes)
See the section below. Fixes to implement: bake licence constants into the sealed
build (close the env bypass), manager-side licence enforcement (agent cannot run
jobs for an expired entitlement), installer defaults to the sealed image.

### P3 · Portal bug sweep + design pass
Live QA of every portal section on an isolated stack (`-p vedha-portalqa`), with a
bug list and fixes, one section at a time: Overview → Scans → Findings →
Remediation → Reports → Scope → Probe → Assistant → Settings.

## Agent / code protection — research

**Threat model.** The customer has root on the machine running the agent. Anything
shipped there can eventually be read by a determined attacker; the goal is to make
copying/reusing it **expensive, detectable and useless without your server**.
Order of effectiveness:

1. **Don't ship the valuable parts (strongest, already mostly true).** CVE
   matching, posture rules, correlation, risk scoring, AI and reports run on the
   manager. The agent only collects facts. Keep it that way: any new "smart"
   logic goes manager-side. A stolen agent with no manager is a port scanner.
2. **Server-side entitlement is the real licence.** A licence file checked only on
   the customer's box can be defeated by setting the clock back or patching the
   binary. The manager is authoritative: an expired or disabled entitlement means the
   manager dispatches no jobs and accepts no facts from that agent. (P0-2 plus the
   P2 hook on job dispatch and ingest.)
3. **Native compilation (have it).** Nuitka turns Python into C and then machine code:
   no `.py` or `.pyc` in the image. The free edition leaves string constants readable;
   **Nuitka Commercial** adds constant encryption and anti-debug. Cython is similar
   but covers less. PyArmor is weaker (bytecode obfuscation plus a runtime that decrypts
   into memory) and is not recommended over Nuitka.
4. **Close the gaps in today's sealed build:**
   - `LICENSE_ENFORCED`, `PROBE_LICENSE_PUBKEY`, `HW_BIND_FINGERPRINT` are read from
     env at runtime → `docker run -e LICENSE_ENFORCED=false …` or a
     self-generated key pair **bypasses the licence entirely**. Fix: generate an
     `agent/_sealed_consts.py` inside `Dockerfile.sealed` before Nuitka compiles,
     so the values are compiled-in constants and env is ignored when `SEALED=True`.
   - `install.sh` defaults to the plaintext image. Default customer installs to the
     sealed image; keep plaintext only for the lab.
   - Expiry uses the local clock. Combine it with (2): the manager checks the time.
5. **Image supply chain.** Sign images with **cosign** and verify the signature in
   `install.sh` (the installer already pins a tar SHA-256; a signature proves who
   built it). Distribute from a private registry with per-customer pull tokens
   that you can revoke.
6. **Encrypted images** (ocicrypt / `ctr` encrypted layers) protect the image in
   transit and at rest, but the runtime must decrypt it to run it, so they add little
   against someone with root. Low priority.
7. **Runtime hardening that also protects IP:** read-only root FS, `cap_drop` all except
   NET_RAW, no shell in the image (distroless), no debug tools, `no-new-privileges`,
   seccomp profile. This leaves an intruder with fewer tools to dump the process.
8. **Hardware roots of trust (enterprise tier):** TPM-sealed secrets or remote
   attestation (TPM quote, or a confidential VM such as SEV-SNP/TDX) before the
   manager issues a token. Strong but heavy; offer it as an option for BFSI customers.
9. **Legal and detection.** EULA/licence terms, per-customer watermark in the
   binary (a build ID tied to the customer), and heartbeat telemetry so a copied probe
   shows up as a second agent with the same build ID.

**Recommendation:** (1) + (2) + (4) now. They are cheap and close real bypasses.
Then (5). Offer (8) only when a customer's contract needs it.

## Status (2026-09-28)

| # | Item | State |
|---|---|---|
| P0-1 | Portal aggressive block (both paths, uc codes, tuning strip) | ✅ done, live-verified |
| P0-2 | Entitlements + quota/expiry enforcement, refunds (migration 0049) | ✅ done, live-verified on Postgres |
| P0-3 | Operator plan API (GET/PUT/adjust) | ✅ done |
| P1-1 | Customers page: Engagement → Plan → Login; per-customer Plan panel | ✅ done |
| P1-2 | Portal plan strip, scanner gating, Settings → Plan & licence | ✅ done |
| P2 | Sealed-build licence bypass closed (compiled-in constants) | ✅ done, verified on the real Nuitka binary |
| P3 | Portal bug sweep | ✅ first pass done (see below) |

### Bugs found and fixed during the sweep
1. Migration 0049 failed on a **fresh install** (uncommitted enum literal in one transaction).
2. One-click **access link never signed in** (fragment erased → remount cancelled the login);
   then a failed link showed **no error**; a link opened on an already-open login page did nothing.
3. **API outage rendered as "0 open findings"**: React Query pauses retries in an unfocused
   window and paused queries reported not-loading. Affects operator and portal.
4. Page **header tools painted over the title** (Findings, even at 1440 px); sign-out could scroll away.
5. "The last scan came back clean" shown when **no scan had ever run**.
6. Header showed "Customer" instead of the signed-in email (new `GET /portal/me`).
7. Engagement "Time remaining" showed **NaNd** with no end date.
8. Stale licence key shown on a POC; deep-only use case refused as "unknown use case".

### Still open (not fixed in this pass)
- The sweep ran on an empty tenant: data-dependent views (findings detail, reports with
  content, remediation bundles) need a pass on a tenant with a completed scan.
- Fleet page shows customers the operator's "Set MANAGER_PUBLIC_URL" warning when unset.
- `install.sh` still defaults to the plaintext image, and `Dockerfile.sealed` still calls itself
  a non-shipping artifact. Promoting the sealed image to the customer default is a release
  decision (it now passes parity plus the bypass check).
- Footer clock is UTC while the project renders IST; footer ENGINE/API/DB dots are static.

### Research: verified facts (not assumptions)
- Customers **today receive the plaintext Python image** (`install.sh:206` → `vedha-agent:local`).
- Before this branch, `docker run -e LICENSE_ENFORCED=false -e HW_BIND_FINGERPRINT=` disabled both
  gates on the sealed binary, and a customer-supplied `PROBE_LICENSE_PUBKEY` accepted a
  self-signed licence. Both are now refused by the compiled binary (tested).

## Round 2 (2026-09-29) — per-scan-type allowances + single-asset Deep scan

**Change of policy:** aggressive is no longer blocked outright; each customer's plan
decides. Existing customers are unchanged (aggressive/deep default to *off*).

| Scan type | Runs | Plan setting (NULL = unlimited, 0 = not included) |
|---|---|---|
| Stealth | probe preset `light` | `stealth_quota` (default unlimited) |
| Normal | probe preset `standard` | `normal_quota` (default unlimited) |
| Aggressive | probe preset `deep` (~2,500 enterprise ports) over the chosen scope | `aggressive_quota` (default 0) |
| Deep | `uc_deep_port_sweep`: all 65,535 ports + full assessment on **one asset** | `deep_quota` (default 0) + `deep_repeat_policy` |

- `scan_quota` remains an optional overall cap across all types.
- Deep: exactly one IP, inside scope, outside exclusions; the server pins the use case,
  preset and target on both portal paths (`targets` and `target` both overwritten).
  `distinct` refuses an asset that already had a deep scan; `repeat` allows it.
  The history (`deep_scanned_targets`) is released by a refund and cleared by "Reset usage".
- Full-port use cases are reachable **only** as a Deep scan (403 otherwise, including by `uc` code).
- Refunds return the same type: `scan_requests.quota_mode`, job `_quota_mode` / `_deep_target`.

**Verified live** (real Postgres, stand-in agent): aggressive limit, deep refusals (range, two
assets, excluded host, out of scope, repeat under `distinct`), job pinned to
`uc_deep_port_sweep` / `deep` / one `/32`, cancel and reject refunds releasing the asset,
portal dial and Deep card states.
