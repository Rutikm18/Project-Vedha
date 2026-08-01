# Node Description Batch 82 of 119

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
For an entity node (any other kind — e.g. a person, place, event, object),
describe what the entity is and its role, grounded in its type, its
relations (neighbors) and the provided citations/evidence — e.g.
"Lady Carfax, a wealthy heiress who disappears en route to Lausanne.".
Ground entity descriptions in the citations/evidence when present; do not
speculate beyond the context, so a node with no supporting context may be
left out of the reply.
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "exploit_safety_rationale_21": "Raised when a target IP is outside the engagement scope CIDRs." | kind=entity | source=manager/backend/app/exploit/safety.py:L21 | neighbors=[OutOfScopeError] | lang=en
- "exploit_safety_rationale_217": "Raises OutOfScopeError if target_ip is not in scope or is excluded." | kind=entity | source=manager/backend/app/exploit/safety.py:L217 | neighbors=[validate_scope()] | lang=en
- "exploit_safety_rationale_240": "True if this target requires human manager approval before exploit runs." | kind=entity | source=manager/backend/app/exploit/safety.py:L240 | neighbors=[requires_approval()] | lang=en
- "exploit_safety_rationale_25": "Raised when a job would exceed the maximum hosts per run." | kind=entity | source=manager/backend/app/exploit/safety.py:L25 | neighbors=[BlastRadiusExceededError] | lang=en
- "exploit_safety_rationale_29": "Raised when a high-risk target requires manager approval before running." | kind=entity | source=manager/backend/app/exploit/safety.py:L29 | neighbors=[ApprovalRequiredError] | lang=pt
- "exposure_route_exposure": "Exposure" | kind=code-symbol | source=manager/frontend/app/api/analytics/exposure/route.ts:L10 | neighbors=[route.ts] | lang=en
- "exposure_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/analytics/exposure/route.ts:L15 | neighbors=[route.ts] | lang=en
- "findings_page_complianceref": "ComplianceRef" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L45 | neighbors=[page.tsx] | lang=en
- "findings_page_copybtn": "CopyBtn()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L127 | neighbors=[page.tsx] | lang=en
- "findings_page_coverage_color": "COVERAGE_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L77 | neighbors=[page.tsx] | lang=en
- "findings_page_detectioncoverage": "DetectionCoverage" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L24 | neighbors=[page.tsx] | lang=en
- "findings_page_detectionpill": "DetectionPill()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L190 | neighbors=[page.tsx] | lang=en
- "findings_page_epssbar": "EpssBar()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L204 | neighbors=[page.tsx] | lang=en
- "findings_page_exploitmaturity": "ExploitMaturity" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L23 | neighbors=[page.tsx] | lang=en
- "findings_page_finding": "Finding" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L53 | neighbors=[page.tsx] | lang=en
- "findings_page_findingpage": "FindingPage" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L87 | neighbors=[page.tsx] | lang=en
- "findings_page_findingstatus": "FindingStatus" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L22 | neighbors=[page.tsx] | lang=en
- "findings_page_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L95 | neighbors=[page.tsx] | lang=en
- "findings_page_fixfirststrip": "FixFirstStrip()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L782 | neighbors=[page.tsx] | lang=en
- "findings_page_getlocationsearch": "getLocationSearch()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L32 | neighbors=[page.tsx] | lang=en
- "findings_page_getserverlocationsearch": "getServerLocationSearch()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L36 | neighbors=[page.tsx] | lang=en
- "findings_page_kevbadge": "KevBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L164 | neighbors=[page.tsx] | lang=en
- "findings_page_kill_chain_phase_color": "KILL_CHAIN_PHASE_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L83 | neighbors=[page.tsx] | lang=en
- "findings_page_killchainstep": "KillChainStep" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L50 | neighbors=[page.tsx] | lang=en
- "findings_page_killchainviz": "KillChainViz()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L256 | neighbors=[page.tsx] | lang=en
- "findings_page_maturity_color": "MATURITY_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L74 | neighbors=[page.tsx] | lang=en
- "findings_page_priority_color": "PRIORITY_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L80 | neighbors=[page.tsx] | lang=en
- "findings_page_remediationchecklist": "RemediationChecklist()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L303 | neighbors=[page.tsx] | lang=en
- "findings_page_remstep": "RemStep" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L40 | neighbors=[page.tsx] | lang=en
- "findings_page_riskbreakdown": "RiskBreakdown" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L46 | neighbors=[page.tsx] | lang=en
- "findings_page_riskbreakdownbar": "RiskBreakdownBar()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L225 | neighbors=[page.tsx] | lang=en
- "findings_page_sev_color": "SEV_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L63 | neighbors=[page.tsx] | lang=en
- "findings_page_sevbadge": "SevBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L141 | neighbors=[page.tsx] | lang=en
- "findings_page_severity": "Severity" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L21 | neighbors=[page.tsx] | lang=en
- "findings_page_sla_hours": "SLA_HOURS" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L107 | neighbors=[page.tsx] | lang=en
- "findings_page_status_color": "STATUS_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L66 | neighbors=[page.tsx] | lang=en
- "findings_page_status_label": "STATUS_LABEL" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L70 | neighbors=[page.tsx] | lang=en
- "findings_page_statusbadge": "StatusBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L177 | neighbors=[page.tsx] | lang=en
- "findings_page_subscribetolocationchange": "subscribeToLocationChange()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L27 | neighbors=[page.tsx] | lang=en
- "findings_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L26 | neighbors=[route.ts] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-081.json

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
