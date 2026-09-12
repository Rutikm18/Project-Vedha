# Node Description Batch 263 of 380

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "portal_portalshell_sessiontimer": "SessionTimer()" | kind=code-symbol | source=manager/frontend/components/portal/PortalShell.tsx:L252 | neighbors=[PortalShell.tsx]
- "portal_timestamp_timestampprops": "TimestampProps" | kind=code-symbol | source=manager/frontend/components/portal/Timestamp.tsx:L68 | neighbors=[Timestamp.tsx]
- "portscan_ratelimiter_init": ".__init__()" | kind=code-symbol | source=portscan.py:L96 | neighbors=[RateLimiter]
- "portscan_rationale_74": "Map a connect()-time OSError to (state, reason). Unknown stays visible     as ('" | kind=entity | source=portscan.py:L74 | neighbors=[classify_os_error()]
- "probes_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/scan/probes/route.ts:L6 | neighbors=[route.ts]
- "prompts_report_controlitem": "ControlItem" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L134 | neighbors=[report.ts]
- "prompts_report_domains": "DOMAINS" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L195 | neighbors=[report.ts]
- "prompts_report_effort": "Effort" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L31 | neighbors=[report.ts]
- "prompts_report_reportvalidation": "ReportValidation" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L388 | neighbors=[report.ts]
- "prompts_report_sections_generation_order": "GENERATION_ORDER" | kind=code-symbol | source=manager/frontend/lib/prompts/report-sections.ts:L442 | neighbors=[report-sections.ts]
- "prompts_report_sev_rank": "SEV_RANK" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L199 | neighbors=[report.ts]
- "prompts_report_severity": "Severity" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L29 | neighbors=[report.ts]
- "prompts_report_severity_weight": "SEVERITY_WEIGHT" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L191 | neighbors=[report.ts]
- "register_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/agents/register/route.ts:L12 | neighbors=[route.ts]
- "reject_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/reject/route.ts:L4 | neighbors=[route.ts]
- "remediation_route_supported_os": "SUPPORTED_OS" | kind=code-symbol | source=manager/frontend/app/api/findings/[id]/remediation/route.ts:L5 | neighbors=[route.ts]
- "report_finding_model_aggravating": "AGGRAVATING" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L264 | neighbors=[finding-model.ts]
- "report_finding_model_confidence": "Confidence" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L142 | neighbors=[finding-model.ts]
- "report_finding_model_confidencelevel": "ConfidenceLevel" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L140 | neighbors=[finding-model.ts]
- "report_finding_model_detection": "DETECTION" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L151 | neighbors=[finding-model.ts]
- "report_finding_model_gap": "Gap" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L650 | neighbors=[finding-model.ts]
- "report_finding_model_metric_name": "METRIC_NAME" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L240 | neighbors=[finding-model.ts]
- "report_finding_model_metric_value": "METRIC_VALUE" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L248 | neighbors=[finding-model.ts]
- "report_finding_model_outcome": "OUTCOME" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L281 | neighbors=[finding-model.ts]
- "report_finding_model_prereq": "PREREQ" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L266 | neighbors=[finding-model.ts]
- "report_finding_model_priority": "Priority" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L373 | neighbors=[finding-model.ts]
- "report_finding_model_priority_label": "PRIORITY_LABEL" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L382 | neighbors=[finding-model.ts]
- "report_finding_model_prioritycode": "PriorityCode" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L371 | neighbors=[finding-model.ts]
- "report_finding_model_provenance": "Provenance" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L498 | neighbors=[finding-model.ts]
- "report_finding_model_rawremediation": "RawRemediation" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L60 | neighbors=[finding-model.ts]
- "report_finding_model_rawverification": "RawVerification" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L72 | neighbors=[finding-model.ts]
- "report_finding_model_redaction": "Redaction" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L578 | neighbors=[finding-model.ts]
- "report_finding_model_redactionrule": "RedactionRule" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L523 | neighbors=[finding-model.ts]
- "report_finding_model_remediationstep": "RemediationStep" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L607 | neighbors=[finding-model.ts]
- "report_finding_model_rules": "RULES" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L544 | neighbors=[finding-model.ts]
- "report_finding_model_sla": "Sla" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L448 | neighbors=[finding-model.ts]
- "report_finding_model_sla_days": "SLA_DAYS" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L442 | neighbors=[finding-model.ts]
- "report_finding_model_slastate": "SlaState" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L446 | neighbors=[finding-model.ts]
- "report_finding_model_vectormetric": "VectorMetric" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L219 | neighbors=[finding-model.ts]
- "report_finding_model_vectorreading": "VectorReading" | kind=code-symbol | source=manager/frontend/lib/report/finding-model.ts:L228 | neighbors=[finding-model.ts]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-262.json

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
