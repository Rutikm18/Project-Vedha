# Hardened vedha-agent — phase-by-phase build log

**Branch:** `cross-os-vedha-agent-install`
**Approach:** each phase is TDD (failing test → implementation → green → commit); pure/injectable logic is separated from IO so it unit-tests with no network and no root. No product code was written before its contract/design existed.

**Totals:** 10 commits · **~84 unit tests authored, all green** · brain CLI runnable on macOS/Linux/Windows.

**Design source:** the second-pass senior review (OT safety, EDR collision, durable queue, typed scope, identity/authz, observability, config precedence, exit codes, data/privacy, compliance) + `docs/superpowers/specs/2026-09-10-hardened-vedha-agent-architecture.md`.

---

## Phase 0 — Design & contracts (no product code)

Fixed the models *before* code, as the review's Task 0a/0b required.

### 0a — STRIDE threat model
`docs/superpowers/specs/2026-09-10-vedha-agent-threat-model.md`
- Assets (device key, job-signing anchor, scan results, host root, Manager, queue key), 4 trust boundaries, 6 attacker profiles.
- Full STRIDE table with **one control per entry**; uncontrolled entries = roadmap.
- Locked 4 models: **identity** (enrollment CA ≠ job-signing key), **authorization** (local scope only ever *narrows* the Manager ceiling), **typed scope**, **data classification** (confidential/encrypted/minimized).

### 0b/0c — versioned interface contracts
`docs/superpowers/specs/2026-09-10-vedha-agent-interface-contracts.md`
- `CONTRACT_VERSION 1.0.0`. brain↔daemon (config schema + precedence, exit-state protocol, enrollment env) + agent↔Manager (signed-job envelope, result idempotency + site key, mTLS, kill switch) + an 8-row contract-test plan.
- Removed the "verify enrollment vars by archaeology" risk — later **verified against the real daemon in Phase 6**.

---

## Phase 1 — Typed-scope model
**File:** `agent/scope_model.py` · **Tests:** `tests/test_scope_model.py` (18)
Replaces the flat `/24` string (the review's core scope fix).
- `classify_interface` — loopback / tunnel / container / virtual / physical.
- `is_denied` — **fail-closed** permanent denylist: loopback, link-local incl. **`169.254.169.254`**, multicast, reserved, broadcast, **Manager's own address**, and **IPv6** (out of scope v1).
- `Segment` + `validate_segment` — typed IT/IoT/OT/NEVER; **OT-active rejected**, NEVER-active rejected, active segment needs a `site` key.
- `target_allowed` — the agent's **independent** job-scope re-check (OT/NEVER never match).
- `detect_container` + `refusal_reason` — docker/cgroup/**WSL2** → refuse LAN scan.
- `ipv6_scope_note`, `parse_linux_ip_json`.
**Failure points closed:** review #5 (site key), #6 (container/WSL2), cloud-metadata + manager-address denial.

---

## Phase 2 — Config precedence + real doctor
**Files:** `agent/config_model.py`, `agent/doctor.py` · **Tests:** `test_config_model.py` (5) + `test_doctor.py` (7)
- **config_model:** `resolve(cli, env, probe_env, pushed)` → validated values **+ a source map** (precedence CLI > env > probe.env > Manager > default), type coercion; `parse_env_file`; `render_effective` → `config --effective`.
- **doctor:** pure checks with remediation — `check_python`, **`check_clock`** (skew), `check_disk`, **`classify_connectivity`** (real DNS→TCP→TLS→cert-chain), `check_privilege`; `exit_code`, `format_report`, `run()`.
**Failure points closed:** #7 (clock skew), #8 (config drift), the §7 `doctor` bugs (`or True` false-positive + never-contacts-manager).

---

## Phase 3 — Exit-state protocol + supervisor
**Files:** `agent/exit_state.py`, `agent/supervisor.py` · **Tests:** `test_exit_state.py` (6) + `test_supervisor.py` (6)
- **exit_state:** 5 classes (`success 0`/`retryable 10`/`fatal-config 20`/`fatal-identity 30`/`awaiting-approval 40`), reason→class (**unknown → retryable**), `exit-state.json` + `VEDHA-EXIT …` stderr line emit/parse.
- **supervisor:** per-class policy — success/fatal-config **stop**; fatal-identity **bounded** re-enroll; retryable **capped** retries with **duration-based** backoff (no wall-clock → no NTP retry storm); awaiting-approval **polls without counting**; **kill switch** stops before spawn. The cap = `StartLimitBurst` equivalent.
**Failure points closed:** #9 (overloaded codes), #13 (infinite self-heal), §5 monotonic backoff.

---

## Phase 4 — Durable encrypted result queue
**File:** `agent/result_queue.py` · **Tests:** `test_result_queue.py` (9)
- **Crash-safe append** (temp → `fsync` → atomic rename → dir fsync, `0600`).
- **Idempotent + at-least-once** — persists until `ack(job_id)`; replays dedup on the Manager.
- **Bounded + drop-oldest** size/count + age `prune()`.
- **Backpressure** — `should_backpressure()` stops new scans at high-water.
- **Encrypted at rest** — pluggable cipher; default host-sealed **Fernet** (`queue.key`, 0600).
**Failure points closed:** #3 (silent data loss), #4 (disk-full fleet-wide).

---

## Phase 5 — Self-scan (own IP, manager-less) — RUNNABLE
**File:** `agent/self_scan.py` · **Tests:** `test_self_scan.py` (6)
Assembles Phase 1 + 4: `plan_self_scan` detects own IPv4, **refuses** in container/WSL2 / no-IP / denylisted, scopes to a single `/32` (`site="self"`); `execute` writes the scope file, runs the existing local engine, **archives a summary through the durable queue**. Live: `python -m agent.self_scan`. Safe by construction.

---

## Phase 6 — Optional connect + uplink security
**File:** `agent/connect.py` · **Tests:** `test_connect.py` (9)
Connect is **opt-in** (self-scan needs no Manager).
- **Verified enrollment env** (resolved against `agent/agent.py`, not guessed): `pat → VEDHA_PAT`, `token → PROBE_ENROLL_TOKEN`, `pairing → neither`. Contract doc corrected.
- **`verify_job`** — Ed25519 signature vs a **pinned** key + contract-version + validity window.
- **`admit_job`** — the **independent ceiling**: a valid signed job is still refused if any target is outside the agent's own IT/IoT scope (job can only request a *subset*).
- **`kill_switch_active`** (`STOP` file) + supervisor-driven launcher.
**Failure points closed:** #10/#11 (supply-chain / rogue-Manager authorization).

---

## Phase 7 — Dependency bootstrap + shims + brain CLI (+ strict-security toggle)
**Files:** `agent/deps.py`, `agent/bootstrap.py`, `agent/setup.py`, `install.sh`, `install.ps1` · **Tests:** `test_deps.py` (4) + `test_bootstrap.py` (5) + `test_setup_cli.py` (4)
- **deps:** venv + **wheel-first** pip; **strict = wheel-only** (never compiles untrusted source); idempotent by requirements-hash.
- **bootstrap:** per-OS Python install command (apt/dnf/pacman/brew/winget) + the **optional strict-security** toggle: `security_mode` (permissive default = verify-and-warn; `--strict` = fail-closed) and `verify_download` (skippable this initial phase).
- **setup:** the **one brain CLI** — `doctor · config · self-scan · connect`.
- **install.sh** (brain-path: Layer-1 Python per OS → hand off) + **install.ps1** (winget). Smoke-verified `install.sh doctor` end-to-end.
**Failure points closed:** supply-chain / Layer-1+2 dependency install; "one command per OS".

---

## Phase 8 — Observability + diagnostics
**File:** `agent/obs.py` (+ `collect-diagnostics` in the CLI) · **Tests:** `test_obs.py` (5)
Redaction-first (logs + bundle = the review's top disclosure vector):
- `redact` / `log_line` — structured JSON, word-boundary secret masking, correlation id.
- `heartbeat_metrics` — **low-cardinality** set, **no IP/host/target labels** (TSDB-safe, guarded by a test).
- `mask_ip` + `build_diagnostics` — config secrets stripped, own-IPs masked.
- `collect-diagnostics` wired into the CLI; smoke-verified the bundle carries **no secrets**.
**Failure points closed:** #12 (diagnostics leak), §6 observability gap.

---

## Net result

- **Brain CLI surface:** `doctor · config · self-scan · connect · collect-diagnostics` (macOS/Linux/Windows).
- **Runnable today:** `sh install.sh self-scan` / `.\install.ps1 self-scan` (no Manager); `connect` opt-in.
- **Review failure register (15 rows):** agent-side items #3–#14 built + tested; **#1 (OT) deferred by design**; **#2/#10(partial)/#15 (signing/SBOM/parser-fuzzing) → Phase 10**.

## Remaining phases
- **Phase 9** — service install with restart limits (systemd / launchd / Scheduled Task), rendered *from* the config object.
- **Phase 10** — code signing + SBOM + 3-OS CI + SOC/uninstall/network/data-handling docs.

## Test count by file
| File | Tests |
|---|---|
| test_scope_model | 18 |
| test_config_model | 5 |
| test_doctor | 7 |
| test_exit_state | 6 |
| test_supervisor | 6 |
| test_result_queue | 9 |
| test_self_scan | 6 |
| test_connect | 9 |
| test_bootstrap | 5 |
| test_deps | 4 |
| test_setup_cli | 4 |
| test_obs | 5 |
| **Total** | **84** |
