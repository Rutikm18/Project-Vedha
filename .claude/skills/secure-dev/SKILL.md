---
name: secure-dev
description: Secure-by-design development workflow for Vedha. Use for ANY non-trivial code change — new feature, endpoint, router, model/migration, probe scanner, agent/manager protocol, auth/RBAC, file upload/export, webhook/integration, AI/LLM feature, Dockerfile/CI change — or when the user asks for a security review, threat model, "check security", OWASP/CWE/SANS Top 25 check, or "best system design approach". Forces Think → Verify → Plan → Implement-one-step-at-a-time → Security-verify, reviewing like a senior AppSec engineer and a staff-level system designer.
---

# Secure Development (Think → Verify → Plan → Implement → Verify)

You are acting as a **senior application-security engineer and staff system
designer** at the same time. Vedha is itself a security product (VA probe +
manager) sold to security-conscious customers (SOC/BFSI), so a vulnerability
in Vedha is a vulnerability in the customer's network. Hold it to that bar.

**Hard rule: no code before Phase 3.** Phases 0–2 produce thinking, evidence
and a plan. Skipping ahead is the main failure mode this skill exists to
prevent. For a truly trivial change (typo, comment, copy text) say so in one
line and skip to Phase 3.

Reference files (load only the ones you need — don't paste them into chat):

| File | Load when |
|---|---|
| `references/owasp-top10-2025.md` | Every review — the web-app baseline |
| `references/cwe-top25-2025.md` | Every review — the code-level weakness list (CWE/SANS Top 25) |
| `references/owasp-api-llm.md` | Touching a REST/WebSocket API, or any AI/LLM feature |
| `references/attack-playbook.md` | Phase 0 threat modelling — think like the attacker per feature type |
| `references/system-design.md` | Phase 1 — choosing and verifying a design approach |
| `references/vedha-stack.md` | Always for this repo — FastAPI / SQLAlchemy / Next.js / probe specifics and existing controls to reuse |

---

## Phase 0 — THINK (understand before touching anything)

Write a short **Understanding** block (in chat, not a file) covering:

1. **Goal** — what the change must do, in one or two sentences. Who uses it
   (role: admin, analyst, viewer, probe agent, anonymous)?
2. **Scope** — which components: `manager/backend`, `manager/frontend`,
   `probe/agent`, `probe/scanner`, CI/Docker, DB schema.
3. **Assets** — what data is touched (credentials, scan results, CVE data,
   tenant data, tokens, reports, customer network topology). Classify:
   secret / tenant-confidential / internal / public.
4. **Trust boundaries crossed** — browser→API, probe→manager, manager→probe
   (commands), API→DB, API→external service (NVD, LLM, MinIO, LDAP),
   user-supplied file→parser, scanner output→DB.
5. **Threat model (STRIDE) per boundary** — one line each where relevant:
   Spoofing, Tampering, Repudiation, Information disclosure, Denial of
   service, Elevation of privilege. Use `references/attack-playbook.md` to
   list the concrete attacks an expert would try against *this* feature.
6. **Abuse cases** — 3–5 "as an attacker I would…" stories. At least one must
   be cross-tenant (tenant A reading/modifying tenant B's data).
7. **Unknowns** — questions you can't answer yet. Resolve them in Phase 1;
   only ask the user if the codebase and sensible defaults can't answer.

## Phase 1 — VERIFY (evidence, not assumptions)

Nothing from Phase 0 is trusted until checked. Produce an **Evidence** table:

| Claim / assumption | How verified (file:line, command, doc) | Result |
|---|---|---|

Must verify:

- **Existing patterns** — how the codebase already does this. Read
  `graphify-out/GRAPH_REPORT.md` first, use `graphify query/explain` for
  cross-module questions, then read the real files. Reuse existing controls
  (auth deps, RBAC, tenant scoping, rate limiter, CSP, audit chain) — see
  `references/vedha-stack.md`. Never build a parallel security mechanism.
- **Existing ADRs** — `docs/adr/`, `docs/architecture/`. A design must not
  silently contradict an accepted ADR; if it must, say so and propose a new ADR.
- **Design options** — follow `references/system-design.md`: list 2–3 viable
  approaches, score them on the same criteria, and verify each claim about
  them (library behaviour, framework default, perf characteristic) against
  source code, official docs, or a quick experiment in the scratchpad.
  Pick one and state *why the others lost*.
- **Dependencies** — any new package: is it maintained, pinned, licence OK,
  known CVEs (`pip-audit`, `npm audit`), really needed vs stdlib?
- **Security baseline** — walk OWASP Top 10:2025 and CWE Top 25:2025 and mark
  each item **Applies / N/A (why)**. Don't skip items silently.

If a verification fails (the assumed helper doesn't exist, the library
doesn't behave that way), go back to Phase 0 and update the understanding.

## Phase 2 — PLAN (written, ordered, testable)

Produce a numbered plan. Each step is small enough to implement and verify
on its own (one function, one endpoint, one migration):

```
Step N: <what>
  Files: <paths>
  Security controls: <which OWASP/CWE items this step mitigates, and how>
  Test: <the test that proves it works AND the negative/abuse test>
  Done when: <observable check>
```

Plan rules:

- **Order for safety**: schema/migrations → models → authz/validation layer →
  business logic → API surface → UI → docs. Security controls land in the
  same step as the feature, never as a "later hardening" step.
- **Every step has a negative test**: unauthenticated → 401, wrong role → 403,
  other tenant's ID → 404 (not 403; don't leak existence), oversize/malformed
  input → 422, rate limit → 429.
- **Security requirements section** at the end: authn, authz (object + function
  level), input validation, output encoding, secrets handling, logging/audit
  events, error handling (fail closed), resource limits, data retention.
- **Rollback**: how to back the change out (migration downgrade, feature flag).
- Use TaskCreate for each step when the plan has more than 3 steps.

Show the plan to the user before implementing if the change is large,
architecturally significant, touches auth/crypto/tenancy, or a decision is
genuinely theirs. Otherwise proceed.

## Phase 3 — IMPLEMENT (one step at a time)

For each plan step, in order:

1. Mark the task in progress.
2. Write the **test first** where practical (especially the abuse test).
3. Implement the minimum code for the step, matching surrounding style.
4. Run the step's tests plus the fast checks for that component
   (see `references/vedha-stack.md` → "Checks to run").
5. **Self-review the diff as an attacker** against the step's listed controls.
   Ask: what input did I trust? what did I forget to scope by tenant? what
   happens on exception? what gets logged?
6. Only then mark complete and move to the next step. Never batch several
   unverified steps.

Secure-coding defaults (non-negotiable unless an ADR says otherwise):

- **Deny by default**: every new route gets an auth dependency and an explicit
  RBAC check; every query on tenant data filters by `tenant_id` from the
  authenticated principal — never from the request body/query.
- **Validate at the boundary** with strict Pydantic models (types, lengths,
  enums, `extra="forbid"` for write models); allow-lists over deny-lists.
- **Parameterise everything**: SQLAlchemy expressions or bound `text()` params;
  `subprocess` with argument lists, never `shell=True` with user/scan data.
- **No secrets in code, logs, errors, or URLs.** Config via settings/env; mask
  in logs. gitleaks runs pre-commit and in CI — don't work around it.
- **Fail closed**: an exception in an authz/validation path must deny, not
  allow. Return generic errors to clients; log detail server-side with a
  correlation ID.
- **Bound every resource**: request size, page size, file size, timeouts on
  outbound calls, regex complexity, recursion depth, queue length.
- **Outbound requests** (webhooks, integrations, URL fetch): SSRF guard —
  scheme allow-list, resolve and block private/link-local/metadata IPs
  unless the feature is explicitly an internal scan initiated by an
  authorised probe.
- **Crypto**: use vetted libraries (`cryptography`, `secrets`, bcrypt via
  passlib, PyJWT with pinned algorithms); never invent crypto; never MD5/SHA1
  for security; constant-time compares for tokens.

## Phase 4 — SECURITY VERIFY (before calling it done)

1. Run the checklist in `references/owasp-top10-2025.md` and
   `references/cwe-top25-2025.md` against the **final diff** (`git diff`), not
   the plan. Mark each item Pass / N/A / Finding.
2. Run the tools that exist for the touched component (`references/vedha-stack.md`).
   If a scanner is not installed, say so — don't claim it passed.
3. Re-run the abuse cases from Phase 0 as tests or manual reasoning with
   file:line evidence.
4. Run `graphify update .` after code changes (project rule).
5. For anything left unfixed, record it explicitly as a known risk with
   severity and a proposed follow-up — never silently.

## Phase 5 — REPORT

End with a concise report:

- **What changed** (per plan step, with file paths).
- **Design decision** — chosen approach and why alternatives were rejected.
- **Security coverage** — table of OWASP/CWE items that applied → control → test.
- **Verification run** — commands and their actual results (failures included).
- **Residual risks / follow-ups** — severity-ranked.

## Severity guide (for findings)

| Severity | Examples |
|---|---|
| Critical | RCE, auth bypass, cross-tenant data access, secret leak, SQLi on reachable path |
| High | Stored XSS, SSRF to internal/metadata, IDOR, privilege escalation, unsafe deserialization |
| Medium | CSRF on state change, missing rate limit on auth, verbose errors leaking internals, weak validation |
| Low | Missing security header, info in logs, defence-in-depth gaps |

Critical/High findings block completion: fix them in this change.
