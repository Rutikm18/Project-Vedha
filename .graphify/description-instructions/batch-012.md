# Node Description Batch 13 of 104

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

- "commands_interactive_wizardvalidate": "wizardValidate()" | kind=code-symbol | source=manager/frontend/cli/commands/interactive.ts:L1468 | neighbors=[interactive.ts, mainMenu(), runValidationFlow(), ask(), choose(), confirm()]
- "commands_status": "status.ts" | kind=code-symbol | source=manager/frontend/cli/commands/status.ts:L1 | neighbors=[index.ts, auth.ts, apiFetch(), requireAuth(), buildStatusCommand(), ScanRow]
- "detection_correlator": "correlator.py" | kind=code-symbol | source=manager/backend/app/detection/correlator.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, AttackAction, _aware(), DetectionCorrelator, DetectionGap, DetectionResultDTO]
- "detection_engine_ai_normalizer_aiclient": "AIClient" | kind=code-symbol | source=manager/detection_engine/ai_normalizer.py:L88 | neighbors=[ai_normalizer.py, .propose_cpe(), CPECandidate, Fact, Protocol, pipeline.py — Phase 1 + Phase 2 end to …]
- "detection_engine_bridge": "engine_bridge.py" | kind=code-symbol | source=manager/backend/app/detection/engine_bridge.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, create_findings_from_facts(), detect_findings_from_facts(), _ensure_importable(), run_detection_job()]
- "detection_engine_verifier": "verifier.py" | kind=code-symbol | source=manager/detection_engine/verifier.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, classify_tier(), deception_score(), _evidence_scanners(), EvidenceTier, verify()]
- "detection_engine_vuln_db": "vuln_db.py" | kind=code-symbol | source=manager/detection_engine/vuln_db.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, _content_hash(), _default_products(), load_snapshot(), SnapshotMeta]
- "detection_siem_siemqueryengine": "SIEMQueryEngine" | kind=code-symbol | source=manager/backend/app/detection/siem.py:L50 | neighbors=[siem.py, ElasticSIEM, Abstract SIEM connector., SentinelSIEM, .__init__(), .query_alerts()]
- "discovery_service_id_servicefingerprint": "ServiceFingerprint" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L14 | neighbors=[service_id.py, .identify(), NucleiScanner, NucleiScanner — async subprocess wrappe…, Parse nuclei JSONL output → list of Fin…, Given a list of service names on an ass…]
- "discovery_service_id_serviceidentifier": "ServiceIdentifier" | kind=code-symbol | source=manager/backend/app/discovery/service_id.py:L73 | neighbors=[service_id.py, .identify(), DiscoveryJobPayload, DiscoveryWorker, DiscoveryWorker — full async pipeline: …, Pulled from Redis list `discovery:queue…]
- "e2e_run": "run.py" | kind=code-symbol | source=manager/frontend/tests/e2e/run.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, main(), make_fake_tools(), probe_env(), run_probe()]
- "engine_types_severity": "Severity" | kind=code-symbol | source=manager/frontend/lib/engine/types.ts:L1 | neighbors=[findings.ts, scanner.ts, types.ts, finding-id.ts, findings-store.ts, nuclei-parser.ts]
- "exploit_orchestrator_exploitorchestrator_execute": ".execute()" | kind=code-symbol | source=manager/backend/app/exploit/orchestrator.py:L123 | neighbors=[ExploitOrchestrator, ._check_blast_radius(), ._audit(), ._check_approval_required(), .select_exploit(), .validate_safety()]
- "lib_findings_store_savefindings": "saveFindings()" | kind=code-symbol | source=manager/frontend/lib/findings-store.ts:L51 | neighbors=[tools.ts, route.ts, findings-store.ts, createFinding(), ensureDir(), getAllFindings()]
- "lib_job_store_readjobs": "readJobs()" | kind=code-symbol | source=manager/frontend/lib/job-store.ts:L25 | neighbors=[job-store.ts, createJob(), getAllJobs(), getJobByScanId(), getNextJobForAgent(), markDispatched()]
- "list_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scans/list/route.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, auth-middleware.ts, withAuth(), job-store.ts, getAllJobs(), permissions-store.ts]
- "netexec_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/netexec/route.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, findings-store.ts, createFinding(), NxcHost, parseNxcOutput()]
- "register_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/agents/register/route.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, adapters.ts, toUiAgent(), backend.ts, backend(), with-backend.ts]
- "routers_attack_paths_rationale_1": "Attack path analysis API (AttackPathService).  GET /engagements/{id}/attack-path" | kind=entity | source=manager/backend/app/routers/attack_paths.py:L1 | neighbors=[PathAnalyzer, GraphBuilder, GraphVisualizer, Asset, AttackPath, Engagement]
- "routers_engagements_refresh_overview_cache": "_refresh_overview_cache()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L96 | neighbors=[engagements.py, bulk_import_assets(), create_engagement(), import_facts(), Write-through cache refresh on the WRIT…, _compute_overview()]
- "scanner_db": "db.go" | kind=code-symbol | source=probe-go/scanner/db.go:L1 | neighbors=[2885afa Add comprehensive probe testing…, dial(), ProbeDB(), probeMongo(), probeMSSQL(), probeMysql()]
- "scanner_service_banner": "service_banner.py" | kind=code-symbol | source=probe/scanner/service_banner.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, pipeline.py, run_scan.py, main(), ServiceBannerScanner]
- "scanner_windows_collector_windowscollector": "WindowsCollector" | kind=code-symbol | source=probe/scanner/windows_collector.py:L236 | neighbors=[windows_collector.py, ._collect_host(), ._full_user(), .__init__(), .run(), ._smb_result()]
- "schemas_auth": "auth.py" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, CurrentUser, LoginRequest, PersonalAccessTokenCreate, PersonalAccessTokenCreated]
- "services_job_result_service_rationale_1": "job_result_service.py — shared job result processing. Single source of truth for" | kind=entity | source=manager/backend/app/services/job_result_service.py:L1 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_job_result_service_rationale_140": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L140 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_job_result_service_rationale_35": "Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu" | kind=entity | source=manager/backend/app/services/job_result_service.py:L35 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "tests_test_attack_paths": "test_attack_paths.py" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, built_graph(), demo(), TestGraphBuilder, TestGraphVisualizer, TestNeo4jClient]
- "tests_test_cli_fakeclient": "FakeClient" | kind=code-symbol | source=probe/tests/test_cli.py:L152 | neighbors=[test_cli.py, .__init__(), .request(), test_cmd_doctor_success_with_online_age…, test_cmd_scan_run_builds_dispatch_paylo…, test_poll_job_rejects_invalid_timing()]
- "tests_test_detection_core_mock_kev_db": "_mock_kev_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L86 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()]
- "tests_test_exploit_engine_testexploitorchestrator_make_orchestrator": "._make_orchestrator()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L246 | neighbors=[TestExploitOrchestrator, .test_generate_dns_callback_token_forma…, .test_generate_dns_callback_token_uniqu…, .test_select_exploit_by_cve(), .test_select_exploit_fallback_no_cve(), .test_select_exploit_log4shell()]
- "tests_test_pat_auth": "test_pat_auth.py" | kind=code-symbol | source=manager/backend/tests/test_pat_auth.py:L1 | neighbors=[2885afa Add comprehensive probe testing…, test_new_pat_token_shape_and_hash_stabi…, test_pat_builder_rejects_unknown_scope(), test_pat_builder_returns_token_once_and…, test_pat_builder_supports_non_expiring_…, test_pat_scope_allows_probe_cli_paths()]
- "tests_test_probe_core_testtuningfromparams": "TestTuningFromParams" | kind=code-symbol | source=probe/tests/test_probe_core.py:L747 | neighbors=[test_probe_core.py, .test_clamped_rate(), .test_defaults(), .test_no_ssh_creds_without_user(), .test_passive_listen_seconds(), .test_recheck_hours()]
- "tests_test_scope_validator_testvalidatetargetsinscope": "TestValidateTargetsInScope" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L14 | neighbors=[test_scope_validator.py, .test_empty_targets(), .test_hostname_passes_through(), .test_invalid_cidr_ignored(), .test_ip_in_cidr_allowed(), .test_multiple_cidrs()]
- "tests_test_transport_testsubmitresult": "TestSubmitResult" | kind=code-symbol | source=probe/tests/test_transport.py:L182 | neighbors=[test_transport.py, .test_2xx_variants_return_true(), .test_client_errors_return_false_no_dat…, .test_large_payload_is_gzipped(), .test_network_error_returns_false(), .test_server_error_returns_false()]
- "testssl_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/testssl/route.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, findings-store.ts, createFinding(), testssl-parser.ts, parseTestsslOutput()]
- "verify_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/auth/verify/route.ts:L1 | neighbors=[2885afa Add comprehensive probe testing…, 298a9d4 trim frontend to 7 core pages; …, auth-store.ts, verifyOtp(), permissions-store.ts, addUser()]
- "vuln_prioritizer_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/[id]/vuln-prioritizer/route.ts:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, ai-engine.ts, AssetInput, FindingInput, vulnPrioritizer, DEMO_ASSETS]
- "websocket_manager_graphwebsocketmanager": "GraphWebSocketManager" | kind=code-symbol | source=manager/backend/app/websocket/manager.py:L229 | neighbors=[manager.py, .broadcast_graph_update(), .broadcast_layout_update(), .broadcast_node_update(), .handle_client(), ._handle_message()]
- "workflow_asset": "asset.py" | kind=code-symbol | source=probe/workflow/asset.py:L1 | neighbors=[298a9d4 trim frontend to 7 core pages; …, test_probe_core.py, scanner_base.py, Asset, _parse_ts(), PortFact]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-012.json

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
