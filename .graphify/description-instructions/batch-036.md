# Node Description Batch 37 of 104

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

- "models_outbox": "outbox.py" | kind=code-symbol | source=manager/backend/app/models/outbox.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, OutboxEvent, outbox.py — transactional outbox for du…]
- "models_outbox_rationale_1": "outbox.py — transactional outbox for durable, exactly-once background work.  THE" | kind=entity | source=manager/backend/app/models/outbox.py:L1 | neighbors=[Base, TimestampMixin, outbox.py]
- "models_scan_job": "scan_job.py" | kind=code-symbol | source=manager/backend/app/models/scan_job.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, ScanJob]
- "models_scan_result_rationale_11": "Append-only raw probe facts (P3-#10).      Decoupled from scan_jobs so:       (a" | kind=entity | source=manager/backend/app/models/scan_result.py:L11 | neighbors=[Base, TimestampMixin, ScanResult]
- "native_port_scan_nativeportscan": "nativePortScan()" | kind=code-symbol | source=manager/frontend/lib/engine/native/port-scan.ts:L221 | neighbors=[tool-runners.ts, port-scan.ts, resolvePorts()]
- "netexec_route_post": "POST()" | kind=code-symbol | source=manager/frontend/app/api/scan/netexec/route.ts:L41 | neighbors=[route.ts, parseNxcOutput(), runNxc()]
- "pipeline_pipeline_assembleerror": "assembleError()" | kind=code-symbol | source=probe-go/pipeline/pipeline.go:L428 | neighbors=[pipeline.go, assemble(), Run()]
- "pipeline_route_runnaabustage": "runNaabuStage()" | kind=code-symbol | source=manager/frontend/app/api/scan/pipeline/route.ts:L40 | neighbors=[route.ts, stealthToScanParams(), runPipelineBackground()]
- "pipeline_route_runnmapstage": "runNmapStage()" | kind=code-symbol | source=manager/frontend/app/api/scan/pipeline/route.ts:L122 | neighbors=[route.ts, stealthToScanParams(), runPipelineBackground()]
- "pipeline_route_stealthtoscanparams": "stealthToScanParams()" | kind=code-symbol | source=manager/frontend/app/api/scan/pipeline/route.ts:L31 | neighbors=[route.ts, runNaabuStage(), runNmapStage()]
- "probe_go_main_run": "run()" | kind=code-symbol | source=probe-go/main.go:L220 | neighbors=[main.go, localScan(), main()]
- "probe_go_main_selftest": "selfTest()" | kind=code-symbol | source=probe-go/main.go:L240 | neighbors=[main.go, main(), isDirWritable()]
- "probe_pipeline_clean": "_clean()" | kind=code-symbol | source=probe/pipeline.py:L251 | neighbors=[pipeline.py, Make a raw banner safe and readable for…, _rollup()]
- "probe_pipeline_rollup": "_rollup()" | kind=code-symbol | source=probe/pipeline.py:L275 | neighbors=[pipeline.py, _clean(), _run_active()]
- "probe_pipeline_shared": "_shared()" | kind=code-symbol | source=probe/pipeline.py:L132 | neighbors=[pipeline.py, Make a per-host scanner instance share …, _run_active()]
- "routers_ad_run_ad_assessment_and_save": "_run_ad_assessment_and_save()" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L129 | neighbors=[ad.py, Background task: run the AD assessment …, _set_job_status()]
- "routers_agents_enqueue_agent_job": "enqueue_agent_job()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L504 | neighbors=[agents.py, _encrypt_scope_for_agent(), _resolve_scan_type()]
- "routers_agents_get_agent_jobs": "get_agent_jobs()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L393 | neighbors=[agents.py, _agent_ownership_check(), _encrypt_scope_for_agent()]
- "routers_ai_report_build_engagement_summary": "_build_engagement_summary()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L211 | neighbors=[ai_report.py, _run_generation(), _run_regeneration()]
- "routers_ai_report_pending_outputs": "_pending_outputs()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L188 | neighbors=[ai_report.py, approve_report(), reject_report()]
- "routers_ai_report_run_regeneration": "_run_regeneration()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L320 | neighbors=[ai_report.py, Background task: regenerate rejected se…, _build_engagement_summary()]
- "routers_attack_paths_blast_radius": "blast_radius()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L137 | neighbors=[attack_paths.py, _asset_labels(), _build_analyzer()]
- "routers_attack_paths_get_attack_path": "get_attack_path()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L75 | neighbors=[attack_paths.py, _asset_labels(), _explain_hop()]
- "routers_attack_paths_list_attack_paths": "list_attack_paths()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L43 | neighbors=[attack_paths.py, _path_summary(), _recompute_and_store()]
- "routers_detection_run_correlation": "_run_correlation()" | kind=code-symbol | source=manager/backend/app/routers/detection.py:L233 | neighbors=[detection.py, Background task: pull SIEM/EDR telemetr…, _set_job()]
- "routers_detection_runs_run_dict": "_run_dict()" | kind=code-symbol | source=manager/backend/app/routers/detection_runs.py:L37 | neighbors=[detection_runs.py, latest_run_delta(), list_detection_runs()]
- "routers_engagements_overview_cache_key": "_overview_cache_key()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L34 | neighbors=[engagements.py, engagements_overview(), _refresh_overview_cache()]
- "routers_engagements_parse_probe_file": "_parse_probe_file()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L178 | neighbors=[engagements.py, import_facts(), Parse a probe export into (facts, scan_…]
- "routers_engagements_promote_from_facts": "_promote_from_facts()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L225 | neighbors=[engagements.py, import_facts(), Upsert assets (and their services) from…]
- "routers_engagements_read_capped": "_read_capped()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L160 | neighbors=[engagements.py, import_facts(), Read an UploadFile in chunks, aborting …]
- "routers_exploits_approval_out": "_approval_out()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L434 | neighbors=[exploits.py, ApprovalOut, list_approvals()]
- "routers_exploits_get_approval_or_404": "_get_approval_or_404()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L409 | neighbors=[exploits.py, approve_exploit(), reject_exploit()]
- "routers_exploits_get_exploit_result": "get_exploit_result()" | kind=code-symbol | source=manager/backend/app/routers/exploits.py:L206 | neighbors=[exploits.py, _get_result_or_404(), _result_out()]
- "runtimeerror": "RuntimeError" | kind=code-symbol | neighbors=[HWBindError, AgentUnavailableError, LLMUnavailableError]
- "scanner_db_probemongo": "probeMongo()" | kind=code-symbol | source=probe-go/scanner/db.go:L199 | neighbors=[db.go, ProbeDB(), dial()]
- "scanner_db_probemssql": "probeMSSQL()" | kind=code-symbol | source=probe-go/scanner/db.go:L136 | neighbors=[db.go, ProbeDB(), dial()]
- "scanner_db_probemysql": "probeMysql()" | kind=code-symbol | source=probe-go/scanner/db.go:L73 | neighbors=[db.go, ProbeDB(), dial()]
- "scanner_db_probepostgres": "probePostgres()" | kind=code-symbol | source=probe-go/scanner/db.go:L107 | neighbors=[db.go, ProbeDB(), dial()]
- "scanner_db_proberedis": "probeRedis()" | kind=code-symbol | source=probe-go/scanner/db.go:L176 | neighbors=[db.go, ProbeDB(), dial()]
- "scanner_db_scanner_dbscanner_scan_port": "._scan_port()" | kind=code-symbol | source=probe/scanner/db_scanner.py:L256 | neighbors=[DBScanner, ._probe_one(), .scan_target()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-036.json

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
