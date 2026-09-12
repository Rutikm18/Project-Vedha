# Node Description Batch 267 of 380

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

- "reportsection_finding_model_slastate": "SlaState" | kind=code-symbol | source=reportsection/finding-model.ts:L441 | neighbors=[finding-model.ts]
- "reportsection_finding_model_tier_meta": "TIER_META" | kind=code-symbol | source=reportsection/finding-model.ts:L611 | neighbors=[finding-model.ts]
- "reportsection_finding_model_triagesort": "triageSort()" | kind=code-symbol | source=reportsection/finding-model.ts:L713 | neighbors=[finding-model.ts]
- "reportsection_finding_model_vectormetric": "VectorMetric" | kind=code-symbol | source=reportsection/finding-model.ts:L219 | neighbors=[finding-model.ts]
- "reportsection_finding_model_vectorreading": "VectorReading" | kind=code-symbol | source=reportsection/finding-model.ts:L228 | neighbors=[finding-model.ts]
- "reportsection_findingreport_copybutton": "CopyButton()" | kind=code-symbol | source=reportsection/FindingReport.tsx:L61 | neighbors=[FindingReport.tsx]
- "reportsection_findingreport_evidenceartifact": "EvidenceArtifact()" | kind=code-symbol | source=reportsection/FindingReport.tsx:L118 | neighbors=[FindingReport.tsx]
- "reportsection_findingreport_findingreportprops": "FindingReportProps" | kind=code-symbol | source=reportsection/FindingReport.tsx:L202 | neighbors=[FindingReport.tsx]
- "reportsection_findingreport_findingssection": "FindingsSection()" | kind=code-symbol | source=reportsection/FindingReport.tsx:L545 | neighbors=[FindingReport.tsx]
- "reportsection_findingreport_gap": "Gap()" | kind=code-symbol | source=reportsection/FindingReport.tsx:L94 | neighbors=[FindingReport.tsx]
- "reportsection_findingreport_prose": "Prose()" | kind=code-symbol | source=reportsection/FindingReport.tsx:L103 | neighbors=[FindingReport.tsx]
- "reportsection_findingreport_section": "Section()" | kind=code-symbol | source=reportsection/FindingReport.tsx:L76 | neighbors=[FindingReport.tsx]
- "reportsection_findingreport_sevfilter": "SevFilter" | kind=code-symbol | source=reportsection/FindingReport.tsx:L543 | neighbors=[FindingReport.tsx]
- "reportsection_findingreport_sevtag": "SevTag()" | kind=code-symbol | source=reportsection/FindingReport.tsx:L48 | neighbors=[FindingReport.tsx]
- "reportsection_spec_a": "a" | kind=code-symbol | source=reportsection/spec.ts:L148 | neighbors=[spec.ts]
- "reportsection_spec_bare": "bare" | kind=code-symbol | source=reportsection/spec.ts:L144 | neighbors=[spec.ts]
- "reportsection_spec_base": "base" | kind=code-symbol | source=reportsection/spec.ts:L15 | neighbors=[spec.ts]
- "reportsection_spec_dirty": "dirty" | kind=code-symbol | source=reportsection/spec.ts:L105 | neighbors=[spec.ts]
- "reportsection_spec_f": "F()" | kind=code-symbol | source=reportsection/spec.ts:L25 | neighbors=[spec.ts]
- "reportsection_spec_group": "group()" | kind=code-symbol | source=reportsection/spec.ts:L13 | neighbors=[spec.ts]
- "reportsection_spec_lowkev": "lowKev" | kind=code-symbol | source=reportsection/spec.ts:L45 | neighbors=[spec.ts]
- "reportsection_spec_now": "NOW" | kind=code-symbol | source=reportsection/spec.ts:L24 | neighbors=[spec.ts]
- "reportsection_spec_ok": "ok()" | kind=code-symbol | source=reportsection/spec.ts:L9 | neighbors=[spec.ts]
- "reportsection_spec_p0sla": "p0sla" | kind=code-symbol | source=reportsection/spec.ts:L57 | neighbors=[spec.ts]
- "reportsection_spec_r": "r" | kind=code-symbol | source=reportsection/spec.ts:L115 | neighbors=[spec.ts]
- "request_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/auth/request/route.ts:L7 | neighbors=[route.ts]
- "results_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/detection-validation/results/route.ts:L5 | neighbors=[route.ts]
- "reveal_route_get": "GET()" | kind=code-symbol | source=manager/frontend/app/api/customers/[id]/reveal/route.ts:L8 | neighbors=[route.ts]
- "routers_ad_ad_assessment_status": "ad_assessment_status()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L99 | neighbors=[ad.py]
- "routers_ad_launch_ad_assessment": "launch_ad_assessment()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L64 | neighbors=[ad.py]
- "routers_agent_advisor_run_advisor": "run_advisor()" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L50 | neighbors=[agent_advisor.py]
- "routers_agent_ws_rationale_115": "Persistent WebSocket for probe → manager push communication.      Authentication" | kind=entity | source=manager/backend/app/routers/agent_ws.py:L115 | neighbors=[agent_websocket_endpoint()]
- "routers_agent_ws_rationale_41": "Read an agent bearer token exclusively from the non-logged auth header." | kind=entity | source=manager/backend/app/routers/agent_ws.py:L41 | neighbors=[_agent_token_from_websocket()]
- "routers_agent_ws_rationale_52": "Validate eligibility and atomically claim a WebSocket job offer." | kind=entity | source=manager/backend/app/routers/agent_ws.py:L52 | neighbors=[_claim_pushed_job()]
- "routers_agents_agentbootstraprequest_validate_network_segments": ".validate_network_segments()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L647 | neighbors=[AgentBootstrapRequest]
- "routers_agents_agentregisterrequest_validate_network_segments": ".validate_network_segments()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L223 | neighbors=[AgentRegisterRequest]
- "routers_agents_enqueuejobrequest_validate_uc": "._validate_uc()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L362 | neighbors=[EnqueueJobRequest]
- "routers_agents_heartbeatrequest_require_fence_for_running_job": ".require_fence_for_running_job()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L248 | neighbors=[HeartbeatRequest]
- "routers_agents_list_agents": "list_agents()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L827 | neighbors=[agents.py]
- "routers_agents_rationale_1003": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L1003 | neighbors=[get_job_status()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-266.json

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
