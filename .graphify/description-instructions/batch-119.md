# Node Description Batch 120 of 186

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

- "findings_page_epssbar": "EpssBar()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L268 | neighbors=[page.tsx]
- "findings_page_exploitmaturity": "ExploitMaturity" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L23 | neighbors=[page.tsx]
- "findings_page_finding": "Finding" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L53 | neighbors=[page.tsx]
- "findings_page_findingpage": "FindingPage" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L97 | neighbors=[page.tsx]
- "findings_page_findingstatus": "FindingStatus" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L22 | neighbors=[page.tsx]
- "findings_page_findingsummary": "FindingSummary" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L105 | neighbors=[page.tsx]
- "findings_page_getlocationsearch": "getLocationSearch()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L32 | neighbors=[page.tsx]
- "findings_page_getserverlocationsearch": "getServerLocationSearch()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L36 | neighbors=[page.tsx]
- "findings_page_kevbadge": "KevBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L174 | neighbors=[page.tsx]
- "findings_page_kill_chain_phase_color": "KILL_CHAIN_PHASE_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L83 | neighbors=[page.tsx]
- "findings_page_killchainstep": "KillChainStep" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L50 | neighbors=[page.tsx]
- "findings_page_killchainviz": "KillChainViz()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L320 | neighbors=[page.tsx]
- "findings_page_maturity_color": "MATURITY_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L74 | neighbors=[page.tsx]
- "findings_page_needsreviewchip": "NeedsReviewChip()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L207 | neighbors=[page.tsx]
- "findings_page_priority_color": "PRIORITY_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L80 | neighbors=[page.tsx]
- "findings_page_regressionbadge": "RegressionBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L219 | neighbors=[page.tsx]
- "findings_page_remediationchecklist": "RemediationChecklist()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L367 | neighbors=[page.tsx]
- "findings_page_remstep": "RemStep" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L40 | neighbors=[page.tsx]
- "findings_page_riskbreakdown": "RiskBreakdown" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L46 | neighbors=[page.tsx]
- "findings_page_riskbreakdownbar": "RiskBreakdownBar()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L289 | neighbors=[page.tsx]
- "findings_page_sev_color": "SEV_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L63 | neighbors=[page.tsx]
- "findings_page_sevbadge": "SevBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L151 | neighbors=[page.tsx]
- "findings_page_severity": "Severity" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L21 | neighbors=[page.tsx]
- "findings_page_sla_hours": "SLA_HOURS" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L117 | neighbors=[page.tsx]
- "findings_page_spotlight": "spotlight()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L903 | neighbors=[page.tsx]
- "findings_page_status_color": "STATUS_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L66 | neighbors=[page.tsx]
- "findings_page_status_label": "STATUS_LABEL" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L70 | neighbors=[page.tsx]
- "findings_page_statusbadge": "StatusBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L241 | neighbors=[page.tsx]
- "findings_page_subscribetolocationchange": "subscribeToLocationChange()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L27 | neighbors=[page.tsx]
- "findings_page_verification_meta": "VERIFICATION_META" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L187 | neighbors=[page.tsx]
- "findings_page_verificationbadge": "VerificationBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L193 | neighbors=[page.tsx]
- "findings_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L27 | neighbors=[route.ts]
- "findings_route_positiveint": "positiveInt()" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L22 | neighbors=[route.ts]
- "findings_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L103 | neighbors=[route.ts]
- "findings_route_status_to_api": "STATUS_TO_API" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L12 | neighbors=[route.ts]
- "findings_route_valid_severities": "VALID_SEVERITIES" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L11 | neighbors=[route.ts]
- "findings_route_valid_sorts": "VALID_SORTS" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L19 | neighbors=[route.ts]
- "findings_route_valid_verification": "VALID_VERIFICATION" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L20 | neighbors=[route.ts]
- "fleet_page_enrollmentrequest": "EnrollmentRequest" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L11 | neighbors=[page.tsx]
- "fleet_page_fetchjson": "fetchJson()" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L41 | neighbors=[page.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-119.json

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
