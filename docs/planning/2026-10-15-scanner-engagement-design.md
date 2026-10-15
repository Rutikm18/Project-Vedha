# Engagement scanner design and delivery checks

Date: 2026-10-15. Mode: Operate. Scope: refine the existing scanner; preserve Vedha branding and current authorization, scan engines and plan rules.

Research: [primary sources and executable policy audit](../research/2026-10-15-engagement-scanner-ux-and-safety.md). Visual authority: [existing Vedha design system](../design/design-system.md), globals.css and PageShell. No new visual identity is introduced.

| Decision | Interface and acceptance check |
|---|---|
| Primary job | Select engagement, choose engagement assessment or deep scan, verify target and launch. One primary action for the visible task. |
| Intensity | Native radio group: Stealth / Normal / Aggressive; Normal default, preserve each engagement's choice in the browser session. Descriptions follow actual engine behavior. No speedometer, IDS avoidance claim or false full-port promise. |
| Deep | Select exactly one IP from that engagement's discovered assets; allow one manually entered IP when needed. IPv4 and IPv6 literals only, host prefix allowed; reject lists, ranges, malformed IPs, exclusions and out-of-scope values. Server remains authoritative. |
| Scope | Inherit engagement boundaries; editable target narrowing and exclusions are in one Advanced scope disclosure. Changing engagement clears the deep IP, stale jobs and probe selection. Old asynchronous responses cannot replace the new engagement's data. |
| Readiness | Loading/error/empty are distinct. Missing catalog, failed setup, absent authorized scope or no capable online agent prevents launch. Deep uses the deep-capable selected agent. Portal quotas and repeat policy remain enforced. |
| Brand | Existing system font; 4px spacing scale; neutral flat surfaces; blue #1D4ED8 light / #60A5FA dark only for actions, focus and selection. Severity colors never encode scan intensity. |
| Results | Real job state and history, with advanced execution evidence collapsed. No scan is run as part of visual QA. |
| Attack paths delivery | Main already includes PR #20 and version 1.0.408. Remove the frontend build-only hiding of the new operator workspace; retain backend feature, tenant, role and engagement gates. Make the dashboard's environment entry explicit and distinguish stored per-engagement results. Explicit overview URL remains available. |
| Verification | Unit tests for target cardinality/parser/boundaries and request payloads; engagement switch/race and native keyboard controls exercised with isolated fixtures; type, lint, build; one batched desktop/mobile/theme review, one repair pass if required. |

No backend scan intensity defaults, rate limits, fragile-host protections, entitlement rules or attack-path evidence gates are relaxed. No schema migration is needed. Revert this UI/configuration commit to roll back.

## Verification completed

- Frontend: 749 tests in 81 suites pass; changed-file ESLint, type check and standard production build pass. The build does not set the removed attack-path frontend feature flag.
- Backend: 80 existing scope-target, portal policy, operator deep-scan and enqueue-intensity tests pass. Backend policy and scan engine source are unchanged.
- Browser: engagement mode memory, target reset on engagement change, native arrow-key mode selection, excluded IP filtering, manual multi-IP rejection and foreign-scope rejection were exercised. An isolated simulated dispatch sent one target, the selected engagement and the selected deep-capable agent, without rate/concurrency overrides. No network scan occurred.
- Production HTTP seam: default attack-path workspace, explicit overview, and dashboard entry all serve the environment link without a build flag. Six malformed/list/range request variants return 422 before enqueue.
- Design: mechanical detector returned no findings. Desktop and phone layouts, light and dark themes reviewed in one batch; one repair batch and confirmation completed. Existing brand tokens preserved.
- Live-environment limitation: the original local API, PostgreSQL and Redis were not listening. The Docker executable is a dangling link to an absent Docker Desktop application. The frontend was restarted on 3114 against its original API address; it needs those existing backend services restored. The separate localhost:3115 UI preview uses explicitly named UI-test engagements and a simulated agent on a fixture-only backend. It is not a live environment assessment.
