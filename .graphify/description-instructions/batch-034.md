# Node Description Batch 35 of 134

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
- "lib_severity_severity": "Severity" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L13 | neighbors=[LiveOverview.tsx, PatchComparisonMatrix.tsx, SlaStatus.tsx, severity.ts]
- "lib_severity_toseverity": "toSeverity()" | kind=code-symbol | source=manager/frontend/lib/severity.ts:L117 | neighbors=[PatchComparisonMatrix.tsx, SlaStatus.tsx, severity.ts, sev()]
- "lib_target_parser_parsetargets": "parseTargets()" | kind=code-symbol | source=manager/frontend/lib/target-parser.ts:L72 | neighbors=[scanner.ts, target-parser.ts, estimateHostCount(), isValidTarget()]
- "logout_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/logout/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, POST(), 2885afa Add comprehensive probe testing…]
- "models_agent_recommendation": "agent_recommendation.py" | kind=code-symbol | source=manager/backend/app/models/agent_recommendation.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, AgentRecommendation, agent_recommendation.py — decisions/act…, 2885afa Add comprehensive probe testing…]
- "models_asset": "asset.py" | kind=code-symbol | source=manager/backend/app/models/asset.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, Asset, 298a9d4 trim frontend to 7 core pages; …]
- "models_detection_run": "detection_run.py" | kind=code-symbol | source=manager/backend/app/models/detection_run.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, DetectionRun, detection_run.py — one execution of the…, 2885afa Add comprehensive probe testing…]
- "models_enums_userrole": "UserRole" | kind=code-symbol | source=manager/backend/app/models/enums.py:L4 | neighbors=[enums.py, str, User, Idempotent admin seeder — production-gr…]
- "models_exploit_result": "exploit_result.py" | kind=code-symbol | source=manager/backend/app/models/exploit_result.py:L1 | neighbors=[cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, ExploitResult, 298a9d4 trim frontend to 7 core pages; …]
- "models_llm_output_rationale_13": "Every LLM generation is persisted here for human-in-the-loop review.      AI out" | kind=entity | source=manager/backend/app/models/llm_output.py:L13 | neighbors=[LLMOutput, Base, TimestampMixin, ReviewStatus]
- "models_outbox": "outbox.py" | kind=code-symbol | source=manager/backend/app/models/outbox.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, OutboxEvent, outbox.py — transactional outbox for du…, 2885afa Add comprehensive probe testing…]
- "models_probe_enrollment_probeenrollmenttoken": "ProbeEnrollmentToken" | kind=code-symbol | source=manager/backend/app/models/probe_enrollment.py:L72 | neighbors=[probe_enrollment.py, Base, TimestampMixin, Pre-authorized, Site-bound enrollment t…]
- "models_scan_job_attempt_scanjobattempt": "ScanJobAttempt" | kind=code-symbol | source=manager/backend/app/models/scan_job_attempt.py:L11 | neighbors=[scan_job_attempt.py, One immutable, fenced execution claim f…, Base, TimestampMixin]
- "models_scan_result": "scan_result.py" | kind=code-symbol | source=manager/backend/app/models/scan_result.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, ScanResult, 298a9d4 trim frontend to 7 core pages; …]
- "models_tenant": "tenant.py" | kind=code-symbol | source=manager/backend/app/models/tenant.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, d1b4dd3 trim frontend to 7 core pages; …, Tenant, 298a9d4 trim frontend to 7 core pages; …]
- "models_tenant_tenant": "Tenant" | kind=code-symbol | source=manager/backend/app/models/tenant.py:L11 | neighbors=[tenant.py, Base, Base, Idempotent admin seeder — production-gr…]
- "models_user": "user.py" | kind=code-symbol | source=manager/backend/app/models/user.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, d1b4dd3 trim frontend to 7 core pages; …, User, 298a9d4 trim frontend to 7 core pages; …]
- "native_dir_bust_nativedirbust": "nativeDirBust()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dir-bust.ts:L113 | neighbors=[tool-runners.ts, dir-bust.ts, loadWordlist(), probe()]
- "native_dns_recon_nativednsrecon": "nativeDnsRecon()" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L53 | neighbors=[tool-runners.ts, dns-recon.ts, attemptZoneTransfer(), safe()]
- "probe_pipeline_collector": "_Collector" | kind=code-symbol | source=probe/pipeline.py:L121 | neighbors=[pipeline.py, .__init__(), .write(), _run_active()]
- "probe_push_results": "push_results.py" | kind=code-symbol | source=probe/push_results.py:L1 | neighbors=[0b7bcb8 feat: probe bootstrap key — sel…, die(), load_facts(), main()]
- "probe_selftest_live_handler": "_Handler" | kind=code-symbol | source=probe/selftest_live.py:L46 | neighbors=[selftest_live.py, .do_GET(), .do_OPTIONS(), .log_message()]
- "probe_selftest_live_main": "main()" | kind=code-symbol | source=probe/selftest_live.py:L91 | neighbors=[selftest_live.py, check(), _fact(), _free_port()]
- "probe_showcase_run_main": "main()" | kind=code-symbol | source=probe/showcase_run.py:L100 | neighbors=[showcase_run.py, list_use_cases(), _print_summary(), _split()]
- "routers_activity_rationale_1": "Recent activity feed.  A tenant-wide, read-only stream of the operator-relevant" | kind=entity | source=manager/backend/app/routers/activity.py:L1 | neighbors=[activity.py, Engagement, Finding, ScanJob]
- "routers_agent_ws_agent_token_from_websocket": "_agent_token_from_websocket()" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L40 | neighbors=[agent_ws.py, agent_websocket_endpoint(), Read an agent bearer token exclusively …, Read an agent bearer token exclusively …]
- "routers_agent_ws_claim_pushed_job": "_claim_pushed_job()" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L46 | neighbors=[agent_ws.py, agent_websocket_endpoint(), Validate eligibility and atomically cla…, Validate eligibility and atomically cla…]
- "routers_agents_get_agent_jobs": "get_agent_jobs()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L778 | neighbors=[agents.py, _agent_can_execute_job(), _agent_ownership_check(), _encrypt_scope_for_agent()]
- "routers_ai_report_run_regeneration": "_run_regeneration()" | kind=code-symbol | source=manager/backend/app/routers/ai_report.py:L381 | neighbors=[ai_report.py, Background task: regenerate rejected se…, _build_engagement_summary(), Background task: regenerate rejected se…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-034.json

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
