# Node Description Batch 51 of 104

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

- "netexec_route_parsenxcoutput": "parseNxcOutput()" | kind=code-symbol | source=manager/frontend/app/api/scan/netexec/route.ts:L22 | neighbors=[route.ts, POST()]
- "netexec_route_runnxc": "runNxc()" | kind=code-symbol | source=manager/frontend/app/api/scan/netexec/route.ts:L33 | neighbors=[route.ts, POST()]
- "nmap_route_parsenmapxml": "parseNmapXml()" | kind=code-symbol | source=manager/frontend/app/api/scan/nmap/route.ts:L89 | neighbors=[route.ts, route.ts]
- "nmap_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/scan/nmap/route.ts:L215 | neighbors=[route.ts, validateTarget()]
- "nmap_route_validatetarget": "validateTarget()" | kind=code-symbol | source=manager/frontend/app/api/scan/nmap/route.ts:L62 | neighbors=[route.ts, POST()]
- "pipeline_pipeline_buildhostsmap": "buildHostsMap()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L434 | neighbors=[pipeline.go, assemble()]
- "pipeline_pipeline_clamp": "clamp()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L523 | neighbors=[pipeline.go, Run()]
- "pipeline_pipeline_clampint": "clampInt()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L536 | neighbors=[pipeline.go, Run()]
- "pipeline_pipeline_countopenports": "countOpenPorts()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L497 | neighbors=[pipeline.go, assemble()]
- "pipeline_pipeline_dedup": "dedup()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L511 | neighbors=[pipeline.go, Run()]
- "pipeline_pipeline_factsasmaps": "factsAsMaps()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L323 | neighbors=[pipeline.go, Run()]
- "pipeline_pipeline_intersect": "intersect()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L361 | neighbors=[pipeline.go, Run()]
- "pipeline_pipeline_looksliketls": "looksLikeTLS()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L348 | neighbors=[pipeline.go, Run()]
- "pipeline_pipeline_ptr": "ptr()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L549 | neighbors=[pipeline.go, Run()]
- "pipeline_pipeline_servicefilterfor": "serviceFilterFor()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L333 | neighbors=[pipeline.go, Run()]
- "pipeline_pipeline_tofact": "toFact()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L371 | neighbors=[pipeline.go, Run()]
- "pipeline_pipeline_toset": "toSet()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L353 | neighbors=[pipeline.go, Run()]
- "pipeline_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/scan/pipeline/route.ts:L549 | neighbors=[route.ts, runPipelineBackground()]
- "pipeline_route_runeyewitnessstage": "runEyewitnessStage()" | kind=code-symbol | source=manager/frontend/app/api/scan/pipeline/route.ts:L426 | neighbors=[route.ts, runPipelineBackground()]
- "pipeline_route_runnucleistage": "runNucleiStage()" | kind=code-symbol | source=manager/frontend/app/api/scan/pipeline/route.ts:L247 | neighbors=[route.ts, runPipelineBackground()]
- "pipeline_route_runtestsslstage": "runTestsslStage()" | kind=code-symbol | source=manager/frontend/app/api/scan/pipeline/route.ts:L349 | neighbors=[route.ts, runPipelineBackground()]
- "probe_go_main_envfilepath": "envFilePath()" | kind=code-symbol | source=probe-go/main.go:L267 | neighbors=[main.go, main()]
- "probe_go_main_findservicelabel": "findServiceLabel()" | kind=code-symbol | source=probe-go/main.go:L176 | neighbors=[main.go, renderReport()]
- "probe_go_main_isdirwritable": "isDirWritable()" | kind=code-symbol | source=probe-go/main.go:L283 | neighbors=[main.go, selfTest()]
- "probe_go_main_protoor": "protoOr()" | kind=code-symbol | source=probe-go/main.go:L212 | neighbors=[main.go, renderReport()]
- "probe_pipeline_collector_write": ".write()" | kind=code-symbol | source=probe/pipeline.py:L126 | neighbors=[_Collector, _run_active()]
- "probe_run_scan_main": "main()" | kind=code-symbol | source=probe/run_scan.py:L135 | neighbors=[run_scan.py, _orchestrate()]
- "probe_run_scan_orchestrate": "_orchestrate()" | kind=code-symbol | source=probe/run_scan.py:L62 | neighbors=[run_scan.py, main()]
- "prompts_report": "report.ts" | kind=code-symbol | source=manager/frontend/lib/prompts/report.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, ai-engine.ts]
- "prompts_triage": "triage.ts" | kind=code-symbol | source=manager/frontend/lib/prompts/triage.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, ai-engine.ts]
- "routers_activity_recent_activity": "recent_activity()" | kind=code-symbol | source=manager/backend/app/routers/activity.py:L41 | neighbors=[activity.py, ActivityItem]
- "routers_ad_set_job_status": "_set_job_status()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L201 | neighbors=[ad.py, _run_ad_assessment_and_save()]
- "routers_agent_advisor_list_recommendations": "list_recommendations()" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L72 | neighbors=[agent_advisor.py, _rec_dict()]
- "routers_agent_advisor_rec_dict": "_rec_dict()" | kind=code-symbol | source=manager/backend/app/routers/agent_advisor.py:L31 | neighbors=[agent_advisor.py, list_recommendations()]
- "routers_agent_ws_agent_websocket_endpoint": "agent_websocket_endpoint()" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L43 | neighbors=[agent_ws.py, Persistent WebSocket for probe → manage…]
- "routers_agent_ws_rationale_1": "agent_ws.py — WebSocket endpoint for probe push connectivity.  Probes connect vi" | kind=entity | source=manager/backend/app/routers/agent_ws.py:L1 | neighbors=[ScanJob, agent_ws.py]
- "routers_agent_ws_rationale_44": "Persistent WebSocket for probe → manager push communication.      Query params:" | kind=entity | source=manager/backend/app/routers/agent_ws.py:L44 | neighbors=[ScanJob, agent_websocket_endpoint()]
- "routers_agents_get_job_status": "get_job_status()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L458 | neighbors=[agents.py, Lets the frontend poll a specific job's…]
- "routers_agents_heartbeat": "heartbeat()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L356 | neighbors=[agents.py, _agent_ownership_check()]
- "routers_agents_list_use_cases": "list_use_cases()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L264 | neighbors=[agents.py, Returns the finite library of scan use-…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-050.json

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
