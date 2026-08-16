# Node Description Batch 16 of 209

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

- "routers_agents_rationale_265": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L265 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_459": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L459 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_detection_rationale_1": "Detection validation API (DetectionValidationAPI).  POST /engagements/{id}/detec" | kind=entity | source=manager/backend/app/routers/detection.py:L1 | neighbors=[detection.py, AttackAction, DetectionCorrelator, AttackTimeline, DetectionConfig, DetectionResult]
- "routers_detection_rationale_240": "Background task: pull SIEM/EDR telemetry, correlate, persist results." | kind=entity | source=manager/backend/app/routers/detection.py:L240 | neighbors=[_run_correlation(), AttackAction, DetectionCorrelator, AttackTimeline, DetectionConfig, DetectionResult]
- "routers_health": "health.py" | kind=code-symbol | source=manager/backend/app/routers/health.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, b5ffcb0 Refactor Vedha probe installer …, d1b4dd3 trim frontend to 7 core pages; …, database.py, dependencies.py, version.py]
- "scanner_delta_scanner": "delta_scanner.py" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, Delta, DeltaEngine, _extract_service(), _extract_version(), main()]
- "scanner_findings_data": "_data()" | kind=code-symbol | source=probe/scanner/findings.py:L114 | neighbors=[findings.py, build_service_index(), _rule_rdp(), _rule_smb(), _rule_snmp(), _rule_tls()]
- "scanner_ja4s": "ja4s.py" | kind=code-symbol | source=probe/scanner/ja4s.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _alpn_code(), compute_ja4s(), _ext_types(), ja4s_from_fields(), ja4s_from_parsed()]
- "scanner_port_scanner_scanmetrics": "ScanMetrics" | kind=code-symbol | source=probe/scanner/port_scanner.py:L154 | neighbors=[port_scanner.py, .scan_target(), Per-target scan accounting — the comple…, .classified(), .complete(), .degraded()]
- "scanner_scan_funnel": "scan_funnel.py" | kind=code-symbol | source=probe/scanner/scan_funnel.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, build_default_funnel(), _candidate_ports(), FunnelResult, _is_alive(), main()]
- "scanner_scanner_base_adaptiveratecontroller": "AdaptiveRateController" | kind=code-symbol | source=probe/scanner/scanner_base.py:L330 | neighbors=[scanner_base.py, .acquire(), .__init__(), ._on_loss(), ._on_success(), .report_loss()]
- "scanner_scanner_base_run_cli": "run_cli()" | kind=code-symbol | source=probe/scanner/scanner_base.py:L777 | neighbors=[scanner_base.py, Wire argparse args into a scanner insta…, .run(), expand_targets(), ResultWriter, .close()]
- "scanner_snmp_scanner_snmpscanner": "SNMPScanner" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L245 | neighbors=[snmp_scanner.py, Phase 1 (community discovery) + Phase 2…, BaseScanner, ._amplification_factor(), ._discover_community(), .__init__()]
- "schemas_auth": "auth.py" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, CurrentUser, LoginRequest, PersonalAccessTokenCreate]
- "schemas_engagement": "engagement.py" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, EngagementCreate, EngagementDetail, EngagementFilter]
- "scripts_startup_validator_checkresult": "CheckResult" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L34 | neighbors=[startup_validator.py, .validate(), .validate(), .validate(), .validate(), .validate()]
- "scripts_startup_validator_validationreport_add": ".add()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L45 | neighbors=[.validate(), .validate(), .validate(), .validate(), .validate(), .validate()]
- "services_llm": "llm.py" | kind=code-symbol | source=manager/backend/app/services/llm.py:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, 75650c1 feat: add Posture & Patch-Compa…, 88c9278 feat(ai): pin manager LLM pipel…, cac022c Everything is done and verified…]
- "services_llm_managerllmservice_generate": ".generate()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L287 | neighbors=[ManagerLlmService, ._build_system(), ._default_runtime(), ._dispatch(), ._ensure_installed_ollama_model(), ._runtime()]
- "states_datastate_emptystate": "EmptyState()" | kind=code-symbol | source=manager/frontend/components/states/DataState.tsx:L38 | neighbors=[DashboardGrid.tsx, ExposureCards.tsx, PatchComparisonMatrix.tsx, PostureScorecard.tsx, SlaStatus.tsx, page.tsx]
- "tests_assistant_test": "assistant.test.ts" | kind=code-symbol | source=manager/frontend/tests/assistant.test.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 65f22a7 Add comprehensive tests for aut…, route.ts, POST(), assistant.ts, cveRecordToFactCard()]
- "tests_scanner_adapters_test": "scanner-adapters.test.ts" | kind=code-symbol | source=manager/frontend/tests/scanner-adapters.test.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, netexec-parser.ts, parseNetExecLog(), openvas-client.ts, parseOpenVASHelperOutput()]
- "tests_test_ai_engine_testllmreportgenerator": "TestLLMReportGenerator" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L177 | neighbors=[test_ai_engine.py, .test_complete_retries_then_succeeds(), .test_detection_rule_explanation(), .test_executive_summary_persists_pendin…, .test_technical_finding_runs_guard(), .test_unavailable_without_client()]
- "tests_test_attack_paths_testgraphvisualizer": "TestGraphVisualizer" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L185 | neighbors=[test_attack_paths.py, .test_d3_highlights_top_path(), .test_d3_marks_compromised(), .test_d3_shape(), .test_layout_is_deterministic(), PathAnalyzer]
- "tests_test_auth_login_make_db": "_make_db()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L69 | neighbors=[test_auth_login.py, AsyncSession mock that returns user on …, .test_raises_bcrypt_failure_on_passlib_…, .test_raises_disabled_tenant(), .test_raises_disabled_user(), .test_not_expired_when_future()]
- "tests_test_customer_access_mock_db": "_mock_db()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L27 | neighbors=[test_customer_access.py, db.execute yields the given scalar_one_…, .test_approve_dispatches_job_and_links_…, .test_approve_non_pending_is_conflict(), .test_approve_without_assigned_agent_is…, .test_assigns_agent_to_engagement()]
- "tests_test_db_scanner": "test_db_scanner.py" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, db_scanner.py, FakeReader, FakeWriter, _probe(), _run()]
- "tests_test_detection_core_candidate": "_candidate()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L44 | neighbors=[test_detection_core.py, .test_cpe23_format(), .test_ai_assisted_carried_through(), .test_authoritative_source_confirms(), .test_inferred_match_has_backport_note(), .test_match_produces_finding()]
- "tests_test_detection_validation_action": "_action()" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L37 | neighbors=[test_detection_validation.py, .test_compute_coverage(), .test_detected_by_siem(), .test_detected_when_edr_not_blocking(), .test_gap_report_ignores_detected(), .test_generate_gap_report()]
- "tests_test_main_scripts_hardening": "test_main_scripts_hardening.py" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, scanner_base.py, make_smb2_error(), make_smb2_success(), _run(), _scope()]
- "tests_test_main_scripts_ja4s": "test_main_scripts_ja4s.py" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4s.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _ext(), _serverhello(), test_empty_extensions_sentinel(), test_extension_hash_is_order_sensitive(), test_ja4s_from_bad_serverhello_is_none()]
- "tests_test_passive_collector": "test_passive_collector.py" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L1 | neighbors=[b4b12a9 Rename project and update files, passive_collector.py, scanner_base.py, _Socket, test_collector_raises_when_no_listener_…, test_ot_udp_backend_never_joins_or_tran…]
- "tests_test_probe_core_testexpandtargets": "TestExpandTargets" | kind=code-symbol | source=probe/tests/test_probe_core.py:L145 | neighbors=[test_probe_core.py, .test_cidr_24(), .test_dedup(), .test_empty_input(), .test_hostname_passthrough(), .test_range()]
- "tests_test_probe_core_testworkflowcache": "TestWorkflowCache" | kind=code-symbol | source=probe/tests/test_probe_core.py:L745 | neighbors=[test_probe_core.py, .test_all_entries_for_host(), .test_get_missing(), .test_load_handles_corrupt_lines(), .test_put_get(), .test_save_and_load_roundtrip()]
- "tests_test_scan_funnel_testscanfunnel": "TestScanFunnel" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L119 | neighbors=[test_scan_funnel.py, .test_db_scanner_invoked_with_db_port(), .test_db_scanner_not_invoked_without_db…, .test_dead_host_forced_runs_full(), .test_dead_host_skips_port_scan(), .test_deep_scanner_receives_only_open_p…]
- "tests_test_seed_admin": "test_seed_admin.py" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, b5ffcb0 Refactor Vedha probe installer …, seed_admin.py, TestDatabaseUnavailable, TestDriftDetection, TestExistingAdminNoReset]
- "tests_test_task_runner_testrunnerscopevalidation": "TestRunnerScopeValidation" | kind=code-symbol | source=probe/tests/test_task_runner.py:L204 | neighbors=[test_task_runner.py, .test_allows_in_scope_target(), .test_explicit_empty_local_ceiling_fail…, .test_local_ceiling_filters_manager_aut…, .test_local_ceiling_is_forwarded_to_eng…, .test_manager_job_without_scope_fails_c…]
- "vuln_nuclei_nucleiscanner_run_scan": ".run_scan()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L118 | neighbors=[NucleiScanner, NucleiRunReport, NucleiScanError, ._consume_stdout(), ._partial_or_raise(), ._read_stderr()]
- "workflow_cli": "cli.py" | kind=code-symbol | source=probe/workflow/cli.py:L1 | neighbors=[b4b12a9 Rename project and update files, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, scanner_base.py, _build_creds(), _build_mode()]
- "workflow_workflow_engine_sink": "_Sink" | kind=code-symbol | source=probe/workflow/workflow_engine.py:L144 | neighbors=[workflow_engine.py, In-memory ResultWriter stand-in — Passi…, _run_inventory(), _run_passive(), .close(), .__init__()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-015.json

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
