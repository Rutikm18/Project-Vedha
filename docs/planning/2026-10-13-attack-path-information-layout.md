# Attack-path investigation layout

## Task and diagnosis

An analyst needs to establish scope, understand the captured result, inspect a connection or finding, and decide what evidence or remediation to review next. The previous layout used an expanded selection panel, repeated headings and qualifications, an empty 510px map and a second investigation below the graph. Those regions pushed the useful finding and its next action out of the first viewport.

This refinement retains Vedha's brand, theme, existing API and finding-backed accuracy contract. It changes information placement and progressive disclosure, rather than adding inferred data or another attack engine.

## Information placement

| Analyst decision | Location | Behaviour |
| --- | --- | --- |
| Which assessments am I reviewing? | Compact scope strip at the top | Show selected count and names; expand inline to search authorized assessments and change selection. Analyze stays adjacent. |
| Does the displayed result match my selection? | Notice immediately below scope | Retain explicit previous-selection, pending, failed and reassessment notices. Never silently relabel an older result. |
| What data is available? | Captured-scope and coverage row | Show assessment/finding coverage before results, with incomplete connection evidence stated explicitly. |
| Do recorded connections exist? | Paths / Findings & evidence tabs | Lead with Paths when connections exist; otherwise lead with captured findings. Explicit tab choices remain stable. Both panels stay mounted so switching views preserves local inspection and fix previews. |
| Which routes matter? | Four compact path measures above the map | Confirmed routes, possible routes, critical assets reached, and enabling findings. Possible routes come from enumerated possible paths, rather than subtracting independently bounded counts. |
| What does this connection mean? | Inspector beside the map on wide containers | Highlight the inspected connection in brand blue; preserve solid/dashed confidence cues. Include the enabling finding in its accessible name. Finding identity, system direction, confidence, severity, source link and recorded remediation remain together. |
| What can I do when connections are missing? | Compact empty result | Show captured systems/findings/critical classifications and a working Review finding evidence action. Withhold the empty canvas and irrelevant map controls. Explain that zero routes is not evidence of safety. |
| What evidence is needed for a finding? | Finding queue, required conditions and evidence inspector | On wide screens, place the selected finding and its missing conditions beside the list, with the inspector to the right. Lead with next action and required evidence; the speculative candidate chain is an optional disclosure. |
| Where did the finding come from? | Selected-finding header and inspector | Retain the original assessment/system and direct links to the source assessment and finding. |
| What changed, and how should I interpret it? | Comparison and reading-guide disclosures | Preserve fixes, dismissals, pending confirmation and missing-record distinctions. Move unavailable grades and method explanation out of primary metrics. |

## Responsive and interaction rules

- Use existing spacing and semantic theme tokens. Keep the shared app shell and navigation.
- A map container below 980px places its inspector below the canvas with a Back to map action. Graph controls provide a text-list alternative and usable touch targets.
- A finding container below 1080px places the condition inspector below the selected finding; below 600px the queue also stacks above the details. Explicit Back to findings and Back to required evidence actions restore focus to the corresponding controls.
- Phone scope controls use a compact row, retain a visible assessment-name summary and expand inline. Long names wrap in the selector and finding queue without inventing shortened identities.
- Tabs support Left/Right, Home/End and standard focus order. Hidden panels stay out of the accessibility tree. Scope search changes the visible options without changing the selection.
- Loading, errors, incompatible captures, read-only roles, empty authorized options, incomplete coverage and changed selection retain explicit recovery information.

## Validation

Use one desktop/phone inspection batch, apply its corrections together, then one confirmation batch. Cover scope search and selection mismatch, keyboard tabs, source-finding selection, condition inspection and return focus, light/dark themes, the actual empty-record state and the separately labelled connected example. Run the frontend regression suite, lint, production build and a final layout detector. Browser measurements are checked directly rather than inferred from the Node tests.

The local environment still contains synthetic findings with no stored connections. The layout must make those records useful without substituting the made-up demonstration graph.
