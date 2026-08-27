# Node Description Batch 21 of 236

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

- "main_scripts_scanner_base_adaptiveratecontroller": "AdaptiveRateController" | kind=code-symbol | source=probe/main_scripts/scanner_base.py:L401 | neighbors=[scanner_base.py, .acquire(), .__init__(), ._on_loss(), ._on_success(), .report_loss()] | lang=en
- "main_scripts_snmp_scanner_snmpscanner": "SNMPScanner" | kind=code-symbol | source=probe/main_scripts/snmp_scanner.py:L245 | neighbors=[snmp_scanner.py, Phase 1 (community discovery) + Phase 2…, BaseScanner, ._amplification_factor(), ._discover_community(), .__init__()] | lang=en
- "models_agent_recommendation_agentrecommendation": "AgentRecommendation" | kind=code-symbol | source=manager/backend/app/models/agent_recommendation.py:L34 | neighbors=[agent_recommendation.py, Base, TimestampMixin, AgentDecisionEngine, AgentUnavailableError, agent.py — AgentDecisionEngine: the age…] | lang=en
- "models_detection_config_detectionconfig": "DetectionConfig" | kind=code-symbol | source=manager/backend/app/models/detection_config.py:L10 | neighbors=[detection_config.py, Base, TimestampMixin, Per-engagement SIEM + EDR connection se…, Base, TimestampMixin] | lang=en
- "native_dns_recon": "dns-recon.ts" | kind=code-symbol | source=manager/frontend/lib/engine/native/dns-recon.ts:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, tool-runners.ts, attemptZoneTransfer(), COMMON_SUBDOMAINS, DnsReconResult, nativeDnsRecon()] | lang=en
- "routers_ad": "ad.py" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, dependencies.py, ad_assessment_status(), ADAssessRequest, launch_ad_assessment(), Neo4jConfig] | lang=en
- "routers_ad_adassessrequest": "ADAssessRequest" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L42 | neighbors=[ad.py, BaseModel, ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus] | lang=en
- "routers_ad_neo4jconfig": "Neo4jConfig" | kind=code-symbol | source=manager/backend/app/routers/ad.py:L36 | neighbors=[ad.py, BaseModel, ADAssessmentRunner, Engagement, FindingSeverity, FindingStatus] | lang=en
- "routers_agents_agent_can_execute_job": "_agent_can_execute_job()" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L160 | neighbors=[agents.py, _job_reachability_scope(), _required_scan_type(), _scope_is_reachable(), enqueue_agent_job(), get_agent_jobs()] | lang=en
- "routers_agents_agentrefreshrequest": "AgentRefreshRequest" | kind=code-symbol | source=manager/backend/app/routers/agents.py:L221 | neighbors=[agents.py, BaseModel, Asset, Engagement, ScanJobStatus, ScanJobType] | lang=en
- "routers_engagements_refresh_overview_cache": "_refresh_overview_cache()" | kind=code-symbol | source=manager/backend/app/routers/engagements.py:L98 | neighbors=[engagements.py, bulk_import_assets(), create_engagement(), import_facts(), Write-through cache refresh on the WRIT…, _compute_overview()] | lang=en
- "runtimeerror": "RuntimeError" | kind=code-symbol | neighbors=[LeaseLostError, HWBindError, AgentUnavailableError, LLMUnavailableError, StartupAbortError, PassiveListenerError] | lang=en
- "scanner_accuracy": "accuracy.py" | kind=code-symbol | source=probe/scanner/accuracy.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, evaluate_corpus(), _expected_keys(), _finding_key(), format_report(), _main()] | lang=en
- "services_sla": "sla.py" | kind=code-symbol | source=manager/backend/app/services/sla.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, c5ebd38 feat(sla): per-tenant custom SL…, config.py, compute(), default_windows(), SlaResult] | lang=en
- "sla_summary_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/findings/sla-summary/route.ts:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, backend(), withBackend(), ApiSlaItem, ApiSlaSummary, GET] | lang=en
- "tests_test_agent_dispatch": "test_agent_dispatch.py" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 22701ea Add tests for scanner parity an…, b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, _claim_fixture(), TestAgentWebSocketAuthentication] | lang=en
- "tests_test_agent_identity": "test_agent_identity.py" | kind=code-symbol | source=probe/tests/test_agent_identity.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, b4b12a9 Rename project and update files, agent.py, engine.py, transport.py, _cached_transport()] | lang=en
- "tests_test_agents_redis": "_redis()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L26 | neighbors=[test_agents.py, .test_404_when_engagement_missing(), .test_materializes_direct_job_capabilit…, .test_rejects_server_side_type(), .test_scope_fields_cannot_override_enga…, .test_success_creates_pending_job()] | lang=en
- "tests_test_agents_testpromoteassets": "TestPromoteAssets" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L701 | neighbors=[test_agents.py, Discovery results → assets/services pro…, .test_creates_asset_and_services_with_c…, .test_dedupes_duplicate_services_in_sam…, .test_empty_result_is_noop(), .test_skips_host_without_ip()] | lang=en
- "tests_test_ai_engine": "test_ai_engine.py" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _asset(), _finding(), _mock_db(), _resp(), TestHallucinationGuard] | lang=en
- "tests_test_ai_normalizer_testproposecandidates": "TestProposeCandidates" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L153 | neighbors=[test_ai_normalizer.py, .test_ai_assisted_flag_set_on_candidate…, .test_cache_hit_bypasses_client(), .test_client_failure_returns_empty(), .test_malformed_response_missing_produc…, .test_malformed_response_not_a_list_ret…] | lang=en
- "tests_test_attack_path_correlation_get": "_get()" | kind=code-symbol | source=manager/backend/tests/test_attack_path_correlation.py:L19 | neighbors=[test_attack_path_correlation.py, test_cleartext_cluster_needs_two(), test_device_role_from_facts_also_amplif…, test_exposed_db_with_unauth_is_critical…, test_legacy_windows_smbv1_plus_rdp(), test_ntlm_relay_high_when_smbv1_also_en…] | lang=en
- "tests_test_attack_paths_testneo4jclient": "TestNeo4jClient" | kind=code-symbol | source=manager/backend/tests/test_attack_paths.py:L220 | neighbors=[test_attack_paths.py, .test_run_without_connection_returns_em…, .test_run_write_noop_without_connection…, .test_sync_to_neo4j_noop_without_client…, PathAnalyzer, GraphBuilder] | lang=en
- "tests_test_auth_login_teststartupdiagnostics": "TestStartupDiagnostics" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L251 | neighbors=[test_auth_login.py, .test_bcrypt_round_trip_passes(), .test_cookie_config_fatal_in_production…, .test_cookie_config_ok_in_development(), .test_database_check_returns_fatal_on_c…, .test_jwt_secret_known_weak_is_fatal()] | lang=en
- "tests_test_customer_access_operator": "_operator()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L23 | neighbors=[test_customer_access.py, .test_approve_dispatches_job_and_links_…, .test_approve_non_pending_is_conflict(), .test_approve_without_assigned_agent_is…, .test_assigns_agent_to_engagement(), .test_unknown_agent_is_404()] | lang=en
- "tests_test_detection_validation": "test_detection_validation.py" | kind=code-symbol | source=manager/backend/tests/test_detection_validation.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _action(), pytest_addoption(), TestDetectionCorrelator, TestEDRParsing, TestSIEMParsing] | lang=en
- "tests_test_exploit_engine_rationale_1": "Unit tests for the exploitation engine.  All external connections (Metasploit RP" | kind=entity | source=manager/backend/tests/test_exploit_engine.py:L1 | neighbors=[test_exploit_engine.py, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError] | lang=en
- "tests_test_exploit_engine_rationale_420": "Run against a live Metasploitable2 lab target.     Requires: msfrpcd running, Me" | kind=entity | source=manager/backend/tests/test_exploit_engine.py:L420 | neighbors=[TestMetasploitIntegration, MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError] | lang=pt
- "tests_test_exploit_engine_rationale_465": "Register --msf-host CLI option for integration tests." | kind=entity | source=manager/backend/tests/test_exploit_engine.py:L465 | neighbors=[pytest_addoption(), MetasploitRPCClient, MetasploitRPCError, NucleiExploitRunner, ApprovalRequiredError, BlastRadiusExceededError] | lang=en
- "tests_test_main_scripts_adaptive_timeout": "test_main_scripts_adaptive_timeout.py" | kind=code-symbol | source=probe/tests/test_main_scripts_adaptive_timeout.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, adaptive_timeout.py, test_estimate_converges_on_stable_rtt(), test_fast_lan_gets_short_timeout_slow_w…, test_first_sample_sets_srtt_and_timeout…, test_invalid_band_rejected()] | lang=en
- "tests_test_main_scripts_correlation_run": "_run()" | kind=code-symbol | source=probe/tests/test_main_scripts_correlation.py:L13 | neighbors=[test_main_scripts_correlation.py, test_cleartext_cluster_fires_on_two_cle…, test_correlation_does_not_cross_hosts(), test_correlations_are_evidence_backed(), test_legacy_windows_surface_smbv1_plus_…, test_no_legacy_surface_with_only_smbv1()] | lang=en
- "tests_test_main_scripts_device_testclassifydevice": "TestClassifyDevice" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L17 | neighbors=[test_main_scripts_device.py, .test_domain_controller(), .test_iot_camera(), .test_network_device_router(), .test_printer(), .test_service_product_reinforces_server…] | lang=en
- "tests_test_main_scripts_errno": "test_main_scripts_errno.py" | kind=code-symbol | source=probe/tests/test_main_scripts_errno.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _oserr(), test_definitive_states(), test_describe_os_error_is_fully_debugga…, test_dns_failure_is_error_not_filtered(), test_errno_none_falls_back_to_os_error()] | lang=en
- "tests_test_new_scanners_make_scan_record": "_make_scan_record()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L315 | neighbors=[test_new_scanners.py, .test_diff_detects_new_service(), .test_diff_detects_service_gone(), .test_diff_detects_state_change_to_open…, .test_diff_high_severity_port_heuristic…, .test_diff_no_change_produces_no_servic…] | lang=en
- "tests_test_new_scanners_testiotscanner": "TestIoTScanner" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L246 | neighbors=[test_new_scanners.py, .test_coap_get_wellknown_header(), .test_coap_get_wellknown_path(), .test_coap_response_parse_205(), .test_coap_response_parse_404(), .test_coap_response_parse_short()] | lang=en
- "tests_test_outbox_reclaim_now": "_now()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L25 | neighbors=[test_outbox_reclaim.py, test_boundary_at_exactly_the_lease_is_r…, test_dead_letter_and_requeue_are_mutual…, test_dead_letter_stmt_targets_exhausted…, test_expired_processing_lock_is_reclaim…, test_fresh_processing_lock_is_not_recla…] | lang=en
- "tests_test_portal_read_testcreatescanrequest": "TestCreateScanRequest" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L242 | neighbors=[test_portal_read.py, .test_creates_pending_request_with_targ…, .test_excluded_target_is_422(), .test_operator_cannot_create(), .test_out_of_scope_target_is_422(), .test_queue_cap_is_conflict()] | lang=en
- "tests_test_probe_core_testparseports": "TestParsePorts" | kind=code-symbol | source=probe/tests/test_probe_core.py:L189 | neighbors=[test_probe_core.py, .test_bad_token_raises(), .test_comma_separated(), .test_duplicates_removed(), .test_mixed(), .test_out_of_range_raises()] | lang=en
- "tests_test_probe_core_testusecasesresolve": "TestUseCasesResolve" | kind=code-symbol | source=probe/tests/test_probe_core.py:L911 | neighbors=[test_probe_core.py, .test_default_discovery(), .test_fallback_to_job_type(), .test_fallback_to_scan_type(), .test_full_assessment(), .test_network_va_resolves()] | lang=en
- "tests_test_remediation_kb_f": "_f()" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L11 | neighbors=[test_remediation_kb.py, .test_cve_without_keyword_is_patch(), .test_keyword_categories(), .test_order_specificity_anon_ftp_beats_…, .test_unmatched_is_generic(), .test_missing_os_defaults_to_generic()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-020.json

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
