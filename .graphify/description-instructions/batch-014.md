# Node Description Batch 15 of 131

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "workflow_router": "router.py" | kind=code-symbol | source=probe/workflow/router.py:L1 | neighbors=[bb0ef3d feat(probe): route DB services …, d1b4dd3 trim frontend to 7 core pages; …, test_probe_core.py, test_router_db.py, looks_like_db(), looks_like_http()] | lang=en
- "activity_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/activity/route.ts:L1 | neighbors=[ApiActivity, GET, backend.ts, backend(), with-backend.ts, withBackend()] | lang=en
- "agent_agent_startup_gauntlet": "_startup_gauntlet()" | kind=code-symbol | source=probe/agent/agent.py:L736 | neighbors=[agent.py, main(), Run all startup security checks before …, _check_anti_debug(), say(), Run all startup security checks before …] | lang=en
- "agent_agent_ws_run_job": "_ws_run_job()" | kind=code-symbol | source=probe/agent/agent.py:L598 | neighbors=[agent.py, Run one job while keeping WS status/res…, _run_ws_push_loop(), _ws_http_poll_fallback(), say(), Run one job while keeping WS status/res…] | lang=en
- "agent_cli_cmd_auth_login": "cmd_auth_login()" | kind=code-symbol | source=probe/agent/cli.py:L237 | neighbors=[cli.py, CliError, ConfigStore, .set_profile(), _env(), ManagerClient] | lang=en
- "agent_result_spool": "result_spool.py" | kind=code-symbol | source=probe/agent/result_spool.py:L1 | neighbors=[ResultSpool, result_spool.py — local result persiste…, 10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, test_integration.py] | lang=en
- "assistant_factcard": "FactCard.tsx" | kind=code-symbol | source=manager/frontend/components/assistant/FactCard.tsx:L1 | neighbors=[page.tsx, AssistantDrawer.tsx, FactCard(), Pip(), assistant.ts, FactCardVM] | lang=en
- "auth_jwt": "jwt.py" | kind=code-symbol | source=manager/backend/app/auth/jwt.py:L1 | neighbors=[config.py, create_access_token(), create_device_access_token(), create_refresh_token(), decode_token(), _now()] | lang=en
- "commands_logout": "logout.ts" | kind=code-symbol | source=manager/frontend/cli/commands/logout.ts:L1 | neighbors=[clearSession(), loadSession(), buildLogoutCommand(), 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, index.ts] | lang=en
- "commands_status": "status.ts" | kind=code-symbol | source=manager/frontend/cli/commands/status.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildStatusCommand(), ScanRow, STATUS_COLOR, d1b4dd3 trim frontend to 7 core pages; …] | lang=en
- "commands_whoami": "whoami.ts" | kind=code-symbol | source=manager/frontend/cli/commands/whoami.ts:L1 | neighbors=[apiFetch(), requireAuth(), buildWhoamiCommand(), 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, index.ts] | lang=en
- "commit:repo:github.com/Rutikm18/Project-Vedha@bb0ef3d473623bac3404761b5c3d34baa72612dd": "bb0ef3d feat(probe): route DB services on non-standard ports via banner signatu…" | kind=Commit | source=git | neighbors=[backup-before-secret-removal, main, spike/probe-go, b4b12a9 Rename project and update files, test_router_db.py, router.py] | lang=en
- "detection_correlator": "correlator.py" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, AttackAction, _aware(), DetectionCorrelator, DetectionGap, DetectionResultDTO] | lang=en
- "detection_engine_ingest_ingest_file": "ingest_file()" | kind=code-symbol | source=manager/detection_engine/ingest.py:L99 | neighbors=[ingest.py, _classify_confidence(), _extract_aliases(), IngestResult, .get_or_create_asset(), QuarantinedLine] | lang=en
- "detection_engine_pipeline_rationale_1": "pipeline.py — Phase 1 + Phase 2 end to end: JSONL in, Findings out.    ingest" | kind=entity | source=manager/detection_engine/pipeline.py:L1 | neighbors=[pipeline.py, AIClient, AINormalizerCache, CPECandidate, EpssDB, KevDB] | lang=en
- "detection_engine_pipeline_rationale_110": "Phase 2 exit criteria: recall gain from AI assist, with zero precision     regre" | kind=entity | source=manager/detection_engine/pipeline.py:L110 | neighbors=[ab_evaluate(), AIClient, AINormalizerCache, CPECandidate, EpssDB, KevDB] | lang=en
- "detection_engine_pipeline_rationale_40": "exposure: optional {asset_ip: {\"internet_facing\": bool, \"auth_enforced\":     boo" | kind=entity | source=manager/detection_engine/pipeline.py:L40 | neighbors=[run_pipeline(), AIClient, AINormalizerCache, CPECandidate, EpssDB, KevDB] | lang=en
- "detection_engine_verifier": "verifier.py" | kind=code-symbol | source=manager/detection_engine/verifier.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, classify_tier(), deception_score(), _evidence_scanners(), EvidenceTier, verify()] | lang=en
- "discovery_finding_translator": "finding_translator.py" | kind=code-symbol | source=manager/backend/app/discovery/finding_translator.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, create_findings_from_probe_result(), _find_open_duplicate(), _map_severity(), _resolve_asset()] | lang=en
- "discovery_service_id_serviceidentifier": "ServiceIdentifier" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L72 | neighbors=[service_id.py, .identify(), DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…] | lang=en
- "engine_tool_runners_bin": "bin()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L72 | neighbors=[tool-runners.ts, binName(), runDbEnum(), runFfuf(), runHttpx(), runNaabu()] | lang=en
- "engine_tool_runners_collectprocess": "collectProcess()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L132 | neighbors=[tool-runners.ts, runDbEnum(), runFfuf(), runHostDiscovery(), runNmapNse(), runSshAudit()] | lang=en
- "exploit_orchestrator_exploitorchestrator_execute": ".execute()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L120 | neighbors=[ExploitOrchestrator, ._check_blast_radius(), ._audit(), ._check_approval_required(), .select_exploit(), .validate_safety()] | lang=en
- "frontend_next_config": "next.config.mjs" | kind=code-symbol | source=manager/frontend/next.config.mjs:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, __dirname, frontendRoot, nextConfig] | lang=en
- "graph_visualizer_graphvisualizer": "GraphVisualizer" | kind=code-symbol | source=manager/backend/app/graph/visualizer.py:L43 | neighbors=[visualizer.py, .__init__(), .to_d3(), Attack path analysis API (AttackPathSer…, Unit tests for the attack-path analysis…, TestGraphBuilder] | lang=en
- "lib_clients_store_read": "read()" | kind=code-symbol | source=manager/frontend/lib/clients-store.ts:L52 | neighbors=[clients-store.ts, createClient(), getClient(), getClientBySubdomain(), listClients(), ensureDir()] | lang=en
- "lib_permissions_store_read": "read()" | kind=code-symbol | source=manager/frontend/lib/permissions-store.ts:L25 | neighbors=[permissions-store.ts, addUser(), getAllUsers(), getUser(), isEmailAllowed(), isScopeAllowed()] | lang=en
- "models_agent": "agent.py" | kind=code-symbol | source=manager/backend/app/models/agent.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, b5ffcb0 Refactor Vedha probe installer …, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, Enum, Agent] | lang=en
- "register_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/agents/register/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, toUiAgent(), backend(), withBackend(), GET, 2885afa Add comprehensive probe testing…] | lang=en
- "request_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/request/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, generateOtp(), isEmailAllowed(), POST(), 2885afa Add comprehensive probe testing…] | lang=en
- "routers_ad_rationale_1": "Active Directory assessment API.  POST /engagements/{id}/ad/assess        — laun" | kind=entity | source=manager/backend/app/routers/ad.py:L1 | neighbors=[ad.py, ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus, ScanJobStatus] | lang=en
- "routers_ad_rationale_135": "Background task: run the AD assessment and persist findings + job result." | kind=entity | source=manager/backend/app/routers/ad.py:L135 | neighbors=[_run_ad_assessment_and_save(), ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus, ScanJobStatus] | lang=en
- "routers_agents_agent_can_execute_job": "_agent_can_execute_job()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L209 | neighbors=[agents.py, _job_reachability_scope(), _required_scan_type(), _scope_is_reachable(), enqueue_agent_job(), get_agent_jobs()] | lang=en
- "routers_agents_agent_ownership_check": "_agent_ownership_check()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L444 | neighbors=[agents.py, get_agent_jobs(), heartbeat(), Verify that the JWT token bearer IS the…, refresh_agent_registration(), submit_job_result()] | lang=en
- "routers_agents_rationale_106": "Return whether a probe's declared networks fully cover a job's scope.      A pro" | kind=entity | source=manager/backend/app/routers/agents.py:L106 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=pt
- "routers_agents_rationale_142": "Return the narrow IP scope needed to route this job.      The engagement scope r" | kind=entity | source=manager/backend/app/routers/agents.py:L142 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_210": "Apply capability and network reachability policy to one dispatch." | kind=entity | source=manager/backend/app/routers/agents.py:L210 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_390": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L390 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_428": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L428 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en
- "routers_agents_rationale_447": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L447 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-014.json

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
