# Vedha Project Status

As of **2026-10-03**. The integration branch has landed on `main`; the security, notification, API-key and AI-runtime work below is on `claude/adoring-maxwell-uz71b2`, awaiting merge. This is the single place for what is done, what is open, and what needs the owner.
Claude updates it at the end of every finished piece of work: a change-log row, then the sections above it.

## At a glance

**Production is stopped for a redeploy (1 Oct 2026, intentional).** On `main`, the code for automatic AI routing, customer reporting, customer plans, a responsive dashboard and one-command HTTPS is merged; what else blocks a fully working production system is configuration and API credit, not code.

| Area | State |
| --- | --- |
| `origin/main` | `58f1a5d`. The integration branch landed at `46623ae` (agent install, portal plan locks, report export fix, new logo, Technical Findings report, operator Deep scan, design system doc), followed by `make prod-diagnose`. **Not yet on it:** the commits on `claude/adoring-maxwell-uz71b2` (see *Done, waiting for merge*), which already contains `58f1a5d` |
| Production | [app.vedhasec.com](https://app.vedhasec.com) / [api.vedhasec.com](https://api.vedhasec.com) — **stopped for a redeploy on 1 Oct** (owner). Was healthy on 1.0.325 on 30 Sep |
| Tests | On `claude/adoring-maxwell-uz71b2` (3 Oct): backend 2,396 passed, 9 skipped · frontend 451 of 451 · probe 2,512 (not re-run, no probe change) · lint 0 errors · one Alembic head (`0057`) |
| AI providers | Anthropic: no API credit · OpenAI: key rejected on AWS · Gemini: works, but its key was not on the AWS server |
| Unmerged branches | `claude/adoring-maxwell-uz71b2` (ready to merge) · `codex/customer-portal-engagement-parity` (not merged: 52 conflicts, only its remediation workspace is missing, see [the assessment](planning/2026-10-03-branch-merge-assessment.md)) · `probe-standalone` (never merge) |

The things that matter most right now:

1. Merge `claude/adoring-maxwell-uz71b2` into `main`, then redeploy. `main` already has the report-export fix, agent install, plan locks and the new logo; the branch adds the security hardening, working API keys, real notification rules and the live AI chain in Settings.
2. Finish the production redeploy; attach an Elastic IP so the DNS record (`13.127.147.205`) stays valid across restarts.
3. Fix the AWS `.env` (Gemini key, OpenAI key, blank `LLM_PROVIDER`), then `make full`. This restores AI Brain and report generation.
4. Agent install in client environments (P0-3) is done and documented. To go live: create the release key, publish a release, and get `vedhasec.com` categorised by web filters (see *Needs you*).

## Done

Merged and pushed to `origin/main`, newest first.

| Shipped | Area | What | Ref |
| --- | --- | --- | --- |
| 3 Oct 2026 | Agent | Agent install in client environments (P0-3): the manager serves a signed agent, Fleet → Add agent issues single-use install tokens, access expiry is set from Fleet and enforced, on-prem bundles are encrypted (migrations 0052, 0053) | `46623ae` |
| 3 Oct 2026 | Portal | Plan locks: per customer, lock finding severities and portal features (POC vs licensed); one server-side guard; teaser rows and lock panels (migration 0054) | `46623ae` |
| 3 Oct 2026 | Reports / Brand | Report export fixed (the menu was clipped by the page header); Technical Findings report; new logo and favicon; design system doc | `46623ae` |
| 1 Oct 2026 | Scanner | Operator Scanner gets the single-asset Deep scan card (every TCP port on one IP); never charged to the customer's Deep allowance | `feat/operator-deep-scan` |
| 1 Oct 2026 | Reports | Complete customer security reporting: canonical report document, scan provenance (ported from the Codex branch, migrations renumbered to 0050 / 0051, no model picker) | `82492a7`, `b6a3b60` |
| 30 Sep 2026 | UI | Responsive dashboard and canonical reporting | `f70f392` |
| 29 Sep 2026 | Deploy | One-command HTTPS: `make tls DOMAIN=… EMAIL=…` and the `./setup-https.sh` wizard; production live on vedhasec.com | `17df1b4`–`fbaa397` |
| 29 Sep 2026 | Portal | Customer plans (POC / licensed), per-scan-type allowances, single-asset Deep scan (migration 0049); sealed-probe licence bypass closed | `08abe7e` |
| 29 Sep 2026 | Portal | Fixed `crypto.randomUUID is not a function` on plain-HTTP origins | `9563ab4` |
| 28 Sep 2026 | Reports | Export to PDF / Word / Excel / CSV, report filters, per-finding status | `114fc83` |
| 28 Sep 2026 | AI | Production fixes: unreachable Ollama skipped, reports fall back to free models when premium fails, every provider named in errors, API-key fragments scrubbed from logs | `6607084` |
| 28 Sep 2026 | Deploy | AWS compose passes the AI settings; `install.sh` keeps keys added to `.env` by hand; no provider pinning | `5791bc3` |
| 28 Sep 2026 | AI | Automatic premium → free AI chain: shared cooldowns, spend caps, answer reuse, Groq, agent failover to OpenAI ([ADR-0004](adr/0004-ai-fallback-chain.md)) | `f7bffef` |
| 27 Sep 2026 | Remediation | Contextual remediation: rule-keyed recipes, fix bundles, due dates, AI refinement, XLSX tracker | `1cdd416` |
| 27 Sep 2026 | Findings | Grouped findings view, remediation OS auto-detect, clipboard fallback on HTTP | `main` |
| 25 Sep 2026 | AI / compliance | Asset tags, regional compliance packs, sector AI, cloud / hybrid / sovereign AI gateway, AI audit chain | `9bbacb8` |
| 25 Sep 2026 | Findings | Per-scan findings: label, filter and compare by scan | `main` |
| 23 Sep 2026 | Security | P0 hardening: single-use refresh tokens with reuse revocation, proxy-aware login rate limit, IDOR fixes | `security/p0-fixes` |
| 23 Sep 2026 | Detection | Every finding gets a verification verdict (migration 0044) | `main` |
| 12 Sep 2026 | Scanner | Aggressive scans no longer die: 47 → 4.3 MB per host, two-phase ports, per-host result chunks (0041) | `main` |
| Aug–Sep 2026 | Detection | Manager posture rules (25), exposed-service detection, KEV + EPSS exploitability, detection trace, IPv6 discovery | `main` |
| Aug–Sep 2026 | Scanner / probe | Scanner v2 and v3 identification, AIMD pacing, probe sealing (native binary + signed licence), AWS deploy paths | `main` |

## Pending

Status values: **Blocked on you** · **Not started** · **In progress** · **Deferred** · **Done**. *(from notes)* marks items taken from earlier session notes and not re-checked.

### Roadmap — next 8 workstreams

Priority order from the [next-8 workstreams plan](planning/2026-09-29-next-8-workstreams-plan.md) (29 Sep).

| Priority | Workstream | Status | Size | Next step |
| --- | --- | --- | --- | --- |
| P0-1 | Security review + software testing | Done | L | Done per owner (1 Oct); P0 hardening bundle `security/p0-fixes` + master test plan on `main`. The hardening items below are still present in the code |
| P0-2 | Fix the AI integration | Blocked on you | S–M | Code done on `main`; server `.env` + API credit needed (see *Needs you*) |
| P0-3 | Agent install in client environments | Done | M | Built, tested and documented: the manager serves a signed agent containing only the agent's own code; Fleet → Add agent issues a single-use install token (1 h / 24 h / 7 d); access expiry is set from Fleet and enforced by the manager; on-prem customers get encrypted bundles. Docs: [operator runbook](operations/AGENT_DISTRIBUTION.md), [customer guide](probe/CUSTOMER_AGENT_INSTALL.md), [approach §10–11](planning/2026-10-01-agent-install-approach.md). On `main` (`46623ae`) |
| P0-3b | Agent install, next phase | Not started | M | Pipeline, needs a Windows runner/VM: Windows download route + PowerShell installer + Fleet OS switch, a real Windows install, licence at enrolment for the sealed agent, Podman/RHEL, an amd64 live test, auto-update, support bundle ([plan](planning/2026-10-02-agent-code-fixes-plan.md)) |
| P1-1 | Deep scan (all 65,535 ports, one host) in the operator Scanner | Done | S | Card on the operator Scanner; the ≤3-host Deep Port Sweep stays in the catalog (hidden while `SHOW_EXTENDED_USE_CASES = false`) |
| P1-2 | Mobile-friendly UI + dashboard polish | Done | L | Done per owner (3 Oct); responsive dashboard landed in `f70f392`, layout overlaps fixed on `origin/main` |
| P2-1 | Website content | Not started | S | Platform choice needed |
| P2-2 | Platform walkthrough + feature videos | Not started | M | After P1, so recordings show the final UI |

### Done, waiting for merge (`claude/adoring-maxwell-uz71b2`)

| Item | Area | Notes |
| --- | --- | --- |
| Backend hardening | Security | API docs (`/docs`, `/redoc`, `/openapi.json`) are off when `APP_ENV=production`; one limiter (30 per minute per signed-in user) covers every AI-spending route; the API image runs as a non-root user (uid 10001) and the code stays root-owned and read-only to it. Checked live: `/docs` is 404 in production mode, the 31st AI call returns 429, and a second user on the same address is unaffected (an IP key would have put everyone behind the dashboard in one bucket, because the proxy does not forward the browser's address). **The image build itself was not run (no Docker daemon in the session)**; as a stand-in, the API, `alembic upgrade head`, the seed script and a real detection run were all run as uid 10001 against a root-owned read-only copy of the code, with no permission errors. |
| Script Content-Security-Policy | Security | A fresh nonce per request with `strict-dynamic` and no `unsafe-inline`; the root layout stamps its inline theme script. Checked in Chromium on a production build: no violations on the login, portal and operator pages, forms still work, injected inline script and event handlers are blocked. |
| Legacy OTP login removed | Security | The old email-code endpoints and stores minted tokens nothing accepts, returned the code in the response when no mail key was set, and fell back to a default secret. Gone, together with the JWT secret the compose files passed to the frontend container for it and the two packages nothing imports any more (`resend`, `tweetnacl`; the lockfile loses exactly those and `postal-mime`). The CLI now signs in with email and password and swaps that session for a 30-day revocable token (`api:read`, `api:write`; it cannot mint tokens); `vedha logout` revokes it. Checked live end to end. |
| API keys fixed | Settings | Creating a key from Settings **never worked**: the proxy called a backend path that does not exist, double-encoded the body, and the page sent scopes the backend rejects. Fixed, with a read-only / read and write / probe picker (default read-only), a 7 / 30 / 90 / 365-day expiry (default 90), and Revoked / Expired / No expiry / Unused markers. (Settings defect D2.) |
| Operator console gate | Portal | A customer account typing its login on the operator sign-in now gets a clear message and a link to the portal sign-in, no session is left behind, and refresh never turns a customer token into an operator session. Checked live and in the browser. |
| Notification rules | Settings | Rules were never stored and nothing sent those alerts (only the test button queued a message). Now stored per organisation (migration **`0055`**), editable in Settings (“saved” only after the server confirms), and real for four events: Critical and High findings opened by a scan, report approved, new probe enrolled. Checked live: a queued event went through the outbox worker to a Slack-style webhook, and a broken email channel did not block it. (Settings defect D1.) |
| AI runtime shows the live chain | Settings | Replaces the four static provider cards with the real fallback chain: order, tier, state (ready / cooling / blocked), spend against the cap and what to fix. Shared with AI Brain. Customers do not see spend or server setting names. (Settings defect D3.) |
| Browser checks done | UI | AI Brain chain panel, sidebar logo, the Plan panel's Portal access section, and the customer portal under locks (locked findings appear only as “2 locked findings · Available on a licensed plan”, no locked title leaks, the Reports lock panel shows). |
| Remediation workspace | Remediation | Ported from the Codex branch: deterministic, review-only fix artifacts (PowerShell / shell / runbook) with content hashes and an operation catalog; nothing is executed. Tenant-scoped, audited (metadata only), allow-listed selectors (no commands inferred from finding prose). Findings page gets bulk select and a workspace dialog. |
| AI agent hardening | AI | Bounded context and a target allow-list: advisor output is treated as untrusted, and a target outside the engagement is dropped. Confidence is clamped (a large value used to crash the agent on `Numeric(4,1)`). |
| Notification events connected | Notifications | SLA at risk (a watcher loop, deduplicated per transition by `sla_alerts`, migration **`0056`**; interval `SLA_WATCH_INTERVAL_SECONDS`), finding status changed, and detection coverage gap now have producers, each in a savepoint so a failed alert never fails the work. |
| N+1 asset lookups removed | Backend | Detection resolved assets one query per finding; it now primes one cache per run. Guarded by a query-count test (fake DB and real Postgres). |
| Organisation policies | Settings | Migration **`0057`**, admin-only, audited with before and after. **Sign-in network allowlist**: checked at sign-in and at every refresh; admins are always exempt so a bad list cannot lock everyone out; outsiders get the same generic 401 as a wrong password. Optional **absolute session limit** (operator / customer hours, from the `auth_time` claim). **Scanning**: weekly or one-off blackout windows (time-zone and DST aware, midnight crossing) and global exclusions merged into every probe job. **New-customer defaults**: lock severities / features, POC length and a support contact, applied on provisioning and shown on the portal lock panel. Settings page: Sign-in policy, Scanning, New customers. Managers see the scan and customer sections read-only; the sign-in policy is admin-only. Verified live on Postgres and Chromium. |
| Portal wording under locks | Portal | Findings summary and the Executive report no longer say “no open findings” / “every open finding” when a plan hides severities. |

### Other open items

| Item | Area | Status | Why it is open · next step |
| --- | --- | --- | --- |
| Plan-lock known gaps (your choice) | Portal | Deferred | Raw scan evidence is not locked, so service banners could hint at a locked finding. Posture and analytics scores use only the findings the customer can see. Seen in the browser on 3 Oct: with 2 Critical and 1 High locked, the dashboard says “No critical or high findings open”, the Findings tiles show 0 Critical and 0 High and say “Counts cover every open finding in scope”, while the list below shows “2 locked findings”. Consider wording that counts locked findings |
| Non-root backend image not built | Security | Not started | No Docker daemon in the session (the same checks passed as uid 10001 on a read-only copy of the code). After the redeploy confirm the `api` and `migrate` containers start and `docker compose exec api id` shows uid 10001. If the agent-release folder is unreadable inside the container, run `chmod -R a+rX manager/agent-releases` |
| Content-Security-Policy over HTTPS in production | Security | Not started | Checked on a local production build over HTTP. After the deploy open the login page and one operator page with the browser console open and confirm there are no CSP errors |
| Frontend packages `pdfkit` and `@playwright/test` missing from the installed `node_modules` | Frontend | Blocked on you | Declared by the 30 Sep / 1 Oct reporting and responsive commits but not installed: `tests/report-export*.test.ts` fail and `tsc` reports 3 errors until `npm install` runs in `manager/frontend`. |
| Batch lane for reports (about 50% cheaper) | AI | Deferred | Makes report generation an hours-long async job — a product decision. |
| Require MFA (TOTP) | Security | Not started | Only an `mfa_enabled` column exists; enrolment, verification and recovery codes are a feature of their own. Idle sign-out was left out on purpose: it is enforced in the browser only, so the absolute session limit (server-side) is the real control |
| Node CLI calls Anthropic directly | AI | Deferred | `manager/frontend/cli` bypasses the manager's gateway and fallback. Operator-local, not on the customer data path. |
| Portal Spec 2 (incident IDs `VDH-####`) and Spec 3 (integrations) *(from notes)* | Portal | Deferred | Each needs its own spec. |

## Needs you

These need your accounts, your server or your decision.

- [ ] Production redeploy (in progress, owner). Attach an Elastic IP so `13.127.147.205` in DNS survives restarts
- [ ] On the AWS server (`/opt/Project-Vedha`): `git pull`, then in `.env` set `LLM_PROVIDER=` (blank) and add `GEMINI_API_KEY=<key>`
- [ ] Fix `OPENAI_API_KEY` on AWS: the server's key is rejected (it appears to be missing the `sk-` prefix). Use the full `sk-proj-…` key or leave it blank
- [ ] Run `make full`, then clear stale cooldowns:
  `docker exec vedha-redis-1 sh -c 'for p in "ai:cool:*" "ai:strikes:*" "ai:probe:*"; do redis-cli --scan --pattern "$p" | xargs -r redis-cli del; done'`
- [ ] Re-run the AI diagnostic and confirm `GENERATE OK -> served by gemini`
- [ ] Rotate the OpenAI key: a fragment of it was written to the AWS API logs before the scrub fix
- [ ] Add Anthropic API credit at console.anthropic.com so Claude answers first (Claude Pro/Max subscriptions do not include API access)
- [ ] Run `npm install` in `manager/frontend` (adds `pdfkit` and `@playwright/test`, which the reporting work needs). Other sessions share that `node_modules`, so I left it to you
- [ ] Optional: add a free `GROQ_API_KEY` as a second free fallback, and set `AI_DAILY_CAP_USD` (e.g. `anthropic=20,openai=10`)
- [ ] After the redeploy, set up Email and Slack under Settings (the new notification rules only reach channels that are set up), then press the integration's test button. `AUTH_SECRET` is no longer read by the frontend; it can be removed from the AWS `.env` (harmless if left)
- [ ] Command-line users: `vedha login` now asks for email and password instead of emailing a code, and stores a 30-day token that `vedha logout` revokes
- [ ] **Today:** submit `vedhasec.com` for web-filter categorisation (Palo Alto, Zscaler, Fortinet, Cisco Talos, Broadcom, Check Point). Domains under about 32 days old are commonly blocked as "newly registered", which would stop customer agents reaching the manager
- [ ] Merge `claude/adoring-maxwell-uz71b2` into `main`. It already contains `origin/main` `58f1a5d`, so `git push origin claude/adoring-maxwell-uz71b2:main` is a fast-forward; or open a pull request. Then redeploy. In your primary checkout, commit or set aside uncommitted changes and pull
- [ ] After deploying, the migrations run `0052` and `0053` (agent install), `0054` (plan locks) `0055` (notification rules), `0056` (SLA alerts) and `0057` (organisation policies). Existing customers keep full access until you lock something; every organisation starts with the default notification rules and no sign-in restriction.
- [ ] Before saving a sign-in network list: the backend must see the real client address (trusted proxy headers). Test with a non-admin account first. Administrators are exempt by design, and personal access tokens are not subject to the list (it applies to sign-in and refresh)
- [ ] Optional: set `SLA_WATCH_INTERVAL_SECONDS` (SLA-at-risk alerts); after the deploy confirm the API logs show the SLA watch loop running
- [ ] Clean up the plan-locks / export test leftovers: containers `vedha-export-before`, `vedha-export-after`, `vedha-export-ui-before`, `vedha-export-ui-after`, `vedha-locks-pg`; images `vedha-frontend:exporttest`, `:exportfix`, `:menufix`; and, once pushed, the merged branches and worktrees listed in the change log row for 2026-10-03 (merge all)
- [ ] On your build machine, run `make agent-keygen`. Keep `~/.vedha/agent-release-key.pem` off the server and back it up offline. Put the printed `AGENT_RELEASE_PUBLIC_KEY=…` in the AWS `.env`
- [ ] Once the merge is deployed (it runs migration 0052): `make agent-release`, then `make agent-publish TO=ubuntu@<server>:/opt/Project-Vedha/manager/agent-releases`. Fleet → Add agent then shows the release ([runbook](operations/AGENT_DISTRIBUTION.md))
- [ ] Remove the agent-install test leftovers on your Mac (Claude's safety hook blocks container removal): the `vedha-agentinst` compose project, the containers `vedha-agent-e2e`, `-e2e2`, `-e2e3`, `-round0`, `-round1`, `-round2` and their `-state` volumes, and the images `vedha-e2e-customer-host:local`, `vedha-e2e-vendor-host:local`, `vedha-backend:9.9.9`, `vedha-frontend:9.9.9`, `vedha-backend:agentinst`
- [ ] Decide the roadmap questions in the [next-8 workstreams plan](planning/2026-09-29-next-8-workstreams-plan.md#decisions-needed-from-you): P0 order, which paid AI API and monthly cap, sealed agent image by default, retire the ≤3-host deep scan, website platform and video voice
- [ ] Decide: port the Codex branch's remediation workspace onto `main`? A literal merge conflicts in 52 files and would overwrite code already ported; the missing part is about 18 new files (`app/ai/remediation_workspace.py`, its context service, 3 backend tests, `RemediationWorkspaceDialog.tsx`, a preview route, the model picker you declined) plus edits to `routers/remediation.py`, schemas and `ai/agent.py`
- [ ] Decide: batch lane for reports (cheaper, but reports become asynchronous)?

## Change log

One row per finished piece of work, newest first.

| Date | Change | Ref |
| --- | --- | --- |
| 2026-10-03 | Organisation policies (migration 0057): sign-in network allowlist with admin exemption and generic 401, absolute session limit, scan blackouts and exclusions, new-customer defaults, Settings UI. Plus: remediation workspace and agent hardening ported, notification events connected (0056), N+1 removed, portal wording under locks. Backend 2,396 passed, frontend 451 of 451 | `claude/adoring-maxwell-uz71b2` |
| 2026-10-03 | Settings defects D1–D3 closed. **Notifications:** rules are stored per organisation (migration 0055) and honoured by a new dispatcher; real producers for Critical/High findings opened by a scan, report approved and new probe enrolled; unconnected events are labelled in Settings. Verified on Postgres 16: migration up/down/up, API round trip, the detection hook's query, and delivery through the outbox worker to a webhook (a failing email channel did not block Slack). **API keys:** creation had never worked (wrong backend path, double-encoded body, invalid scopes); fixed, with scope presets, expiry and Revoked / Expired / No expiry / Unused markers. **AI runtime:** live fallback chain instead of four static cards. Checked in Chromium against the real API. Unit tests found a logging bug in the new code (structlog reserves `event`) before it shipped | `6ff5847`, `6da6ef6` |
| 2026-10-03 | Operator console gate: a portal customer typing their account on the operator sign-in gets a clear message and a link, no session is left behind, and refresh cannot upgrade a customer token. Checked live (customer → 403 and no cookies; admin unaffected; portal gate unchanged) and in the browser | `960d4ad` |
| 2026-10-03 | Legacy OTP login removed (endpoints, stores, default signing secret, and the JWT secret the compose files gave the frontend). CLI sign-in is now email and password, exchanged for a 30-day revocable token. Verified live: wrong password, rate limit, token works, token cannot mint tokens, logout revokes it (401 afterwards) | `1b2bb21` |
| 2026-10-03 | Script Content-Security-Policy: nonce and `strict-dynamic`, no `unsafe-inline`. Checked in Chromium on a production build: no violations on five pages, forms hydrate, injected inline script and event handlers blocked | `53b1bc8` |
| 2026-10-03 | Backend hardening: API docs off in production, one 30-per-minute limiter on every AI-spending route, non-root API image. Verified live (production-mode `/docs` is 404; the 31st call is 429 with Retry-After; another user is unaffected). The limiter was first keyed by IP and corrected to per user after review, since the dashboard proxy hides client addresses. Image build not run (no Docker daemon) | `a094646` |
| 2026-10-03 | Browser checks: AI Brain chain panel, sidebar logo, Plan panel's Portal access, and the customer portal under locks all render and behave as designed. Environment for the checks: local Postgres 16 and Redis, the real API and a production-style frontend, Chromium via Playwright. Noted the 0-count wording gap in the plan-lock row above | — |
| 2026-10-03 | Merged all unmerged work onto `integrate/all-to-main` (from `integrate/agent-install-to-main` + `feat/portal-plan-locks` + local `main`'s design-system doc). Conflicts: `VERSION` (kept the highest), `docs/STATUS.md` (combined by hand), and migration id `0052`, which both branches used: plan locks renumbered to `0054`, one Alembic head. Not merged: the Codex branch (see the assessment) and `probe-standalone` (never). Branches now fully contained and safe to delete after the push: `feat/portal-plan-locks`, `fix/report-export`, `feat/operator-deep-scan`, `docs/status-refresh`, `integrate/agent-install-to-main`, `feat/agent-install`, `docs/agent-install-approach`, `feat/technical-finding-report`, `feat/reporting-boardroom-redesign` | `integrate/all-to-main` |
| 2026-10-03 | New logo and favicon: shared `VedhaMark` / `VedhaLogoStacked` components, favicon SVG + ICO + Apple icon, brand files in `public/brand/`; both login pages checked in the browser | `1ab403d` |
| 2026-10-03 | Settings page research and design doc (no code): a new structure, each field's meaning, default, owner and effect, and 4 defects found in today's page | `docs/superpowers/specs/2026-10-03-settings-page-design.md` |
| 2026-10-03 | Portal plan locks: severity and feature locks per customer, a central server guard, teaser rows and lock panels in the portal | `35581b4`–`72d6bea` |
| 2026-10-02 | Report export fixed: the page header clipped the menu, which now opens above the page. Verified in the production image on desktop and mobile | `c4161aa` |
| 2026-10-02 | Agent install Phase 1 (P0-3) built on `feat/agent-install` and proven end to end on an isolated stack. The manager serves a signed agent release: installer and manifest are public, the image needs a live install token. Install tokens are engagement-bound and single-use (migration 0052). Fleet → Add agent works for the operator and the portal. The installer verifies signature and checksum and gains `--proxy` / `--ca-bundle`. On-prem bundles are encrypted to the customer's key. The live test found and fixed 4 bugs: an agent start failure from hardware binding, an enrolment commit race that burnt tokens, the loader's file count, and an old `cryptography` version | `feat/agent-install` |
| 2026-10-03 | P0-3 closed and integrated: `feat/agent-install` + local `main` merged onto `origin/main` on `integrate/agent-install-to-main` (conflicts: VERSION, Makefile, and the WebSocket TLS fix that two sessions had written separately, now one helper with certifi, CA bundle, verify-off and mTLS). Docs finished (runbook: expiry, code boundary; customer guide: lifetimes, access dates; approach §11). P1-2 marked done per owner. Also merged the self-contained `feat/technical-finding-report` (standalone Technical Findings report) and `feat/reporting-boardroom-redesign` (spec + plan). Integrated tests: backend 2,234, probe 2,512, frontend 366 of 368 (`pdfkit`). The Codex branch was assessed, not merged (52 conflicts, already ported in part; [assessment](planning/2026-10-03-branch-merge-assessment.md)) | `integrate/agent-install-to-main` |
| 2026-10-02 | Windows-first agent quick wins on `feat/agent-install`: customers' agent now ships only its own 73 modules (the Linux image no longer carries `scanner/findings.py`, the judgement rules; `vedha-agent runtime-check` gates the build); Windows single-instance lock and MAC lookup fixed; agent access expiry set from Fleet and enforced by the manager (migration 0053; in-flight uploads still land); install-command lifetime picker (1 h / 24 h / 7 d); legacy Windows scripts no longer default to the old test IP or exclude `python.exe` from Defender. Backend 2,232, probe 2,497, frontend fleet 13 tests pass. The compiled Windows build, signed installer and Windows VM test are in the pipeline ([plan](planning/2026-10-02-agent-code-fixes-plan.md)) | `feat/agent-install` |
| 2026-10-03 | Finished the started agent work and tested it live. **Expiry** was incomplete: the WebSocket path ignored it and an expired agent wiped its own identity and re-enrolled; fixed (manager refuses connect, job claim and idle heartbeat; the agent waits and keeps its identity). Live run on a real agent: expire → offline + waits (0 restarts, no re-enrolment) → extend → resumes by itself in ~3 min; the three lifetime presets return the right expiry and others 422. **Compiled build:** the sealed Linux image compiles only the agent closure (verified: `runtime-check` OK in the binary, no source/`findings` in the image, manifest parity). That check found the sealed image had been shipping without `impacket` / `ldap3` / `dnspython`, silently losing the SMB, LDAP and DNS checks; fixed. Windows compiled build + CI job written, **not yet run**. Tests: backend 2,234, probe 2,506 | `feat/agent-install` |
| 2026-10-01 | Operator Deep scan (P1-1) done: same one-asset card as the portal, never charged to the customer; checked live in the browser; 2,139 backend tests pass; frontend 337 of 339 (the 2 failures are the missing `pdfkit` / `@playwright/test` packages) | `feat/operator-deep-scan` |
| 2026-10-01 | Refreshed after `b6a3b60`: reporting and responsive dashboard moved to Done; production stopped for a redeploy (owner); security review marked done (owner) | — |
| 2026-10-01 | Status moved into the repo as `docs/STATUS.md`; added the production URLs and version (1.0.325) and the next-8 workstreams roadmap | — |
| 2026-09-30 | First status doc, built from the repo history and earlier session notes | — |
| 2026-09-28 | AWS AI outage diagnosed: seeded `LLM_PROVIDER=ollama`, no Anthropic credit, rejected OpenAI key, no Gemini key on the server. Code fixes pushed | `6607084` |
| 2026-09-28 | Automatic premium → free AI chain merged and pushed; AWS deploy scripts fixed | `f7bffef`, `5791bc3` |
