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
Composite finding risk uses the Manager's 0–1000 contract. It is additive and
explainable: impact (CVSS + severity) is 40%, exploit likelihood (EPSS + KEV +
validated exploit) is 25%, asset/exposure context is 20%, and verification
quality is 15%. An upstream posture score never maps directly to 1000.

## Findings decision model

The Findings page is ordered around the analyst's decisions, not around the
database schema:

- Portfolio metrics answer "how much exposure exists?" They render an em dash
  while the summary is unavailable because an unverified zero would imply a
  safe state.
- Visible queue triage answers "what needs action on this page?" Its scope is
  explicit because urgency and SLA counts are calculated from the loaded page,
  not the entire portfolio.
- The triage-model explanation is a disclosure. It keeps severity, priority,
  and risk definitions available without pushing the working queue below a
  permanently open legend.
- Analyst queue controls use persistent labels and explicit sort options.
  Predictable controls are safer than cycling buttons when filters affect an
  operational decision set.
- Finding cards read in decision order: severity and lifecycle, P0–P5 response
  priority, Manager risk `/1000`, affected host, decision drivers, then evidence
  metrics. "Why now" chips expose the facts that influence urgency instead of
  asking the analyst to infer them from color.
- Finding detail follows the same operational sequence: Overview establishes the
  affected system and decision context; Evidence preserves reviewable artifacts;
  Remediation renders the Manager's structured, OS-aware plan; History explains
  stored operator actions and system observations. Threat-intelligence and
  compliance views remain outside the detail navigation until their data
  contracts and decision use are ready for operators.
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
