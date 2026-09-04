# Learnings

## 2026-08-11

### Coverage ledger
**What:** A per-`DetectionRun` record of `(asset, service_identity, scanner)` tuples that were *provably* re-scanned (`scanner_runs[].status == completed`), derived from probe telemetry.
**Why:** Auto-resolution requires proof that we *looked* at an asset/service and didn't see the finding — not just that the finding wasn't in the result. Degraded/skipped/failed scanners must not count as coverage.

### Coverage-gated auto-resolution with confirmation window
**What:** A finding is auto-closed only when its asset/service appears in the coverage ledger AND the finding is absent for N consecutive qualifying runs (N varies by severity: default 1 for low/medium, 2 for critical/KEV).
**Why:** The existing `first_seen`/`last_seen`/`detection_run_id` infrastructure surfaced "resolution candidates" but deliberately never auto-closed them; partial/degraded scans made absence untrustworthy. The confirmation window absorbs flaky or partial scans before committing to `remediated`.

### DB-version guard on auto-resolution
**What:** Before treating a finding's absence as a remediation signal, compare the run's `vuln_db_version` against the `detected_db_version` stamped on the finding. A mismatch means the vuln DB changed, not that the host was patched.
**Why:** A pinned-DB refresh can drop or rename CVE matches; without this guard, a DB update would appear as a mass-remediation wave on the dashboard.

### Regression detection on auto-resolved findings
**What:** If a finding already marked `remediated` is observed again in a later covered run, it is auto-reopened with a `reopened_count` increment and a `REGRESSION` badge.
**Why:** A vulnerability that came back after being closed is higher-urgency than a fresh one and must be surfaced distinctly rather than merged silently into open findings.

### Tiered verification (passive + active)
**What:** A two-tier FP-reduction approach: (1) passive — offline cross-corroboration of all asset facts using the LangGraph subgraph, confidence can only be maintained or lowered; (2) active — approval-gated, non-destructive validation job sent back to the probe (safe PoC / protocol handshake) for high-sev/KEV suspected findings.
**Why:** Version-matching alone produces false positives from backported fixes; a safe PoC that *fails* on a version match is the strongest possible FP signal (`contradicted` state), and a PoC that *succeeds* is the one legitimate path to upgrading a network-observed finding to `confirmed`.

### LangGraph verification/triage subgraph
**What:** A bounded `StateGraph` (`intake → corroborate → decide_escalation → [active_validation →] interpret → finalize`) with durable checkpoints and a human-in-the-loop interrupt at the approval gate; lives in `app/ai/verification_graph.py`, optional behind a settings flag.
**Why:** The active-validation escalation is a stateful, interruptible workflow (reason → request external job → wait → interpret result) — LangGraph's checkpoint/pause/resume maps 1:1 to this; direct-SDK tool-use loops don't give durable state-machine semantics across the async validation round-trip.

### Risk rank (composite priority)
**What:** A single 0–1000 score combining base CVSS severity, exploit likelihood (EPSS + KEV), verification state, confidence, asset criticality, and exposure (internet-facing, auth-enforced) — used as the default sort order on the findings dashboard.
**Why:** Raw severity alone over-ranks low-confidence inferred findings on hardened internal assets; the composite rank surfaces verified + exploitable + internet-exposed findings at the top while sinking `contradicted` / low-confidence ones.

## 2026-09-03

### PostgreSQL `bit(n)::numeric` cast incompatibility
**What:** PostgreSQL cannot cast `bit(n)` to `numeric` for any `n`; only `bit(n)` → integer is allowed, and only when `n ≤ 64`.
**Why:** Migration 0036's Crockford base32 backfill used `::bit(128)::numeric` to compute `uuid % 32**6`, which crashed on every PostgreSQL version. Fix: since `32**6 = 2**30` and `2**64 % 2**30 = 0`, only the lower 64 bits matter — replace with `::bit(64)::bigint & 1073741823`.

### BFF (Backend-for-Frontend) route pattern in Next.js
**What:** All API calls from the browser go through Next.js route handlers in `app/api/*/route.ts` that extract the bearer token and proxy to FastAPI; the browser never talks to FastAPI directly. Uses `withBackend()` wrapper from `lib/with-backend.ts`.
**Why:** Vedha's frontend has no auth logic of its own — FastAPI owns RBAC and tenant isolation, so the BFF is a thin token-forwarding proxy rather than a second auth system.

### Expandable finding cards with CVSS vector breakdown
**What:** A collapsible `<FindingCard>` component that shows severity badge + CVSS score when collapsed, and on expand renders the full CVSS vector parsed into per-metric tiles (AV, AC, PR, UI, S, C, I, A) with human-readable labels.
**Why:** The previous technical findings tab showed single-line description/impact/remediation; professional VAPT reports (NCC Group, Rapid7) always expose the raw CVSS vector and per-metric breakdown so clients can assess their specific environment.

### Tenant-scoped users router (FastAPI)
**What:** A new `GET /users` endpoint in `app/routers/users.py` that returns all non-client operator accounts scoped to the caller's `tenant_id`, with deactivate/activate soft-disable endpoints for admin role only.
**Why:** The Settings Team section needed to list and manage operator accounts; the User model existed but had no router, so the Settings page had no way to fetch the team.

### AI report generation workflow (polling pattern)
**What:** A "Generate Draft" button POSTs to a background job endpoint, then polls a status endpoint every 2.5 seconds using React Query's `refetchInterval` until `status === "complete"` or `"failed"`, then reveals the draft sections with per-section approve/reject controls.
**Why:** LLM report generation takes 10–60 seconds; blocking the UI is unacceptable, and the hallucination guard runs after generation, so the polling model maps cleanly onto the existing `ai_report.py` job queue.

---

## Expert map — all concepts to master

> These are the core concepts that appear throughout Vedha. Learn them in the order listed under each section.

---

## Python & FastAPI core

### `async` / `await` in Python
**What:** `async def` defines a coroutine; `await` suspends it until the awaited operation completes, returning control to the event loop so other coroutines can run. Never blocks the OS thread.
**Why:** Every FastAPI route, SQLAlchemy query, Redis call, and HTTP request in Vedha is async — blocking any one of them (e.g. `time.sleep`, bcrypt) stalls the entire server.

### `asyncio.gather`
**What:** Runs multiple coroutines concurrently in the same event loop and collects their results as a list. `await asyncio.gather(a(), b())` starts both without waiting for `a` to finish before starting `b`.
**Why:** Vedha uses `gather` to fan out scanner jobs, but sharing a single `AsyncSession` across gathered coroutines causes "session already in use" errors — each coroutine needs its own session.

### FastAPI router (`APIRouter`)
**What:** Groups related endpoints with a shared `prefix`, `tags`, and dependency defaults. Included in the app via `app.include_router(router)`.
**Why:** Every Vedha subsystem (findings, agents, users, detection) is its own router file so the codebase stays modular and main.py stays readable.

### FastAPI `Depends` and dependency injection
**What:** `Depends(fn)` tells FastAPI to call `fn` and inject its return value into the route. Used for database sessions, auth, RBAC, Redis connections.
**Why:** `DB = Annotated[AsyncSession, Depends(get_db)]` gives every route a fresh async DB session automatically; no manual session management per route.

### `Annotated` type hints (Python 3.11+)
**What:** `Annotated[T, metadata]` attaches extra information (like FastAPI's `Depends` or validators) to a type without changing runtime behavior. FastAPI reads the metadata to wire up injection.
**Why:** The pattern `current_user: Annotated[AuthUser, require_role(["admin"])]` combines "get the current user" and "check role" in one declaration — no manual guard code in the route body.

### Pydantic `BaseModel`
**What:** A class whose field types are validated at runtime when an instance is created. JSON bodies are automatically parsed into Pydantic models in FastAPI routes.
**Why:** Every request body, response schema, and internal data contract in Vedha is a Pydantic model — it catches bad input at the boundary before it touches the database.

### `model_config = {"from_attributes": True}`
**What:** Tells Pydantic v2 to read field values from object attributes (e.g. SQLAlchemy ORM rows) instead of dictionary keys. Required when returning ORM objects directly as response models.
**Why:** Without this, `UserOut.model_validate(orm_row)` fails because SQLAlchemy rows are not dicts.

### SQLAlchemy `AsyncSession`
**What:** An async-capable database session. All queries must be `await`ed. Obtained via `async_sessionmaker` and used as a context manager (`async with session:`) or via FastAPI's `Depends`.
**Why:** Vedha's database is PostgreSQL over asyncpg; using the synchronous `Session` would block the event loop on every query.

### SQLAlchemy `select()` query style
**What:** `select(Model).where(Model.field == value)` builds a query object; `await session.execute(stmt)` runs it; `.scalars().all()` extracts the ORM objects.
**Why:** This is the async-compatible way to query — the older `session.query(Model)` API does not support async.

### SQLAlchemy `Mapped` + `mapped_column`
**What:** Type-annotated column declarations introduced in SQLAlchemy 2.0. `Mapped[str]` declares a non-nullable string column; `Mapped[str | None]` is nullable.
**Why:** Vedha models use these throughout (e.g. `User`, `Finding`) — they generate the correct DDL and provide IDE type checking without separate `Column()` definitions.

### SQLAlchemy `relationship` and `lazy="noload"`
**What:** Declares a link between two ORM models. `lazy="noload"` means the related object is never automatically fetched — you must explicitly join or use `selectinload()` when you need it.
**Why:** Accidental lazy loads in async context raise `MissingGreenlet` errors; `noload` is the safe default and forces explicit intent.

### Alembic migration (`revision`, `upgrade`, `downgrade`)
**What:** Each migration is a Python file with a `revision` ID, `down_revision` pointer, and `upgrade()`/`downgrade()` functions using `op.*` helpers (`add_column`, `create_index`, `execute`).
**Why:** Vedha's schema evolves through 36+ migrations; Alembic tracks which revision the database is at and applies only the missing ones in order.

### Alembic `op.execute` for data backfills
**What:** Runs raw SQL inside a migration, useful for computing and writing data that pure DDL can't express (e.g. generating Crockford base32 references from UUIDs).
**Why:** Migration 0036 needed to compute SCN job references from existing UUID rows — the logic can't be expressed in DDL alone so `op.execute` was used with a CTE.

### PostgreSQL CTE (`WITH ... AS (...)`)
**What:** A Common Table Expression names an intermediate query result that can be referenced in the main query. Used for clarity and to avoid repeating a subquery.
**Why:** Migration 0036 computed the base32 suffix in a `WITH encoded AS (SELECT ...)` CTE, then joined it back to `UPDATE scan_jobs SET reference = encoded.reference`.

### PostgreSQL `generate_series`
**What:** A set-returning function: `generate_series(0, 5)` produces rows `0,1,2,3,4,5`. Used to expand a single row into N rows for aggregation.
**Why:** The base32 backfill in migration 0036 cross-joined each scan job with `generate_series(0, 5)` to compute one digit per index, then `string_agg`'d them back into the 6-character suffix.

### PostgreSQL UUID primary keys
**What:** `UUID(as_uuid=True)` stores a 128-bit universally unique identifier as a native PG `uuid` type. Generated server-side with `gen_random_uuid()`.
**Why:** Vedha uses UUIDs for all primary and foreign keys to avoid enumerable IDs and to support cross-service ID generation without a central counter.

### PostgreSQL `Enum` type
**What:** A named server-side type (e.g. `userrole`) that restricts a column to a fixed set of strings. SQLAlchemy maps it to a Python `enum.Enum`.
**Why:** `UserRole`, `FindingSeverity`, `ScanJobStatus`, etc. are all PG enums — invalid values are rejected at the DB level, not just the application level.

### Soft delete (`is_active` flag)
**What:** Instead of `DELETE`-ing a row, set a boolean `is_active = False`. The record stays in the database (preserving audit trail and foreign key integrity) but is excluded from normal queries.
**Why:** Deactivating a user account in Vedha must keep their audit history and finding authorship intact — a hard delete would break foreign key references and erase context.

### `TimestampMixin` (created_at / updated_at)
**What:** A SQLAlchemy mixin that adds `created_at` (server default `now()`) and `updated_at` (auto-updated on flush) to every model that inherits it.
**Why:** Every Vedha model inherits `TimestampMixin` so filtering by recency, auditing timelines, and reporting "discovered at" are always available without per-model boilerplate.

### `structlog` structured logging
**What:** Logs are emitted as key-value pairs (`log.info("event_name", key=value, ...)`) instead of plain strings. In production they are JSON; in development they are colour-rendered.
**Why:** JSON logs are machine-parseable by log aggregators (CloudWatch, Loki, Datadog) — searching for `engagement_id=X` is instant; searching through concatenated strings is not.

### FastAPI `BackgroundTasks`
**What:** `background_tasks.add_task(fn, arg)` schedules `fn` to run after the HTTP response is sent, without blocking the request. The client gets a 202 immediately.
**Why:** AI report generation, scan job dispatch, and notification emails run as background tasks so the HTTP response is instant and the heavy work runs asynchronously.

### `bcrypt` password hashing
**What:** A deliberately slow one-way hash algorithm. The "cost factor" controls how many rounds of computation run — higher cost means longer to hash, making brute force impractical.
**Why:** Vedha originally called bcrypt inside an async route, which blocked the event loop for ~100 ms per login. Fix: run bcrypt in a thread pool via `asyncio.to_thread`.

### JWT (JSON Web Token)
**What:** A signed, self-contained token encoding claims (user ID, tenant ID, role, expiry). The server signs it; clients present it in the `Authorization: Bearer` header. No session state on the server.
**Why:** Vedha's auth issues short-lived access tokens and longer-lived refresh tokens. The access token is verified on every request by `TenantIsolationMiddleware` without hitting the database.

### Personal Access Token (PAT)
**What:** A long-lived, opaque token issued to automation identities (probe agents, CI pipelines). Stored hashed; the prefix (first N chars) is shown for identification without revealing the full token.
**Why:** Probe agents run unattended — they need a credential that isn't tied to an interactive user session. PATs have explicit scopes and expiry and can be revoked individually.

### Tenant isolation middleware
**What:** A Starlette middleware that runs before every route, validates the JWT/PAT, and injects `tenant_id`, `user_id`, `role` into `request.state`. Routes read these via `get_current_user`.
**Why:** Multi-tenant SaaS must never leak one tenant's data to another. Centralising the check in middleware means no route can accidentally skip it.

### RBAC (`require_role`)
**What:** `require_role(["admin", "manager"])` returns a FastAPI dependency that raises 403 if the caller's role is not in the allowed list. Composed with `Annotated` in route signatures.
**Why:** Vedha has 6 roles (admin, manager, tester, analyst, auditor, client) with different permissions — e.g. only admin can deactivate users, only client role is limited to one engagement.

### Redis pub/sub for WebSocket backplane
**What:** When multiple uvicorn workers each hold their own WebSocket connections, a worker receiving a scan result must forward it to whichever worker holds the probe's socket. Redis pub/sub is used as the shared message bus.
**Why:** Without this, a result sent to worker A would never reach the browser connected to worker B. The backplane runs as a background asyncio task per worker.

### `asynccontextmanager` lifespan (FastAPI)
**What:** `@asynccontextmanager async def lifespan(app):` replaces `on_startup`/`on_shutdown` hooks. Code before `yield` runs at startup; code after `yield` runs at shutdown.
**Why:** Vedha's lifespan starts the Redis backplane task, runs startup diagnostics, and cancels the task cleanly on shutdown — all in one place with proper `try/finally` cleanup.

---

## Security & VAPT concepts

### CVSS (Common Vulnerability Scoring System)
**What:** A standardised 0–10 numeric score for vulnerability severity. Composed of a vector string like `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` encoding 8 base metrics.
**Why:** Vedha displays CVSS scores and parses vector strings into per-metric breakdowns (AV=Network, PR=None, etc.) so clients can understand why a score is high and assess compensating controls.

### CVSS metrics at a glance
**What:** AV=Attack Vector (N/A/L/P), AC=Attack Complexity (L/H), PR=Privileges Required (N/L/H), UI=User Interaction (N/R), S=Scope (U/C), C/I/A=Confidentiality/Integrity/Availability impact (N/L/H).
**Why:** Knowing what each letter means lets you read a vector string and immediately know "this is network-exploitable with no auth" (AV:N/PR:N) vs "requires local access" (AV:L).

### MITRE ATT&CK framework
**What:** A structured knowledge base of adversary tactics (the *why*: Initial Access, Persistence, Exfiltration…) and techniques (the *how*: T1059, T1078…). Techniques have sub-techniques (T1059.001).
**Why:** Vedha tags every posture finding with ATT&CK technique IDs so operators can map "what the attacker can do" from a vulnerability to the kill chain phase it enables.

### CWE (Common Weakness Enumeration)
**What:** A catalogue of software and hardware weakness *types* (e.g. CWE-89 SQL Injection, CWE-79 XSS, CWE-306 Missing Authentication). Not the same as a CVE (a specific vulnerability instance).
**Why:** Vedha attaches CWE IDs to findings so developers can look up the class of defect and its general mitigations, not just the specific CVE patch.

### CVE (Common Vulnerabilities and Exposures)
**What:** A unique identifier (e.g. CVE-2021-44228) for a specific publicly disclosed vulnerability in a specific product version. Maintained in the NVD (National Vulnerability Database).
**Why:** Vedha's detection engine maps CPE data from scanners to CVEs via NVD lookups, so a discovered service version becomes a list of known exploitable vulnerabilities.

### CPE (Common Platform Enumeration)
**What:** A structured naming scheme for software, hardware, and operating systems: `cpe:2.3:a:vendor:product:version:*:*:*:*:*:*:*`. Used as the lookup key into the NVD CVE database.
**Why:** The probe's CPE normaliser converts raw banner strings ("Apache httpd 2.4.51") into a CPE URI, which the manager then queries against the CVE database to find applicable vulnerabilities.

### CISA KEV (Known Exploited Vulnerabilities)
**What:** CISA's curated list of CVEs with confirmed real-world exploitation. Published as a JSON feed, updated frequently. Has federal remediation deadlines (FCEB agencies: 2 weeks for critical KEV).
**Why:** Vedha joins KEV data onto POSTURE-track findings to escalate their risk score — a KEV finding on an internet-facing host is an immediate P0 regardless of base CVSS score.

### EPSS (Exploit Prediction Scoring System)
**What:** A 0–1 probability score published daily by FIRST.org predicting the likelihood that a CVE will be exploited in the next 30 days, based on PoC activity, social media, dark web signals.
**Why:** A CVE with CVSS 9.8 but EPSS 0.01 is theoretically severe but practically unlikely to be attacked soon; EPSS helps Vedha prioritise the small fraction of CVEs that will actually be weaponised.

### Port scanning — TCP SYN vs connect
**What:** SYN scan sends a SYN packet and reads the response (SYN-ACK = open, RST = closed) without completing the handshake — fast and stealthy, requires raw socket (root). Connect scan completes the full TCP handshake — slower but works without root.
**Why:** Vedha's probe uses SYN scan for speed in network sweeps, but falls back to connect scan when running without elevated privileges.

### Banner grabbing
**What:** After TCP connect, read the first bytes the server sends before sending anything. Most services (SSH, SMTP, FTP, HTTP) announce their software and version in the banner.
**Why:** Vedha's `service_banner` scanner grabs banners to identify service type and version, which feeds CPE normalisation and CVE matching.

### Service fingerprinting patterns
**What:** Matching banner content against a library of regex patterns to identify the service (e.g. `SSH-2.0-OpenSSH_8.2` → OpenSSH 8.2). CPE is then synthesised from vendor/product/version tokens.
**Why:** The same port (e.g. 443) can run HTTPS, MQTT over TLS, or custom protocols — regex fingerprinting distinguishes them so detection rules fire on the right service.

### SNMP (Simple Network Management Protocol)
**What:** A UDP protocol (port 161) for network device management and monitoring. Community strings act as passwords — `public` / `private` are common weak defaults.
**Why:** Vedha's posture rules flag SNMP with default community strings as a high-severity exposure because they allow full device enumeration and sometimes configuration changes.

### RDP (Remote Desktop Protocol)
**What:** Microsoft's remote desktop protocol on port 3389 (TCP). Historically a major attack surface (BlueKeep CVE-2019-0708, PrintNightmare path).
**Why:** RDP required two probes in Vedha — a TCP port check (gate 1) AND a credential/auth banner check (gate 2) — because port open alone doesn't confirm an exploitable service.

### Crockford Base32 encoding
**What:** A base-32 alphabet (`0-9A-Z` minus I, L, O, U) designed for human readability — no ambiguous characters. Encodes arbitrary bytes as a fixed-length string.
**Why:** Vedha's scan job references (SCN-YYMMDD-XXXXXX) use Crockford base32 for the 6-char suffix so references can be read over the phone without confusing `0` with `O` or `1` with `I`.

### Network CIDR notation
**What:** `192.168.1.0/24` means the first 24 bits are the network address, giving 256 host addresses (.0 to .255). `/16` gives 65536 hosts, `/32` is a single host.
**Why:** Vedha's engagement scope is stored as CIDR ranges; the probe iterates hosts within the CIDR for discovery, and findings are scoped to IPs within the authorised range.

### VAPT methodology (black / grey / white box)
**What:** Black box = no prior knowledge (attacker perspective). Grey box = partial knowledge (credentials but no source). White box = full access (source code, configs). Vedha is primarily grey/white box network VA.
**Why:** Understanding the box type determines what scanner outputs are trustworthy — a white-box scan can correlate configuration files; a black-box scan relies only on network-visible evidence.

### MITRE ATT&CK tactics vs techniques
**What:** Tactics are goal categories (14 total: Reconnaissance, Resource Development, Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, C2, Exfiltration, Impact). Techniques are specific methods within a tactic.
**Why:** When tagging a finding, Vedha maps it to a technique ID (T1xxxxx) not just a tactic, so the ATT&CK navigator heatmap shows exactly which techniques the attacker could use.

---

## Frontend — React & Next.js

### Next.js App Router vs Pages Router
**What:** App Router uses the `app/` directory; every file is a Server Component by default. Add `"use client"` at the top to opt into the browser runtime. Pages Router (old) uses `pages/` directory — everything was client-side.
**Why:** Vedha uses App Router (`app/` directory). Most pages are `"use client"` because they need React state, browser APIs (clipboard, `window.print`), and React Query hooks.

### Server Component vs Client Component
**What:** Server Components run only on the server — no hooks, no browser APIs, no state. Client Components (`"use client"`) render on the server first then hydrate in the browser — they can use hooks and event handlers.
**Why:** Vedha's pages are client components because they fetch data dynamically via React Query hooks. Layout wrappers (`PageShell`) can be server components since they have no interactivity.

### React Query `useQuery`
**What:** `useQuery({ queryKey, queryFn })` fetches data, caches it by `queryKey`, and exposes `{ data, isLoading, error, refetch }`. Automatic refetch on focus, stale time, and retry logic are built in.
**Why:** Every data-fetching call in Vedha (findings, engagements, agents) goes through `useQuery` so the UI is always in sync with the server and loading/error states are handled uniformly.

### React Query `queryKey`
**What:** An array that uniquely identifies a cached query: `["findings", engagementId]`. Changing any element invalidates the cache and triggers a refetch. Must include all variables the query depends on.
**Why:** `["report-findings", engagementId]` ensures that switching engagements triggers a fresh fetch — without the ID in the key, all engagements would share the same cached result.

### React Query `useMutation`
**What:** `useMutation({ mutationFn })` wraps a write operation (POST/PUT/DELETE). Returns `{ mutate, isPending, isError }`. Call `queryClient.invalidateQueries` in `onSuccess` to refresh dependent queries.
**Why:** Creating a PAT, deactivating a user, and revoking a token all use `useMutation` — on success they invalidate the relevant query so the list updates without a page refresh.

### React Query `refetchInterval`
**What:** A number (milliseconds) or a function returning a number/false. When set, `useQuery` polls the endpoint on that interval. Return `false` to stop polling (e.g. when a job is complete).
**Why:** The AI report status query polls every 2.5 s while the job is running and stops when `status === "complete"` — `refetchInterval: (query) => query.state.data?.status === "complete" ? false : 2500`.

### `useCallback` hook
**What:** Returns a memoised version of a callback function — only recreates it when its dependency array changes. Prevents child components from re-rendering because a new function reference was passed as a prop.
**Why:** The `CopyButton`'s click handler is wrapped in `useCallback` so it isn't recreated on every parent render — important when buttons appear in long lists.

### `useMemo` hook
**What:** Memoises the result of an expensive computation — only re-runs when dependencies change. Use for derived data: filtering, grouping, sorting.
**Why:** The MITRE technique map in the Coverage tab is computed from all findings with `useMemo` so it isn't recomputed on every keystroke or state update that doesn't affect the findings array.

### CSS custom properties (design tokens)
**What:** `--accent: #1D4ED8` declares a variable; `color: var(--accent)` reads it. Can be overridden in a child selector or a `:root` with `prefers-color-scheme`.
**Why:** Every colour, radius, shadow, and spacing value in Vedha is a token (e.g. `--sev-critical-color`, `--bg-panel`, `--font-mono`). Changing a token updates the entire UI — no find-and-replace.

### CSS `color-mix(in srgb, ...)`
**What:** `color-mix(in srgb, red 15%, transparent)` blends two colours in the sRGB colour space. Useful for generating tints and ghost backgrounds from a single token.
**Why:** Severity badge backgrounds in Vedha use `color-mix(in srgb, var(--sev-critical-color) 12%, transparent)` so the tint automatically updates if the token value changes.

### `@media print` CSS
**What:** CSS rules inside `@media print` only apply when the page is sent to a printer or saved as PDF. Elements with `.no-print` are hidden.
**Why:** Vedha's report page has a "Print / Export PDF" button — `.no-print` hides the navigation, controls, and buttons so the printed output looks like a clean professional document.

### Next.js dynamic route params (`[param]`)
**What:** A folder named `[engagementId]` creates a dynamic route segment. The param is available in the route handler via `params.engagementId`.
**Why:** BFF routes like `app/api/ai/report/[engagementId]/status/[jobId]/route.ts` use nested dynamic segments to proxy engagement- and job-scoped requests to FastAPI.

### `lucide-react` icon library
**What:** A tree-shakeable React icon component library. Each icon is a named export: `import { Shield } from "lucide-react"`. Accepts `size`, `color`, `strokeWidth` props.
**Why:** Vedha uses lucide-react throughout the UI for semantic icons (Shield = security, Terminal = scanner output, Flame = active exploitation) — all sized consistently via the `size` prop.

### TypeScript `interface` vs `type`
**What:** Both define object shapes. `interface` is extensible (can be re-declared to merge). `type` is more flexible (can be a union, intersection, primitive alias). In practice, use `interface` for object shapes, `type` for everything else.
**Why:** Vedha uses `interface` for API response shapes (`interface Finding { ... }`) and `type` for union literals (`type ReportTab = "executive" | "technical" | ...`).

### TypeScript `Annotated` + generic components
**What:** `Record<string, string>` is an object with string keys and string values. `Array<T>` or `T[]` is a typed array. Generics like `fetchJson<Finding[]>` let one function work with any return type while keeping type safety.
**Why:** `fetchJson<FindingPage>(url)` returns a `FindingPage` — TypeScript knows the shape at the call site so autocomplete works and mismatched field names are caught at compile time.

---

## AI / LLM concepts

### Prompt engineering — system vs user message
**What:** The *system* message sets the model's persona, output format, and rules that must always apply. The *user* message is the per-request instruction. Keep constraints in the system message so they aren't accidentally overridden.
**Why:** Vedha's LLM report generator has a strict system message ("only use evidence already in the finding, never invent CVE IDs") to prevent hallucination — moving those constraints to user messages would make them optional.

### Hallucination guard
**What:** A post-generation validation step that checks LLM output against the input facts — e.g. verifying that every CVE ID mentioned in the output appears in the finding's evidence, and that no host name was invented.
**Why:** LLMs can confidently generate plausible but false CVE IDs and CVSS scores. Vedha's `HallucinationGuard` rejects output that contains IDs not in the source facts, preventing false evidence in client reports.

### Structured output (JSON mode)
**What:** Asking the model to respond with valid JSON matching a specific schema, either via a system-prompt instruction or a provider's native `response_format: {type: "json_object"}` parameter.
**Why:** Vedha's remediation planner uses structured output to get `{ steps: [...], priority: "...", estimated_effort: "..." }` — parsing free-form prose for these fields would be fragile.

### Context window and token budget
**What:** LLMs have a fixed maximum input+output length measured in tokens (~¾ of a word each). Exceeding the context window causes truncation or errors. Larger windows cost more.
**Why:** A full Vedha engagement might have 200 findings — naively passing all of them would exceed the context window. The report generator passes a summary + top N findings, not the full set.

### Temperature in LLM calls
**What:** A 0–2 parameter controlling randomness. 0 = deterministic (always picks the most likely token). Higher values produce more varied, creative, but less predictable output.
**Why:** Vedha's executive summary generator uses a low temperature (~0.3) for factual, consistent output — you don't want a different risk assessment every time you regenerate.

### `httpx` async HTTP client
**What:** An async-capable Python HTTP library with a similar API to `requests`. Used with `async with httpx.AsyncClient() as client: await client.post(...)`.
**Why:** Vedha's LLM service uses `httpx` to call Ollama, OpenRouter, and Anthropic APIs without blocking the event loop — `requests` would block and stall the entire FastAPI server.

### Multi-provider LLM routing
**What:** An abstraction layer that accepts a `provider` setting (ollama/openrouter/anthropic) and routes the same prompt to the correct API endpoint + authentication. Provider-specific differences (model names, auth headers, JSON shapes) are hidden behind the interface.
**Why:** Vedha supports three LLM providers so operators can choose between local (Ollama, no data egress), free cloud (OpenRouter), and commercial (Anthropic) — the detection and report code doesn't need to know which is active.

### LangGraph `StateGraph`
**What:** A directed graph where nodes are Python functions and edges define control flow. State is a typed dictionary passed between nodes. Supports conditional edges, loops, and human-in-the-loop interrupts via checkpoints.
**Why:** The verification subgraph (`intake → corroborate → decide → validate → finalize`) is a stateful multi-step workflow that may pause waiting for a human approval — LangGraph's checkpoint/resume handles this without manual state machines.

### RAG (Retrieval-Augmented Generation)
**What:** Before calling the LLM, retrieve relevant context from a vector database or document store and include it in the prompt. The model answers based on retrieved facts, not just its training data.
**Why:** Vedha's customer AI chat uses a form of RAG — it fetches the engagement's findings and passes them as context so the model answers questions about *this specific engagement*, not generic security advice.

### Human-in-the-loop (HITL) in AI workflows
**What:** An interrupt point in an AI pipeline where execution pauses until a human approves, rejects, or modifies the proposed action. The checkpoint saves state so the workflow resumes exactly where it paused.
**Why:** Vedha's active-validation step (sending a PoC probe back to the client network) requires human approval before execution — accidental probes outside authorised scope would violate the engagement contract.

---

## Architecture & infrastructure

### Multi-tenant SaaS data model
**What:** Every table has a `tenant_id` foreign key. The middleware injects `tenant_id` from the token; every query adds `.where(Model.tenant_id == current_user.tenant_id)`. One database, logical separation per tenant.
**Why:** Vedha serves multiple security consultancies from one deployment. Without tenant scoping, firm A could read firm B's findings — a catastrophic data breach.

### Probe / Manager architecture
**What:** The *probe* is a lightweight Python binary that runs inside the client's network, performs scans, and ships JSON facts to the *manager* API. The manager detects vulnerabilities, stores findings, and serves the dashboard. No direct database access from the probe.
**Why:** Client networks are firewalled — the probe only needs outbound HTTPS to the manager. The manager never needs to reach into the client network. This boundary also protects the manager's DB credentials.

### WebSocket push (real-time scan updates)
**What:** The probe maintains a persistent WebSocket connection to the manager (`/ws/agent/{probe_id}`). The manager pushes scan job assignments down this channel and receives status updates up it.
**Why:** Polling for scan results introduces latency and load. WebSocket gives the probe immediate job dispatch and gives the dashboard real-time progress without polling.

### gzip request middleware
**What:** A Starlette middleware that detects `Content-Encoding: gzip` on incoming requests, decompresses the body before passing it to the route, and resets `Content-Length`. FastAPI doesn't do this by default.
**Why:** A full /24 network scan result can be several MB of JSON. Probes gzip payloads before sending — without the middleware, the compressed bytes reach the route as garbage and JSON parsing fails.

### Docker Compose multi-service setup
**What:** `docker-compose.yml` defines `manager`, `db`, `redis`, `migrate`, and `probe` services with shared networks, volume mounts, and `depends_on` ordering. `make aws-up` runs the full stack.
**Why:** Every Vedha dependency (PostgreSQL, Redis, the manager API) must start in the correct order with the correct environment. Docker Compose encodes this dependency graph declaratively.

### Alembic `async` engine setup
**What:** Alembic's default engine is synchronous. For async SQLAlchemy, you must configure `alembic.ini` with `asyncpg` driver and use `run_sync` inside the async connection context.
**Why:** Vedha's models use `AsyncSession` — running migrations with the sync engine against the same asyncpg database works, but the Alembic config must explicitly use the `async` engine runner.

### `asyncio.to_thread` for blocking operations
**What:** `await asyncio.to_thread(blocking_fn, arg)` runs `blocking_fn` in a separate OS thread so the event loop is not blocked. Use for CPU-bound or blocking I/O operations that have no async equivalent.
**Why:** `bcrypt.hashpw` is intentionally slow (blocking). Running it directly in an async route blocks the event loop for ~100ms per call, degrading all concurrent requests. `to_thread` isolates it.

### Connection pooling (`async_sessionmaker`)
**What:** SQLAlchemy's `async_sessionmaker` creates a pool of database connections reused across requests rather than opening a new connection per request. Configurable with `pool_size`, `max_overflow`, `pool_timeout`.
**Why:** Opening a new PostgreSQL connection per request adds ~5–50ms latency. The pool keeps N connections warm, making each query start instantly.

### Redis as a cache and pub/sub bus
**What:** Redis is an in-memory data store used in Vedha for two purposes: (1) caching hot query results, (2) pub/sub message passing between uvicorn workers for WebSocket dispatch.
**Why:** Multiple uvicorn workers each have their own in-memory state. A scan result arriving at worker-1 must reach the browser connected to worker-2 — Redis pub/sub is the shared message bus.

### `Enum` in Python (`str, enum.Enum`)
**What:** `class UserRole(str, enum.Enum): admin = "admin"` creates a string enum. Values compare equal to their plain string (`UserRole.admin == "admin"` is True). SQLAlchemy maps it to a PG Enum.
**Why:** Using enums instead of raw strings for roles, severities, and statuses means typos are caught at Python import time (AttributeError), not at runtime when a bad string reaches the database.

### `Annotated` dependency chaining (FastAPI pattern)
**What:** `AuthUser = Annotated[CurrentUser, Depends(get_current_user)]` creates a reusable alias. Then `Annotated[AuthUser, require_role(["admin"])]` adds another constraint — FastAPI flattens nested `Annotated` automatically.
**Why:** Every protected route in Vedha uses `current_user: Annotated[AuthUser, require_role([...])]` — one declaration provides auth + RBAC without duplicating the `Depends(get_current_user)` call.

### `@pytest.mark.asyncio` and async tests
**What:** `pytest-asyncio` lets you write `async def test_foo(): await something()`. Mark individual tests with `@pytest.mark.asyncio` or set `asyncio_mode = "auto"` in `pyproject.toml`.
**Why:** Vedha's backend tests use async SQLAlchemy sessions and async HTTP clients — synchronous test functions can't `await` them, so async test functions with pytest-asyncio are required.

### Environment variables and `pydantic-settings`
**What:** `pydantic-settings` reads environment variables into a typed Pydantic model. `class Settings(BaseSettings): DATABASE_URL: str` auto-reads `DATABASE_URL` from the environment or a `.env` file.
**Why:** All Vedha secrets (DB URL, JWT secret, API keys) are in `.env` — never hardcoded. `get_settings()` returns a cached `Settings` instance read once at startup.

### `uvicorn` ASGI server
**What:** The production-grade ASGI server that serves FastAPI. `uvicorn app.main:app --workers 4` runs 4 worker processes. Each worker has its own event loop.
**Why:** Multiple workers handle concurrent requests without GIL contention, but they share no in-memory state — hence Redis for shared state and pub/sub.

### `Fernet` symmetric encryption
**What:** `cryptography.fernet.Fernet` provides authenticated symmetric encryption. `Fernet(key).encrypt(plaintext)` returns a URL-safe base64 token; `decrypt` reverses it. The key must be kept secret.
**Why:** Vedha uses Fernet to store the client portal's temporary password encrypted at rest (`portal_password_enc`) so operators can re-reveal it without storing it in plaintext.
