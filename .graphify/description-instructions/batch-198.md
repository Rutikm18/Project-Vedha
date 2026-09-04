# Node Description Batch 199 of 330

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

- "exposure_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/analytics/exposure/route.ts:L15 | neighbors=[route.ts]
- "findings_page_autoresolvedbadge": "AutoResolvedBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L401 | neighbors=[page.tsx]
- "findings_page_chiprow": "ChipRow()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L451 | neighbors=[page.tsx]
- "findings_page_compliancepanel": "CompliancePanel()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1314 | neighbors=[page.tsx]
- "findings_page_complianceref": "ComplianceRef" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L96 | neighbors=[page.tsx]
- "findings_page_copybtn": "CopyBtn()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L286 | neighbors=[page.tsx]
- "findings_page_coverage_color": "COVERAGE_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L77 | neighbors=[page.tsx]
- "findings_page_cvechip": "CveChip()" | kind=code-symbol | source=manager/frontend/app/portal/findings/page.tsx:L42 | neighbors=[page.tsx]
- "findings_page_cvss_aggravating": "CVSS_AGGRAVATING" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L846 | neighbors=[page.tsx]
- "findings_page_cvss_metric": "CVSS_METRIC" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L834 | neighbors=[page.tsx]
- "findings_page_cvssmetric": "CvssMetric" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L848 | neighbors=[page.tsx]
- "findings_page_detailtab": "DetailTab" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1487 | neighbors=[page.tsx]
- "findings_page_detectioncoverage": "DetectionCoverage" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L59 | neighbors=[page.tsx]
- "findings_page_detectionpill": "DetectionPill()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L419 | neighbors=[page.tsx]
- "findings_page_engagementoption": "EngagementOption" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L214 | neighbors=[page.tsx]
- "findings_page_epssbar": "EpssBar()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L268 | neighbors=[page.tsx]
- "findings_page_event_color": "EVENT_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1343 | neighbors=[page.tsx]
- "findings_page_eventactor": "eventActor()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1358 | neighbors=[page.tsx]
- "findings_page_eventdetaillabel": "eventDetailLabel()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1383 | neighbors=[page.tsx]
- "findings_page_eventnarrative": "eventNarrative()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1364 | neighbors=[page.tsx]
- "findings_page_evidencegallery": "EvidenceGallery()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L635 | neighbors=[page.tsx]
- "findings_page_evidencepresentation": "evidencePresentation()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L618 | neighbors=[page.tsx]
- "findings_page_exploitmaturity": "ExploitMaturity" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L58 | neighbors=[page.tsx]
- "findings_page_finding": "Finding" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L136 | neighbors=[page.tsx]
- "findings_page_findingoverview": "FindingOverview()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L962 | neighbors=[page.tsx]
- "findings_page_findingpage": "FindingPage" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L193 | neighbors=[page.tsx]
- "findings_page_findingrow": "FindingRow" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L2041 | neighbors=[page.tsx]
- "findings_page_findingstatus": "FindingStatus" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L57 | neighbors=[page.tsx]
- "findings_page_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L201 | neighbors=[page.tsx]
- "findings_page_findingtimeline": "FindingTimeline" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L76 | neighbors=[page.tsx]
- "findings_page_fmteventts": "fmtEventTs()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L470 | neighbors=[page.tsx]
- "findings_page_fmtrelativets": "fmtRelativeTs()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L477 | neighbors=[page.tsx]
- "findings_page_getlocationsearch": "getLocationSearch()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L83 | neighbors=[page.tsx]
- "findings_page_getserverlocationsearch": "getServerLocationSearch()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L87 | neighbors=[page.tsx]
- "findings_page_intelpanel": "IntelPanel()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1188 | neighbors=[page.tsx]
- "findings_page_kevbadge": "KevBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L355 | neighbors=[page.tsx]
- "findings_page_kill_chain_phase_color": "KILL_CHAIN_PHASE_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L83 | neighbors=[page.tsx]
- "findings_page_killchainstep": "KillChainStep" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L133 | neighbors=[page.tsx]
- "findings_page_killchainviz": "KillChainViz()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L548 | neighbors=[page.tsx]
- "findings_page_maturity_color": "MATURITY_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L74 | neighbors=[page.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-198.json

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
