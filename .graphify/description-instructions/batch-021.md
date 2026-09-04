# Node Description Batch 22 of 330

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

- "main_scripts_smb_enum_scanner": "smb_enum_scanner.py" | kind=code-symbol | source=probe/main_scripts/smb_enum_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, _decode(), _enum_shares(), _enum_users_ridcycle(), _enum_users_samr(), main()]
- "models_detection_run_detectionrun": "DetectionRun" | kind=code-symbol | source=manager/backend/app/models/detection_run.py:L40 | neighbors=[detection_run.py, Base, TimestampMixin, engine_bridge.py — run the deterministi…, A previously-remediated finding whose i…, Background entry point (P1: keep detect…]
- "path_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/portal/[...path]/route.ts:L1 | neighbors=[22701ea Add tests for scanner parity an…, backend.ts, backend(), BackendError, bearerFrom(), cookieFrom()]
- "routers_agent_ws": "agent_ws.py" | kind=code-symbol | source=manager/backend/app/routers/agent_ws.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, database.py, _agent_token_from_websocket()]
- "routers_agents_agent_can_execute_job": "_agent_can_execute_job()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L161 | neighbors=[agents.py, _job_reachability_scope(), _required_scan_type(), _scope_is_reachable(), enqueue_agent_job(), get_agent_jobs()]
- "routers_agents_rationale_1": "Agent registration, heartbeat, job polling, and result submission." | kind=entity | source=manager/backend/app/routers/agents.py:L1 | neighbors=[agents.py, Asset, Engagement, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_208": "Encrypt the engagement scope for a specific agent's public key.      Reads agent" | kind=entity | source=manager/backend/app/routers/agents.py:L208 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_246": "Verify that the JWT token bearer IS the agent they claim to be.      Every heart" | kind=entity | source=manager/backend/app/routers/agents.py:L246 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_265": "Returns the finite library of scan use-cases operators can dispatch to probes." | kind=entity | source=manager/backend/app/routers/agents.py:L265 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_agents_rationale_459": "Lets the frontend poll a specific job's status without knowing which agent has i" | kind=entity | source=manager/backend/app/routers/agents.py:L459 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJobType, ScanJob]
- "routers_detection_rationale_1": "Detection validation API (DetectionValidationAPI).  POST /engagements/{id}/detec" | kind=entity | source=manager/backend/app/routers/detection.py:L1 | neighbors=[detection.py, AttackAction, DetectionCorrelator, AttackTimeline, DetectionConfig, DetectionResult]
- "routers_detection_rationale_240": "Background task: pull SIEM/EDR telemetry, correlate, persist results." | kind=entity | source=manager/backend/app/routers/detection.py:L240 | neighbors=[_run_correlation(), AttackAction, DetectionCorrelator, AttackTimeline, DetectionConfig, DetectionResult]
- "routers_engagements_refresh_overview_cache": "_refresh_overview_cache()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L124 | neighbors=[engagements.py, bulk_import_assets(), create_engagement(), import_facts(), Write-through cache refresh on the WRIT…, _compute_overview()]
- "scanner_ja4s": "ja4s.py" | kind=code-symbol | source=probe/scanner/ja4s.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _alpn_code(), compute_ja4s(), _ext_types(), ja4s_from_fields(), ja4s_from_parsed()]
- "scanner_port_scanner_portscanner_attempt": "._attempt()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L448 | neighbors=[PortScanner, _family_of(), _harvest_tcp_stack(), ._build(), ._scan_port(), One connect() and its classification. A…]
- "scanner_port_scanner_portscanner_scan_target": ".scan_target()" | kind=code-symbol | source=probe/scanner/port_scanner.py:L602 | neighbors=[PortScanner, ._is_ambiguous(), ._reprobe_ambiguous(), ScanMetrics, .record(), .summary()]
- "scanner_rdp_scanner": "rdp_scanner.py" | kind=code-symbol | source=probe/scanner/rdp_scanner.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 8f6bf49 Refactor code structure and rem…, build_connection_request(), main(), parse_connection_confirm()]
- "scanner_run_all": "run_all.py" | kind=code-symbol | source=probe/scanner/run_all.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, 6e2818f Add support for additional serv…, 8f6bf49 Refactor code structure and rem…, _advertised_dynamic_ports(), _log()]
- "scanner_snmp_scanner_snmpscanner": "SNMPScanner" | kind=code-symbol | source=probe/scanner/snmp_scanner.py:L245 | neighbors=[snmp_scanner.py, Phase 1 (community discovery) + Phase 2…, BaseScanner, ._amplification_factor(), ._discover_community(), .__init__()]
- "schemas_ai": "ai.py" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, 75650c1 feat: add Posture & Patch-Compa…, 7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…]
- "schemas_auth": "auth.py" | kind=code-symbol | source=manager/backend/app/schemas/auth.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 22701ea Add tests for scanner parity an…, d1b4dd3 trim frontend to 7 core pages; …, CurrentUser, LoginRequest, PersonalAccessTokenCreate]
- "schemas_engagement": "engagement.py" | kind=code-symbol | source=manager/backend/app/schemas/engagement.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, EngagementCreate, EngagementDetail, EngagementFilter]
- "scripts_startup_validator_checkresult": "CheckResult" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L34 | neighbors=[startup_validator.py, .validate(), .validate(), .validate(), .validate(), .validate()]
- "scripts_startup_validator_validationreport_add": ".add()" | kind=code-symbol | source=manager/backend/scripts/startup_validator.py:L45 | neighbors=[.validate(), .validate(), .validate(), .validate(), .validate(), .validate()]
- "services_llm_managerllmservice_generate": ".generate()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L328 | neighbors=[ManagerLlmService, ._build_system(), ._default_runtime(), ._dispatch(), ._ensure_installed_ollama_model(), ._runtime()]
- "tests_campaign_store_test": "campaign-store.test.ts" | kind=code-symbol | source=manager/frontend/tests/campaign-store.test.ts:L1 | neighbors=[d98f654 feat(manager): network-VA campa…, campaign-store.ts, CampaignSnapshot, getCampaign(), isSafeCampaignId(), listCampaigns()]
- "tests_scanner_adapters_test": "scanner-adapters.test.ts" | kind=code-symbol | source=manager/frontend/tests/scanner-adapters.test.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, netexec-parser.ts, parseNetExecLog(), openvas-client.ts, parseOpenVASHelperOutput()]
- "tests_test_ai_engine_testllmreportgenerator": "TestLLMReportGenerator" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L177 | neighbors=[test_ai_engine.py, .test_complete_retries_then_succeeds(), .test_detection_rule_explanation(), .test_executive_summary_persists_pendin…, .test_technical_finding_runs_guard(), .test_unavailable_without_client()]
- "tests_test_attack_paths_testgraphvisualizer": "TestGraphVisualizer" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L185 | neighbors=[test_attack_paths.py, .test_d3_highlights_top_path(), .test_d3_marks_compromised(), .test_d3_shape(), .test_layout_is_deterministic(), PathAnalyzer]
- "tests_test_auth_login_make_db": "_make_db()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L69 | neighbors=[test_auth_login.py, AsyncSession mock that returns user on …, .test_raises_bcrypt_failure_on_passlib_…, .test_raises_disabled_tenant(), .test_raises_disabled_user(), .test_not_expired_when_future()]
- "tests_test_branch_registry_testregistryconsistency": "TestRegistryConsistency" | kind=code-symbol | source=probe/tests/test_branch_registry.py:L34 | neighbors=[test_branch_registry.py, .test_branch_component_map_is_derived(), .test_catalog_entries_are_labelled(), .test_components_are_unique(), .test_every_branch_has_a_scanner_the_en…, .test_every_branch_is_gateable()]
- "tests_test_campaign_progress_progress": "_progress()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L204 | neighbors=[test_campaign_progress.py, _rows(), _scalars(), _user(), _running_run(), test_a_briefly_running_run_is_not_calle…]
- "tests_test_campaign_progress_terminal_status": "_status()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L34 | neighbors=[test_campaign_progress_terminal.py, .test_complete_campaign(), .test_complete_with_gaps(), .test_no_jobs_is_pending(), .test_uncovered_submission_keeps_it_det…, .test_a_dead_queue_is_still_reported_as…]
- "tests_test_customer_access_mock_db": "_mock_db()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L27 | neighbors=[test_customer_access.py, db.execute yields the given scalar_one_…, .test_approve_dispatches_job_and_links_…, .test_approve_non_pending_is_conflict(), .test_approve_without_assigned_agent_is…, .test_assigns_agent_to_engagement()]
- "tests_test_db_scanner": "test_db_scanner.py" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, db_scanner.py, FakeReader, FakeWriter, _probe(), _run()]
- "tests_test_detection_pipeline_gaps": "test_detection_pipeline_gaps.py" | kind=code-symbol | source=manager/backend/tests/test_detection_pipeline_gaps.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, _ctx, _fact(), test_a_non_dict_data_payload_is_quarant…, test_accepted_facts_excludes_what_inges…, test_accepted_facts_falls_back_to_raw_w…]
- "tests_test_finding_events_testsynthesize": "TestSynthesize" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L44 | neighbors=[test_finding_events.py, .test_auto_resolution_event(), .test_detected_actor_falls_back_to_dete…, .test_detected_actor_labels_network_va_…, .test_genesis_detected_from_first_seen(), .test_manual_remediation_event()]
- "tests_test_main_scripts_ja4s": "test_main_scripts_ja4s.py" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4s.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, _ext(), _serverhello(), test_empty_extensions_sentinel(), test_extension_hash_is_order_sensitive(), test_ja4s_from_bad_serverhello_is_none()]
- "tests_test_passive_collector": "test_passive_collector.py" | kind=code-symbol | source=probe/tests/test_passive_collector.py:L1 | neighbors=[b4b12a9 Rename project and update files, passive_collector.py, scanner_base.py, _Socket, test_collector_raises_when_no_listener_…, test_ot_udp_backend_never_joins_or_tran…]
- "tests_test_posture_rules": "test_posture_rules.py" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 8f6bf49 Refactor code structure and rem…, _asset(), _fact(), TestHardenedGroundTruth, TestInvariants]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-021.json

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
