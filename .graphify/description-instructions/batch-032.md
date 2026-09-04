# Node Description Batch 33 of 330

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

- "services_job_result_service_rationale_140": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L140 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_job_result_service_rationale_145": "Upsert discovered hosts/services into the asset inventory.      Keyed by (engage" | kind=entity | source=manager/backend/app/services/job_result_service.py:L145 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_job_result_service_rationale_35": "Process a scan job result.  Called from both HTTP and WebSocket paths.      Retu" | kind=entity | source=manager/backend/app/services/job_result_service.py:L35 | neighbors=[Asset, Engagement, AssetType, ScanJobStatus, ScanJob, ScanResult]
- "services_llm_managerllmservice_generate_with_fallback": ".generate_with_fallback()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L363 | neighbors=[ManagerLlmService, AiRuntimeError, ._build_system(), ._dispatch(), ._ensure_installed_ollama_model(), ._fallback_candidates()]
- "services_llm_runtime": "Runtime" | kind=code-symbol | source=manager/backend/app/services/llm.py:L29 | neighbors=[llm.py, ._default_runtime(), ._fallback_candidates(), ._runtime(), Settings, AiGenerateRequest]
- "services_notifications": "notifications.py" | kind=code-symbol | source=manager/backend/app/services/notifications.py:L1 | neighbors=[6be8259 feat(integrations): outbox deli…, deliver(), enqueue_notification(), notify_tenant(), _send_email(), _send_jira()]
- "services_portal_metrics": "portal_metrics.py" | kind=code-symbol | source=manager/backend/app/services/portal_metrics.py:L1 | neighbors=[35f02a9 feat(portal): rich scan request…, _is_closed(), MetricFinding, open_closed_counts(), _period(), severity_breakdown()]
- "services_reference": "reference.py" | kind=code-symbol | source=manager/backend/app/services/reference.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, _encode(), is_reference(), make_reference(), normalize(), scan_job_reference()]
- "status_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/settings/status/route.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, backend.ts, backend(), BackendError, bearerFrom(), GET()]
- "tests_operator_routes_test": "operator-routes.test.ts" | kind=code-symbol | source=manager/frontend/tests/operator-routes.test.ts:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, f473173 merge: network VA accuracy, KEV…, assistant-access.ts, canMountAssistant(), isAssistantRoute()]
- "tests_test_accuracy_gate_testcorpusvalidation": "TestCorpusValidation" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L89 | neighbors=[test_accuracy_gate.py, .test_corpus_without_any_labels_is_reje…, .test_corpus_without_facts_is_rejected(), .test_ground_truth_states_alone_is_a_va…, .test_malformed_json_is_a_gate_error_no…, .test_missing_directory_is_rejected()]
- "tests_test_accuracy_gate_testshippedcorpora": "TestShippedCorpora" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L42 | neighbors=[test_accuracy_gate.py, .test_an_independently_labeled_corpus_i…, .test_every_independent_corpus_scores_p…, .test_every_shipped_corpus_declares_pro…, .test_gate_passes_on_the_committed_corp…, .test_regression_only_directory_still_w…]
- "tests_test_accuracy_gate_testthresholds": "TestThresholds" | kind=code-symbol | source=probe/tests/test_accuracy_gate.py:L148 | neighbors=[test_accuracy_gate.py, .test_clean_result_produces_no_violatio…, .test_false_positive_finding_trips_prec…, .test_matching_port_state_scores_perfec…, .test_missed_open_port_trips_open_recal…, .test_phantom_open_port_trips_open_prec…]
- "tests_test_active_validation_escalation": "test_active_validation_escalation.py" | kind=code-symbol | source=manager/backend/tests/test_active_validation_escalation.py:L1 | neighbors=[02b6341 feat(active-validation): pure e…, _ev(), test_confirmed_authoritative_does_not_e…, test_high_severity_suspected_escalates_…, test_kev_escalates_even_if_medium(), test_low_severity_non_kev_does_not_esca…]
- "tests_test_adaptive_rate": "test_adaptive_rate.py" | kind=code-symbol | source=probe/tests/test_adaptive_rate.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, scanner_base.py, _EchoProtocol, TestUdpRetransmit, TestUdpScannerAdaptive, TestWindowGating]
- "tests_test_agent_auth_boundary": "test_agent_auth_boundary.py" | kind=code-symbol | source=manager/backend/tests/test_agent_auth_boundary.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, _boundary_test_client(), test_admin_enrollment_approval_is_not_p…, test_agent_jwt_is_blocked_before_human_…, test_human_jwt_still_reaches_human_rout…, test_legacy_agent_jwt_allows_only_workl…]
- "tests_test_agent_dispatch_testtenantwebsocketselection": "TestTenantWebSocketSelection" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L95 | neighbors=[test_agent_dispatch.py, .test_displaced_socket_cannot_unregiste…, .test_first_online_push_cannot_cross_te…, .test_online_heartbeat_clears_finished_…, .test_only_returns_online_agents_in_req…, ScanJobStatus]
- "tests_test_agent_read_tools_result": "_Result" | kind=code-symbol | source=manager/backend/tests/test_agent_read_tools.py:L19 | neighbors=[test_agent_read_tools.py, Mimics the subset of a SQLAlchemy Resul…, .all(), .__init__(), .scalars(), test_list_assets_batches_services_no_n_…]
- "tests_test_auth_login_make_tenant": "_make_tenant()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L61 | neighbors=[test_auth_login.py, .test_raises_bcrypt_failure_on_passlib_…, .test_raises_disabled_tenant(), .test_not_expired_when_future(), .test_raises_expired_password(), .test_raises_password_mismatch()]
- "tests_test_campaign_progress_job": "_job()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L197 | neighbors=[test_campaign_progress.py, _running_run(), test_a_briefly_running_run_is_not_calle…, test_a_wedged_detection_run_explains_it…, test_full_coverage_completes_at_100(), test_naive_started_at_does_not_crash_th…]
- "tests_test_campaign_progress_run": "_run()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L190 | neighbors=[test_campaign_progress.py, _running_run(), test_a_briefly_running_run_is_not_calle…, test_a_wedged_detection_run_explains_it…, test_full_coverage_completes_at_100(), test_naive_started_at_does_not_crash_th…]
- "tests_test_cli_fakeclient": "FakeClient" | kind=code-symbol | source=probe/tests/test_cli.py:L152 | neighbors=[test_cli.py, .__init__(), .request(), test_cmd_doctor_success_with_online_age…, test_cmd_scan_run_builds_dispatch_paylo…, test_poll_job_rejects_invalid_timing()]
- "tests_test_customer_reveal": "test_customer_reveal.py" | kind=code-symbol | source=manager/backend/tests/test_customer_reveal.py:L1 | neighbors=[e3958e7 feat(customers): reveal + copy …, _db(), _operator(), test_reveal_missing_user_is_404(), test_reveal_null_ciphertext_returns_non…, test_reveal_returns_decrypted_password()]
- "tests_test_detection_core_mock_kev_db": "_mock_kev_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L92 | neighbors=[test_detection_core.py, .test_enriches_cvss_from_vuln_db(), .test_enriches_epss(), .test_enriches_kev(), .test_idempotent(), .test_no_data_still_sets_priority()]
- "tests_test_device_profile": "test_device_profile.py" | kind=code-symbol | source=manager/backend/tests/test_device_profile.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, test_ambiguous_keeps_asset_type_none_bu…, test_device_profiles_extracts_role_deta…, test_every_device_type_maps_to_the_righ…, test_malformed_entries_are_skipped(), test_non_device_inventory_result_yields…]
- "tests_test_dns_scanner": "test_dns_scanner.py" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, scanner_base.py, TestAxfrBounded, TestDeriveZones, TestDNSFindings, TestDNSScanner]
- "tests_test_exploit_engine_testexploitorchestrator_make_orchestrator": "._make_orchestrator()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L246 | neighbors=[TestExploitOrchestrator, .test_generate_dns_callback_token_forma…, .test_generate_dns_callback_token_uniqu…, .test_select_exploit_by_cve(), .test_select_exploit_fallback_no_cve(), .test_select_exploit_log4shell()]
- "tests_test_exploitability_finding": "_finding()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L33 | neighbors=[test_exploitability.py, .test_declared_severity_is_never_rewrit…, .test_idempotent_across_repeated_applic…, .test_kev_raises_the_score_and_priority…, .test_no_databases_is_a_no_op(), .test_reason_is_recorded_in_notes()]
- "tests_test_exploitability_testtiers": "TestTiers" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L73 | neighbors=[test_exploitability.py, .test_elevated_epss_band(), .test_epss_max_takes_the_worst_linked_c…, .test_high_epss_without_kev_is_likely(), .test_kev_listed_is_actively_exploited(), .test_kev_outranks_epss()]
- "tests_test_exposed_services_testporthypothesiscontradiction": "TestPortHypothesisContradiction" | kind=code-symbol | source=manager/detection_engine/tests/test_exposed_services.py:L188 | neighbors=[test_exposed_services.py, A catalog entry is a guess about what a…, .test_airplay_suppresses_the_cassandra_…, .test_airplay_suppresses_the_docker_reg…, .test_an_unrelated_product_does_not_sup…, .test_backdoor_evidence_is_never_suppre…]
- "tests_test_host_health_testsilencedetection": "TestSilenceDetection" | kind=code-symbol | source=probe/tests/test_host_health.py:L36 | neighbors=[test_host_health.py, .test_any_contact_beats_many_failures(), .test_filtered_is_silence_but_only_susp…, .test_no_results_is_not_silence(), .test_open_and_observed_are_contact(), .test_rst_is_contact_not_silence()]
- "tests_test_installer_contract": "test_installer_contract.py" | kind=code-symbol | source=probe/tests/test_installer_contract.py:L1 | neighbors=[81c81cb feat: implement outbox reclaim …, b5ffcb0 Refactor Vedha probe installer …, _dry_run(), test_installer_accepts_enroll_token_and…, test_installer_rejects_missing_or_unkno…, test_installer_requires_only_manager_en…]
- "tests_test_ipmi_scanner": "test_ipmi_scanner.py" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, scanner_base.py, _resp(), TestIPMIFindings, TestIPMIScanner, TestParity]
- "tests_test_job_cancel_job": "_job()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L45 | neighbors=[test_job_cancel.py, test_cancel_records_who_did_it(), test_missing_attempt_row_does_not_break…, test_open_attempt_is_closed_as_cancelle…, test_pending_job_is_cancelled_and_freed…, test_running_job_bumps_the_fence_to_abo…]
- "tests_test_job_cancel_probe_testpollingnoiseissuppressed": "TestPollingNoiseIsSuppressed" | kind=code-symbol | source=probe/tests/test_job_cancel_probe.py:L73 | neighbors=[test_job_cancel_probe.py, The probe polls forever; routine transp…, ._configure(), .test_per_request_info_lines_are_suppre…, .test_probe_debug_restores_full_tracing…, .test_probe_own_narration_is_unaffected…]
- "tests_test_main_scripts_vantage_r": "_r()" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L12 | neighbors=[test_main_scripts_vantage.py, .test_ambiguous_when_only_open_filtered…, .test_auto_detects_external_by_name(), .test_explicit_external_vantage_by_name…, .test_external_exposure_is_flagged(), .test_internal_only_not_called_external…]
- "tests_test_main_scripts_vantage_testreconcilevantages": "TestReconcileVantages" | kind=code-symbol | source=probe/tests/test_main_scripts_vantage.py:L16 | neighbors=[test_main_scripts_vantage.py, .test_ambiguous_when_only_open_filtered…, .test_auto_detects_external_by_name(), .test_explicit_external_vantage_by_name…, .test_external_exposure_is_flagged(), .test_internal_only_not_called_external…]
- "tests_test_network_va_accuracy_listener": "_Listener" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L26 | neighbors=[test_network_va_accuracy.py, .__init__(), ._loop(), ._serve(), .start(), .stop()]
- "tests_test_nuclei_background_sessionfactory": "_SessionFactory" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L59 | neighbors=[test_nuclei_background.py, .__call__(), .__init__(), test_fatal_nuclei_error_marks_backgroun…, test_partial_nuclei_run_preserves_findi…, ScanJobStatus]
- "tests_test_online_finding": "_finding()" | kind=code-symbol | source=probe/tests/test_online.py:L64 | neighbors=[test_online.py, A CVEFinding as the offline pass would …, .test_caches_per_cve_id(), .test_fail_open_leaves_offline_result_u…, .test_gap_fill_sets_cvss_and_recomputes…, .test_online_all_cross_checks_and_annot…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-032.json

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
