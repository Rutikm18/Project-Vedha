# Node Description Batch 20 of 236

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

- "agent_agent_ws_heartbeat_sender": "_ws_heartbeat_sender()" | kind=code-symbol | source=probe/agent/agent.py:L845 | neighbors=[agent.py, Send periodic heartbeats over WebSocket., _run_ws_push_loop(), Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket., Send periodic heartbeats over WebSocket.]
- "agent_cli_configstore": "ConfigStore" | kind=code-symbol | source=probe/agent/cli.py:L55 | neighbors=[cli.py, cmd_auth_login(), cmd_auth_logout(), .get_profile(), .__init__(), .load()]
- "agent_cli_resolve_profile": "resolve_profile()" | kind=code-symbol | source=probe/agent/cli.py:L196 | neighbors=[cli.py, client_from_args(), cmd_daemon_run(), cmd_doctor(), cmd_validate(), CliError]
- "agent_result_spool_resultspool_exists": ".exists()" | kind=code-symbol | source=probe/agent/result_spool.py:L95 | neighbors=[Check if a spooled result exists for th…, ResultSpool, ._path(), .flush_spool(), .load(), .spool_bytes()]
- "agent_transport_transport_ensure_device_access": ".ensure_device_access()" | kind=code-symbol | source=probe/agent/transport.py:L438 | neighbors=[Refresh a device token before expiry; l…, Transport, .connect_ws(), .load_state(), .refresh_device_access(), .heartbeat()]
- "agent_validation": "validation.py" | kind=code-symbol | source=probe/agent/validation.py:L1 | neighbors=[_metric(), _not_scored(), resolve_use_cases(), score_inventory(), target_address_count(), validate_ground_truth()]
- "ai_agent_agentunavailableerror": "AgentUnavailableError" | kind=code-symbol | source=manager/backend/app/ai/agent.py:L58 | neighbors=[agent.py, .run(), RuntimeError, Raised when the Anthropic SDK or API ke…, AgentRecommendation, Asset]
- "app_ratelimit": "ratelimit.py" | kind=code-symbol | source=manager/backend/app/ratelimit.py:L1 | neighbors=[dependencies.py, _check(), client_ip(), rate_limit(), ratelimit.py — P2: Redis-backed rate li…, router.py]
- "assistant_advisorflow": "AdvisorFlow.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/AdvisorFlow.tsx:L1 | neighbors=[AdvisorFlow(), CommandRow(), CopyButton(), PATCH_PILL, RichText(), Section()]
- "auth_jwt": "jwt.py" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L1 | neighbors=[config.py, create_access_token(), create_device_access_token(), create_refresh_token(), decode_token(), _now()]
- "auth_middleware_tenantisolationmiddleware": "TenantIsolationMiddleware" | kind=code-symbol | source=manager/backend/app/auth/middleware.py:L58 | neighbors=[middleware.py, Extracts JWT from Authorization header …, ._authenticate_pat(), .dispatch(), BaseHTTPMiddleware, GzipRequestMiddleware]
- "chat_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/assistant/chat/route.ts:L1 | neighbors=[ManagerAiResponse, POST(), backend.ts, backend(), BackendError, bearerFrom()]
- "cli_auth_requireauth": "requireAuth()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L33 | neighbors=[auth.ts, loadSession(), admin.ts, ask.ts, engagement.ts, interactive.ts]
- "commands_engagement": "engagement.ts" | kind=code-symbol | source=manager/frontend/cli/commands/engagement.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildEngagementCommand(), Engagement, errExit(), STATUS_COLOR]
- "commands_findings": "findings.ts" | kind=code-symbol | source=manager/frontend/cli/commands/findings.ts:L1 | neighbors=[buildFindingsCommand(), Severity, getAllFindings(), getFindingById(), d1b4dd3 trim frontend to 7 core pages; …, index.ts]
- "commands_interactive_runvalidationflow": "runValidationFlow()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1275 | neighbors=[interactive.ts, runAutonomousMode(), runIterativeEngagement(), choose(), confirm(), ln()]
- "commit:repo:github.com/Rutikm18/Agentic-VA-Automation@0557559df67e8c0dcff8a3478ef636be891e24c5": "0557559 scanner: real use-case library, probe-to-manager flow, rebuilt Scanner …" | kind=Commit | source=git | neighbors=[use_cases.py, main, 2885afa Add comprehensive probe testing…, route.ts, route.ts, route.ts]
- "commit:repo:github.com/Rutikm18/Project-Vedha@25344045b42fb3f74183072c0b432ee8c30db287": "2534404 scanner(service_enum): commit owner's in-progress changes as-is + re-sy…" | kind=Commit | source=git | neighbors=[feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, integration/all-branches, main]
- "commit:repo:github.com/Rutikm18/Project-Vedha@35691030666303cbdc4b5214a09373d49b3d2bcf": "3569103 docs(agent): research + design for Vedha Autonomous Engagement Agent" | kind=Commit | source=git | neighbors=[feat/autonomous-offensive-agent, feat/complete-pending-work, feat/engagement-detail-uiux, feat/nvd-vuln-detection-and-ingest-hard…, fix/probe-already-enrolled-409, integration/all-branches]
- "detection_edr": "edr.py" | kind=code-symbol | source=manager/backend/app/detection/edr.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, build_edr_engine(), CrowdStrikeFalcon, EDRDetection, EDRQueryEngine, MicrosoftDefender]
- "detection_engine_ai_normalizer": "ai_normalizer.py" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AIClient, AINormalizerCache, AnthropicAIClient, extract_raw_text(), FakeAIClient]
- "detection_engine_enrichment_db": "enrichment_db.py" | kind=code-symbol | source=manager/detection_engine/enrichment_db.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, d1b4dd3 trim frontend to 7 core pages; …, _cache_key(), _clear_caches(), EpssDB, KevDB]
- "detection_engine_models": "models.py" | kind=code-symbol | source=manager/detection_engine/models.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Asset, Fact, Finding, FindingState, make_finding_id()]
- "detection_siem": "siem.py" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, build_siem_engine(), ElasticSIEM, _parse_dt(), SentinelSIEM, SIEMAlert]
- "draft_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/draft/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, GET(), backend.ts, backend(), BackendError]
- "exploit_msf_client_metasploitrpcclient_call": "._call()" | kind=code-symbol | source=manager/backend/app/exploit/msf_client.py:L151 | neighbors=[MetasploitRPCClient, ._raw_call(), MetasploitRPCError, .disconnect(), .get_job_status(), .kill_job()]
- "exploit_orchestrator_rationale_104": "Raises SafetyViolationError if module or payload is not permitted." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L104 | neighbors=[.validate_safety(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_111": "Raises OutOfScopeError if target_ip not in engagement scope." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L111 | neighbors=[.validate_scope(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_131": "Full exploit execution pipeline with safety, scope, blast radius,         audit" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L131 | neighbors=[.execute(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_253": "Returns a unique FQDN for out-of-band DNS/HTTP callback confirmation.         Fo" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L253 | neighbors=[.generate_dns_callback_token(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_266": "Count running exploit jobs for this engagement; raise if over limit." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L266 | neighbors=[._check_blast_radius(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_297": "Creates and returns an ExploitApprovalRequest if approval is needed." | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L297 | neighbors=[._check_approval_required(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_43": "Coordinates safe exploit validation runs:       1. Safety validation (payload al" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L43 | neighbors=[ExploitOrchestrator, MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "exploit_orchestrator_rationale_68": "Returns {module, payload, safe_check} for the given finding.         Priority: C" | kind=entity | source=manager/backend/app/exploit/orchestrator.py:L68 | neighbors=[.select_exploit(), MetasploitRPCClient, ApprovalRequiredError, BlastRadiusExceededError, AuditLog, Engagement]
- "jobid_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/ai-report/status/[jobId]/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, GET(), backend.ts, backend(), BackendError]
- "lib_httpx_parser": "httpx-parser.ts" | kind=code-symbol | source=manager/frontend/lib/httpx-parser.ts:L1 | neighbors=[b4b12a9 Rename project and update files, tool-runners.ts, HttpxJsonlDecoder, HttpxJsonRecord, HttpxLineParseResult, isOptionalNumber()]
- "lib_naabu_parser": "naabu-parser.ts" | kind=code-symbol | source=manager/frontend/lib/naabu-parser.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, DiscoveredHost, groupNaabuResults(), NaabuRaw, NaabuResult]
- "lib_tenant_server": "tenant-server.ts" | kind=code-symbol | source=manager/frontend/lib/tenant-server.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, Client, getClientBySubdomain(), clientFromRequest(), currentClient(), readTenantSubdomain()]
- "main_scripts_accuracy": "accuracy.py" | kind=code-symbol | source=probe/main_scripts/accuracy.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, evaluate_corpus(), _expected_keys(), _finding_key(), format_report(), _main()]
- "main_scripts_scan_funnel": "scan_funnel.py" | kind=code-symbol | source=probe/main_scripts/scan_funnel.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, build_default_funnel(), _candidate_ports(), FunnelResult, _is_alive(), main()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-019.json

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
