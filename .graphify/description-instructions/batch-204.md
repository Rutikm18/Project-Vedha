# Node Description Batch 205 of 336

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

- "findings_page_sla_hours": "SLA_HOURS" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L247 | neighbors=[page.tsx]
- "findings_page_sortdir": "SortDir" | kind=code-symbol | source=manager/frontend/app/portal/findings/page.tsx:L18 | neighbors=[page.tsx]
- "findings_page_sorthead": "SortHead()" | kind=code-symbol | source=manager/frontend/app/portal/findings/page.tsx:L20 | neighbors=[page.tsx]
- "findings_page_sortkey": "SortKey" | kind=code-symbol | source=manager/frontend/app/portal/findings/page.tsx:L17 | neighbors=[page.tsx]
- "findings_page_source_group_order": "SOURCE_GROUP_ORDER" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L953 | neighbors=[page.tsx]
- "findings_page_sourcegroup": "SourceGroup" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L877 | neighbors=[page.tsx]
- "findings_page_sourcelink": "SourceLink" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L878 | neighbors=[page.tsx]
- "findings_page_spotlight": "spotlight()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1856 | neighbors=[page.tsx]
- "findings_page_status_color": "STATUS_COLOR" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L66 | neighbors=[page.tsx]
- "findings_page_status_label": "STATUS_LABEL" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L70 | neighbors=[page.tsx]
- "findings_page_statusbadge": "StatusBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L410 | neighbors=[page.tsx]
- "findings_page_subscribetolocationchange": "subscribeToLocationChange()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L78 | neighbors=[page.tsx]
- "findings_page_timelineevent": "TimelineEvent" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L64 | neighbors=[page.tsx]
- "findings_page_tint": "TINT" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L231 | neighbors=[page.tsx]
- "findings_page_triagekey": "TriageKey()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L577 | neighbors=[page.tsx]
- "findings_page_vedhaagentoption": "VedhaAgentOption" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L219 | neighbors=[page.tsx]
- "findings_page_verification_meta": "VERIFICATION_META" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L364 | neighbors=[page.tsx]
- "findings_page_verificationbadge": "VerificationBadge()" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L371 | neighbors=[page.tsx]
- "findings_page_workflow": "WORKFLOW" | kind=code-symbol | source=manager/frontend/app/findings/page.tsx:L1489 | neighbors=[page.tsx]
- "findings_route_get": "GET" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L27 | neighbors=[route.ts]
- "findings_route_positiveint": "positiveInt()" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L22 | neighbors=[route.ts]
- "findings_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L108 | neighbors=[route.ts]
- "findings_route_status_to_api": "STATUS_TO_API" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L12 | neighbors=[route.ts]
- "findings_route_valid_severities": "VALID_SEVERITIES" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L11 | neighbors=[route.ts]
- "findings_route_valid_sorts": "VALID_SORTS" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L19 | neighbors=[route.ts]
- "findings_route_valid_verification": "VALID_VERIFICATION" | kind=code-symbol | source=manager/frontend/app/api/findings/route.ts:L20 | neighbors=[route.ts]
- "fleet_fleetjobs_fetchjson": "fetchJson()" | kind=code-symbol | source=manager/frontend/app/fleet/FleetJobs.tsx:L26 | neighbors=[FleetJobs.tsx]
- "fleet_fleetjobs_fleetjobs": "FleetJobs()" | kind=code-symbol | source=manager/frontend/app/fleet/FleetJobs.tsx:L33 | neighbors=[FleetJobs.tsx]
- "fleet_fleetjobs_job": "Job" | kind=code-symbol | source=manager/frontend/app/fleet/FleetJobs.tsx:L14 | neighbors=[FleetJobs.tsx]
- "fleet_fleetjobs_status_color": "STATUS_COLOR" | kind=code-symbol | source=manager/frontend/app/fleet/FleetJobs.tsx:L21 | neighbors=[FleetJobs.tsx]
- "fleet_page_agentstatus": "agentStatus()" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L80 | neighbors=[page.tsx]
- "fleet_page_ago": "ago()" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L87 | neighbors=[page.tsx]
- "fleet_page_enrollmentrequest": "EnrollmentRequest" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L12 | neighbors=[page.tsx]
- "fleet_page_fetchjson": "fetchJson()" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L96 | neighbors=[page.tsx]
- "fleet_page_fleetpage": "FleetPage()" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L107 | neighbors=[page.tsx]
- "fleet_page_fleetresponse": "FleetResponse" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L24 | neighbors=[page.tsx]
- "fleet_page_inputstyle": "inputStyle" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L28 | neighbors=[page.tsx]
- "fleet_page_jobbadge": "jobBadge()" | kind=code-symbol | source=manager/frontend/app/fleet/page.tsx:L68 | neighbors=[page.tsx]
- "fleet_page_portalagent": "PortalAgent" | kind=code-symbol | source=manager/frontend/app/portal/fleet/page.tsx:L26 | neighbors=[page.tsx]
- "fleet_page_portalfleet": "PortalFleet()" | kind=code-symbol | source=manager/frontend/app/portal/fleet/page.tsx:L41 | neighbors=[page.tsx]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-204.json

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
