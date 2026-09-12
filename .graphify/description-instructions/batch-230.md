# Node Description Batch 231 of 380

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

- "findings_page_reason_templates": "REASON_TEMPLATES" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1635 | neighbors=[page.tsx]
- "findings_page_regressionbadge": "RegressionBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L414 | neighbors=[page.tsx]
- "findings_page_rem_risk_color": "REM_RISK_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L796 | neighbors=[page.tsx]
- "findings_page_remediationchecklist": "RemediationChecklist()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L367 | neighbors=[page.tsx]
- "findings_page_remediationos": "RemediationOs" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L116 | neighbors=[page.tsx]
- "findings_page_remediationosfor": "remediationOsFor()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L785 | neighbors=[page.tsx]
- "findings_page_remediationplanresponse": "RemediationPlanResponse" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L127 | neighbors=[page.tsx]
- "findings_page_remediationplanstep": "RemediationPlanStep" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L117 | neighbors=[page.tsx]
- "findings_page_remstep": "RemStep" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L101 | neighbors=[page.tsx]
- "findings_page_riskbreakdown": "RiskBreakdown" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L148 | neighbors=[page.tsx]
- "findings_page_riskbreakdownbar": "RiskBreakdownBar()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L528 | neighbors=[page.tsx]
- "findings_page_sev_color": "SEV_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L63 | neighbors=[page.tsx]
- "findings_page_sev_order": "SEV_ORDER" | kind=code-symbol | source=manager/frontend/app/portal/findings/page.tsx:L15 | neighbors=[page.tsx]
- "findings_page_sevbadge": "SevBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L338 | neighbors=[page.tsx]
- "findings_page_severity": "Severity" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L64 | neighbors=[page.tsx]
- "findings_page_sevs": "SEVS" | kind=code-symbol | source=manager/frontend/app/portal/findings/page.tsx:L14 | neighbors=[page.tsx]
- "findings_page_signalchip": "SignalChip" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L456 | neighbors=[page.tsx]
- "findings_page_sla": "Sla" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L270 | neighbors=[page.tsx]
- "findings_page_sla_hours": "SLA_HOURS" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L268 | neighbors=[page.tsx]
- "findings_page_sortdir": "SortDir" | kind=code-symbol | source=manager/frontend/app/portal/findings/page.tsx:L18 | neighbors=[page.tsx]
- "findings_page_sorthead": "SortHead()" | kind=code-symbol | source=manager/frontend/app/portal/findings/page.tsx:L20 | neighbors=[page.tsx]
- "findings_page_sortkey": "SortKey" | kind=code-symbol | source=manager/frontend/app/portal/findings/page.tsx:L17 | neighbors=[page.tsx]
- "findings_page_source_group_order": "SOURCE_GROUP_ORDER" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1072 | neighbors=[page.tsx]
- "findings_page_sourcegroup": "SourceGroup" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L996 | neighbors=[page.tsx]
- "findings_page_sourcelink": "SourceLink" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L997 | neighbors=[page.tsx]
- "findings_page_spotlight": "spotlight()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1992 | neighbors=[page.tsx]
- "findings_page_status_color": "STATUS_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L66 | neighbors=[page.tsx]
- "findings_page_status_label": "STATUS_LABEL" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L70 | neighbors=[page.tsx]
- "findings_page_statusbadge": "StatusBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L432 | neighbors=[page.tsx]
- "findings_page_subscribetolocationchange": "subscribeToLocationChange()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L88 | neighbors=[page.tsx]
- "findings_page_timelineevent": "TimelineEvent" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L74 | neighbors=[page.tsx]
- "findings_page_tint": "TINT" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L252 | neighbors=[page.tsx]
- "findings_page_triagekey": "TriageKey()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L599 | neighbors=[page.tsx]
- "findings_page_vedhaagentoption": "VedhaAgentOption" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L240 | neighbors=[page.tsx]
- "findings_page_verification_meta": "VERIFICATION_META" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L386 | neighbors=[page.tsx]
- "findings_page_verificationbadge": "VerificationBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L393 | neighbors=[page.tsx]
- "findings_page_workflow": "WORKFLOW" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1624 | neighbors=[page.tsx]
- "findings_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L27 | neighbors=[route.ts]
- "findings_route_positiveint": "positiveInt()" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L22 | neighbors=[route.ts]
- "findings_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L108 | neighbors=[route.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-230.json

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
