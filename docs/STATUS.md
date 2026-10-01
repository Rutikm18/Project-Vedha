# Vedha Project Status

As of **2026-10-01** (refreshed after `b6a3b60`). This is the single place for what is done, what is open, and what needs the owner.
Claude updates it at the end of every finished piece of work: a change-log row, then the sections above it.

## At a glance

**Production is unreachable as of 1 Oct 2026** — see the first item below. On `main`, the code for automatic AI routing, customer reporting, customer plans, a responsive dashboard and one-command HTTPS is merged; what else blocks a fully working production system is configuration and API credit, not code.

| Area | State |
| --- | --- |
| `origin/main` | `b6a3b60`, VERSION 1.0.330 (1 Oct 2026) |
| Production | [app.vedhasec.com](https://app.vedhasec.com) / [api.vedhasec.com](https://api.vedhasec.com) — **down on 1 Oct**: DNS → `13.127.147.205`, but ports 443, 80 and 22 all time out. Healthy on 1.0.325 on 30 Sep |
| Tests | 1,965 backend tests passing at the last full run (28 Sep) |
| AI providers | Anthropic: no API credit · OpenAI: key rejected on AWS · Gemini: works, but its key was not on the AWS server |
| Unmerged branches | `codex/customer-portal-engagement-parity` (report document ported; remediation workspace still not) · `probe-standalone` (never merge) |

The three things that matter most right now:

1. Bring production back: check the EC2 instance state, its public IP vs the DNS record, and the security group.
2. Fix the AWS `.env` (Gemini key, OpenAI key, blank `LLM_PROVIDER`), then `make full`. This restores AI Brain and report generation.
3. Start the security review (P0-1 in the [next-8 workstreams plan](planning/2026-09-29-next-8-workstreams-plan.md)). The portal now serves customers over the internet.

## Done

Merged and pushed to `origin/main`, newest first.

| Shipped | Area | What | Ref |
| --- | --- | --- | --- |
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
| P0-1 | Security review + software testing | Not started | L | Review the internet-facing portal and scan launch path before onboarding more clients |
| P0-2 | Fix the AI integration | Blocked on you | S–M | Code done on `main`; server `.env` + API credit needed (see *Needs you*) |
| P0-3 | Agent install in client environments | Not started | M | A clean, documented, supportable install path |
| P1-1 | Deep scan (all 65,535 ports, one host) in the operator Scanner | Not started | S | Portal has it; bring it to the operator scanner |
| P1-2 | Mobile-friendly UI + dashboard polish | In progress | L | Responsive dashboard landed in `f70f392`; check the remaining pages on a phone |
| P2-1 | Website content | Not started | S | Platform choice needed |
| P2-2 | Platform walkthrough + feature videos | Not started | M | After P1, so recordings show the final UI |

### Other open items

| Item | Area | Status | Why it is open · next step |
| --- | --- | --- | --- |
| Port the Codex branch's remediation workspace | Remediation | Not started | The report document and scan provenance were ported on 1 Oct. Still missing: `app/ai/remediation_workspace.py`, its context service and `RemediationWorkspaceDialog.tsx`. |
| Backend container runs as root | Security | Not started | No `USER` in `manager/backend/Dockerfile`. Add a non-root user. |
| `/docs`, `/redoc`, `/openapi.json` public in production | Security | Not started | Always enabled in `manager/backend/app/main.py`. Disable when `APP_ENV=production`. |
| No `script-src` Content-Security-Policy | Security | Not started | No CSP header found in frontend or deploy config. |
| AI routes have no rate limit | Security | Not started | `/ai/*` can be called without limit, which spends API credit. Reuse the login rate limiter. |
| Legacy OTP auth still in `manager/frontend/lib/auth-store.ts` | Security | Not started | In-memory OTP store left over from old auth. Confirm unused, then remove. |
| Operator console has no role gate *(from notes)* | Portal | Not started | A portal customer can reach the operator login and gets a confusing refusal. |
| AI Brain chain panel not checked in a browser | AI / UI | Not started | Type check and lint pass; visual check still to do. |
| Batch lane for reports (about 50% cheaper) | AI | Deferred | Makes report generation an hours-long async job — a product decision. |
| Node CLI calls Anthropic directly | AI | Deferred | `manager/frontend/cli` bypasses the manager's gateway and fallback. Operator-local, not on the customer data path. |
| Portal Spec 2 (incident IDs `VDH-####`) and Spec 3 (integrations) *(from notes)* | Portal | Deferred | Each needs its own spec. |
| N+1 queries in result ingestion *(from notes)* | Backend | Deferred | `job_result_service.py` looks up assets per host. Needs a fake-DB test harness before touching it. |

## Needs you

These need your accounts, your server or your decision.

- [ ] **Production is down:** in the AWS console, check the instance is running, that its public IP matches the DNS record (`13.127.147.205`; attach an Elastic IP so it stops changing), and that the security group allows 443 / 80 / 22
- [ ] On the AWS server (`/opt/Project-Vedha`): `git pull`, then in `.env` set `LLM_PROVIDER=` (blank) and add `GEMINI_API_KEY=<key>`
- [ ] Fix `OPENAI_API_KEY` on AWS: the server's key is rejected (it appears to be missing the `sk-` prefix). Use the full `sk-proj-…` key or leave it blank
- [ ] Run `make full`, then clear stale cooldowns:
  `docker exec vedha-redis-1 sh -c 'for p in "ai:cool:*" "ai:strikes:*" "ai:probe:*"; do redis-cli --scan --pattern "$p" | xargs -r redis-cli del; done'`
- [ ] Re-run the AI diagnostic and confirm `GENERATE OK -> served by gemini`
- [ ] Rotate the OpenAI key: a fragment of it was written to the AWS API logs before the scrub fix
- [ ] Add Anthropic API credit at console.anthropic.com so Claude answers first (Claude Pro/Max subscriptions do not include API access)
- [ ] Optional: add a free `GROQ_API_KEY` as a second free fallback, and set `AI_DAILY_CAP_USD` (e.g. `anthropic=20,openai=10`)
- [ ] Decide the roadmap questions in the [next-8 workstreams plan](planning/2026-09-29-next-8-workstreams-plan.md#decisions-needed-from-you): P0 order, which paid AI API and monthly cap, sealed agent image by default, retire the ≤3-host deep scan, website platform and video voice
- [ ] Decide: port the Codex branch's remediation workspace onto `main`?
- [ ] Decide: batch lane for reports (cheaper, but reports become asynchronous)?

## Change log

One row per finished piece of work, newest first.

| Date | Change | Ref |
| --- | --- | --- |
| 2026-10-01 | Refreshed after `b6a3b60`: reporting and responsive dashboard moved to Done; production found unreachable (ports 443 / 80 / 22 time out) | — |
| 2026-10-01 | Status moved into the repo as `docs/STATUS.md`; added the production URLs and version (1.0.325) and the next-8 workstreams roadmap | — |
| 2026-09-30 | First status doc, built from the repo history and earlier session notes | — |
| 2026-09-28 | AWS AI outage diagnosed: seeded `LLM_PROVIDER=ollama`, no Anthropic credit, rejected OpenAI key, no Gemini key on the server. Code fixes pushed | `6607084` |
| 2026-09-28 | Automatic premium → free AI chain merged and pushed; AWS deploy scripts fixed | `f7bffef`, `5791bc3` |
