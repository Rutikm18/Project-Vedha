# Engagement scanner: research, interaction model and acceptance checks

Date: 2026-10-15 · Status: implementation recommendation based on current code and primary sources; no scans run for this research.

## Product decision

Use one engagement-scoped scanner workspace. The primary task is **choose engagement → choose assessment coverage → verify scope → launch**. Keep **Stealth / Normal / Aggressive** as the three named assessment presets and offer **Deep scan · one IP** as a separate, explicit task. Normal is the default. Do not present Deep as a fourth point on an intensity dial: it changes the target cardinality and all-port capability, not merely speed.

This is an application of the evidence below, not a claim that any cited standard specifies Vedha's exact UI. There is no universal expert-dashboard layout: clarity, accurate scope, predictable actions, recoverable errors and measured task success are the useful quality bar.

## Existing Vedha behavior, checked before proposing changes

Read alongside [the design system](../design/design-system.md), [the existing interface checkpoints](2026-10-05-expert-product-ui-ux-framework-research.md), [the full-port design and review](../planning/2026-10-09-full-port-deep-scan-design.md), [enterprise Aggressive redesign](../superpowers/plans/2026-09-25-aggressive-enterprise-redesign.md) and [coverage research](2026-10-09-network-va-coverage-framework.md). Historical plans contain superseded limits; executable policy is authoritative.

| Visible choice | Actual current code | Truthful concise description |
|---|---|---|
| Stealth | `light`: quick TCP profile (15 ports), 50 probes/s, concurrency 20, no extra silence retries; narrow UDP catalogue | Lower traffic, focused coverage. It remains an active scan. |
| Normal | `standard`: IT/IoT/OT profile catalogue, 200 probes/s, concurrency 100, one extra silence retry; narrow UDP catalogue | Balanced coverage for routine assessments. |
| Aggressive | `deep`: curated enterprise TCP profile (~2,500 ports), 150 probes/s, concurrency 80, two extra silence retries; wider UDP catalogue | Broader coverage and additional retries. Usually takes longer. |
| Deep scan · one IP | `uc_deep_port_sweep`: all 65,535 TCP ports, assessment on discovered services; exactly one host inside the engagement's allowed scope and outside exclusions | Full TCP-port assessment of one selected IP. |

Sources: `probe/workflow/intensity.py`; `manager/backend/app/services/portal_scan_policy.py`; operator enqueue validation in `manager/backend/app/routers/agents.py`; shared request builders in `manager/frontend/lib/scan-launch.ts`. Preset rates are configured envelopes, not measured sustained throughput, end-to-end HTTP request rates or an ETA. An actual capability's forced port profile can override general breadth.

**Copy defect found:** `manager/frontend/lib/scan-intensity.ts` still describes Aggressive as an all-65,535-port time-budget sweep. The executable preset is the enterprise set. Its Stealth copy also implies reduced IDS/IPS triggers; use lower traffic/focused coverage instead. Assessment mode can still include service, OS and application checks at each preset: Stealth is neither passive-only nor guaranteed harmless to fragile assets. The existing server-side OT/passive and fragile-asset restrictions remain authoritative.

**Validation gap to cover:** `isSingleHost()` in the shared frontend request builder rejects obvious multi-target delimiters and prefixes but does not parse an IP literal. The DeepScanCard and backend perform stricter checks. A malformed hostname can pass the builder alone. Use an actual IPv4/IPv6 parser in the affected entry points and test rejection in the authoritative backend; do not imply this frontend helper proves authorization.

## Primary-source evidence and interpretation

| Primary source, checked 15 October | What it establishes | Application to this design |
|---|---|---|
| [Nmap timing templates](https://nmap.org/book/performance-timing-templates.html) | Timing templates alter delays, timeout and retry behavior. Reduced pacing can greatly increase duration; timing alone does not describe application-probe effects. | Describe traffic, coverage and expected tradeoff separately; never make a speedometer or equate Aggressive with highest rate. Vedha's presets are not Nmap `-T` aliases. |
| [Nmap version detection](https://nmap.org/book/man-version-detection.html) | Version intensity chooses probes; additional probes trade time for identification. Nmap skips printer port 9100 by default because probe data may print. | Discovery breadth and service-check depth are distinct. Preserve fragile-service safeguards; do not promise all application probes are harmless because pacing is low. |
| [Nmap NSE usage](https://nmap.org/book/nse-usage.html) | `safe` scripts are designed to avoid certain disruptive effects but are not guaranteed free of adverse reactions; the default set can include intrusive scripts. | Named profiles must resolve to actual approved checks. Neither a safe tag nor a profile label warrants a zero-impact badge. |
| [ProjectDiscovery Nuclei running documentation](https://docs.projectdiscovery.io/opensource/nuclei/running) | Global request limits, parallel hosts and parallel templates are independent controls. Templates/tags can be excluded; code, headless and fuzzing execution require distinct switches; default exclusions are configurable. | A preset should resolve to a known bounded envelope and approved capabilities. Do not infer safe execution from the word Aggressive or automatically enable excluded intrusive checks. |
| [NIST SP 800-115, §4.3 and Appendix B](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf) | Assessment planning defines scope, permitted actions and constraints. Vulnerability scans can affect hosts/network performance; scanner results require interpretation and can include false positives. | Keep engagement and exact target visible before launch, enforce policy on the server, preserve stop controls and show coverage limitations beside results. Findings count alone does not establish successful or complete assessment. |
| [OWASP WSTG introduction, repository source](https://raw.githubusercontent.com/OWASP/wstg/master/document/2-Introduction/README.md) | Testing should adapt to architecture, threat model and risk. Automated tools complement expert analysis; reporting explains what and how testing occurred. | Use technical evidence and coverage to explain results. Avoid “secure”, “complete protection” or business-logic coverage claims based on a completed network job. This is methodology guidance, not a network scanning preset standard. |
| [NN/g progressive disclosure](https://www.nngroup.com/articles/progressive-disclosure/) | Show frequent important choices first and make secondary options discoverable with clear labels. Hiding essential choices impedes tasks. | Keep engagement, target summary, three presets and primary action visible. Put advanced probe routing, exclusions and capability details under one clearly named disclosure. Do not hide the one-IP requirement or scope behind it. |
| [W3C form grouping](https://www.w3.org/WAI/tutorials/forms/grouping/), [radio group pattern](https://www.w3.org/WAI/ARIA/apg/patterns/radio/) | Related choices need programmatic grouping; a radio group represents one selected option and supports expected keyboard navigation. | Use native radios within a fieldset/legend for presets and one-host selection. A visual card is a label around a radio, not an unrelated toggle. |
| [W3C form notifications](https://www.w3.org/WAI/tutorials/forms/notifications/) | Identify and describe errors in text, connect errors with fields and use accessible notifications appropriately. | Put an actionable error beside the IP field, retain input after rejection and announce queue success/failure without moving focus unexpectedly. |

## Information hierarchy and brand application

| Location | Required visible content | Keep secondary |
|---|---|---|
| Page header | Scanner title, one-sentence purpose, selected engagement | Product marketing, large radar, animation and repeated introductory text |
| First configuration row | Engagement selector; authorized scope summary and exclusions count | Full CIDR inventory, long rules-of-engagement text |
| Primary assessment area | Stealth / Normal / Aggressive, short tradeoff for each; Normal default; explicit target count | Raw rates/retries/concurrency unless requested through “Scan details” |
| Deep scan area | “Deep scan · one IP”; single-selection IP control scoped to that engagement; “All 65,535 TCP ports”; dedicated launch action | No multi-select chips, CIDR textarea, IP import or second target control |
| Launch boundary | Exact engagement, selected target/scope, chosen preset, available agent state; one unambiguous action | Avoid a generic extra approval modal for ordinary authorized launch |
| Work in progress | Queue/running state, actual stage, trustworthy coverage, cancel when supported | Detailed diagnostic logs and engine metadata |
| Below configuration | Engagement-filtered recent scans; status, target, started time, coverage/result link | Full history and log detail behind an explicit link/disclosure |

Use Vedha's system-font stack, 4px spacing, panel/surface tokens, hairline borders and 6–10px radii. Selected controls and primary actions use `--accent` (light `#1D4ED8`; dark `#60A5FA`). Reserve severity colors for vulnerability severity, nominal teal for verified/resolved health, and purple for AI content. Preset cards should use neutral surfaces plus blue selection, not green “safe Stealth” and orange/red “dangerous Aggressive”. Selection needs text/check state plus contrast, not color alone. This follows the repository's brand semantics; it is not a new palette.

At narrow widths stack controls in task order, keep the single-IP requirement beside the field and allow wrapped long engagement names/IP addresses without horizontal page overflow. Keep primary controls keyboard accessible and visibly focused in both themes. The repo's existing WCAG checkpoints distinguish AA minimums from optional 44px touch targets; do not market a Lighthouse score as full WCAG conformance.

## Failure modes and acceptance checks

| Failure | Acceptance check |
|---|---|
| User picks a new engagement but an old target/probe remains selected | Clear/revalidate engagement-dependent targets and agent selection; pending responses cannot restore data from the previous engagement. |
| One-IP request silently expands to the engagement CIDR or discovered hosts | Deep launch always carries one normalized host target; backend rejects empty/list/range/non-host-prefix input for both operator and portal routes. No network job is queued on rejection. |
| One IPv4/IPv6 address entered but outside scope or explicitly excluded | Normalize and enforce IP family, scope containment and exclusion server-side. Test IPv4, IPv6, `/32`, `/128`, malformed literals, ranges, comma/space/newline lists and excluded hosts. |
| UI makes Aggressive mean fastest or Deep means every protocol | Assert copy against actual preset definitions; Deep says full **TCP** coverage and reports any UDP separately. Rates remain envelope metadata, not performance promises. |
| “Stealth” is assumed passive/undetectable or a fragile target is implied safe | Short copy states reduced traffic/focused coverage; preserve existing OT/passive, fragile-asset and engagement policy gates without inventing bypasses. |
| Client hides a mode but raw API bypasses entitlement/authorization | API tests preserve live membership/tenant, engagement scope, entitlement/quota and permitted-use-case checks. Operator and portal allowance policies stay distinct. |
| A disabled launch gives no reason | Put the actual missing prerequisite beside it: select engagement/IP, no eligible probe, not authorized or allowance unavailable. Preserve input after retry. |
| Repeated clicks enqueue duplicate scans | Submit state prevents repeated launch in-flight; retain existing server idempotency/dispatch protections where available and verify one request per action. |
| Queue state is presented as running, failure as empty results, or partial coverage as clean | Separate queued/running/completed/failed/cancelled states; show genuine stage/coverage; unreached checks remain not scanned/unknown. |
| Results from a different engagement appear in history | History and results links use selected authorized engagement; changing engagement clears or refreshes cached rows with visible state. |
| A redesign improves the screenshot but breaks ordinary use | Test keyboard-only selection → IP validation → request preview/error recovery without launching a real scan; verify phone/laptop, long labels, both themes and reduced motion. |

## Small achievable implementation slices

1. Capture the current route, brand tokens and baseline states; compare actual runtime version and feature flags with main.
2. Correct preset semantics/copy and consolidate the visible task hierarchy while reusing the existing launch contracts.
3. Add or polish engagement-scoped single-IP selection and reset/revalidation behavior; retain strict backend policy.
4. Make launch prerequisites, queued/running feedback and recent scan context concise and recoverable.
5. Verify affected request/authorization tests, keyboard and responsive behavior, both themes and production build. Use mocked or isolated fixtures for UI verification; this design work does not require scanning a customer target.

Research limits: no field usability study, customer scan or throughput measurement was performed. Rates and behavior above reflect the inspected source tree on this date and must be rechecked when preset definitions change. Existing older plans and comments are not evidence of live capabilities.
