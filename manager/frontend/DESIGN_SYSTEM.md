# Vedha interface system

Vedha uses color as an operational signal. Color never carries meaning alone:
every signal is paired with a label, count, icon, or state text.

## Typography

- UI and narrative text: native system sans (`-apple-system`, `BlinkMacSystemFont`,
  `Segoe UI`, `Inter`, `Roboto`, `Helvetica Neue`, `Arial`). It is fast, neutral,
  and familiar on operator workstations.
- Evidence and machine data: `SFMono-Regular`, `Cascadia Code`, `Roboto Mono`,
  `Consolas`, monospace. Reserve it for IPs, ports, identifiers, timestamps, and
  scores; do not use it for paragraphs or navigation.
- Numerals use tabular figures when alignment or comparison matters.

## Semantic colors

| Meaning | Light | Dark | Use |
| --- | --- | --- | --- |
| Product/action | `#1D4ED8` | `#60A5FA` | Primary actions, links, selection, active work |
| Critical | `#B91C1C` | `#F87171` | Confirmed or imminent severe exposure; immediate response |
| High | `#C2410C` | `#FB923C` | Urgent exposure requiring near-term action |
| Medium | `#A16207` | `#FBBF24` | Time-bounded remediation; investigate and schedule |
| Low | `#78716C` | `#A8A29E` | Monitor or routine hardening; stone does not imply healthy |
| Informational | `#64748B` | `#94A3B8` | Context, hygiene, and non-urgent observations |
| Healthy/verified | `#0F766E` | `#5EEAD4` | Verified, completed, online, or within SLA only |
| Machine/AI | `#7C3AED` | `#A78BFA` | Machine-generated explanation or recommendation |
| Primary text | `#0F172A` | `#F1F5F9` | Headings and decisive content |
| Secondary text | `#475569` | `#94A3B8` | Supporting content |
| Canvas | `#F3F6FA` | `#111318` | Primary page background and spacing between sections |
| Panel | `#FFFFFF` | `#161820` | Primary data and task surfaces |
| Card | `#FFFFFF` | `#181B24` | Contained records within a page region |
| Secondary surface | `#F8FAFC` | `#1C1F28` | Rows, controls, and nested grouped content |
| Subtle border | `#DCE3EC` | `#252A35` | Section and row separation |
| Default border | `#C5D0DE` | `#343A48` | Controls and stronger container boundaries |

Green is never used for low severity: a low-risk finding is still a finding.
Red is reserved for critical conditions and destructive actions so it retains
urgency. Blue identifies navigation and operator intent. Teal is reserved for
verified or healthy outcomes, and violet identifies machine-generated content.

Across the product, light mode uses a cool `#F3F6FA` canvas so white task
surfaces remain visually distinct. Nested controls and grouped rows use
`#F8FAFC`; they do not create another white card. Dark mode steps from the
`#111318` canvas through `#161820` panels, `#181B24` cards, and `#1C1F28`
nested surfaces. Neutral borders define structure while semantic colors retain
their established meanings in both themes.

## Surface hierarchy

- Canvas separates major page regions and should remain visible around panels.
- Panels contain one operational section, such as a queue, configuration area,
  timeline, or report block. They use the subtle border role.
- Cards represent records inside a section. Avoid wrapping every paragraph or
  metric in another card.
- Secondary surfaces group controls, table headers, nested facts, and read-only
  evidence. They should contrast with their parent panel.
- Default borders identify controls or important boundaries. Strong borders are
  reserved for hover, selection, resize handles, and deliberate emphasis.
- Shadows indicate actual elevation such as menus and dialogs; borders carry
  ordinary section separation.

## Brand mark

Vedha retains its original shield mark across operator navigation, customer
navigation, authentication, and the favicon. The shield uses the product/action
blue token so it remains legible and consistent in both themes.

## Priority mapping

| Priority | Label | Color role |
| --- | --- | --- |
| P0 | Immediate | Critical red |
| P1 | Urgent | High orange |
| P2 | Planned | Medium amber |
| P3 | Monitor | Low stone |
| P4 | Low | Neutral slate |
| P5 | Informational | Muted slate |

Severity communicates technical impact. Priority communicates response order;
the two must remain visibly distinct and must not be treated as synonyms.
Priority is never derived from severity in the browser. The server applies an
ordered rule set (first match wins) over real signals (known-exploited, validated
exploit, EPSS, SLA state) and returns the priority with the deciding rule;
closed findings carry no priority, so no chip is rendered for them.
Composite finding risk uses the Manager's 0–1000 contract. It is additive and
explainable: impact (CVSS + severity) is 40%, exploit likelihood (EPSS + KEV +
validated exploit) is 25%, asset/exposure context is 20%, and verification
quality is 15%. An upstream posture score never maps directly to 1000.
The score is shown with its full working ("How the score is calculated" on the
finding Overview, for operators and customers): every input with its value and
whether it was recorded or defaulted, the weighted sum, the severity-band
placement, and the priority rules with the deciding one marked. The browser only
words what `GET /findings/{id}/risk-explanation` returns; it never recomputes.

## Findings decision model

The Findings page is ordered around the analyst's decisions, not around the
database schema:

- Portfolio metrics answer "how much exposure exists?" They render an em dash
  while the summary is unavailable because an unverified zero would imply a
  safe state.
- The queue begins immediately after portfolio metrics; it does not repeat the
  same posture in a second hero or glossary panel. Search, engagement, agent,
  and sort remain visible while severity, lifecycle, evidence, and risk-signal
  filters use a single "More filters" disclosure.
- Finding records are compact rows. Severity, lifecycle, title, affected host,
  response priority, Manager risk `/1000`, CVSS, EPSS, SLA, and evidence state
  remain scannable without turning each metric into a separate box. Only active
  attention signals add a short text-and-icon line.
- Finding detail follows the same operational sequence: Overview establishes the
  summary, impact, recommended next action, and affected-system facts. Technical
  scoring and attack correlation use disclosures so Evidence, Remediation, and
  History remain the primary review views. Threat-intelligence and compliance
  views remain outside the detail navigation until their data contracts and
  decision use are ready for operators.
- Lifecycle actions use one explicit action selector. The reason composer appears
  only after an action is chosen, reducing competing controls while preserving
  the same auditable backend workflow.
- Lifecycle actions require a concise reason in the interface. The Manager stores
  that reason with the append-only event—not in the mutable finding narrative—so
  accepted risk, false-positive, remediation, and reopen decisions remain auditable.
- "Exploit confirmed" is reserved for backend exploit validation. Evidence
  verdicts such as confirmed, corroborated, or contradicted remain a separate
  filter so the two validation domains cannot be confused.
- Red marks active exploitation, SLA breach, and critical exposure; orange marks
  high urgency; amber marks review or detection uncertainty; stone marks lower
  severity; blue marks selection and operator action; teal marks verified health. Every color is paired
  with text and, where useful, an icon.
- Accepted risk uses amber because the exposure remains unresolved and requires
  governed review; violet stays exclusive to machine-generated content.
- Loading, failure, and empty states make different claims. Failure never renders
  "all clear" and always gives the operator a retry path.

## Layout and interaction

- Use the shared 4/8-based spacing tokens and align labels, values, and controls
  to the same panel edges.
- Operational cards need a title, a time/scope qualifier, and an honest empty,
  loading, and error state.
- Charts require visible labels and exact values in tooltips or legends.
- Interactive targets are at least 44 px on coarse pointers, have keyboard focus,
  and do not depend on hover.
- Motion explains state change only and respects `prefers-reduced-motion`.

## Console UX principles

These govern layout and flow decisions, alongside the signal-colour rules above.
They come from a review of the shipped pages plus practitioner guidance on
security consoles (sources at the end). Treat the sources as direction, not proof:
they are mostly vendor and design-agency writing, not controlled studies.

1. **The primary task is above the fold.** Each page has one job (triage the
   queue, launch a scan, approve a device). That surface starts in the first
   viewport; context, history and explainers follow or collapse.
2. **Order follows state, not a template.** An empty Fleet leads with onboarding;
   a populated one leads with pending approvals, then agents. A customer list
   leads once customers exist. Use CSS `order` so DOM order (and reading order for
   assistive tech) stays stable.
3. **Design by subtraction.** Do not repeat a row, count or explanation that is
   already on screen (e.g. fix-first cards are omitted when the queue is short;
   the ranking key hides while a finding is open). Disclose detail on demand.
4. **Page actions are never clipped.** Header actions keep their size; the title
   and subtitle ellipsize first, then status chips scroll or hide. Chips are
   redundant context, actions are not.
5. **Honest states.** Loading, failure, empty and "not recorded" are different
   claims. Never print `undefined`, never imply liveness (no decorative heartbeat
   with zero agents), and every empty state names the next action and links to it.
6. **State lives in the URL when people will share or return to it.** Settings
   sections use `?section=`, so they can be linked, refreshed and reached from
   other pages (AI Brain links to its runtime settings).
7. **Group long navigation.** More than about seven sibling items get labelled
   groups; the card scrolls internally on short screens.
8. **Touch targets are 44 px where a thumb acts**, with the drawn control smaller
   than its hit area (see the finding row checkbox).
9. **Size responsive controls to their container**, not the viewport: beside a
   sidebar or detail pane a panel is much narrower than the screen (container
   queries on the Findings filter panel).
10. **Copy is part of the interface.** Singular and plural agree ("1 target"), a
    sentence ends once, and server-supplied text is normalised before display.

Sources consulted: NopSec on vulnerability-prioritisation UX
(nopsec.com/blog/designing-a-new-user-experience-for-vulnerability-prioritization),
Fuselab on SOC dashboard design (fuselabcreative.com/cybersecurity-dashboard-design),
Edgescan on noise reduction through design, Basis and SAP Fiori design-system
guidance on dense tables, saved views and density, and public write-ups of Linear
and Vercel interface conventions (keyboard-first, subtle borders, colour reserved
for meaning). Wiz-, Snyk- and CrowdStrike-specific UI teardowns were not found in
searchable form; claims about those products are not relied on here.

## Scan comparison

Compare is a two-scan diff the operator sets up on purpose: nothing is
pre-selected, the same scan cannot fill both sides, and a baseline that ran after
the target is flagged with a swap control. The server decides the buckets:

- New (in the target, not the baseline), Fixed (the reverse), Changed (in both,
  but severity, risk score or status moved) and Unchanged. The view opens on the
  worst news first, and each bucket is a tab rather than a squeezed column so it
  reads the same on a phone.
- Each scan shows what it saw in total (severity bar, average risk). Severity,
  risk and status come from the snapshot each scan recorded, never from today's
  finding, except for older scans that predate snapshots; those say so.
- Lists are capped on screen; CSV and JSON exports carry every row, and Print /
  PDF prints only the comparison.

## Customer portal chrome

The portal uses the product shell, so a customer must never read operator wording in it:
the footer names the surface ("Vedha customer portal"), not "operator console".

- The plan strip states the plan in one line. When every scan type in the plan is open and
  uncapped it says so once ("All scan types, unlimited"); four chips reading "∞" told the
  customer nothing. Per-type chips return as soon as any type is capped, used up or off.
- The page's main action is never only in the header. A header that cannot hold three
  buttons scrolls them out of sight, and the one that mattered (Start scan) went with them.
  Beside the sidebar the header ran out of room at 768px, so up to 900px the engagement
  actions sit in the page (one row of three; full-width buttons below 680px) and the header
  keeps the status. Check a header's actions at 768 as well as at 390 and 1440.
- A report with tabs shows one section at a time. Both sections stay mounted so print and
  PDF carry the whole report, which is why the screen rule that hides the inactive one has
  to exist and the print rule has to override it.
- Tab labels shorten on a narrow screen; they never become icons alone.

## Long lists of sections

A settings area with many sections (fifteen for operators) is one grouped menu below 960px,
not a strip of tabs; a short set (the customer's six) stays as tabs. Tabs are as wide as
their label: the 44px touch-target floor is `!important`, so a content-sized control must say
`min-width: max-content !important` or it collapses and its label spills over its neighbours.

## Campaign views

Pipeline, jobs, findings, raw scanner data and the job queue share one stylesheet
(`components/campaign/campaign-css.ts`): a card is a bordered panel; a section head is a
title, a count and an optional aside; a chip is a small labelled value. Severity and status
always carry a word as well as a colour. Operator-only sections (campaign runs, the
all-engagement probe queue) do not render for a customer: one is always empty for them and
the other repeats the jobs already shown in their pipeline.

## Reports (operator)

Export, both print copies and the downloads are one menu ("Export & print"). The engagement
picker, the draft status and a one-line note share one block, and the AI draft panel is a
single line until a draft needs review, so the report itself is what the page opens on.
