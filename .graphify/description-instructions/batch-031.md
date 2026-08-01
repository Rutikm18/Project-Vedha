# Node Description Batch 32 of 119

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

- "lib_agents_store_registeragent": "registerAgent()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L362 | neighbors=[agents-store.ts, genFieldAgentId(), readFieldAgents(), writeFieldAgents()]
- "lib_agents_store_writefieldagents": "writeFieldAgents()" | kind=code-symbol | source=manager/frontend/lib/agents-store.ts:L350 | neighbors=[agents-store.ts, registerAgent(), updateAgentLastSeen(), ensureDataDir()]
- "lib_ai_engine_getclient": "getClient()" | kind=code-symbol | source=manager/frontend/lib/ai-engine.ts:L422 | neighbors=[ai-engine.ts, chat(), generateReport(), triageFindings()]
- "lib_backend_cookiefrom": "cookieFrom()" | kind=code-symbol | source=manager/frontend/lib/backend.ts:L76 | neighbors=[backend.ts, bearerFrom(), route.ts, backend-auth.test.ts]
- "lib_clients_store_createclient": "createClient()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L87 | neighbors=[clients-store.ts, read(), slugify(), write()]
- "lib_clients_store_updateclient": "updateClient()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L105 | neighbors=[clients-store.ts, read(), slugify(), write()]
- "lib_errors_diagnosespawnerror": "diagnoseSpawnError()" | kind=code-symbol | source=manager/frontend/lib/errors.ts:L244 | neighbors=[tool-runners.ts, errors.ts, VedhaError, AdversaError]
- "lib_httpx_parser_httpxjsonldecoder_decode": ".decode()" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L116 | neighbors=[HttpxJsonlDecoder, .push(), parseHttpxJsonLine(), .finish()]
- "lib_job_store_createjob": "createJob()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L41 | neighbors=[job-store.ts, genJobId(), readJobs(), writeJobs()]
- "lib_nuclei_parser_nucleiseveritytoseverity": "nucleiSeverityToSeverity()" | kind=code-symbol | source=manager/frontend/lib/nuclei-parser.ts:L71 | neighbors=[tool-runners.ts, nuclei-parser.ts, nucleiMatchToFinding(), parsers.test.ts]
- "lib_permissions_store_adduser": "addUser()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L60 | neighbors=[permissions-store.ts, read(), write(), route.ts]
- "lib_permissions_store_isemailallowed": "isEmailAllowed()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L48 | neighbors=[auth-middleware.ts, permissions-store.ts, read(), route.ts]
- "lib_severity_sev_color": "SEV_COLOR" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L29 | neighbors=[FactCard.tsx, page.tsx, severity.ts, page.tsx]
- "lib_target_parser_parsetargets": "parseTargets()" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L72 | neighbors=[scanner.ts, target-parser.ts, estimateHostCount(), isValidTarget()]
- "logout_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/logout/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, POST(), 2885afa Add comprehensive probe testing…]
- "models_agent_recommendation": "agent_recommendation.py" | kind=code-symbol | source=manager/backend/app/models/agent_recommendation.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, AgentRecommendation, agent_recommendation.py — decisions/act…, 2885afa Add comprehensive probe testing…]
- "models_asset": "asset.py" | kind=code-symbol | source=manager/backend/app/models/asset.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, Asset, 298a9d4 trim frontend to 7 core pages; …]
- "models_detection_run": "detection_run.py" | kind=code-symbol | source=manager/backend/app/models/detection_run.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, DetectionRun, detection_run.py — one execution of the…, 2885afa Add comprehensive probe testing…]
- "models_enums_userrole": "UserRole" | kind=code-symbol | source=manager/backend/app/models/enums.py:L4 | neighbors=[enums.py, str, User, Idempotent admin seeder.  Creates a ten…]
- "models_exploit_result": "exploit_result.py" | kind=code-symbol | source=manager/backend/app/models/exploit_result.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, ExploitResult, 298a9d4 trim frontend to 7 core pages; …]
- "models_init": "__init__.py" | kind=code-symbol | source=manager/backend/app/models/__init__.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …]
- "models_llm_output_rationale_13": "Every LLM generation is persisted here for human-in-the-loop review.      AI out" | kind=entity | source=manager/backend/app/models/llm_output.py:L13 | neighbors=[Base, TimestampMixin, ReviewStatus, LLMOutput]
- "models_outbox": "outbox.py" | kind=code-symbol | source=manager/backend/app/models/outbox.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, OutboxEvent, outbox.py — transactional outbox for du…, 2885afa Add comprehensive probe testing…]
- "models_tenant_tenant": "Tenant" | kind=code-symbol | source=manager/backend/app/models/tenant.py:L11 | neighbors=[tenant.py, Base, Base, Idempotent admin seeder.  Creates a ten…]
- "native_dir_bust_nativedirbust": "nativeDirBust()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L113 | neighbors=[tool-runners.ts, dir-bust.ts, loadWordlist(), probe()]
- "native_dns_recon_nativednsrecon": "nativeDnsRecon()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L53 | neighbors=[tool-runners.ts, dns-recon.ts, attemptZoneTransfer(), safe()]
- "probe_pipeline_collector": "_Collector" | kind=code-symbol | source=probe/pipeline.py:L121 | neighbors=[pipeline.py, .__init__(), .write(), _run_active()]
- "probe_selftest_live_handler": "_Handler" | kind=code-symbol | source=probe/selftest_live.py:L46 | neighbors=[selftest_live.py, .do_GET(), .do_OPTIONS(), .log_message()]
- "probe_selftest_live_main": "main()" | kind=code-symbol | source=probe/selftest_live.py:L91 | neighbors=[selftest_live.py, check(), _fact(), _free_port()]
- "probe_showcase_run_main": "main()" | kind=code-symbol | source=probe/showcase_run.py:L100 | neighbors=[showcase_run.py, list_use_cases(), _print_summary(), _split()]
- "routers_activity_rationale_1": "Recent activity feed.  A tenant-wide, read-only stream of the operator-relevant" | kind=entity | source=manager/backend/app/routers/activity.py:L1 | neighbors=[Engagement, Finding, ScanJob, activity.py]
- "routers_agents_get_agent_jobs": "get_agent_jobs()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L614 | neighbors=[agents.py, _agent_can_execute_job(), _agent_ownership_check(), _encrypt_scope_for_agent()]
- "routers_agents_get_job_status": "get_job_status()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L705 | neighbors=[agents.py, Lets the frontend poll a specific job's…, Lets the frontend poll a specific job's…, Lets the frontend poll a specific job's…]
- "routers_agents_list_use_cases": "list_use_cases()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L443 | neighbors=[agents.py, Returns the finite library of scan use-…, Returns the finite library of scan use-…, Returns the finite library of scan use-…]
- "routers_agents_scope_is_reachable": "_scope_is_reachable()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L99 | neighbors=[agents.py, _agent_can_execute_job(), Return whether a probe's declared netwo…, Return whether a probe's declared netwo…]
- "routers_ai_report_run_generation": "_run_generation()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L262 | neighbors=[ai_report.py, Background task: build the summary, gen…, _build_engagement_summary(), _set_job()]
- "routers_attack_paths_all_paths_to_critical": "_all_paths_to_critical()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L191 | neighbors=[attack_paths.py, attack_graph(), list_chokepoints(), _recompute_and_store()]
- "routers_attack_paths_asset_labels": "_asset_labels()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L225 | neighbors=[attack_paths.py, blast_radius(), get_attack_path(), list_chokepoints()]
- "routers_attack_paths_attack_graph": "attack_graph()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L153 | neighbors=[attack_paths.py, _all_paths_to_critical(), _build_analyzer(), _critical_asset_ids()]
- "routers_attack_paths_critical_asset_ids": "_critical_asset_ids()" | kind=code-symbol | source=manager/backend/app/routers/attack_paths.py:L181 | neighbors=[attack_paths.py, attack_graph(), list_chokepoints(), _recompute_and_store()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-031.json

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
