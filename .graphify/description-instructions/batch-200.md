# Node Description Batch 201 of 332

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
- "findings_page_needsreviewchip": "NeedsReviewChip()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L383 | neighbors=[page.tsx]
- "findings_page_portalfindings": "PortalFindings()" | kind=code-symbol | source=manager/frontend/app/portal/findings/page.tsx:L161 | neighbors=[page.tsx]
- "findings_page_prefersreducedmotion": "prefersReducedMotion()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L277 | neighbors=[page.tsx]
- "findings_page_priority": "Priority" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L60 | neighbors=[page.tsx]
- "findings_page_priority_color": "PRIORITY_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L80 | neighbors=[page.tsx]
- "findings_page_prioritybadge": "PriorityBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L330 | neighbors=[page.tsx]
- "findings_page_reason_templates": "REASON_TEMPLATES" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1500 | neighbors=[page.tsx]
- "findings_page_regressionbadge": "RegressionBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L392 | neighbors=[page.tsx]
- "findings_page_remediationchecklist": "RemediationChecklist()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L367 | neighbors=[page.tsx]
- "findings_page_remediationos": "RemediationOs" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L97 | neighbors=[page.tsx]
- "findings_page_remediationosfor": "remediationOsFor()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L691 | neighbors=[page.tsx]
- "findings_page_remediationplanresponse": "RemediationPlanResponse" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L108 | neighbors=[page.tsx]
- "findings_page_remediationplanstep": "RemediationPlanStep" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L98 | neighbors=[page.tsx]
- "findings_page_remstep": "RemStep" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L91 | neighbors=[page.tsx]
- "findings_page_riskbreakdown": "RiskBreakdown" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L129 | neighbors=[page.tsx]
- "findings_page_riskbreakdownbar": "RiskBreakdownBar()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L506 | neighbors=[page.tsx]
- "findings_page_sev_color": "SEV_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L63 | neighbors=[page.tsx]
- "findings_page_sev_order": "SEV_ORDER" | kind=code-symbol | source=manager/frontend/app/portal/findings/page.tsx:L15 | neighbors=[page.tsx]
- "findings_page_sevbadge": "SevBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L316 | neighbors=[page.tsx]
- "findings_page_severity": "Severity" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L56 | neighbors=[page.tsx]
- "findings_page_sevs": "SEVS" | kind=code-symbol | source=manager/frontend/app/portal/findings/page.tsx:L14 | neighbors=[page.tsx]
- "findings_page_signalchip": "SignalChip" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L434 | neighbors=[page.tsx]
- "findings_page_sla": "Sla" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L249 | neighbors=[page.tsx]
- "findings_page_sla_hours": "SLA_HOURS" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L247 | neighbors=[page.tsx]
- "findings_page_sortdir": "SortDir" | kind=code-symbol | source=manager/frontend/app/portal/findings/page.tsx:L18 | neighbors=[page.tsx]
- "findings_page_sorthead": "SortHead()" | kind=code-symbol | source=manager/frontend/app/portal/findings/page.tsx:L20 | neighbors=[page.tsx]
- "findings_page_sortkey": "SortKey" | kind=code-symbol | source=manager/frontend/app/portal/findings/page.tsx:L17 | neighbors=[page.tsx]
- "findings_page_source_group_order": "SOURCE_GROUP_ORDER" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L953 | neighbors=[page.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-200.json

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
