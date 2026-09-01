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
| Product/action | `#0F766E` | `#5EEAD4` | Primary actions, links, selection, active work |
| Critical | `#B91C1C` | `#FF5C6C` | Confirmed or imminent severe exposure; immediate response |
| High | `#C2410C` | `#FF8A3D` | Urgent exposure requiring near-term action |
| Medium | `#A16207` | `#F5C84C` | Time-bounded remediation; investigate and schedule |
| Low | `#2563EB` | `#60A5FA` | Monitor or routine hardening; blue avoids implying healthy |
| Healthy/verified | `#16825D` | `#4ADEA3` | Verified, completed, online, or within SLA only |
| Primary text | `#18202B` | `#EEF3F8` | Headings and decisive content |
| Secondary text | `#4E5B6B` | `#B8C4D0` | Supporting content |
| Canvas | `#F4F6F8` | `#0C1118` | Page background |
| Panel | `#FFFFFF` | `#121923` | Data surfaces |

Green is never used for low severity: a low-risk finding is still a finding.
Red is reserved for critical conditions and destructive actions so it retains
urgency. Teal identifies navigation and operator intent, not risk.

## Priority mapping

| Priority | Label | Color role |
| --- | --- | --- |
| P0 | Immediate | Critical red |
| P1 | Urgent | High orange |
| P2 | Planned | Medium amber |
| P3 | Monitor | Low blue |
| P4 | Low | Neutral slate |
| P5 | Informational | Muted slate |

Severity communicates technical impact. Priority communicates response order;
the two must remain visibly distinct and must not be treated as synonyms.
Composite finding risk uses the Manager's 0–1000 contract. Detection-engine
posture scores are normalized once at the backend boundary; the browser never
recalculates the underlying risk.

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
- "Exploit confirmed" is reserved for backend exploit validation. Evidence
  verdicts such as confirmed, corroborated, or contradicted remain a separate
  filter so the two validation domains cannot be confused.
- Red marks active exploitation, SLA breach, and critical exposure; orange marks
  high urgency; amber marks review or detection uncertainty; blue marks lower
  severity; teal marks selection and operator action. Every color is paired
  with text and, where useful, an icon.
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
