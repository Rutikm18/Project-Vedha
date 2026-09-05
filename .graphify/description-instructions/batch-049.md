# Node Description Batch 50 of 336

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

- "supporting_research_test_evidence_store_testidentity": "TestIdentity" | kind=code-symbol | source=Supporting_research/test_evidence_store.py:L95 | neighbors=[test_evidence_store.py, .setUp(), .test_fingerprint_identity_finds_exactl…, .test_hostname_never_overrides_a_finger…, .test_ip_identity_is_wrong_in_both_dire…, .test_observations_without_any_fingerpr…]
- "test_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/integrations/test/route.ts:L1 | neighbors=[6be8259 feat(integrations): outbox deli…, backend.ts, backend(), with-backend.ts, withBackend(), POST]
- "tests_findings_adapters_test": "findings-adapters.test.ts" | kind=code-symbol | source=manager/frontend/tests/findings-adapters.test.ts:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, adapters.ts, toApiFindingPatch(), toUiFinding()]
- "tests_test_accuracy_gate_port_fact": "_port_fact()" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L36 | neighbors=[test_accuracy_gate.py, .test_ground_truth_states_alone_is_a_va…, .test_gate_counts_the_two_kinds_separat…, .test_regression_only_directory_still_w…, .test_matching_port_state_scores_perfec…, .test_thresholds_are_overridable()]
- "tests_test_agent_dispatch_testagentwebsocketauthentication": "TestAgentWebSocketAuthentication" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L16 | neighbors=[test_agent_dispatch.py, .test_accepts_bearer_header(), .test_rejects_query_string_credentials(), ScanJobStatus, ScanJobType, AgentConnectionManager]
- "tests_test_agent_dispatch_testjobsecretboundary": "TestJobSecretBoundary" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L67 | neighbors=[test_agent_dispatch.py, .test_allows_non_secret_scan_tuning(), .test_detects_persisted_secret_material…, ScanJobStatus, ScanJobType, AgentConnectionManager]
- "tests_test_agent_policy": "test_agent_policy.py" | kind=code-symbol | source=manager/backend/tests/test_agent_policy.py:L1 | neighbors=[bc08715 feat(agent): risk-tier action c…, ecbb4ad feat(agent): rules-of-engagemen…, _roe(), TestClassifyAction, TestEvaluateAction, test_agent_policy.py — the pure determi…]
- "tests_test_agents_testgetagentjobs": "TestGetAgentJobs" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L298 | neighbors=[test_agents.py, .test_404_when_agent_unknown(), .test_jobs_include_params(), .test_skips_job_outside_declared_networ…, .test_skips_job_when_capability_is_miss…, ScanJobType]
- "tests_test_agents_testotprofilegate": "TestOTProfileGate" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L170 | neighbors=[test_agents.py, .test_allows_passive_discovery_on_ot_en…, .test_blocks_active_scan_type_on_ot_eng…, .test_blocks_explicit_active_scan_type_…, .test_it_and_iot_profiles_unaffected(), ScanJobType]
- "tests_test_agents_testpromoteassets_test_dedupes_duplicate_services_in_same_probe_result": ".test_dedupes_duplicate_services_in_same_probe_result()" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L759 | neighbors=[A single web scan can emit multiple fac…, TestPromoteAssets, A single web scan can emit multiple fac…, A single web scan can emit multiple fac…, A single web scan can emit multiple fac…, A single web scan can emit multiple fac…]
- "tests_test_ai_engine_asset": "_asset()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L36 | neighbors=[test_ai_engine.py, .test_technical_finding_runs_guard(), .test_explain_prediction_fallback_shape…, .test_extract_features_order_and_values…, .test_higher_cvss_scores_higher(), .test_predict_priority_uses_fallback_wh…]
- "tests_test_ai_engine_mock_db": "_mock_db()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L170 | neighbors=[test_ai_engine.py, .test_complete_retries_then_succeeds(), .test_detection_rule_explanation(), .test_executive_summary_persists_pendin…, .test_technical_finding_runs_guard(), .test_unavailable_without_client()]
- "tests_test_ai_engine_rationale_1": "Unit tests for the AI engine (Prompt 8).  The Anthropic client is mocked (no API" | kind=entity | source=manager/backend/tests/test_ai_engine.py:L1 | neighbors=[test_ai_engine.py, HallucinationGuard, LLMReportGenerator, LLMUnavailableError, VulnPrioritizer, ReviewStatus]
- "tests_test_campaign_progress_rows": "_rows()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L21 | neighbors=[test_campaign_progress.py, _progress(), A result whose .all() returns raw rows …, _run_scenario(), test_campaign_progress_aggregates_jobs_…, test_campaign_progress_no_detection_yet…]
- "tests_test_campaign_progress_run_scenario": "_run_scenario()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L117 | neighbors=[test_campaign_progress.py, Build a campaign_progress scenario with…, _rows(), _scalars(), test_completed_run_is_not_stuck_at_dete…, test_pipeline_advances_through_every_ph…]
- "tests_test_campaign_progress_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L13 | neighbors=[test_campaign_progress.py, _progress(), test_campaign_progress_aggregates_jobs_…, test_campaign_progress_no_detection_yet…, test_completed_run_is_not_stuck_at_dete…, test_pipeline_advances_through_every_ph…]
- "tests_test_cve_correlation_testvulndb": "TestVulnDB" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L119 | neighbors=[test_cve_correlation.py, .test_counts(), .test_cves_for_cpe_in_range(), .test_kev_sorts_first(), .test_out_of_range_excluded(), .test_vendor_norm()]
- "tests_test_db_scanner_testmysqlxvsoracle": "TestMysqlxVsOracle" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L53 | neighbors=[test_db_scanner.py, .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle(), .test_oracle_rejects_garbage_with_type_…, .test_oracle_reply_not_misread_as_mysql…, .test_oracle_still_identified()]
- "tests_test_detection_coverage_test_completed_no_blind_is_plain_complete": "test_completed_no_blind_is_plain_complete()" | kind=code-symbol | source=manager/backend/tests/test_detection_coverage.py:L73 | neighbors=[test_detection_coverage.py, _job(), _rows(), _run(), _scalars(), _user()]
- "tests_test_detection_coverage_test_completed_with_blind_rules_is_complete_with_gaps": "test_completed_with_blind_rules_is_complete_with_gaps()" | kind=code-symbol | source=manager/backend/tests/test_detection_coverage.py:L47 | neighbors=[test_detection_coverage.py, _job(), _rows(), _run(), _scalars(), _user()]
- "tests_test_dns_scanner_testderivezones": "TestDeriveZones" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L25 | neighbors=[test_dns_scanner.py, .test_bounded(), .test_explicit_zone_used_as_is(), .test_extra_before_target_derived(), .test_hostname_target_reduces_to_regist…, .test_ip_target_derives_nothing()]
- "tests_test_engine_bridge_ingest_health": "test_engine_bridge_ingest_health.py" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_ingest_health.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, test_census_survives_an_engine_that_ret…, test_healthy_facts_ingest_completely_an…, test_partial_drift_still_detects_but_re…, test_total_shape_drift_is_reported_not_…, test_engine_bridge_ingest_health.py — a…]
- "tests_test_exploit_engine_testmetasploitrpcclient_make_client": "._make_client()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L183 | neighbors=[TestMetasploitRPCClient, .test_get_job_status_running(), .test_kill_job(), .test_list_modules_exploit(), .test_run_module_error_raises(), .test_run_module_returns_job_id()]
- "tests_test_finding_events_testmerge": "TestMerge" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L92 | neighbors=[test_finding_events.py, ._stored(), ._synth(), .test_labels_attached(), .test_sorted_oldest_first(), .test_stored_supersedes_synthesized_sam…]
- "tests_test_finding_section_testfindingsection_sum": "._sum()" | kind=code-symbol | source=probe/tests/test_finding_section.py:L48 | neighbors=[TestFindingSection, .test_backward_compatible_keys_kept(), .test_clean_host_shows_no_findings_hone…, .test_each_finding_tagged_with_verified…, .test_findings_are_ranked_worst_first(), .test_vulnerable_host_shows_ranked_vuln…]
- "tests_test_finding_section_testscannerregistry": "TestScannerRegistry" | kind=code-symbol | source=probe/tests/test_finding_section.py:L17 | neighbors=[test_finding_section.py, .test_registry_aligns_with_manager_vali…, .test_unknown_scanner_is_not_trusted(), .test_unvalidated_scanners_are_not_veri…, .test_user_validated_scanners_are_verif…, .test_verification_report_shape()]
- "tests_test_host_discovery_mobile_testdevicehint": "TestDeviceHint" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L52 | neighbors=[test_host_discovery_mobile.py, .test_iphone_lockdownd_port(), .test_mobile_vendor(), .test_no_signal(), .test_plain_vendor_passthrough(), .test_randomized_mac_is_mobile()]
- "tests_test_host_health_testverdict": "TestVerdict" | kind=code-symbol | source=probe/tests/test_host_health.py:L83 | neighbors=[test_host_health.py, .test_a_broken_liveness_probe_never_abo…, .test_firewalled_host_that_still_answer…, .test_flaky_host_can_be_suspected_again…, .test_host_that_stopped_answering_is_of…, .test_no_recheck_is_spent_below_thresho…]
- "tests_test_hw_bind": "test_hw_bind.py" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, hw_bind.py, TestCheckHwBind, TestGetHwId, Tests for agent/hw_bind.py, 2885afa Add comprehensive probe testing…]
- "tests_test_integration_testscopevalidationpipeline": "TestScopeValidationPipeline" | kind=code-symbol | source=probe/tests/test_integration.py:L165 | neighbors=[test_integration.py, Phase 1: combined scope validation (val…, .test_accepts_in_scope_rejects_out_of_s…, .test_all_excluded_returns_empty(), .test_excludes_override_scope(), .test_merge_exclusions_deduplicates()]
- "tests_test_integration_testwebsocketmessageprotocol": "TestWebSocketMessageProtocol" | kind=code-symbol | source=probe/tests/test_integration.py:L273 | neighbors=[test_integration.py, Phase 2: WebSocket message parsing., .test_heartbeat_message(), .test_hello_message(), .test_job_push_message(), .test_result_message()]
- "tests_test_integrations": "test_integrations.py" | kind=code-symbol | source=manager/backend/tests/test_integrations.py:L1 | neighbors=[027f4e4 feat(integrations): per-tenant …, _db(), _operator(), TestListIntegrations, TestPutIntegration, test_integrations.py — operator notific…]
- "tests_test_ipv6_discovery_testdiscoverfiltering_patch": "._patch()" | kind=code-symbol | source=probe/tests/test_ipv6_discovery.py:L39 | neighbors=[TestDiscoverFiltering, .test_dedups(), .test_excludes_own_addresses(), .test_keeps_usable_drops_dead_states(), .test_link_local_can_be_excluded(), .test_never_raises_on_empty()]
- "tests_test_ipv6_wiring_wire": "_wire()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L73 | neighbors=[test_ipv6_wiring.py, test_disabled_by_default(), test_discovery_failure_does_not_abort_t…, test_in_scope_neighbour_is_added_and_sc…, test_out_of_scope_neighbour_is_reported…, test_the_fact_records_both_sides()]
- "tests_test_job_cancel_probe": "test_job_cancel_probe.py" | kind=code-symbol | source=probe/tests/test_job_cancel_probe.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, transport.py, TestHeartbeatOutcomes, TestPollingNoiseIsSuppressed, transport(), Probe-side operator job control + polli…]
- "tests_test_job_cancel_probe_testpollingnoiseissuppressed_configure": "._configure()" | kind=code-symbol | source=probe/tests/test_job_cancel_probe.py:L77 | neighbors=[TestPollingNoiseIsSuppressed, .test_per_request_info_lines_are_suppre…, .test_probe_debug_restores_full_tracing…, .test_probe_own_narration_is_unaffected…, .test_transport_errors_still_surface(), .test_transport_loggers_are_quiet_by_de…]
- "tests_test_job_cancel_test_missing_attempt_row_does_not_break_cancel": "test_missing_attempt_row_does_not_break_cancel()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L143 | neighbors=[test_job_cancel.py, _count(), _db(), _job(), _one(), _user()]
- "tests_test_job_cancel_test_open_attempt_is_closed_as_cancelled": "test_open_attempt_is_closed_as_cancelled()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L128 | neighbors=[test_job_cancel.py, _count(), _db(), _job(), _one(), _user()]
- "tests_test_job_cancel_test_pending_job_is_cancelled_and_freed": "test_pending_job_is_cancelled_and_freed()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L78 | neighbors=[test_job_cancel.py, _count(), _db(), _job(), _one(), _user()]
- "tests_test_job_cancel_test_running_job_bumps_the_fence_to_abort_the_probe": "test_running_job_bumps_the_fence_to_abort_the_probe()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L102 | neighbors=[test_job_cancel.py, _count(), _db(), _job(), _one(), _user()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-049.json

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
