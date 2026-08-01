# Node Description Batch 15 of 119

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

- "workflow_cache_workflowcache": "WorkflowCache" | kind=code-symbol | source=probe/workflow/cache.py:L78 | neighbors=[cache.py, In-memory (host, port, scanner) -> Cach…, .all_entries_for_host(), .get(), .__init__(), ._load()]
- "workflow_modes_engagementmode": "EngagementMode" | kind=code-symbol | source=probe/workflow/modes.py:L51 | neighbors=[modes.py, assessment(), discovery(), host_discovery(), port_scan(), re_scan()]
- "workflow_workflow_engine_sink": "_Sink" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L133 | neighbors=[workflow_engine.py, In-memory ResultWriter stand-in — Passi…, _run_inventory(), _run_passive(), .close(), .__init__()]
- "activity_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/activity/route.ts:L1 | neighbors=[ApiActivity, GET, backend.ts, backend(), with-backend.ts, withBackend()]
- "ad_findings": "findings.py" | kind=code-symbol | source=manager/backend/app/ad/findings.py:L1 | neighbors=[ADConnectionError, ADError, build_ad_finding(), DependencyMissingError, severity_from_str(), Shared building blocks for the Active D…]
- "agent_agent_main": "main()" | kind=code-symbol | source=probe/agent/agent.py:L69 | neighbors=[agent.py, _bounded_env_int(), _load_env(), _obtain_identity(), _run_polled_job_with_heartbeats(), _run_ws_push_loop()]
- "agent_agent_runjob": ".runJob()" | kind=code-symbol | source=probe-go/agent/agent.go:L551 | neighbors=[agent.py, mapToJob(), resultToMap(), .Run(), say(), .runPolledJob()]
- "agent_agent_runpollloop": ".runPollLoop()" | kind=code-symbol | source=probe-go/agent/agent.go:L393 | neighbors=[agent.py, .Run(), .heartbeatWithRetry(), .rejectJob(), .runPolledJob(), say()]
- "agent_agent_ws_test": "agent_ws_test.go" | kind=code-symbol | source=probe-go/agent/agent_ws_test.go:L1 | neighbors=[boolToInt(), readJSONFile(), TestResultPayloadWrapsManagerContract(), TestWSJSONWriterSerializesConcurrentWri…, TestWSSessionExecutesOnlyAfterPositiveC…, TestWSSessionRequiresAtomicClaimFeature…]
- "agent_result_spool": "result_spool.py" | kind=code-symbol | source=probe/agent/result_spool.py:L1 | neighbors=[ResultSpool, result_spool.py — local result persiste…, 10dfc80 Add comprehensive probe testing…, b4b12a9 Rename project and update files, test_integration.py, test_result_spool.py]
- "agent_result_spool_resultspool_exists": ".exists()" | kind=code-symbol | source=probe/agent/result_spool.py:L86 | neighbors=[Check if a spooled result exists for th…, ResultSpool, ._path(), .flush_spool(), .load(), .spool_count()]
- "agent_transport_transporterror": "TransportError" | kind=code-symbol | source=probe/agent/transport.py:L33 | neighbors=[transport.py, Raised when a transport operation fails…, .connect_ws(), .poll_jobs(), .refresh_registration(), .register()]
- "ai_prioritizer": "prioritizer.py" | kind=code-symbol | source=manager/backend/app/ai/prioritizer.py:L1 | neighbors=[extract_features(), _to_float(), VulnPrioritizer, VulnPrioritizer — ML-based vulnerabilit…, 10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …]
- "auth_pat": "pat.py" | kind=code-symbol | source=manager/backend/app/auth/pat.py:L1 | neighbors=[build_personal_access_token(), hash_pat_token(), new_pat_token(), pat_display_prefix(), pat_scope_allows(), validate_pat_scopes()]
- "branch:repo:github.com/Rutikm18/Agentic-VA-Automation#main": "main" | kind=Branch | source=git | neighbors=[0510df3 going to build prompt and conne…, 0557559 scanner: real use-case library,…, 2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, 8d65c92 first commit, a388bb3 script updated, architecture de…]
- "branch:repo:github.com/Rutikm18/Project-Vedha#main": "main" | kind=Branch | source=git | neighbors=[0510df3 going to build prompt and conne…, 10dfc80 Add comprehensive probe testing…, 8d65c92 first commit, a388bb3 script updated, architecture de…, a789cca scanner: real use-case library,…, bd7383f scanner fine ..now integrations]
- "cli_auth_apifetch": "apiFetch()" | kind=code-symbol | source=manager/frontend/cli/auth.ts:L46 | neighbors=[auth.ts, serverUrl(), admin.ts, engagement.ts, interactive.ts, report.ts]
- "cli_llm_client": "client()" | kind=code-symbol | source=manager/frontend/cli/llm.ts:L10 | neighbors=[llm.ts, commentOnStage(), explainFindings(), planExploit(), recommendNextPhase(), streamAsk()]
- "commands_interactive_picktargets": "pickTargets()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L226 | neighbors=[interactive.ts, ask(), choose(), confirm(), detectLocalSubnet(), inferHostsFromFindings()]
- "commands_interactive_wizardengagement": "wizardEngagement()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1769 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), divider(), fetchEngagements()]
- "commands_interactive_wizardreport": "wizardReport()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1847 | neighbors=[interactive.ts, mainMenu(), ask(), choose(), confirm(), divider()]
- "commands_interactive_wizardvalidate": "wizardValidate()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1465 | neighbors=[interactive.ts, mainMenu(), runValidationFlow(), ask(), choose(), confirm()]
- "commit:repo:github.com/Rutikm18/Project-Vedha@95904f12026e4ec0fa276f7b30f0017fca2b0bea": "95904f1 feat(probe): detect SMB signing-required from negotiate response" | kind=Commit | source=git | neighbors=[5c8e696 docs(probe): correct overclaimi…, use_cases.py, backup-before-secret-removal, feat/probe-usecase-alignment, e8262a3 feat(probe): explicit unauthent…, smb_scanner.py]
- "commit:repo:github.com/Rutikm18/Project-Vedha@bce780a80117d235fa4faedbd73cffc97843cefa": "bce780a feat(probe): enumerate HTTP methods via OPTIONS in web scanner" | kind=Commit | source=git | neighbors=[use_cases.py, backup-before-secret-removal, feat/probe-usecase-alignment, 01f4398 feat(probe): IoT survey reaches…, web_scanner.py, test_use_cases.py]
- "commit:repo:github.com/Rutikm18/Project-Vedha@fe868e690970a25ff8241b441d44ee46cbc77f09": "fe868e6 feat(probe): real UDP amplification probes (monlist, open recursion, me…" | kind=Commit | source=git | neighbors=[e8262a3 feat(probe): explicit unauthent…, use_cases.py, backup-before-secret-removal, feat/probe-usecase-alignment, bce780a feat(probe): enumerate HTTP met…, udp_scanner.py]
- "dashboard_protocolrow": "ProtocolRow.tsx" | kind=code-symbol | source=manager/frontend/components/dashboard/ProtocolRow.tsx:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ProtocolRow(), riskColor(), ProtocolRisk, 298a9d4 trim frontend to 7 core pages; …, Exposure.tsx]
- "detection_engine_ai_normalizer_aiclient": "AIClient" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L88 | neighbors=[ai_normalizer.py, .propose_cpe(), CPECandidate, Fact, Protocol, pipeline.py — Phase 1 + Phase 2 end to …]
- "detection_engine_consistency": "consistency.py" | kind=code-symbol | source=manager/detection_engine/consistency.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, aggregate(), ConsistencyReport, FindingConsistency, format_line(), wilson_ci()]
- "detection_siem_siemqueryengine": "SIEMQueryEngine" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L50 | neighbors=[siem.py, ElasticSIEM, Abstract SIEM connector., SentinelSIEM, .__init__(), .query_alerts()]
- "discovery_service_id_serviceidentifier": "ServiceIdentifier" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L73 | neighbors=[service_id.py, .identify(), DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…]
- "enum": "Enum" | kind=code-symbol | neighbors=[models.py, FindingState, SourceConfidence, verifier.py, agent.py, enums.py]
- "exploit_orchestrator_exploitorchestrator_execute": ".execute()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L123 | neighbors=[ExploitOrchestrator, ._check_blast_radius(), ._audit(), ._check_approval_required(), .select_exploit(), .validate_safety()]
- "exposure_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/analytics/exposure/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, Exposure, GET, backend(), withBackend(), 2885afa Add comprehensive probe testing…]
- "frontend_next_config": "next.config.mjs" | kind=code-symbol | source=manager/frontend/next.config.mjs:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, __dirname, frontendRoot, nextConfig, securityHeaders]
- "lib_job_store_readjobs": "readJobs()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L25 | neighbors=[job-store.ts, createJob(), getAllJobs(), getJobByScanId(), getNextJobForAgent(), markDispatched()]
- "probe_selftest_live": "selftest_live.py" | kind=code-symbol | source=probe/selftest_live.py:L1 | neighbors=[b4b12a9 Rename project and update files, engine.py, _c(), check(), _fact(), _free_port()]
- "probe_showcase_run": "showcase_run.py" | kind=code-symbol | source=probe/showcase_run.py:L1 | neighbors=[b4b12a9 Rename project and update files, engine.py, use_cases.py, _c(), list_use_cases(), main()]
- "routers_analytics": "analytics.py" | kind=code-symbol | source=manager/backend/app/routers/analytics.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, dependencies.py, exposure(), ExposureAnalytics, ProtocolRisk, ZoneHealth]
- "routers_attack_paths_rationale_1": "Attack path analysis API (AttackPathService).  GET /engagements/{id}/attack-path" | kind=entity | source=manager/backend/app/routers/attack_paths.py:L1 | neighbors=[PathAnalyzer, GraphBuilder, GraphVisualizer, Asset, AttackPath, Engagement]
- "routers_vuln_scans_run_nuclei_and_save": "_run_nuclei_and_save()" | kind=code-symbol | source=manager/backend/app/routers/vuln_scans.py:L271 | neighbors=[vuln_scans.py, Run Nuclei and always leave its job in …, _finish_cancelled_nuclei_job(), _finish_failed_nuclei_job(), _nuclei_finding(), _nuclei_terminal_result()]

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
