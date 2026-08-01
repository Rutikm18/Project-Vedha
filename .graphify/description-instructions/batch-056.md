# Node Description Batch 57 of 119

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

- "pipeline_pipeline_buildhostsmap": "buildHostsMap()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L489 | neighbors=[pipeline.go, assemble()]
- "pipeline_pipeline_clamp": "clamp()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L566 | neighbors=[pipeline.go, Run()]
- "pipeline_pipeline_clampint": "clampInt()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L579 | neighbors=[pipeline.go, Run()]
- "pipeline_pipeline_countopenports": "countOpenPorts()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L552 | neighbors=[pipeline.go, assemble()]
- "pipeline_pipeline_dedup": "dedup()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L511 | neighbors=[pipeline.go, Run()]
- "pipeline_pipeline_factsasmaps": "factsAsMaps()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L335 | neighbors=[pipeline.go, Run()]
- "pipeline_pipeline_intersect": "intersect()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L411 | neighbors=[pipeline.go, Run()]
- "pipeline_pipeline_looksliketls": "looksLikeTLS()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L398 | neighbors=[pipeline.go, Run()]
- "pipeline_pipeline_ptr": "ptr()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L592 | neighbors=[pipeline.go, Run()]
- "pipeline_pipeline_reject": "Reject()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L485 | neighbors=[pipeline.go, assembleError()]
- "pipeline_pipeline_resolverequestedhosts": "resolveRequestedHosts()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L383 | neighbors=[pipeline.go, Run()]
- "pipeline_pipeline_servicefilterfor": "serviceFilterFor()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L345 | neighbors=[pipeline.go, Run()]
- "pipeline_pipeline_tofact": "toFact()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L421 | neighbors=[pipeline.go, Run()]
- "pipeline_pipeline_toset": "toSet()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L403 | neighbors=[pipeline.go, Run()]
- "pipeline_pipeline_validateplan": "ValidatePlan()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L360 | neighbors=[pipeline.go, Run()]
- "probe_go_main_envfilepath": "envFilePath()" | kind=code-symbol | source=probe-go/main.go:L267 | neighbors=[main.go, main()]
- "probe_go_main_findservicelabel": "findServiceLabel()" | kind=code-symbol | source=probe-go/main.go:L176 | neighbors=[main.go, renderReport()]
- "probe_go_main_isdirwritable": "isDirWritable()" | kind=code-symbol | source=probe-go/main.go:L283 | neighbors=[main.go, selfTest()]
- "probe_go_main_protoor": "protoOr()" | kind=code-symbol | source=probe-go/main.go:L212 | neighbors=[main.go, renderReport()]
- "probe_pipeline_collector_write": ".write()" | kind=code-symbol | source=probe/pipeline.py:L126 | neighbors=[_Collector, _run_active()]
- "probe_run_scan_main": "main()" | kind=code-symbol | source=probe/run_scan.py:L135 | neighbors=[run_scan.py, _orchestrate()]
- "probe_run_scan_orchestrate": "_orchestrate()" | kind=code-symbol | source=probe/run_scan.py:L62 | neighbors=[run_scan.py, main()]
- "probe_selftest_live_check": "check()" | kind=code-symbol | source=probe/selftest_live.py:L38 | neighbors=[selftest_live.py, main()]
- "probe_selftest_live_fact": "_fact()" | kind=code-symbol | source=probe/selftest_live.py:L81 | neighbors=[selftest_live.py, main()]
- "probe_selftest_live_free_port": "_free_port()" | kind=code-symbol | source=probe/selftest_live.py:L69 | neighbors=[selftest_live.py, main()]
- "probe_showcase_run_list_use_cases": "list_use_cases()" | kind=code-symbol | source=probe/showcase_run.py:L39 | neighbors=[showcase_run.py, main()]
- "probe_showcase_run_print_summary": "_print_summary()" | kind=code-symbol | source=probe/showcase_run.py:L49 | neighbors=[showcase_run.py, main()]
- "probe_showcase_run_split": "_split()" | kind=code-symbol | source=probe/showcase_run.py:L35 | neighbors=[showcase_run.py, main()]
- "prompts_exploit_builder": "exploit-builder.ts" | kind=code-symbol | source=manager/frontend/lib/prompts/exploit-builder.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, 298a9d4 trim frontend to 7 core pages; …]
- "reports_page_formatdate": "formatDate()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L84 | neighbors=[page.tsx, ReportsPage()]
- "reports_page_reportspage": "ReportsPage()" | kind=code-symbol | source=manager/frontend/app/reports/page.tsx:L297 | neighbors=[page.tsx, formatDate()]
- "routers_activity_recent_activity": "recent_activity()" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L41 | neighbors=[activity.py, ActivityItem]
- "routers_ad_set_job_status": "_set_job_status()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L201 | neighbors=[ad.py, _run_ad_assessment_and_save()]
- "routers_agent_advisor_list_recommendations": "list_recommendations()" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L72 | neighbors=[agent_advisor.py, _rec_dict()]
- "routers_agent_advisor_rec_dict": "_rec_dict()" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L31 | neighbors=[agent_advisor.py, list_recommendations()]
- "routers_agent_ws_rationale_44": "Persistent WebSocket for probe → manager push communication.      Query params:" | kind=entity | source=manager/backend/app/routers/agent_ws.py:L44 | neighbors=[ScanJob, agent_websocket_endpoint()]
- "routers_agents_heartbeat": "heartbeat()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L547 | neighbors=[agents.py, _agent_ownership_check()]
- "routers_agents_job_params_contain_secret": "_job_params_contain_secret()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L74 | neighbors=[agents.py, enqueue_agent_job()]
- "routers_agents_refresh_agent_registration": "refresh_agent_registration()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L587 | neighbors=[agents.py, _agent_ownership_check()]
- "routers_agents_register_agent": "register_agent()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L459 | neighbors=[agents.py, AgentRegisterResponse]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-056.json

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
