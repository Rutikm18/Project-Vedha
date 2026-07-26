# Node Description Batch 74 of 104

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

- "exploit_safety_rationale_240": "True if this target requires human manager approval before exploit runs." | kind=entity | source=manager/backend/app/exploit/safety.py:L240 | neighbors=[requires_approval()] | lang=en
- "exploit_safety_rationale_25": "Raised when a job would exceed the maximum hosts per run." | kind=entity | source=manager/backend/app/exploit/safety.py:L25 | neighbors=[BlastRadiusExceededError] | lang=en
- "exploit_safety_rationale_29": "Raised when a high-risk target requires manager approval before running." | kind=entity | source=manager/backend/app/exploit/safety.py:L29 | neighbors=[ApprovalRequiredError] | lang=pt
- "exposure_route_exposure": "Exposure" | kind=code-symbol | source=manager/frontend/app/api/analytics/exposure/route.ts:L10 | neighbors=[route.ts] | lang=en
- "exposure_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/analytics/exposure/route.ts:L15 | neighbors=[route.ts] | lang=en
- "eyewitness_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/scan/eyewitness/route.ts:L10 | neighbors=[route.ts] | lang=en
- "findings_page_complianceref": "ComplianceRef" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L25 | neighbors=[page.tsx] | lang=en
- "findings_page_copybtn": "CopyBtn()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L116 | neighbors=[page.tsx] | lang=en
- "findings_page_coverage_color": "COVERAGE_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L77 | neighbors=[page.tsx] | lang=en
- "findings_page_detectioncoverage": "DetectionCoverage" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L18 | neighbors=[page.tsx] | lang=en
- "findings_page_detectionpill": "DetectionPill()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L176 | neighbors=[page.tsx] | lang=en
- "findings_page_epssbar": "EpssBar()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L190 | neighbors=[page.tsx] | lang=en
- "findings_page_exploitmaturity": "ExploitMaturity" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L17 | neighbors=[page.tsx] | lang=en
- "findings_page_finding": "Finding" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L33 | neighbors=[page.tsx] | lang=en
- "findings_page_findingstatus": "FindingStatus" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L16 | neighbors=[page.tsx] | lang=en
- "findings_page_kevbadge": "KevBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L150 | neighbors=[page.tsx] | lang=en
- "findings_page_kill_chain_phase_color": "KILL_CHAIN_PHASE_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L83 | neighbors=[page.tsx] | lang=en
- "findings_page_killchainstep": "KillChainStep" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L30 | neighbors=[page.tsx] | lang=en
- "findings_page_killchainviz": "KillChainViz()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L242 | neighbors=[page.tsx] | lang=en
- "findings_page_maturity_color": "MATURITY_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L74 | neighbors=[page.tsx] | lang=en
- "findings_page_priority_color": "PRIORITY_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L80 | neighbors=[page.tsx] | lang=en
- "findings_page_remediationchecklist": "RemediationChecklist()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L289 | neighbors=[page.tsx] | lang=en
- "findings_page_remstep": "RemStep" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L20 | neighbors=[page.tsx] | lang=en
- "findings_page_riskbreakdown": "RiskBreakdown" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L26 | neighbors=[page.tsx] | lang=en
- "findings_page_riskbreakdownbar": "RiskBreakdownBar()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L211 | neighbors=[page.tsx] | lang=en
- "findings_page_sev_color": "SEV_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L63 | neighbors=[page.tsx] | lang=en
- "findings_page_sevbadge": "SevBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L127 | neighbors=[page.tsx] | lang=en
- "findings_page_severity": "Severity" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L15 | neighbors=[page.tsx] | lang=en
- "findings_page_sla_hours": "SLA_HOURS" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L91 | neighbors=[page.tsx] | lang=en
- "findings_page_status_color": "STATUS_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L66 | neighbors=[page.tsx] | lang=en
- "findings_page_status_label": "STATUS_LABEL" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L70 | neighbors=[page.tsx] | lang=en
- "findings_page_statusbadge": "StatusBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L163 | neighbors=[page.tsx] | lang=en
- "findings_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L13 | neighbors=[route.ts] | lang=en
- "findings_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L45 | neighbors=[route.ts] | lang=en
- "findings_route_valid_severities": "VALID_SEVERITIES" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L11 | neighbors=[route.ts] | lang=en
- "frontend_eslint_config_eslintconfig": "eslintConfig" | kind=code-symbol | source=manager/frontend/eslint.config.mjs:L5 | neighbors=[eslint.config.mjs] | lang=en
- "frontend_middleware_config": "config" | kind=code-symbol | source=manager/frontend/middleware.ts:L57 | neighbors=[middleware.ts] | lang=en
- "frontend_middleware_public_paths": "PUBLIC_PATHS" | kind=code-symbol | source=manager/frontend/middleware.ts:L5 | neighbors=[middleware.ts] | lang=en
- "frontend_middleware_public_prefixes": "PUBLIC_PREFIXES" | kind=code-symbol | source=manager/frontend/middleware.ts:L8 | neighbors=[middleware.ts] | lang=en
- "frontend_next_config_dirname": "__dirname" | kind=code-symbol | source=manager/frontend/next.config.mjs:L4 | neighbors=[next.config.mjs] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-073.json

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
