# Node Description Batch 230 of 380

Graphify is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the prompt below and write
your JSON answer to the answer file.

## Prompt

You are documenting nodes in a knowledge graph.
For each entry below, write ONE concise factual plain-language sentence
describing what it is or does. Use only the provided context.
For a code symbol (kind=code-symbol — a function, class, or constant),
describe what the function/symbol does based on its name, source location
and neighbors — e.g. "Resolves the configured ontology profile from graphify.yaml.".
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "findings_page_detectioncoverage": "DetectionCoverage" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L67 | neighbors=[page.tsx]
- "findings_page_detectionpill": "DetectionPill()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L441 | neighbors=[page.tsx]
- "findings_page_engagementoption": "EngagementOption" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L235 | neighbors=[page.tsx]
- "findings_page_epssbar": "EpssBar()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L268 | neighbors=[page.tsx]
- "findings_page_event_color": "EVENT_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1468 | neighbors=[page.tsx]
- "findings_page_eventactor": "eventActor()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1483 | neighbors=[page.tsx]
- "findings_page_eventdetaillabel": "eventDetailLabel()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1508 | neighbors=[page.tsx]
- "findings_page_eventnarrative": "eventNarrative()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1489 | neighbors=[page.tsx]
- "findings_page_evidencefact": "EvidenceFact" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L115 | neighbors=[page.tsx]
- "findings_page_evidencefacts": "EvidenceFacts()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L744 | neighbors=[page.tsx]
- "findings_page_evidencegallery": "EvidenceGallery()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L640 | neighbors=[page.tsx]
- "findings_page_evidencepresentation": "evidencePresentation()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L618 | neighbors=[page.tsx]
- "findings_page_evidenceview": "EvidenceView()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L764 | neighbors=[page.tsx]
- "findings_page_exploitationview": "ExploitationView" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L107 | neighbors=[page.tsx]
- "findings_page_exploitmaturity": "ExploitMaturity" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L66 | neighbors=[page.tsx]
- "findings_page_finding": "Finding" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L155 | neighbors=[page.tsx]
- "findings_page_findingoverview": "FindingOverview()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1081 | neighbors=[page.tsx]
- "findings_page_findingpage": "FindingPage" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L214 | neighbors=[page.tsx]
- "findings_page_findingrow": "FindingRow" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L2177 | neighbors=[page.tsx]
- "findings_page_findingstatus": "FindingStatus" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L65 | neighbors=[page.tsx]
- "findings_page_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L222 | neighbors=[page.tsx]
- "findings_page_findingsworkspaceapi": "FindingsWorkspaceApi" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L71 | neighbors=[page.tsx]
- "findings_page_findingtimeline": "FindingTimeline" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L86 | neighbors=[page.tsx]
- "findings_page_fmteventts": "fmtEventTs()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L492 | neighbors=[page.tsx]
- "findings_page_fmtrelativets": "fmtRelativeTs()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L499 | neighbors=[page.tsx]
- "findings_page_getlocationsearch": "getLocationSearch()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L93 | neighbors=[page.tsx]
- "findings_page_getserverlocationsearch": "getServerLocationSearch()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L97 | neighbors=[page.tsx]
- "findings_page_intelpanel": "IntelPanel()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1309 | neighbors=[page.tsx]
- "findings_page_kevbadge": "KevBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L377 | neighbors=[page.tsx]
- "findings_page_kill_chain_phase_color": "KILL_CHAIN_PHASE_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L83 | neighbors=[page.tsx]
- "findings_page_killchainstep": "KillChainStep" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L152 | neighbors=[page.tsx]
- "findings_page_killchainviz": "KillChainViz()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L570 | neighbors=[page.tsx]
- "findings_page_maturity_color": "MATURITY_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L74 | neighbors=[page.tsx]
- "findings_page_needsreviewchip": "NeedsReviewChip()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L405 | neighbors=[page.tsx]
- "findings_page_portalfindings": "PortalFindings()" | kind=code-symbol | source=manager/frontend/app/portal/findings/page.tsx:L161 | neighbors=[page.tsx]
- "findings_page_portalfindingspage": "PortalFindingsPage()" | kind=code-symbol | source=manager/frontend/app/portal/findings/page.tsx:L6 | neighbors=[page.tsx]
- "findings_page_prefersreducedmotion": "prefersReducedMotion()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L298 | neighbors=[page.tsx]
- "findings_page_priority": "Priority" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L68 | neighbors=[page.tsx]
- "findings_page_priority_color": "PRIORITY_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L80 | neighbors=[page.tsx]
- "findings_page_prioritybadge": "PriorityBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L352 | neighbors=[page.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-229.json

Keep each description factual and concise (one sentence). No markdown, no prose
outside the JSON object. It is acceptable to omit a node if context is
insufficient — but include every node you can ground confidently.

Example answer format:
```json
{
  "node_id_1": "Resolves the configured ontology profile from graphify.yaml.",
  "node_id_2": "Colonel James Barclay, an antagonist in The Crooked Man."
}
```
