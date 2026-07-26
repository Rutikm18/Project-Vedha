# Vedha Probe & Manager — Testing Plan

> Companion to the probe design (headless-default + optional console, single-probe
> sequential queue, thin-probe/fat-manager). This plan says **what to test, at which
> layer, how to run it, and what must never ship broken.**

---

## 0. Verified baseline (2026-07-23)

All three suites currently pass. Re-establish this green baseline before adding features.

| Suite | Result | Canonical command |
|---|---|---|
| Probe unit/integration | **290 passed** | `cd probe && .venv/bin/python -m pytest -q` |
| Manager backend | **241 passed, 3 skipped** | `make test` |
| Detection engine | **146 passed** | `manager/backend/.venv/bin/python -m pytest detection_engine/tests -q` |

**Total: 677 tests green.**

> ⚠️ **Run the probe suite with its explicit venv Python** (`probe/.venv/bin/python -m pytest`).
> A bare `pytest` or `python3 -m pytest` can be intercepted by a shell hook (RTK) and fail
> to spawn. The manager pattern (`./.venv/bin/python -m pytest`) is the same rule.

---

## 1. Test layers (the pyramid)

| Layer | Proves | Location | Speed |
|---|---|---|---|
| **Unit — probe** | scope validation, crypto, transport, spool, task-runner logic (mocked I/O) | `probe/tests/` (11 files) | seconds |
| **Unit — manager** | detection, agents, PAT auth, enrichment, attack paths | `manager/backend/tests/`, `manager/detection_engine/tests/` | seconds |
| **Safety / negative** ⭐ | out-of-scope refused, OT blocked, excludes dropped, forged dispatch refused | `probe/tests/test_scope_validator.py` + `Probe_testing.md §3A.6` | seconds |
| **Contract** | probe facts payload ⟷ manager ingest schema stay in lockstep | *(to add)* `probe/tests/test_wire_contract.py` | seconds |
| **Accuracy** | per-scanner precision / recall / false-positive vs. hand-verified truth | `probe/MANUAL_TESTING.md` (12 steps) | manual |
| **Smoke / integration** | all scanners + orchestrator run end-to-end against a real target | `probe/test_all.sh`, `probe/tests/test_integration.py` | ~1 min |
| **Full lab (e2e)** | probe → facts → detection → dashboard, two machines | `Probe_testing.md §3A` (Mac + Windows) | manual |

---

## 2. The safety gate (non-negotiable — blocks release)

For a scanner the failure mode isn't "wrong answer," it's **"scanned something you weren't
authorized to, inside a client's network."** These tests are a hard CI gate: if any fail,
**nothing ships.**

- [x] Out-of-scope target → refused / produces no scan work (`test_scope_validator.py`)
- [x] Excluded ranges → dropped before any packet (`test_scope_validator.py`)
- [x] OT profile → refuses active use-cases, exit code 2, **no override** (`pipeline.py`)
- [x] Manager-issued job with no authoritative scope → refused (`test_task_runner.py`)
- [ ] **NEW** Forged / unsigned job on the fallback path → refused (signed dispatch)
- [ ] **NEW** Console dry-run / preview → **zero packets sent** (assert via no `send`/`connect`)

> Wire these into a dedicated target: `make test-safety` → runs only the negative/scope
> tests, run on **every** commit.

---

## 3. New-feature test matrix (write the test first — TDD)

Every feature from the design ships with its test defined up front. "Extends" = add cases to
the existing file; "new" = new test module.

| Feature | Test(s) | Layer | File |
|---|---|---|---|
| **Enrollment token (operator-set expiry)** | past `expires_at` → refused; `max_uses` decrements to dead; `revoke` kills unused token; both `expires_in` and `expires_at` honored; **license issued in the same exchange** | unit + integration | manager `test_agents.py` / new `test_enroll_tokens.py`; probe enroll path |
| **Job lease / requeue** | claim sets `lease_expires_at`; heartbeat **renews** it (long scan safe); lapse → requeue (bounded retries); replayed `job_id` → idempotent, no double-count | unit + integration | manager `test_agents.py`; probe `test_task_runner.py`, `test_transport.py` |
| **Cancel** | queued cancel → dropped (probe never sees it); running cancel → abort + **partial result** submitted | unit + integration | manager tests; probe `test_task_runner.py` |
| **Signed dispatch (Ed25519)** ⭐ | unsigned/forged job on fallback path → refused; valid manager signature → accepted; wrong-key signature → refused | unit (safety) | probe `test_scope_validator.py`, `test_scope_crypt.py` |
| **Facts signing + audit chain** | probe signs facts with identity key; manager verifies; tampered facts break the hash chain; ledger links `scope → facts → findings` | unit | probe `test_scope_crypt.py`; manager new `test_audit_chain.py` |
| **Console enqueue (Approach A)** | `Enqueue` → creates a queue job and **never scans locally**; dry-run preview → expands scope with **zero packets** | integration | probe new `test_console.py`; manager `test_agents.py` |
| **Kill switch / global pause** | `paused` flag on heartbeat → probe stops pulling; resume → resumes | unit | probe `test_transport.py` |
| **Proxy / corporate CA** | probe dials out through an HTTP(S) proxy + custom `PROBE_CA_BUNDLE` | integration | probe `test_transport.py` |
| **Versioned wire contract** | probe declares facts-schema version at register; manager confirms or refuses with "upgrade probe"; facts payload matches ingest schema | contract | probe new `test_wire_contract.py`; manager ingest test |

---

## 4. How to run everything

```bash
# ── Inner loop (run constantly while coding) ──────────────────────────
cd probe && .venv/bin/python -m pytest -q          # probe: 290 tests, ~1.5s
make test                                          # manager backend
manager/backend/.venv/bin/python -m pytest detection_engine/tests -q

# ── Safety gate (every commit / CI) ───────────────────────────────────
cd probe && .venv/bin/python -m pytest tests/test_scope_validator.py -q
# (+ make test-safety once the target exists)

# ── Smoke (before a probe release) ────────────────────────────────────
cd probe && ./test_all.sh 127.0.0.1 scope.txt

# ── Full e2e (before shipping to a client) ────────────────────────────
#   follow Probe_testing.md §3A — two-machine lab (Mac + Windows)
```

---

## 5. CI wiring (recommended)

| Trigger | Runs |
|---|---|
| **Every PR / commit** | probe unit + manager unit + detection engine + **safety gate** + contract |
| **Nightly** | smoke (`test_all.sh` against a fixture host) + accuracy spot-checks |
| **Pre-release (probe image)** | full smoke + safety gate + a scripted slice of the §3A lab |
| **Pre-release (manager)** | full backend + detection + attack-path suites |

**Definition of done for any feature:** its row in §3 is implemented as a *failing test first*,
then made green, the **safety gate stays green**, and the contract test still passes.

---

## 6. Known gaps to convert into tests (from `CURRENT_STATE.md §8`)

Track these as accuracy-regression tests so they don't silently worsen:

- TLS 1.3 false-negative vs. real endpoints (Python OpenSSL ClientHello difference)
- UDP result ambiguity (no-reply conflates closed/filtered/no-response)
- IPv4-only scanners (udp/smb/snmp/db hardcode `AF_INET`)
- `pipeline.py` fixed deep-inspection port table (HTTPS on 9443 not routed)
