# Node Description Batch 23 of 380

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

- "routers_scan_schedules": "scan_schedules.py" | kind=code-symbol | source=manager/backend/app/routers/scan_schedules.py:L1 | neighbors=[eec1b35 feat(scheduling): scan-schedule…, dependencies.py, create_schedule(), delete_schedule(), _engagement_or_404(), list_schedules()]
- "routers_sla_policy": "sla_policy.py" | kind=code-symbol | source=manager/backend/app/routers/sla_policy.py:L1 | neighbors=[c5ebd38 feat(sla): per-tenant custom SL…, dependencies.py, get_sla_policy(), _out(), put_sla_policy(), resolve_windows()]
- "routers_vuln_scans_rationale_272": "Background task: run nuclei, persist findings, trigger enrichment." | kind=entity | source=manager/backend/app/routers/vuln_scans.py:L272 | neighbors=[Asset, Engagement, FindingSeverity, FindingStatus, ScanJobStatus, ScanJobType]
- "scanner_delta_scanner": "delta_scanner.py" | kind=code-symbol | source=probe/scanner/delta_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, 8f6bf49 Refactor code structure and rem…, Delta, DeltaEngine, _extract_service(), _extract_version()]
- "scanner_mobile_scanner": "mobile_scanner.py" | kind=code-symbol | source=probe/scanner/mobile_scanner.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _adb_checksum(), _build_adb_cnxn(), _build_mdns_query(), main(), MobileScanner]
- "scanner_smb_enum_scanner": "smb_enum_scanner.py" | kind=code-symbol | source=probe/scanner/smb_enum_scanner.py:L1 | neighbors=[6e2818f Add support for additional serv…, _decode(), _enum_shares(), _enum_users_ridcycle(), _enum_users_samr(), main()]
- "scanner_va_campaign_progressreporter": "ProgressReporter" | kind=code-symbol | source=probe/scanner/va_campaign.py:L169 | neighbors=[va_campaign.py, build_campaign(), ._current(), ._eta_seconds(), .finish(), ._flush()]
- "schemas_ai": "ai.py" | kind=code-symbol | source=manager/backend/app/schemas/ai.py:L1 | neighbors=[10ceaca feat: implement AI model fallba…, 1fe16c8 stable but some dead code, need…, 30261eb feat: enhance advisor flow with…, 75650c1 feat: add Posture & Patch-Compa…, 7a637eb feat: network VA accuracy, KEV …, ef14810 Implement instance locking mech…]
- "services_llm_managerllmservice_dispatch": "._dispatch()" | kind=code-symbol | source=manager/backend/app/services/llm.py:L386 | neighbors=[ManagerLlmService, AiRuntimeError, ._anthropic(), ._gemini(), ._ollama(), ._openai()]
- "tests_assistant_test": "assistant.test.ts" | kind=code-symbol | source=manager/frontend/tests/assistant.test.ts:L1 | neighbors=[1fe16c8 stable but some dead code, need…, 65f22a7 Add comprehensive tests for aut…, d98f654 feat(manager): network-VA campa…, route.ts, POST(), assistant.ts]
- "tests_test_ad_assessment_rationale_1": "Unit tests for the Active Directory assessment module (Prompt 5).  All directory" | kind=entity | source=manager/backend/tests/test_ad_assessment.py:L1 | neighbors=[test_ad_assessment.py, ADCSChecker, CertTemplate, ASREPRoastChecker, BloodHoundCollector, KerberoastChecker]
- "tests_test_ai_engine_testllmreportgenerator": "TestLLMReportGenerator" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L177 | neighbors=[test_ai_engine.py, .test_complete_retries_then_succeeds(), .test_detection_rule_explanation(), .test_executive_summary_persists_pendin…, .test_system_prompt_is_prompt_cached(), .test_technical_finding_runs_guard()]
- "tests_test_detection_core_candidate": "_candidate()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L50 | neighbors=[test_detection_core.py, .test_cpe23_format(), .test_ai_assisted_carried_through(), .test_authoritative_source_confirms(), .test_inferred_match_has_backport_note(), .test_match_produces_finding()]
- "tests_test_enqueue_intensity": "test_enqueue_intensity.py" | kind=code-symbol | source=manager/backend/tests/test_enqueue_intensity.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, test_every_manager_code_maps_to_a_known…, test_intensity_accepts_code_or_name(), test_invalid_intensity_is_rejected_at_t…, test_normalize_intensity_name_maps_code…, test_numeric_uc_code_accepted()]
- "tests_test_evidence_summary": "test_evidence_summary.py" | kind=code-symbol | source=manager/backend/tests/test_evidence_summary.py:L1 | neighbors=[ef14810 Implement instance locking mech…, test_booleans_render_yes_no_with_exposu…, test_common_keys_get_friendly_labels_in…, test_enrichment_kev_and_epss_are_surfac…, test_lists_are_joined_not_json(), test_nested_dicts_do_not_leak_raw_json()]
- "tests_test_exploitability": "test_exploitability.py" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L1 | neighbors=[7a637eb feat: network VA accuracy, KEV …, f473173 merge: network VA accuracy, KEV…, _epss(), _fact(), _finding(), _kev()]
- "tests_test_finding_events": "test_finding_events.py" | kind=code-symbol | source=manager/backend/tests/test_finding_events.py:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, d98f654 feat(manager): network-VA campa…, f473173 merge: network VA accuracy, KEV…, _finding(), TestEventTypeForStatus]
- "tests_test_finding_out_computed": "test_finding_out_computed.py" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L1 | neighbors=[42f4e28 feat: enhance security operatio…, 7d8d3f3 merge: resolve conflicts with o…, 8ebc053 feat(risk-rank-ui): surface ver…, f473173 merge: network VA accuracy, KEV…, _base(), test_confirmed_exploited_outranks_contr…]
- "tests_test_finding_out_enrichment_phase3": "test_finding_out_enrichment_phase3.py" | kind=code-symbol | source=manager/backend/tests/test_finding_out_enrichment_phase3.py:L1 | neighbors=[6cf7e16 Expose report enrichment on Fin…, _base(), test_detection_method_from_exploit_vali…, test_detection_method_from_verification…, test_detection_method_none_when_unprove…, test_epss_percentile_surfaced_from_evid…]
- "tests_test_job_cancel_db": "_db()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L69 | neighbors=[test_job_cancel.py, test_cancel_records_who_did_it(), test_job_outside_the_tenant_is_not_foun…, test_missing_attempt_row_does_not_break…, test_open_attempt_is_closed_as_cancelle…, test_pending_job_is_cancelled_and_freed…]
- "tests_test_job_cancel_one": "_one()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L60 | neighbors=[test_job_cancel.py, A db.execute() result whose scalar_one_…, test_cancel_records_who_did_it(), test_job_outside_the_tenant_is_not_foun…, test_missing_attempt_row_does_not_break…, test_open_attempt_is_closed_as_cancelle…]
- "tests_test_job_cancel_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_job_cancel.py:L29 | neighbors=[test_job_cancel.py, The REAL CurrentUser, not a SimpleNames…, test_cancel_records_who_did_it(), test_job_outside_the_tenant_is_not_foun…, test_missing_attempt_row_does_not_break…, test_open_attempt_is_closed_as_cancelle…]
- "tests_test_main_scripts_adaptive_timeout": "test_main_scripts_adaptive_timeout.py" | kind=code-symbol | source=probe/tests/test_main_scripts_adaptive_timeout.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 26ea68c Add comprehensive tests for OS …, adaptive_timeout.py, test_estimate_converges_on_stable_rtt(), test_fast_lan_gets_short_timeout_slow_w…, test_first_sample_sets_srtt_and_timeout…]
- "tests_test_main_scripts_completeness": "test_main_scripts_completeness.py" | kind=code-symbol | source=probe/tests/test_main_scripts_completeness.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, port_scanner.py, scanner_base.py, _metrics(), _rec(), test_duplicate_port_is_detected()]
- "tests_test_main_scripts_coverage": "test_main_scripts_coverage.py" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, ae08d19 feat(scanner): adaptive timeout…, port_scanner.py, scanner_base.py, _closed(), _mk_scanner()]
- "tests_test_main_scripts_hardening": "test_main_scripts_hardening.py" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, 4d0377d Add unit tests for SMB scanner,…, scanner_base.py, make_smb2_error(), make_smb2_success(), _run()]
- "tests_test_new_scanners_testdeltaengine": "TestDeltaEngine" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L380 | neighbors=[test_new_scanners.py, .test_diff_detects_new_service(), .test_diff_detects_service_gone(), .test_diff_detects_state_change_to_open…, .test_diff_high_severity_port_heuristic…, .test_diff_no_change_produces_no_servic…]
- "tests_test_nuclei_scanner_fakeprocess": "FakeProcess" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L30 | neighbors=[test_nuclei_scanner.py, .__init__(), .kill(), .terminate(), .wait(), test_nonzero_exit_retains_and_marks_par…]
- "tests_test_pipeline_concurrency": "test_pipeline_concurrency.py" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, _db_with(), _event(), test_a_first_delivery_still_runs_detect…, test_a_missing_submission_is_not_an_err…, test_a_redelivered_submission_is_not_de…]
- "tests_test_posture_trace_asset": "_asset()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L24 | neighbors=[test_posture_trace.py, .test_key_absent_is_missing_input_not_c…, .test_key_present_false_is_clean_no_mat…, .test_key_present_true_is_match(), .test_missing_input_invariant_across_al…, ._mixed()]
- "tests_test_posture_trace_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L17 | neighbors=[test_posture_trace.py, .test_key_absent_is_missing_input_not_c…, .test_key_present_false_is_clean_no_mat…, .test_key_present_true_is_match(), .test_missing_input_invariant_across_al…, ._mixed()]
- "tests_test_probe_core_testgate5": "TestGate5" | kind=code-symbol | source=probe/tests/test_probe_core.py:L322 | neighbors=[test_probe_core.py, .test_dynamically_routed_overrides_port…, .test_explicit_snmp_does_not_require_tc…, .test_iot_profile_no_smb(), .test_it_profile_tls_with_tls_port(), .test_mcp_ai_allowed_on_it_ai_port()]
- "tests_test_probe_enrollment": "test_probe_enrollment.py" | kind=code-symbol | source=manager/backend/tests/test_probe_enrollment.py:L1 | neighbors=[81c81cb feat: implement outbox reclaim …, b5ffcb0 Refactor Vedha probe installer …, test_device_access_token_has_dedicated_…, test_ed25519_proof_of_possession_reject…, test_enroll_token_create_defaults_and_b…, test_enroll_token_usable_only_while_liv…]
- "tests_test_scanner_congestion_testreprobecleanuppass": "TestReprobeCleanupPass" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L337 | neighbors=[test_scanner_congestion.py, A host that rate-limits its RSTs answer…, ._rate_limited(), ._silent_attempt(), ._summary(), .test_cleanup_raises_the_timeout_floor()]
- "tests_test_task_runner": "test_task_runner.py" | kind=code-symbol | source=probe/tests/test_task_runner.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, 1fe16c8 stable but some dead code, need…, b4b12a9 Rename project and update files, task_runner.py, _fake_run_scan(), runner()]
- "tests_test_task_runner_testrunnerheadless": "TestRunnerHeadless" | kind=code-symbol | source=probe/tests/test_task_runner.py:L46 | neighbors=[test_task_runner.py, Tests that use the real engine but with…, .test_explicit_empty_targets_never_expa…, .test_rejects_empty_targets(), .test_rejects_non_object_params(), .test_rejects_non_string_target()]
- "tests_test_tier1_wiring_gate": "test_tier1_wiring_gate.py" | kind=code-symbol | source=probe/tests/test_tier1_wiring_gate.py:L1 | neighbors=[64e8290 feat(campaign): implement VA ca…, 6e2818f Add support for additional serv…, scan_funnel.py, scanner_base.py, _funnel(), test_every_it_branch_has_port_table_ent…]
- "tests_test_validation_ingest": "test_validation_ingest.py" | kind=code-symbol | source=manager/backend/tests/test_validation_ingest.py:L1 | neighbors=[50d6554 feat(active-validation): approv…, _exec(), _finding(), test_confirmed_never_overrides_human_cl…, test_confirmed_raises_certainty(), test_contradicted_marks_false_positive_…]
- "tests_test_xml_parser_testnmapxmlparser": "TestNmapXMLParser" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L42 | neighbors=[test_xml_parser.py, .setup_method(), .test_cpe_extraction(), .test_empty_scan(), .test_empty_string(), .test_malformed_xml_returns_empty()]
- "tools_installer_installtool": "installTool()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L156 | neighbors=[tools.ts, installer.ts, installAll(), downloadFile(), extract(), getInstalledRecord()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-022.json

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
