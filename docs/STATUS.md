# Vedha Project Status

As of **2026-10-03** (all unmerged work combined on `integrate/all-to-main`, awaiting your push). This is the single place for what is done, what is open, and what needs the owner.
Claude updates it at the end of every finished piece of work: a change-log row, then the sections above it.

## At a glance

**Production is stopped for a redeploy (1 Oct 2026, intentional).** On `main`, the code for automatic AI routing, customer reporting, customer plans, a responsive dashboard and one-command HTTPS is merged; what else blocks a fully working production system is configuration and API credit, not code.

| Area | State |
| --- | --- |
| `origin/main` | `4c78573`. **Everything not yet on it is combined on `integrate/all-to-main`, tested, not yet pushed**: agent install, portal plan locks, report export fix, new logo, Technical Findings report, operator Deep scan, design system doc |
| Production | [app.vedhasec.com](https://app.vedhasec.com) / [api.vedhasec.com](https://api.vedhasec.com) — **stopped for a redeploy on 1 Oct** (owner). Was healthy on 1.0.325 on 30 Sep |
| Tests | On `integrate/all-to-main` (3 Oct): backend 2,276 passed, 8 skipped · frontend 375 of 377 (the 2 = missing `pdfkit`) · probe 2,512 (no probe change since the agent-install run) · lint 0 errors · one Alembic head (`0054`) |
| AI providers | Anthropic: no API credit · OpenAI: key rejected on AWS · Gemini: works, but its key was not on the AWS server |
| Unmerged branches | `integrate/all-to-main` (everything below, ready to publish) · `codex/customer-portal-engagement-parity` (not merged: 52 conflicts, only its remediation workspace is missing, see [the assessment](planning/2026-10-03-branch-merge-assessment.md)) · `probe-standalone` (never merge) |

The things that matter most right now:

1. Push `integrate/all-to-main` to `main` and redeploy. It fixes the production report export and brings agent install, plan locks and the new logo.
2. Finish the production redeploy; attach an Elastic IP so the DNS record (`13.127.147.205`) stays valid across restarts.
3. Fix the AWS `.env` (Gemini key, OpenAI key, blank `LLM_PROVIDER`), then `make full`. This restores AI Brain and report generation.
4. Agent install in client environments (P0-3) is done and documented. To go live: publish the integration branch, create the release key, publish a release, and get `vedhasec.com` categorised by web filters (see *Needs you*).

## Done

Merged and pushed to `origin/main`, newest first.

| Shipped | Area | What | Ref |
| --- | --- | --- | --- |
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
| P0-3 | Agent install in client environments | Done | M | Built, tested and documented: the manager serves a signed agent containing only the agent's own code; Fleet → Add agent issues a single-use install token (1 h / 24 h / 7 d); access expiry is set from Fleet and enforced by the manager; on-prem customers get encrypted bundles. Docs: [operator runbook](operations/AGENT_DISTRIBUTION.md), [customer guide](probe/CUSTOMER_AGENT_INSTALL.md), [approach §10–11](planning/2026-10-01-agent-install-approach.md). On `integrate/agent-install-to-main`, awaiting publish |
| P0-3b | Agent install, next phase | Not started | M | Pipeline, needs a Windows runner/VM: Windows download route + PowerShell installer + Fleet OS switch, a real Windows install, licence at enrolment for the sealed agent, Podman/RHEL, an amd64 live test, auto-update, support bundle ([plan](planning/2026-10-02-agent-code-fixes-plan.md)) |
| P1-1 | Deep scan (all 65,535 ports, one host) in the operator Scanner | Done | S | Card on the operator Scanner; the ≤3-host Deep Port Sweep stays in the catalog (hidden while `SHOW_EXTENDED_USE_CASES = false`) |
| P1-2 | Mobile-friendly UI + dashboard polish | Done | L | Done per owner (3 Oct); responsive dashboard landed in `f70f392`, layout overlaps fixed on `origin/main` |
| P2-1 | Website content | Not started | S | Platform choice needed |
| P2-2 | Platform walkthrough + feature videos | Not started | M | After P1, so recordings show the final UI |

### Done on `integrate/all-to-main`, waiting for push

| Item | Area | Notes |
| --- | --- | --- |
| Agent install (P0-3) | Agent | See the roadmap row above and the change log. Migrations `0052`, `0053` |
| Report export did nothing in production | Reports | The Export menu opened inside a page-header box that hides overflow, so nothing showed. It now opens in a layer above the page, closes on Escape, an outside click or scroll, and fits a phone screen. Reproduced in the production image; checked on desktop and mobile; PDF download verified |
| Portal plan locks (POC vs licensed) | Portal | Per customer, at any time, on POC or licensed plans, the operator locks finding severities (a new POC starts with Critical + High locked) and features (AI assistant, Reports, Remediation & fix bundles, Compliance briefs). Locked findings never leave the server: one database-level guard filters every customer query. The portal shows them as "N locked findings · Available on a licensed plan"; locked features show a lock panel; written reports are withheld while any severity is locked. Migration **`0054`** (renumbered from `0052` to follow agent install). [Design](superpowers/specs/2026-10-02-portal-plan-locks-design.md) |
| New logo and favicon | Brand | The new mark replaces the shield in the sidebar and on both login pages; the stacked logo heads the customer portal login. Favicon as SVG (follows light/dark), ICO and Apple touch icon. Brand files in `manager/frontend/public/brand/` |
| Technical Findings report, boardroom reporting spec, operator Deep scan, design system doc | Reports / Scanner / Design | Merged from their branches and local `main` |
| Settings page redesign: research and design | Settings | Doc only; build not started. Draws on GitHub, Vercel, Datadog, Stripe, Tenable, Rapid7, Snyk, Salesforce and Checkmarx; gives every field its meaning, default, owner, effect and backend status; found 4 defects in today's page (below). [Design](superpowers/specs/2026-10-03-settings-page-design.md) |

### Other open items

| Item | Area | Status | Why it is open · next step |
| --- | --- | --- | --- |
| Settings: Notifications "Save" stores nothing | Settings | Not started | It waits 600 ms and says "saved", but the rules reset on reload. Persist them or remove the button (defect D1 in the settings design) |
| Settings: API keys always read + write, never expire | Settings | Not started | The model has scopes and an expiry, but the UI ignores both (defect D2) |
| Settings: AI Runtime shows the old provider cards | Settings | Not started | Replace with live fallback-chain status (defect D3) |
| Plan-lock known gaps (your choice) | Portal | Deferred | Raw scan evidence is not locked, so service banners could hint at a locked finding. Posture and analytics scores use only the findings the customer can see |
| Plan locks and sidebar logo not checked in a browser | Portal / UI | Not started | Covered by tests and the server is the gate; the Plan panel's *Portal access* section, the portal lock panels and the sidebar logo need a signed-in visual check after deploy |
| Port the Codex branch's remediation workspace | Remediation | Not started | The report document and scan provenance were ported on 1 Oct. Still missing: `app/ai/remediation_workspace.py`, its context service and `RemediationWorkspaceDialog.tsx`. |
| Backend container runs as root | Security | Not started | No `USER` in `manager/backend/Dockerfile`. Add a non-root user. |
| `/docs`, `/redoc`, `/openapi.json` public in production | Security | Not started | Always enabled in `manager/backend/app/main.py`. Disable when `APP_ENV=production`. |
| No `script-src` Content-Security-Policy | Security | Not started | No CSP header found in frontend or deploy config. |
| AI routes have no rate limit | Security | Not started | `/ai/*` can be called without limit, which spends API credit. Reuse the login rate limiter. |
| Legacy OTP auth still in `manager/frontend/lib/auth-store.ts` | Security | Not started | In-memory OTP store left over from old auth. Confirm unused, then remove. |
| Operator console has no role gate *(from notes)* | Portal | Not started | A portal customer can reach the operator login and gets a confusing refusal. |
| AI Brain chain panel not checked in a browser | AI / UI | Not started | Type check and lint pass; visual check still to do. |
| Frontend packages `pdfkit` and `@playwright/test` missing from the installed `node_modules` | Frontend | Blocked on you | Declared by the 30 Sep / 1 Oct reporting and responsive commits but not installed: `tests/report-export*.test.ts` fail and `tsc` reports 3 errors until `npm install` runs in `manager/frontend`. |
| Batch lane for reports (about 50% cheaper) | AI | Deferred | Makes report generation an hours-long async job — a product decision. |
| Node CLI calls Anthropic directly | AI | Deferred | `manager/frontend/cli` bypasses the manager's gateway and fallback. Operator-local, not on the customer data path. |
| Portal Spec 2 (incident IDs `VDH-####`) and Spec 3 (integrations) *(from notes)* | Portal | Deferred | Each needs its own spec. |
| N+1 queries in result ingestion *(from notes)* | Backend | Deferred | `job_result_service.py` looks up assets per host. Needs a fake-DB test harness before touching it. |

### Testing round 1 — gaps kept in the pipeline (needs depth research before any build)

Source: the 3 Oct test report (single Windows 11 host, rig packs 1–4). **Nothing here is started.** The **Code check** column records what was verified in the repo on 3 Oct, by reading code only (none of it was reproduced on a running system, so confirm live before filing a bug): **Confirmed** (the code shows the cause), **Partly** (the claim is narrower than reported), **Stale** (largely already handled) or **Not found** (cause not located). Order is the report's priority order.

| # | Gap | Priority | Code check | Where the research should start |
| --- | --- | --- | --- | --- |
| 1 | Chain of custody empty on every finding (tool, source, time, operator, SHA-256 "not recorded") | Fix first, blocks client delivery | **Confirmed.** The report reads `tool`, `source_host`, `captured_at`, `captured_by` and `sha256` from each evidence item and flags what is missing, but nothing in detection, discovery or the agent writes `captured_by`, `source_host` or `sha256` | `app/services/report_document.py` (`_artifact`), `lib/report/finding-model.ts` (`provenanceOf`). Decide who stamps custody (the agent at capture, or the manager at ingest) and what exactly is hashed |
| 2 | Duplicate findings: one service gives 3–6 findings (FTP ×3, Telnet ×3) | Fix first | **Confirmed.** Separate producers each create a finding for the same cleartext service: the exposed-service posture rules (`port_intel`), the legacy `discovery/service_vuln.py` ("Cleartext service exposed (Telnet)"), the probe-findings translator, and `CORR-CLEARTEXT-CLUSTER`. Dedup is per (engagement, asset, title), so different titles never merge | `engine_bridge.py`, `discovery/finding_translator.py`. Needs a condition-level key (host + port + condition) across producers, or retiring the overlapping legacy producer |
| 3 | Host TLS / SCHANNEL weakness missed (SSL2/3, TLS 1.0/1.1, RC4/DES) | Fix first | **Partly.** TLS scanning and rules exist (`POSTURE-TLS-DEPRECATED-VERSION`, `-WEAK-CIPHER`, `-SELF-SIGNED`) for web, mail, LDAPS and WinRM-TLS ports. **Confirmed gap:** `tls_scan` is deliberately never run on RDP 3389, SMB 445 or MSRPC 135 (`workflow/router.py` skips ports observed not to speak TLS, and RDP negotiates TLS inside its own protocol), so the SCHANNEL protocol and cipher set behind those listeners is never measured. RDP only gets `POSTURE-RDP-NO-TLS` | `probe/scanner/rdp_scan`, `tls_scanner.py`, `workflow/router.py`. Research: a TLS-inside-RDP handshake probe per protocol version and cipher |
| 4 | Version → CVE false positives (vsftpd 3.0.3, OpenSSH 9.5) | Fix first | **Partly.** The matcher treats `introduced` with no `fixed` as "vulnerable onward" (OSV convention, pinned by a test). Unparseable versions are skipped, not matched, so "defaults to match all" is not what the code does. Likely cause: Debian OSV records for *unfixed* CVEs are `[0, unbounded)` and match every upstream banner version | `detection_engine/matcher.py` (`_version_in_ranges`), `osv_debian_snapshot.json`. Research: mark open-ended or distro-unfixed matches as suspected, or bound them with upstream NVD data |
| 5 | KEV escalation not OS-gated (BlueKeep on Windows 11) | Next | **Confirmed.** `_KEV_LINKS` in `exploitability.py` maps a rule to CVEs with no OS or product applicability, so `POSTURE-RDP-NO-NLA` links CVE-2019-0708 on any Windows version | `detection_engine/exploitability.py`. Add an applicability field (OS family and version range) per link |
| 6 | EPSS alone makes a finding Critical (a DoS at confidence 30); priority and severity disagree | Next | **Confirmed.** `_compute_priority` order is KEV, then EPSS ≥ high → "critical", then CVSS, with no regard to impact or match confidence; `engine_bridge` then maps priority to severity | `detection_engine/enrichment.py`, `engine_bridge.py` (`_PRIORITY_TO_SEVERITY`). Decide which field drives the queue; cap EPSS promotion by confidence and impact |
| 7 | Placeholder leakage ("Restrict not recorded/tcp") and "not recorded" in the asset table | Next | **Confirmed (asset table), by design (placeholders).** "not recorded" is the designed output when a fact is missing (`remediation/context.py`). The report's asset block reads only the Asset row (`os`, `os_version`, no service or version columns), so values that exist only in the evidence JSON are never shown | `report_document._asset`, `_promote_assets`. Research: why `Asset.os` is not promoted from the fingerprint, and whether the table should read facts |
| 8 | Role misclassification (Windows 11 workstation → hypervisor / print server) | Next | **Partly.** The classifier is port-signal weighted (902/903 → hypervisor, 9100/515/631 → printer). The test host runs VMware and the rig opened mock printer and IoT listeners, so this is at least partly a rig artifact. The real design question is a workstation that runs VMware Workstation or shares a printer | `probe/scanner/device_classifier.py`. Needs a multi-device rig and the role confidence shown to the user |
| 9 | Full-port / UDP profile; rsync 873, LDAP 389, DNS 53 missed | Next | **Partly.** The default IT profile has 95 ports: it includes 389, 53, 3389, 445, 4444, 5985 and 6443 but **not** 873 (rsync) or 5901 (VNC); the IoT profile has 18 ports and OT has 0. So the LDAP and DNS misses are **not** a profile issue (investigate the LDAP / DNS scanners against the rig's protocol mocks); rsync and VNC are | `workflow/gates.py` (`PROFILE_PORTS`), `ldap_scanner`, `dns_scanner`. Re-scan with the full-port + UDP profile first, as the report says |
| 10 | "Closed" (RST) recorded as error; SYN falls back to connect | Later | **Partly stale.** The connect path already maps a refused connection to `closed` (`scanner_base.py`, `port_scanner.py`). A real SYN scan only works on Linux with raw-socket rights (root or `CAP_NET_RAW`); Windows, macOS and containers started with `cap_drop ALL` use the connect fallback by design, so the Windows test falling back is expected. **Not found:** which module records RST as `error` | `probe/scanner/syn_scanner.py` (`_syn_available`). Find the module that reports `error` before treating this as a bug |
| 11 | IPv6 absent | Later | **Stale.** The port scanner resolves with `getaddrinfo` (`AF_UNSPEC`) and records the address family, an IPv6 neighbour-discovery module exists, and IPv6 scope enforcement landed earlier. Not tested end to end on a dual-stack rig | `probe/scanner/ipv6_discovery.py` |
| 12 | SNMP write community (`private`, RW) not distinguished from read-only | Later | **Confirmed, by design.** The SNMP scanner never sends a SET ("No SETs"); `private` is only one candidate community, so write access cannot be proven | `probe/scanner/snmp_scanner.py`. A product and authorization decision: add a controlled, reversible SET probe, or word the finding "community named private; write access not tested" |
| 13 | Report quality: "100% coverage / 0 blind spots", no reproduction steps, duplicate ATT&CK refs ("T1210 T1210"), assessment window earlier than the scan date, AI report offline | Later | **Mostly confirmed.** Coverage is `(detected + prevented) / total` over the ATT&CK techniques the findings themselves map to (`routers/detection.py`) and is passed to the AI narrative as "Detection coverage", so it is close to a tautology. Only Active Directory findings ever record `reproduction_steps`; the report warns when it is missing. **Not found:** where duplicate ATT&CK refs come from (no de-duplication in the report model). The window comes from the engagement's own start and end dates, with no check that scans fall inside it. AI offline is the credit and config issue under P0-2 | `routers/detection.py`, `routers/ai_report.py`, `ad/findings.py`, `finding-model.ts`. Rename to "ATT&CK-mapped"; add repro steps per rule; de-duplicate refs; label the template fallback |
| 14 | Not built: multi-host discovery and change tracking, Active Directory depth (LDAP anon bind, Kerberoast, ADCS, coercion), network infrastructure (L2, VPN appliance CVEs, firmware), IoT depth, credentialed scanning, exploit validation (0 everywhere), multi-vantage exposure | Later | Scope items, not defects | Each needs its own spec and, for most, a multi-host or AD rig |
| 15 | Rig hygiene: the rig on 192.168.1.67 is the owner's real Wi-Fi adapter with four weakness packs applied | **Blocked on you** | Not a code item | Run the four `-Revert` scripts and reboot, then move future rounds to an isolated VMnet segment |

Pipeline order, from the report: custody (1) and dedup (2) gate client delivery; then host TLS (3) and the CVE parser (4); then 5–9. Process rules to keep: verify a miss live before filing it, re-arm and verify the rig before each scan, and label banner-mock detections as fingerprint-tier rather than validated.

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
- [ ] **Today:** submit `vedhasec.com` for web-filter categorisation (Palo Alto, Zscaler, Fortinet, Cisco Talos, Broadcom, Check Point). Domains under about 32 days old are commonly blocked as "newly registered", which would stop customer agents reaching the manager
- [ ] Land everything on `main`. Claude can't publish (safety hook), so run `git push origin integrate/all-to-main:main`. It is a fast-forward of `origin/main` `4c78573`. Then, in the primary checkout, commit or set aside its uncommitted changes and pull. Local `main` is a strict subset of the integration branch
- [ ] After deploying, the migrations run `0052` and `0053` (agent install) and `0054` (plan locks). Existing customers keep full access until you lock something
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
| 2026-10-07 | Deployment hardening from the architecture review: the API trusts forwarded client addresses only from the Docker networks (it trusted `*`, so a direct caller could pick its own address and get around per-address rate limits, the sign-in allowlist and probe auto-enrolment; reproduced with uvicorn 0.32); the main Redis no longer evicts (sessions, lockouts and sign-in codes could be dropped under memory pressure) and the AI answer cache moved to a new `redis-cache` service that may; `/metrics` answers only internal callers; the frontend has the `/api/health` its health check probed; new `backend-ci` workflow (tests on Python 3.12 and an Alembic up/down/up check, which nothing ran before). Backend 2,292 passed on 3.12; migrations checked on a fresh Postgres 16 | `claude/deploy-hardening` |
| 2026-10-04 | Report work only, taken from `claude/adoring-maxwell-uz71b2` (4 commits cherry-picked onto `main`, nothing else from that branch): the new presentation layer behind the web, PDF, Word and Excel report (one shared field model, every field carries its meaning, missing data handled once; IBM Plex fonts bundled; docs plan `planning/2026-10-03-report-formatting-plan.md`), plus two portal-report fixes (the plan-lock flag is a prop; the portal no longer claims "no findings" when plan locks hide severities). Left on that branch, not merged: two-step sign-in, organisation policies, notification rules, the remediation workspace, the AI recommendation check, the security and CSP changes, settings UI and the deployment review. Frontend only: 393 tests pass once `pdfkit` is installed (it is declared in `package.json` but missing from the shared `node_modules`, which is why 2 report-export tests fail on this machine), tsc and lint clean | `integrate/reports-to-main` |
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
