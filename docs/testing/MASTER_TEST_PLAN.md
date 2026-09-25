# Vedha — Master Software Testing Plan & Checklist

> **Scope of this document.** A single, exhaustive checklist of *every* class of testing
> relevant to Vedha, organised along **two lenses** — the **project approach** (test types
> across the SDLC / the test pyramid) and the **platform approach** (per component). For each
> area it states *what to test*, gives an actionable `- [ ]` checklist, names the *tools* to use,
> and gives the *run command / CI gate* where one exists.
>
> **This is the umbrella.** It complements — does not replace — the two focused plans:
> - [`TESTING_PLAN.md`](./TESTING_PLAN.md) — probe+manager layered plan, safety gate, new-feature TDD matrix.
> - [`probe-testing.md`](./probe-testing.md) — the deep two-machine lab (Mac + Windows) e2e procedure.
>
> **Product context that shapes this plan.** Vedha is a **network vulnerability-assessment /
> attack-surface platform**. That makes two test classes *unusually* important and both are hard
> release blockers:
> 1. **Safety** — the probe must *never* touch anything outside authorised scope. A false action
>    here is a client-network incident, not a bug.
> 2. **Accuracy** — findings must be evidence-backed. A false positive erodes trust; a false
>    negative is a missed exposure. Precision/recall are first-class, measured, and gated.
> Because Vedha is itself a *security* product, the platform must also pass the same AppSec bar it
> tests customers against — see **Part B §2** and **Part D**.

---

## 0. How to use this document

- Treat every `- [ ]` as a real checklist item. For a release, copy the relevant sections into
  the release ticket and tick them off.
- **Legend for gates:**
  - 🚦 **Release blocker** — if red, nothing ships.
  - 🔁 **Every PR / commit** — must be green in CI on every change.
  - 🌙 **Nightly / scheduled** — expensive suites run off the PR path.
  - 🧪 **Pre-release** — run before cutting a probe image or manager release.
  - 👤 **Manual / periodic** — human-run (exploratory, UAT, lab, pentest).
- **Current green baseline** (keep this green before adding features):

  | Suite | Command | Baseline |
  |---|---|---|
  | Probe unit/integration | `cd probe && .venv/bin/python -m pytest -q` | see `TESTING_PLAN.md §0` |
  | Manager backend | `make test` | see `TESTING_PLAN.md §0` |
  | Detection engine | `manager/backend/.venv/bin/python -m pytest detection_engine/tests -q` | see `TESTING_PLAN.md §0` |
  | Frontend | `cd manager/frontend && npm test` (`tsx --test tests/*.test.ts`) | 28 suites |

  > ⚠️ Always run pytest through the **explicit venv Python** (`.venv/bin/python -m pytest`), never
  > a bare `pytest` — a shell hook (RTK) can intercept the bare command. (Same rule as `TESTING_PLAN.md`.)

---

## 1. The two lenses (mental model)

```
                    ┌─────────────────────────────────────────────┐
   PROJECT APPROACH │  Static → Unit → Integration → Contract →    │  (Part A)
   (test types /    │  API/Component → System/E2E → Regression →   │
    the pyramid)    │  Smoke/Sanity → Acceptance → Exploratory     │
                    └─────────────────────────────────────────────┘
                    ┌─────────────────────────────────────────────┐
 NON-FUNCTIONAL     │  Performance · Security · Resilience ·       │  (Part B)
                    │  Compatibility · Usability/a11y · Install/   │
                    │  Upgrade · Recovery/DR · Observability ·     │
                    │  Compliance/Privacy · i18n · Maintainability │
                    └─────────────────────────────────────────────┘
                    ┌─────────────────────────────────────────────┐
   PLATFORM         │  Backend · Frontend · Probe/Agent ·          │  (Part C)
   APPROACH         │  Detection Engine · Scanner Accuracy ·       │
   (per component)  │  Deploy/Infra · Data Durability · AI Seam    │
                    └─────────────────────────────────────────────┘
                    ┌─────────────────────────────────────────────┐
   DOMAIN-CRITICAL  │  Scope-Safety Gate · Accuracy Gate ·         │  (Part D)
   (unique to a VA  │  Multi-Tenancy Isolation · Probe Integrity · │
    platform)       │  Fact-Contract / Ingest Gate                 │
                    └─────────────────────────────────────────────┘
```

Read Part A + B for *how much of each kind of testing to do*; read Part C to know *where in the
codebase each applies*; Part D lists the suites that are unique to this product and must never rot;
Part E is the process/governance that binds it together.

---

## 2. Test environments & test-data strategy

Testing quality is capped by environment fidelity. Define these explicitly.

### 2.1 Environments
- [ ] **Local inner-loop** — venvs + `npm`, no Docker. Fast unit/integration. (`make venv`, `make test`)
- [ ] **Local full stack** — `make up` / `docker-compose` (postgres, redis, neo4j, api, worker, frontend, probe, caddy edge, ollama). For integration/E2E/perf smoke.
- [ ] **Ephemeral CI** — GitHub Actions matrix (ubuntu/macos/windows for the probe).
- [ ] **Staging / lab** — the two-machine lab in `probe-testing.md` (real targets in an isolated subnet).
- [ ] **Production-like** — AWS EC2 + Caddy auto-TLS (`docs/deployment/aws-deployment.md`), for install/upgrade/DR rehearsal.
- [ ] Each environment has a **known-good `.env`** derived from `.env.example` / `gen-env.sh`; no shared secrets across envs.

### 2.2 Test data & fixtures
- [ ] **Deterministic fixtures** for unit tests (no live network, no wall-clock, no RNG — see the workflow rule about `Date.now`/random).
- [ ] **Labeled accuracy corpora** with declared `provenance` (`nmap` / second-vantage / manual = evidence; `self_regression` = drift-only). See `probe/tests/fixtures/accuracy_corpus/README.md`.
- [ ] **Synthetic-but-realistic scan targets** in an isolated lab subnet (never public IPs, never client ranges).
- [ ] **Seed data** for the manager (`make seed`) is reproducible and idempotent.
- [ ] **No real secrets/PII in fixtures** — gitleaks pre-commit + `secret-scan.yml` enforce this.
- [ ] Database state is **reset between test runs** (transactional rollback or fresh schema per module).

### 2.3 Tooling matrix (recommended, mapped to the current stack)

| Concern | Backend (Python/FastAPI) | Frontend (Next.js/TS) | Probe (Python, x-OS) |
|---|---|---|---|
| Test runner | `pytest` + `pytest-asyncio` (already used) | `tsx --test` (used) → consider **Vitest** | `pytest` + `pytest-asyncio` |
| Coverage | `pytest-cov` / `coverage.py` | `c8` / `vitest --coverage` | `pytest-cov` |
| Lint / format | **Ruff** (already), `black` optional | **ESLint** (`eslint-config-next`) + Prettier | **Ruff** |
| Types | `mypy` / `pyright` | `tsc --noEmit` (strict) | `mypy` / `pyright` |
| Property-based | **Hypothesis** | `fast-check` | **Hypothesis** |
| Mutation | `mutmut` / `cosmic-ray` | **Stryker** | `mutmut` |
| API/E2E | `httpx.AsyncClient` (used) | **Playwright** (`tests/e2e/` exists) | — |
| Load/perf | **k6** (primary), **Locust** (Python teams) | k6 against BFF | scanner throughput harness |
| Contract | **Schemathesis** (OpenAPI) / **Pact** | Pact consumer | wire-contract pytest |
| SAST | **Semgrep**, **Bandit** | **Semgrep**, ESLint security plugin | **Semgrep**, **Bandit** |
| SCA | **pip-audit**, **Trivy**, OWASP Dependency-Check | **npm audit**, **Trivy** | **pip-audit** |
| Secrets | **gitleaks** (pre-commit, used) | gitleaks | gitleaks |
| DAST | **OWASP ZAP** / StackHawk (against a running stack) | ZAP | — |
| Container | **Trivy** / **Grype** (image scan), **Dockle** | — | Trivy on probe image |
| SBOM | CycloneDX (`agent.release sbom`, already in CI) | `cyclonedx-npm` | CycloneDX (used) |

---

# PART A — PROJECT APPROACH (functional test types)

The classic pyramid: many fast, isolated tests at the bottom; few, slow, high-fidelity tests at the top.

## A1. Static analysis & pre-commit  🔁
*Cheapest defect catch — runs before a test is even executed.*

- [ ] **Linting** clean: `ruff check` (backend + probe), `eslint .` (frontend).
- [ ] **Formatting** enforced (Ruff format / Prettier) — no drift in diffs.
- [ ] **Type checking**: `mypy`/`pyright` on backend & probe; `tsc --noEmit` on frontend with `strict: true`.
- [ ] **Secret scanning**: `gitleaks` pre-commit hook installed *and* `secret-scan.yml` green (SEC-01 containment control).
- [ ] **Large-file / private-key guards** (pre-commit hooks already configured).
- [ ] **SAST** (`semgrep --config auto`, `bandit -r`) — see Part B §2.
- [ ] **Dead code / unused deps** flagged (`ruff`, `ts-prune`, `depcheck`).
- **Tools:** Ruff, ESLint, mypy/pyright, tsc, gitleaks, Semgrep, Bandit.
- **Gate:** pre-commit locally; a `lint` job in CI on every PR.

## A2. Unit testing  🔁
*One unit in isolation; all I/O mocked; sub-second.*

- [ ] Pure logic covered: scope validation, crypto, transport framing, spool/queue, task-runner, detection rules, adapters/parsers.
- [ ] **Async correctness**: tests use `asyncio_mode = strict` (already set); no `gather` on a shared `AsyncSession` (known trap — see `vedha-backend-perf-async`).
- [ ] **No hidden non-determinism**: no live network, no real clock/RNG in unit scope; freeze time where needed.
- [ ] **Boundary & negative cases** for every branch, not just the happy path.
- [ ] Coverage target: **≥ 80 %** on core modules (detection, auth, scope, adapters); track trend, don't chase 100 %.
- [ ] **Property-based tests** (Hypothesis / fast-check) for parsers, schema round-trips, scope math.
- **Run:** `make test`; `cd probe && .venv/bin/python -m pytest -q`; `cd manager/frontend && npm test`.

## A3. Integration testing  🔁
*Two or more real components together (DB, Redis, in-process engines).*

- [ ] **API + DB**: routers hit a real (test) Postgres via `httpx.AsyncClient`; assert persistence + query paths.
- [ ] **Queue/worker**: enqueue → worker picks up → status transitions (`queued → running → done/cancelled`).
- [ ] **Redis-backed** rate limiting, refresh-token store, caches behave under a real Redis.
- [ ] **Detection pipeline**: facts → `run_full_detection` → findings (posture + CVE tracks both fire).
- [ ] **Migrations apply cleanly** on a fresh DB *and* forward from the previous release (Alembic upgrade + downgrade smoke).
- [ ] N+1 query regressions guarded (assert query counts on hot paths — `_list_assets`, dashboards).
- **Tools:** pytest + `httpx.AsyncClient`, `testcontainers` (optional) or the compose stack.

## A4. Contract testing  🔁  🚦(wire contract)
*The seams between independently deployed parts stay in lockstep.*

- [ ] **Probe facts ⟷ manager ingest**: facts payload validates against the ingest schema; a mismatch fails CI, not silently at runtime. (See `TESTING_PLAN.md §3` "Versioned wire contract".)
- [ ] **Facts-schema version negotiation**: probe declares version at register; manager accepts or refuses with "upgrade probe".
- [ ] **Ingest gate is observable**: `DetectionRun.stats["ingest"]` records validated/rejected — a run that silently drops facts is a defect (this is the detection SPOF, per `vedha-ingest-gate-silent-drop`).
- [ ] **REST API contract**: OpenAPI schema is generated and fuzzed (**Schemathesis**) — every documented endpoint accepts its schema and rejects malformed input.
- [ ] **Frontend BFF ⟷ backend**: adapter tests assert the shapes the UI relies on (`lib/adapters.ts`, `findings-adapters`, `scanner-adapters`) don't drift.
- **Tools:** custom pytest wire-contract test, Schemathesis, Pact (if teams split producer/consumer).

## A5. API / component testing  🔁
*Each endpoint & each UI component behaves to spec.*

- [ ] Every router (25: `agents`, `engagements`, `findings`, `portal`, `detection`, `probe_enrollment`, `vuln_scans`, `exploits`, `attack_paths`, `ad`, `customer_access`, …) has: happy path, authz-denied, validation-422, and not-found-404 cases.
- [ ] **Pagination, filtering, sorting** correctness (e.g. findings IP filter — `vedha-verification-never-stamped`).
- [ ] **Idempotency** on retryable POSTs (replayed `job_id` → no double count).
- [ ] **WebSocket** endpoints (`agent_ws`) tested for claim race, token rotation, paused/resume.
- [ ] Frontend **components** render each state: empty, loading, error, populated, unauthorized.
- **Tools:** pytest + httpx; React Testing Library / Playwright component tests.

## A6. System / end-to-end testing  🧪 👤
*The whole product, as a user experiences it.*

- [ ] **Operator flow**: create engagement → set scope → enrol probe → launch scan → facts ingested → findings + detection → report generated.
- [ ] **Customer-portal flow**: portal login (correct audience) → dashboard → scoped findings → AI assistant → scan request.
- [ ] **Probe lifecycle**: enrol → heartbeat → claim job → scan → submit chunked results → lease renew → complete; plus cancel & kill-switch.
- [ ] **Two-machine lab** (Mac + Windows) — the full `probe-testing.md §3A` procedure.
- [ ] **Browser E2E** for the dashboard (`manager/frontend/tests/e2e/`) with **Playwright**.
- **Gate:** pre-release; the lab is manual/periodic.

## A7. Regression testing  🔁  🌙
- [ ] Every fixed bug ships with a **failing-first test** that would catch its return (TDD rule in `TESTING_PLAN.md`).
- [ ] Known-gap list is encoded as **regression tests** (TLS 1.3 FN, UDP ambiguity, IPv4-only scanners, deep-port routing).
- [ ] **Accuracy regression**: the scanner-accuracy gate (`scanner-accuracy.yml`) fails the build when precision/recall drops.
- [ ] **Snapshot/golden** outputs for report generation and adapter transforms, reviewed on change.
- [ ] Full suite runs nightly even when PRs touch a subset.

## A8. Smoke & sanity testing  🔁  🧪
- [ ] **Smoke**: does the stack boot? `make doctor` (Docker, ports, `.env`, insecure prod defaults) + API `/health` 200 + one scan end-to-end (`probe/test_all.sh`).
- [ ] **Sanity**: after a targeted change, the touched area's narrow suite passes before the full run.
- [ ] `python -m agent.setup doctor` exits 0 on a healthy host (already in `agent-ci.yml`).

## A9. Acceptance / UAT  👤
- [ ] Each user story has **explicit acceptance criteria** and is signed off against them.
- [ ] Product/PM validates against `docs/pm/` personas & use cases (`usecases-networkva.md`).
- [ ] Compliance packs (IN/EU/UK/US/ME/APAC) produce the expected report framing per region.

## A10. Exploratory & error-guessing  👤
- [ ] Time-boxed charter-based sessions on new/risky features (portal isolation, AI chat, aggressive scan).
- [ ] Deliberate abuse: malformed uploads, huge scopes, unicode/emoji in names, clock skew, mid-scan probe kill.
- [ ] Findings feed back as new automated regression tests.

---

# PART B — NON-FUNCTIONAL TESTING

## B1. Performance testing  🌙 🧪
*Throughput, latency, and behaviour under load — separate concerns, test each.*

| Sub-type | Question it answers | For Vedha |
|---|---|---|
| **Load** | Behaviour at expected concurrency | N operators + M portal users + K probes heartbeating |
| **Stress** | Where does it break, and how? | ramp until API/worker/DB saturate; assert graceful degradation |
| **Spike** | Sudden burst tolerance | many probes submitting chunked results at once |
| **Soak / endurance** | Leaks & drift over hours | long aggressive scan; watch memory/FD/connection growth |
| **Volume** | Large data sets | 65k-port deep scan across many hosts; large findings tables |
| **Scalability** | Does adding resources help linearly? | worker/replica scaling, DB connection pool |

- [ ] **API load**: k6 scenarios against auth, findings list, dashboards, ingest.
- [ ] **Scan throughput** regression: ports/sec doesn't collapse (guard the AIMD ratchet regression — `vedha-aimd-ratchet-regression`; RST-suppression must not read as congestion).
- [ ] **Aggressive/deep scan memory**: per-host RAM stays bounded (47 MB→4.3 MB/host target; per-host chunk buffer + reaper — `vedha-aggressive-scan-failure`).
- [ ] **Result durability under load**: chunked commits survive a mid-scan crash (partial results recoverable).
- [ ] **DB hot paths**: p95 latency budgets on findings/dashboard queries; N+1s caught.
- [ ] **WebSocket fan-out**: heartbeat/claim latency stable with many probes.
- [ ] Establish **baselines + budgets**; regressions fail the perf job (use `/benchmark`).
- **Tools:** k6 (primary), Locust, JMeter/Gatling (reports), `py-spy`/`memray` (profiling), Prometheus (already instrumented via `prometheus-fastapi-instrumentator`).

## B2. Security testing (the platform itself)  🔁 🌙 🚦 👤
*Vedha is a security product — it must clear the AppSec bar it holds customers to. Anchor to
**OWASP ASVS 5.0** and **OWASP WSTG 4.2/5.0**; use **OWASP Top 10** & **API Security Top 10** as coverage checklists.*

**Static / dependency / supply chain**
- [ ] **SAST**: Semgrep (`--config auto` + custom rules) + Bandit; no high-severity findings unresolved. 🔁
- [ ] **SCA**: `pip-audit`, `npm audit`, Trivy/Dependency-Check on all lockfiles; pinned deps; no known-exploited CVEs. 🔁
- [ ] **Container scan**: Trivy/Grype on the probe & manager images; distroless/minimal base; non-root user. 🧪
- [ ] **SBOM** generated per build (CycloneDX — already in `agent-ci.yml`) and archived. 🔁
- [ ] **Secrets**: gitleaks pre-commit + `secret-scan.yml`; no keys in history. 🔁🚦

**Dynamic / runtime (against a running stack)**
- [ ] **DAST**: OWASP ZAP / StackHawk baseline + full scan against the API and dashboard in CI or nightly. 🌙
- [ ] **AuthN**: password hashing (bcrypt via `passlib`), login rate-limit is **proxy-aware** (X-Forwarded-For not spoofable — `vedha-security-p0-hardening`), account lockout, no user enumeration.
- [ ] **Session/JWT**: refresh tokens are **single-use, reuse-revokes** the family; `aud` claim minted **and verified** (operator vs portal — `vedha-portal-audience-boundary`); short access-token TTL; logout revokes.
- [ ] **AuthZ / IDOR**: every object-scoped endpoint checks ownership; a portal token cannot read another tenant's engagement/findings; operator vs client role boundary enforced (`Role client is not permitted`). 🚦
- [ ] **Multi-tenancy isolation**: cross-engagement data leakage impossible (see Part D §3).
- [ ] **Injection**: SQLi (ORM-parameterised — verify no raw string SQL), command injection in scanner wrappers, path traversal in uploads/reports.
- [ ] **Prompt injection / LLM abuse**: the AI seam sanitises tool/context input, uses structured outputs, and can't be steered to exfiltrate data or run out-of-policy actions (`vedha-ai-pipeline`, "injection hardening").
- [ ] **Crypto**: credential encryption at rest (`test_credential_crypto`), Ed25519 signing for dispatch/facts, TLS everywhere (Caddy), no weak ciphers.
- [ ] **Rate limiting / DoS**: per-IP + per-account limits; large-payload guards (the run-scoped-fact 422 path — `vedha-run-scoped-fact-422`).
- [ ] **Security headers & CORS**: HSTS, CSP, X-Content-Type-Options, locked CORS origins on API and BFF.
- [ ] **Input validation**: Pydantic models reject malformed input with 422, not 500 (IDOR/500 fixes — `vedha-security-p0-hardening`).
- [ ] **Audit trail integrity**: scope→facts→findings ledger; tampered facts break the hash chain.
- [ ] **Manual pentest** of the platform before major releases (or 3rd-party). 👤
- **Tools:** Semgrep, Bandit, pip-audit, npm audit, Trivy, Grype, gitleaks, OWASP ZAP, StackHawk, Burp Suite (manual), Schemathesis (fuzz).
- **Standards:** OWASP ASVS 5.0, OWASP WSTG, OWASP Top 10, OWASP API Security Top 10, OWASP LLM Top 10, CWE, MITRE ATT&CK.

## B3. Reliability, resilience & chaos  🌙 👤
- [ ] **Graceful degradation** when optional services are down (AI/Ollama, Neo4j, integrations import defensively — must not crash the API).
- [ ] **Dependency failure injection**: kill Redis / Postgres / worker mid-flow → clear errors, no data loss, auto-recovery.
- [ ] **Network faults**: probe loses connectivity mid-scan → lease lapses → job requeues (bounded retries), partial results preserved.
- [ ] **Idempotency under retry**: replays don't double-write.
- [ ] **Backpressure**: spool/queue backpressure works (`test_spool_backpressure`); the 3-job queue cap holds; all-cancelled campaigns don't hang at "aggregating" (`vedha-job-control-and-progress`).
- [ ] **Reaper** recovers orphaned per-host chunk buffers.
- **Tools:** toxiproxy / Pumba (container chaos), manual kill tests, `test_gate6_concurrency`, `test_ws_claim_race`.

## B4. Compatibility testing  🔁(probe matrix) 🧪
- [ ] **Cross-OS probe**: unit suite green on **ubuntu / macOS / windows** (already a CI matrix in `agent-ci.yml`); dual-stack IPv4/IPv6 fallback (`test_dualstack_fallback`).
- [ ] **Python version** pinned (3.12) and tested; no reliance on platform-specific behaviour except where guarded (kernel FD limits, `test_kernel_limits`/`test_fd_limit`).
- [ ] **Cross-browser** dashboard: Chrome, Firefox, Safari, Edge (Playwright projects).
- [ ] **Responsive / device**: mobile, tablet, desktop breakpoints (the platform's responsive workstream).
- [ ] **Sealed-binary parity**: the Nuitka-sealed probe behaves identically to source (`probe-seal-parity.yml`) — see Part D §4.
- [ ] **DB/infra versions**: Postgres, Redis, Neo4j versions pinned in compose and tested.

## B5. Usability & accessibility  👤 🌙
- [ ] **Accessibility (a11y)**: WCAG 2.2 AA — keyboard nav, focus order, ARIA roles, contrast, screen-reader labels.
- [ ] Automated a11y scan: **axe-core** / Playwright `@axe-core/playwright` / Lighthouse in CI.
- [ ] **UX correctness**: timestamps render **IST (+05:30), never naive** (`vedha-project-timezone-ist`); dashboards show real data not placeholder zeros (the "Patched always 0" trap — `vedha-dashboard-field-audit`).
- [ ] Error/empty/loading states are informative, not blank.
- [ ] Reduced-motion respected; no motion-only signalling.
- **Tools:** axe-core, Lighthouse, Playwright, manual keyboard/screen-reader passes; `/design-review`, `/qa`.

## B6. Installability, upgrade & migration  🧪 👤
- [ ] **Clean install** from scratch: `install.sh` prod path + `make aws-up` testing path both succeed on a fresh host.
- [ ] **`make doctor`** catches the known API-crash root causes and insecure prod defaults *before* boot (`vedha-aws-deploy`).
- [ ] **DB migrations**: `alembic upgrade head` from an empty DB **and** from the last release's schema; a **downgrade** path exists or is explicitly waived per migration (e.g. 0041/0044).
- [ ] **Backfill migrations** are idempotent and re-runnable (0044 passive-verification backfill).
- [ ] **Probe enrolment / PAT**: mint (`make probe-pat`), enrol, and re-point to a new manager work; credentials record their issuer (`vedha-device-credential-diagnosis`).
- [ ] **Rollback**: a bad release can be rolled back without data corruption.
- [ ] **Config validation**: `gen-env.sh` produces a valid `.env`; missing/insecure values are rejected loudly.

## B7. Recovery, backup & disaster recovery  🧪 👤
- [ ] **Backup**: Postgres (`pgdata`), Neo4j (`neo4jdata`), probe state (`probestate`) volumes are backed up and **restore-tested**.
- [ ] **Restore drill**: restore from backup into a clean stack; verify findings/engagements intact.
- [ ] **RPO/RTO** defined and measured.
- [ ] **Crash consistency**: kill the stack mid-scan; on restart, in-flight jobs resolve (requeue or complete-with-gaps), no corruption.
- [ ] **Data retention / purge** works and is auditable.

## B8. Observability testing  🔁 🌙
- [ ] **Structured logs** (structlog) present at the right levels; no secrets/PII logged.
- [ ] **Metrics** exposed (Prometheus instrumentator) — request latency, error rate, queue depth, scan throughput; alert thresholds defined.
- [ ] **Detection trace**: every posture rule records an outcome (drift/clean/no-evidence) so non-findings explain themselves (`vedha-detection-trace`); the `detection-explain` endpoint returns coherent traces.
- [ ] **Health/readiness** endpoints reflect real dependency state.
- [ ] **Trace/correlation IDs** thread a scan from launch → facts → findings for debuggability.

## B9. Compliance, privacy & legal  👤
- [ ] **Authorisation-to-test** enforced: scope files are the *authoritative* boundary; no scan without an authoritative scope (safety gate, Part D §1).
- [ ] **Data privacy**: PII in scan results handled per policy; encryption at rest + in transit; least-privilege access.
- [ ] **Regional compliance packs** produce correct framing (IN/EU/UK/US/ME/APAC — `vedha-tags-domain-ai-bfsi`).
- [ ] **Audit logging** for security-relevant actions (login, scope change, scan launch, data export).
- [ ] **License/IP protection** of the probe is intact (Part D §4).

## B10. Internationalisation & localisation  🌙
- [ ] **Timezone**: all timestamps aware `+05:30` IST via `project_time`/`scanner_base`; `VEDHA_TZ` override honoured; filenames drop the `Z` (`vedha-project-timezone-ist`).
- [ ] **Unicode** safe end-to-end (hostnames, org names, findings text, report rendering).
- [ ] Number/date formatting consistent across UI and reports.

## B11. Maintainability & test-suite health  🌙
- [ ] **Coverage tracked** with a trend line (not a vanity %); new code doesn't drop it.
- [ ] **Mutation testing** on the highest-stakes modules (scope validation, detection rules, crypto) to prove tests actually *assert* (mutmut / Stryker).
- [ ] **Flaky-test budget = 0**: quarantine + fix; the scanner-accuracy gate must not be flaky.
- [ ] **Test speed** watched — inner loop stays seconds, not minutes.
- [ ] **Drift guard**: `scanner/` ≡ `main_scripts/` parity holds (main_scripts canonical — `vedha-probe-and-lint-gotchas`).

---

# PART C — PLATFORM APPROACH (per component)

## C1. Manager Backend — FastAPI, async SQLAlchemy, 25 routers  (`manager/backend/`)
- [ ] **Unit**: services, detection, auth, adapters (131 test files today — keep growing).
- [ ] **Async traps**: no shared-session `gather`; bcrypt off the event loop (`app/auth/password.py`); detection offloads CPU work off the loop (`test_detection_offloads_event_loop`).
- [ ] **API**: every router's happy/authz/validation/404 paths (Part A5).
- [ ] **DB/migrations**: Alembic up+down, backfills idempotent (Part B6).
- [ ] **Queue/worker**: dispatch, lease, cancel, requeue, idempotency, queue cap.
- [ ] **Rate limiting & refresh store** on real Redis.
- [ ] **WebSocket** (`agent_ws`): claim race, token rotation, paused/resume.
- **Run:** `make test`; `manager/backend/.venv/bin/python -m pytest -q`.

## C2. Manager Frontend — Next.js / React / TypeScript  (`manager/frontend/`)
- [ ] **Component/logic tests** (28 suites via `tsx --test`): adapters, stores, workspaces, parsers, auth gates, session security.
- [ ] **BFF proxy routes** (`app/api/**/route.ts`) tested for auth pass-through, error mapping, no token leakage to the client.
- [ ] **Console-parity seam**: operator and portal share components; portal routes delegate to operator handlers with engagement pinned (`vedha-console-parity-seam`) — assert isolation holds.
- [ ] **E2E** (`tests/e2e/`): Playwright flows for login, dashboard, findings, reports, scan request.
- [ ] **Visual regression** on key screens (Playwright snapshots / Percy-style).
- [ ] **a11y + responsive** (Part B4/B5).
- **Run:** `cd manager/frontend && npm test`; `npx playwright test`.

## C3. Probe / Agent — Python, cross-OS, sealed  (`probe/`)
- [ ] **Safety/scope** (🚦): out-of-scope refused, excludes dropped pre-packet, OT profile refuses active use-cases (exit 2, no override), forged/unsigned dispatch refused, dry-run sends **zero packets** (Part D §1).
- [ ] **Scanners**: TCP/SYN/UDP/service-banner/TLS/DB/FTP/DNS/SMB/SNMP/printer/host-discovery — accuracy + taxonomy (open vs filtered vs closed).
- [ ] **Transport/lease**: heartbeat renews lease, lapse requeues, kill-switch pauses, proxy + custom CA dial-out.
- [ ] **Result durability**: oversized results, chunked submission, stage-boundary commits, backpressure.
- [ ] **Identity/enrolment**: PAT mint/enrol/re-point; token rotation 403 avoidance (single process per `state.json`).
- [ ] **Doctor / self-scan / feasibility / kernel limits** green on each OS.
- [ ] **Sealed-binary parity** (Part D §4).
- **Run:** `cd probe && .venv/bin/python -m pytest -q` (163 test files); CI matrix in `agent-ci.yml`.

## C4. Detection Engine  (`manager/detection_engine/`)
- [ ] **Posture rules** (25 rules): each rule fires on drift, stays clean on compliant facts, and records a trace outcome.
- [ ] **CVE + KEV/EPSS** enrichment joins correctly onto the posture track (e.g. MSRPC epmap → PrintNightmare path).
- [ ] **`run_full_detection`** unifies CVE + posture; both tracks reach Findings.
- [ ] **Fact contract**: rules only consume validated-scanner facts; ingest gate rejects bad payloads *observably*.
- [ ] **Exposed-service detection**: backdoor/DB/container/cleartext/admin from open-port+banner+exposure.
- [ ] **Trust tier + risk scoring** deterministic and explainable.
- **Run:** `manager/backend/.venv/bin/python -m pytest detection_engine/tests -q` (21 test files).

## C5. Scanner Accuracy Corpus  (`probe/tests/fixtures/accuracy_corpus/`)
- [ ] **Precision/recall/FP** scored on every labeled corpus per change (`scanner-accuracy.yml`). 🚦
- [ ] **Provenance honoured**: only independently-labeled corpora (nmap/second-vantage/manual) count as *accuracy* evidence; `self_regression` = drift-only, and the gate says which is which.
- [ ] Thresholds breach → **build fails**.
- [ ] New scanners land with a labeled corpus, not just self-regression.

## C6. Deployment / Infrastructure  (`docker-compose.yml`, `deploy/`, `install.sh`, `Makefile`)
- [ ] **`make doctor`** preflight passes; insecure prod defaults blocked.
- [ ] **Compose stack** boots: postgres, redis, neo4j, migrate, api, worker, probe, frontend, caddy edge, ollama(+model-init).
- [ ] **Caddy auto-TLS** serves the edge on :80/:443; the Windows agent defaults to the Caddy edge.
- [ ] **Install/upgrade/rollback/DR** (Part B6/B7).
- [ ] **Container security**: Trivy scan, non-root, minimal base, pinned images.
- [ ] **IaC / compose lint** (`docker compose config`, hadolint on Dockerfiles).

## C7. Data pipeline & durability
- [ ] **Chunked results**: per-host chunk buffer (migration 0041) commits incrementally; reaper rescues orphans.
- [ ] **Two-phase ports**: assess-fast-set then budgeted tail behaves under scale.
- [ ] **Partial-chunk commit** correctness (`test_partial_chunk_commits`).
- [ ] **Result-scope rejection** path is observable, not a silent stall (`vedha-run-scoped-fact-422`).
- [ ] **Scale walls** documented and asserted (deep ~14–66 hosts, standard ~570, upload ~1,000).

## C8. AI / LLM seam  (`app/ai*`, `agent_advisor`, `ai_report`)
- [ ] **Provider-agnostic** body; pinned to the intended Claude model; auto-detect pinned so provider doesn't drift (`vedha-ai-pipeline`).
- [ ] **Prompt-injection hardening**: untrusted scan/context data can't hijack instructions or exfiltrate.
- [ ] **Structured outputs** validated; malformed model output handled, not crashed.
- [ ] **Portal AI chat** stays security-scoped and labels unverified content (`vedha-portal-assistant-timestamps`).
- [ ] **Cost/latency budgets** and graceful fallback when the AI service is down.
- [ ] **Evals** for report-generation quality (golden prompts, regression on prompt changes).

---

# PART D — DOMAIN-CRITICAL SUITES (unique to a VA platform — never let these rot)

## D1. Scope-Safety Gate  🚦 (hard release blocker)
> Failure mode is not "wrong answer" — it's "scanned something you weren't authorised to, inside a
> client's network." Wire these into `make test-safety`, run on **every** commit.

- [ ] Out-of-scope target → refused / no scan work.
- [ ] Excluded ranges → dropped **before any packet**.
- [ ] OT profile → refuses active use-cases, exit 2, **no override**.
- [ ] Manager job with no authoritative scope → refused.
- [ ] Forged / unsigned dispatch on the fallback path → refused (Ed25519).
- [ ] Console dry-run / preview → **zero packets** (assert no `send`/`connect`).
- [ ] IPv6 scope enforcement (Gate 1b) — scope respected on the v6 path too.

## D2. Accuracy Gate  🚦
- [ ] Precision/recall thresholds enforced by `scanner-accuracy.yml` on every relevant change.
- [ ] At least one **independently-labeled** corpus present (gate warns if only self_regression).
- [ ] The "evidence-backed, anti-false-positive" claim is *measured*, not asserted.

## D3. Multi-Tenancy & Audience Isolation  🚦
- [ ] Portal token (`aud=client`) verified on every portal route; operator token rejected on portal login and vice-versa (`Role client is not permitted`).
- [ ] `aud` claim survives refresh (not dropped) — `vedha-portal-audience-boundary`.
- [ ] Engagement A's data is unreachable from engagement B by any endpoint (IDOR sweep).
- [ ] Console-parity delegation keeps the engagement pin — portal can't widen its own scope.

## D4. Probe Integrity / IP Protection  🧪 🚦
- [ ] **Seal parity**: Nuitka-sealed binary == source behaviour (`probe-seal-parity.yml`).
- [ ] Ed25519-signed, host-locked license verified at start; tampered/relocated license refused.
- [ ] `seal-probe.sh` one-command build reproduces a valid sealed artifact.
- [ ] No source/IP leakage in the shipped artifact (strings/secret scan of the binary).

## D5. Fact-Contract / Ingest Gate  🔁
- [ ] `ingest._validate` rejections are **recorded** in `DetectionRun.stats["ingest"]`, never silent (the real detection SPOF — `vedha-ingest-gate-silent-drop`).
- [ ] Fact-contract corpus captured from real scanners keeps rules and payloads in lockstep.
- [ ] A payload that fails validation surfaces as a visible run gap, not "no findings."

---

# PART E — Test process & governance

## E1. Entry / exit criteria (per release)
- **Entry:** green baseline (§0), migrations apply, `make doctor` clean.
- **Exit (Definition of Done):**
  - [ ] All 🔁 gates green (lint, types, unit, integration, contract, safety, accuracy, secrets, SAST, SCA).
  - [ ] Domain-critical suites (Part D) green — **no exceptions**.
  - [ ] Non-functional budgets met (perf, a11y) or an explicit, signed waiver exists.
  - [ ] New/changed code has tests; bug fixes have failing-first regression tests.
  - [ ] Docs updated (`docs/`), CHANGELOG bumped, `VERSION` bumped.
  - [ ] Manual E2E / lab pass for probe-affecting or scope-affecting changes.

## E2. CI/CD gate map

| Trigger | Runs |
|---|---|
| **Every PR / commit** 🔁 | lint + types + unit (backend/frontend/probe) + integration + contract + **safety gate** + secret-scan + SAST + SCA |
| **Probe path PRs** | `agent-ci.yml` cross-OS matrix + doctor smoke + SBOM |
| **main push (scanner paths)** | `scanner-accuracy.yml` (accuracy gate) + `probe-seal-parity.yml` |
| **Nightly** 🌙 | full regression + smoke against fixture host + DAST + perf baselines + a11y + mutation (rotating) |
| **Pre-release (probe image)** 🧪 | full smoke + safety gate + seal parity + a slice of the two-machine lab + container scan |
| **Pre-release (manager)** 🧪 | full backend + detection + attack-path + migration up/down + DR restore drill |

## E3. Coverage & quality targets
- [ ] Core modules ≥ 80 % line coverage; domain-critical modules (scope, detection, crypto, auth) higher + mutation-tested.
- [ ] Zero known-flaky tests in required gates.
- [ ] Every open known-gap (§A7) has a tracking regression test.

## E4. Defect severity & triage
- **S1 (blocker):** any scope-safety failure, tenant data leak, auth bypass, data corruption, or accuracy-gate breach → stop the line.
- **S2 (critical):** functional break in a core flow, migration failure, perf budget blown > 2×.
- **S3 (major) / S4 (minor):** logged, scheduled, not release-blocking.
- [ ] Every S1/S2 gets a failing-first regression test before the fix merges.

## E5. Traceability
- [ ] A matrix links **requirement / user story → test(s) → gate**. New features add their row (extend `TESTING_PLAN.md §3`).
- [ ] Security requirements trace to ASVS 5.0 control IDs.

## E6. Roles & cadence
- [ ] Devs own unit/integration/contract + failing-first regressions.
- [ ] QA owns E2E, exploratory, UAT coordination, and the lab.
- [ ] Security owns SAST/DAST/SCA config, pentest cadence, and the Part D gates.
- [ ] Release owner runs the E1 checklist and signs off.

---

## Appendix A — Tool quick-install reference

```bash
# Python (backend + probe): put dev tools in the venvs
pip install pytest pytest-asyncio pytest-cov hypothesis ruff mypy \
            bandit pip-audit semgrep schemathesis mutmut memray py-spy

# Frontend
npm i -D vitest @vitest/coverage-v8 @playwright/test @axe-core/playwright \
         eslint prettier stryker

# Security / supply chain (host tools)
brew install trivy grype gitleaks        # or the platform equivalent
# OWASP ZAP: docker run ghcr.io/zaproxy/zaproxy zap-baseline.py -t <URL>

# Load testing
brew install k6                           # or: docker run grafana/k6 run script.js
pip install locust
```

## Appendix B — Command cheat sheet

```bash
# Inner loop
make test                                                    # manager backend
cd probe && .venv/bin/python -m pytest -q                    # probe (163 files)
manager/backend/.venv/bin/python -m pytest detection_engine/tests -q
cd manager/frontend && npm test                              # frontend (tsx --test)

# Gates
cd probe && .venv/bin/python -m pytest tests/test_scope_validator.py -q   # safety
# scanner-accuracy + seal-parity run in CI (main push, probe paths)

# Static & security
ruff check . && mypy .                                       # backend/probe
cd manager/frontend && npx tsc --noEmit && npx eslint .
semgrep --config auto . ; bandit -r manager probe
pip-audit ; (cd manager/frontend && npm audit)
gitleaks detect --source .
trivy image <probe-image> ; trivy image <manager-image>

# Dynamic / load
docker run --rm ghcr.io/zaproxy/zaproxy zap-baseline.py -t http://localhost:<port>
k6 run perf/api-load.js

# Stack
make doctor && make up && make ps && make logs
alembic upgrade head && alembic downgrade -1                 # migration smoke

# E2E
cd manager/frontend && npx playwright test
```

## Appendix C — References & standards
- **OWASP ASVS 5.0** (May 2025) — application security verification — <https://owasp.org/projects/asvs>
- **OWASP WSTG** (4.2, v5 in progress) — web security testing procedures — <https://wstg.owasp.org/>
- **OWASP Top 10**, **API Security Top 10**, **LLM Top 10** — coverage checklists — <https://owasp.org/>
- **OWASP Dependency-Check / Free-for-OSS tools** — <https://owasp.org/www-community/Free_for_Open_Source_Application_Security_Tools>
- **CWE** (weakness taxonomy), **MITRE ATT&CK** (technique mapping), **CISA KEV** + **EPSS** (exploitability).
- **k6** load testing — <https://k6.io/> · **Locust** — <https://locust.io/> · **Playwright** — <https://playwright.dev/> · **Pact** (contract) — <https://pact.io/> · **Schemathesis** (OpenAPI fuzz) · **Semgrep** · **Trivy**.
- **ISTQB** glossary/foundation for test-type definitions; **ISO/IEC 25010** for the non-functional quality model.

## Appendix D — Glossary (quick)
- **SAST/DAST/SCA** — static / dynamic / software-composition analysis.
- **Safety gate** — the scope-enforcement suite; a Vedha-specific hard blocker (Part D §1).
- **Accuracy gate** — precision/recall corpus scoring (Part D §2).
- **Provenance** — how a corpus was labeled; only independent labels prove accuracy.
- **Seal parity** — sealed Nuitka binary behaves identically to source (Part D §4).
- **Fact contract** — the probe-facts ⟷ manager-ingest schema agreement (Part A4 / D5).
- **BFF** — the Next.js backend-for-frontend proxy routes (`app/api/**/route.ts`).

---

*Maintainers: extend this file when a new test class or component appears. Keep §0's baseline
current, and keep every Part D gate green — those are the ones that protect clients and the product.*
