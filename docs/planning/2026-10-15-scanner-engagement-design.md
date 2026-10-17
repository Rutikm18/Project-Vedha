# Engagement scanner design and delivery checks

Date: 2026-10-15. Mode: Operate. Scope: refine the existing scanner; preserve Vedha branding and current authorization, scan engines and plan rules.

Research: [primary sources and executable policy audit](../research/2026-10-15-engagement-scanner-ux-and-safety.md). Visual authority: [existing Vedha design system](../design/design-system.md), globals.css and PageShell. No new visual identity is introduced.

| Decision | Interface and acceptance check |
|---|---|
| Primary job | Select engagement, choose engagement assessment or deep scan, verify target and launch. One primary action for the visible task. |
| Intensity | Native radio group: Stealth / Normal / Aggressive; Normal default, preserve each engagement's choice in the browser session. Descriptions follow actual engine behavior. Retain the familiar intensity dial as a selection indicator, with a neutral track and brand-blue needle. It represents intensity, not throughput; no IDS avoidance claim or false full-port promise. |
| Deep | Select exactly one IP from that engagement's discovered assets; allow one manually entered IP when needed. IPv4 and IPv6 literals only, host prefix allowed; reject lists, ranges, malformed IPs, exclusions and out-of-scope values. Server remains authoritative. |
| Scope | Inherit engagement boundaries; target scope stays visible in the existing setup column; exclusions use a disclosure. Changing engagement clears the deep IP, stale jobs and probe selection. Old asynchronous responses cannot replace the new engagement's data. |
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

## Refinement of the existing console

The first simplification removed too much of the incumbent scanner and was rejected by the user. Preserve its information structure: actual fleet availability, the Network Vulnerability Assessment workflow, and the split between target setup and intensity/launch review. Keep scan history and active-job details in their established positions.

- Use familiar terms: **Configure & launch**, **Target and agent**, **Scan type**, **Target scope**, **Launch scan**, and **Deep scan · one IP**. Explain the active preset once, beside its controls.
- The workflow stage list describes the existing pipeline; it does not pretend to be live scan progress. Fleet counts use actual online agents, and scanning counts exclude offline agents.
- Retain keyboard-operable native radio groups and all one-IP, engagement boundary, exclusion, entitlement and stale-response protections. Disable workflow switching during dispatch. Correct the portal fleet destination to `/portal/fleet`.
- Stack the review below setup on phones. Move the campaign link below the workflow description so the text keeps its reading width; reserve enough room for the Aggressive label.
- Preserve version **1.0.408** and all attack-path delivery changes. This refinement changes presentation and wording; it does not change scan engines or scan policy.

Refinement verification: all 749 frontend tests passed before the final copy adjustment; the 22 affected scanner/entitlement tests and changed-file lint pass afterward. The production build passes. Browser checks covered native arrow-key intensity selection, per-engagement mode memory, engagement reset of the deep IP, filtering of excluded assets and multi-IP rejection. Desktop/phone and light/dark review found two layout issues, corrected together and confirmed. The manual design detector returned no findings. Scanner primary buttons now use the existing `--accent-contrast` token for readable dark-mode text. Live backend limitations above still apply; the preview remains fixture data.

## Color and motion refinement

Preserve the fleet/workflow/configuration structure. Give the workflow a restrained blue tint and solid brand-blue icon, and use Lucide icons and connectors to make its existing sequence easier to scan. Fleet online counts and the actual idle-agent readiness indicator use the existing teal nominal token; scanning counts use blue only when nonzero. Intensity remains entirely within the product blue palette, with a highlighted arc, minor ticks and a selected needle. No severity colors represent intensity.

Motion purpose: selection feedback and bridging scan-type content changes. Pointer selection retargets a 240ms needle transition from its current rotation, using Vedha's existing `--ease-out`. New content settles over 180ms with 4px movement; keyboard interaction is instant. Native radio semantics and focus remain intact. Reduced motion removes transforms and transitions, including press scaling, and cancels the native intro fade if the preference changes. No continuous radar sweep, artificial progress, count animation or moving data is added.

React Bits reference: [Animated Content](https://reactbits.dev/animations/animated-content), its [official source](https://github.com/DavidHDev/react-bits/blob/main/src/ts-default/Animations/AnimatedContent/AnimatedContent.tsx), and [Fade Content](https://reactbits.dev/animations/fade-content). The scanner uses the mount-reveal pattern as inspiration, implemented locally with a small native Web Animations fade and CSS state transitions. It does not install or copy the GSAP implementation. Existing timing, theme and contrast tokens are authoritative; no animation dependency or new font is added.

Color/motion validation: 30 affected scanner, entitlement and preset-parity tests pass; TypeScript, changed-file ESLint and the standard production build pass. The design detector returned no findings. A batched desktop/phone review covered light/dark themes, one-IP form, native keyboard selection and selection indicators. Browser computed styles confirm pointer input uses the 240ms dial transition and arrow-key input uses 0ms. The final repair also suppresses press scaling for keyboard input. Scan policies and backend code are unchanged; the running preview continues to use labeled fixtures and no scan was dispatched.

## Original UI restoration — 2026-10-16

The user rejected the replacement styling and explicitly requested the original UI, organized properly. This direction supersedes the prior blue-only intensity and React Bits-inspired presentation decisions. The original scanner in the primary checkout and commit `4045ee3d` are the visual reference.

Restore the three-zone mint/blue/orange dial, campaign gradient and selected corner accents, original campaign-stage chips, profile/runtime metadata from the catalog, complete agent chips with status/capabilities/location hints, visible scope/exclusion fields, detailed readiness counts, and familiar launch/review grouping. Organize these into aligned desktop columns with consistent field spacing, and stack the same content on narrow screens. Remove the new icon-chain treatment and content entrance effects. Preserve the existing system font and global theme.

The original dark-mode mint is #6EE7B7. Light mode uses #0F766E for readable text; Normal keeps product blue and Aggressive retains the original orange family. The displayed rate comes from the verified current preset metadata and is labeled **preset rate**. Do not restore the old stale 600 pps value or portray configured rates as measured throughput.

Retain the current native radio behavior, engagement mode memory, single-IP picker, scope/exclusion validation, quotas, dispatch locks and stale-response protections. Scan engines, API policy, attack paths and version 1.0.408 are unchanged. Source checks: 30 relevant scanner/entitlement/preset tests, TypeScript and changed-file lint pass. The manual design detector returned no findings.

Restoration verification completed: production build passes. Desktop and phone layouts were checked in both themes; native arrow-key intensity selection works, both scope fields remain visible, and all agent chips retain their status and capability labels. A phone fleet-wrap regression found during confirmation was corrected and verified, together with the dark scrollbar. The preview remains fixture-only; no scan was dispatched.
