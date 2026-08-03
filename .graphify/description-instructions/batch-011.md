# Node Description Batch 12 of 131

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

- "discovery_rate_limiter_ratelimiter": "RateLimiter" | kind=code-symbol | source=manager/backend/app/discovery/rate_limiter.py:L27 | neighbors=[rate_limiter.py, .acquire(), ._consume_token(), .__init__(), .is_within_window(), ._resolve_cidr()]
- "discovery_worker_rationale_1": "DiscoveryWorker — full async pipeline:   Redis queue → nmap subprocess → banner" | kind=entity | source=manager/backend/app/discovery/worker.py:L1 | neighbors=[worker.py, RateLimiter, ServiceIdentifier, NmapXMLParser, ParsedHost, ParsedPort]
- "discovery_worker_rationale_56": "Pulled from Redis list `discovery:queue:{tenant_id}`.     One worker instance pr" | kind=entity | source=manager/backend/app/discovery/worker.py:L56 | neighbors=[DiscoveryWorker, RateLimiter, ServiceIdentifier, NmapXMLParser, ParsedHost, ParsedPort]
- "discovery_worker_rationale_58": "Pulled from Redis list `discovery:queue:{tenant_id}`.     One worker instance pr" | kind=entity | source=manager/backend/app/discovery/worker.py:L58 | neighbors=[RateLimiter, ServiceIdentifier, DiscoveryWorker, NmapXMLParser, ParsedHost, ParsedPort]
- "engagements_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/engagements/route.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, GET, POST, toApiEngagementCreate(), toUiEngagement(), backend()]
- "engine_tool_runners_runnmapnse": "runNmapNse()" | kind=code-symbol | source=manager/frontend/lib/engine/tool-runners.ts:L1043 | neighbors=[tool-runners.ts, runLdapEnum(), runNetbiosEnum(), runNfsEnum(), bin(), collectProcess()]
- "exception": "Exception" | kind=code-symbol | neighbors=[ADError, CliError, LicenseError, TransportError, VedhaAuthError, MetasploitRPCError]
- "exploit_safety": "safety.py" | kind=code-symbol | source=manager/backend/app/exploit/safety.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, ApprovalRequiredError, BlastRadiusExceededError, OutOfScopeError, requires_approval(), SafetyViolationError]
- "graph_builder": "builder.py" | kind=code-symbol | source=manager/backend/app/graph/builder.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, asset_node_id(), _enum_value(), exploit_complexity(), finding_node_id(), GraphBuilder]
- "lib_auth_middleware": "auth-middleware.ts" | kind=code-symbol | source=manager/frontend/lib/auth-middleware.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, AuthContext, Handler, withAuth(), verifyToken()]
- "lib_nmap_parser": "nmap-parser.ts" | kind=code-symbol | source=manager/frontend/lib/nmap-parser.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, extractScripts(), NmapHost, NmapScriptResult, NmapService]
- "models_detection_run_detectionrun": "DetectionRun" | kind=code-symbol | source=manager/backend/app/models/detection_run.py:L40 | neighbors=[detection_run.py, Base, TimestampMixin, engine_bridge.py — run the deterministi…, New raw-facts path: detect CVE findings…, Background entry point (P1: keep detect…]
- "routers_agent_ws": "agent_ws.py" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, database.py, _agent_token_from_websocket()]
- "routers_agents_rationale_1": "Agent registration, heartbeat, job polling, and result submission." | kind=entity | source=manager/backend/app/routers/agents.py:L1 | neighbors=[agents.py, Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_208": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L208 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_246": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L246 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_265": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L265 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_459": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L459 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_detection_rationale_1": "Detection validation API (DetectionValidationAPI).  POST /engagements/{id}/detec" | kind=entity | source=manager/backend/app/routers/detection.py:L1 | neighbors=[detection.py, AttackAction, DetectionCorrelator, AttackTimeline, DetectionConfig, DetectionResult]
- "routers_detection_rationale_240": "Background task: pull SIEM/EDR telemetry, correlate, persist results." | kind=entity | source=manager/backend/app/routers/detection.py:L240 | neighbors=[_run_correlation(), AttackAction, DetectionCorrelator, AttackTimeline, DetectionConfig, DetectionResult]
- "routers_health": "health.py" | kind=code-symbol | source=manager/backend/app/routers/health.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, database.py, dependencies.py, version.py]
- "scanner_snmp_scanner": "snmp_scanner.py" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, run_scan.py, _build_get(), _extract_sysdescr(), main()]
- "schemas_engagement": "engagement.py" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, EngagementCreate, EngagementDetail, EngagementFilter]
- "schemas_finding": "finding.py" | kind=code-symbol | source=manager/backend/app/schemas/finding.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, d1b4dd3 trim frontend to 7 core pages; …, FindingFilter, FindingOut, FindingPatch]
- "scripts_startup_validator_checkresult": "CheckResult" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L34 | neighbors=[startup_validator.py, .validate(), .validate(), .validate(), .validate(), .validate()]
- "scripts_startup_validator_validationreport_add": ".add()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L45 | neighbors=[.validate(), .validate(), .validate(), .validate(), .validate(), .validate()]
- "tests_assistant_test": "assistant.test.ts" | kind=code-symbol | source=manager/frontend/tests/assistant.test.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 65f22a7 Add comprehensive tests for aut…, route.ts, POST(), assistant.ts, cveRecordToFactCard()]
- "tests_scanner_adapters_test": "scanner-adapters.test.ts" | kind=code-symbol | source=manager/frontend/tests/scanner-adapters.test.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, netexec-parser.ts, parseNetExecLog(), openvas-client.ts, parseOpenVASHelperOutput()]
- "tests_test_ai_engine_testllmreportgenerator": "TestLLMReportGenerator" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L177 | neighbors=[test_ai_engine.py, .test_complete_retries_then_succeeds(), .test_detection_rule_explanation(), .test_executive_summary_persists_pendin…, .test_technical_finding_runs_guard(), .test_unavailable_without_client()]
- "tests_test_attack_paths_testgraphvisualizer": "TestGraphVisualizer" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L185 | neighbors=[test_attack_paths.py, .test_d3_highlights_top_path(), .test_d3_marks_compromised(), .test_d3_shape(), .test_layout_is_deterministic(), PathAnalyzer]
- "tests_test_auth_login_make_db": "_make_db()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L69 | neighbors=[test_auth_login.py, AsyncSession mock that returns user on …, .test_raises_bcrypt_failure_on_passlib_…, .test_raises_disabled_tenant(), .test_raises_disabled_user(), .test_not_expired_when_future()]
- "tests_test_db_scanner": "test_db_scanner.py" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, db_scanner.py, FakeReader, FakeWriter, _probe(), _run()]
- "tests_test_detection_core_candidate": "_candidate()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L44 | neighbors=[test_detection_core.py, .test_cpe23_format(), .test_ai_assisted_carried_through(), .test_authoritative_source_confirms(), .test_inferred_match_has_backport_note(), .test_match_produces_finding()]
- "tests_test_detection_validation_action": "_action()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L37 | neighbors=[test_detection_validation.py, .test_compute_coverage(), .test_detected_by_siem(), .test_detected_when_edr_not_blocking(), .test_gap_report_ignores_detected(), .test_generate_gap_report()]
- "tests_test_manager_ai": "test_manager_ai.py" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, config.py, test_ai_request_rejects_unsafe_model_an…, test_manager_ollama_generation_owns_sec…, test_manager_openai_generation_is_serve…, test_manager_openai_rejects_unconfigure…]
- "tests_test_passive_collector": "test_passive_collector.py" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L1 | neighbors=[b4b12a9 Rename project and update files, passive_collector.py, scanner_base.py, _Socket, test_collector_raises_when_no_listener_…, test_ot_udp_backend_never_joins_or_tran…]
- "tests_test_probe_core_testexpandtargets": "TestExpandTargets" | kind=code-symbol | source=probe/tests/test_probe_core.py:L145 | neighbors=[test_probe_core.py, .test_cidr_24(), .test_dedup(), .test_empty_input(), .test_hostname_passthrough(), .test_range()]
- "tests_test_probe_core_testworkflowcache": "TestWorkflowCache" | kind=code-symbol | source=probe/tests/test_probe_core.py:L745 | neighbors=[test_probe_core.py, .test_all_entries_for_host(), .test_get_missing(), .test_load_handles_corrupt_lines(), .test_put_get(), .test_save_and_load_roundtrip()]
- "tests_test_probe_enrollment": "test_probe_enrollment.py" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, test_device_access_token_has_dedicated_…, test_ed25519_proof_of_possession_reject…, test_enroll_token_create_defaults_and_b…, test_enroll_token_usable_only_while_liv…, test_enrollment_create_accepts_optional…]
- "tests_test_seed_admin": "test_seed_admin.py" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, b5ffcb0 Refactor Vedha probe installer …, seed_admin.py, TestDatabaseUnavailable, TestDriftDetection, TestExistingAdminNoReset]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-011.json

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
