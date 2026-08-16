# Node Description Batch 28 of 209

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

- "tests_test_active_validation_escalation_ev": "_ev()" | kind=code-symbol | source=manager/backend/tests/test_active_validation_escalation.py:L6 | neighbors=[test_active_validation_escalation.py, test_confirmed_authoritative_does_not_e…, test_high_severity_suspected_escalates_…, test_kev_escalates_even_if_medium(), test_low_severity_non_kev_does_not_esca…, test_ot_profile_never_escalates()] | lang=en
- "tests_test_agent_dispatch_testatomicwebsocketclaim": "TestAtomicWebSocketClaim" | kind=code-symbol | source=manager/backend/tests/test_agent_dispatch.py:L220 | neighbors=[test_agent_dispatch.py, .test_claim_commits_before_confirmation…, .test_incompatible_capability_is_never_…, .test_lost_atomic_update_is_reported_as…, ScanJobStatus, ScanJobType] | lang=en
- "tests_test_agents_testenqueueagentjob": "TestEnqueueAgentJob" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L43 | neighbors=[test_agents.py, .test_404_when_engagement_missing(), .test_materializes_direct_job_capabilit…, .test_rejects_server_side_type(), .test_scope_fields_cannot_override_enga…, .test_success_creates_pending_job()] | lang=en
- "tests_test_ai_engine_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L24 | neighbors=[test_ai_engine.py, .test_technical_finding_runs_guard(), .test_unavailable_without_client(), .test_explain_prediction_fallback_shape…, .test_extract_features_order_and_values…, .test_higher_cvss_scores_higher()] | lang=en
- "tests_test_ai_normalizer": "test_ai_normalizer.py" | kind=code-symbol | source=manager/detection_engine/tests/test_ai_normalizer.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, _fact(), TestAINormalizerCache, TestExtractRawText, TestFakeAIClient, TestProposeCandidates] | lang=en
- "tests_test_attack_paths_rationale_1": "Unit tests for the attack-path analysis engine (Prompt 6).  The engine is exerci" | kind=entity | source=manager/backend/tests/test_attack_paths.py:L1 | neighbors=[test_attack_paths.py, PathAnalyzer, GraphBuilder, DemoAsset, DemoFinding, Neo4jClient] | lang=en
- "tests_test_engagement_lists": "test_engagement_lists.py" | kind=code-symbol | source=manager/backend/tests/test_engagement_lists.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, _scalars(), test_list_assets_groups_services(), test_list_jobs_returns_results(), _user(), Unit tests for the dashboard list endpo…] | lang=en
- "tests_test_exposure": "test_exposure.py" | kind=code-symbol | source=manager/backend/tests/test_exposure.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, test_critical_stays_critical(), test_external_escalates_one_rung(), test_non_external_never_escalates(), test_service_exposure_flattens_per_port…, test_service_exposure_ignores_malformed…] | lang=en
- "tests_test_finding_out_computed": "test_finding_out_computed.py" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L1 | neighbors=[8ebc053 feat(risk-rank-ui): surface ver…, _base(), test_confirmed_exploited_outranks_contr…, test_explicit_risk_rank_is_preserved(), test_lifecycle_fields_round_trip(), test_risk_rank_is_computed_not_none()] | lang=en
- "tests_test_host_discovery_mobile": "test_host_discovery_mobile.py" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L1 | neighbors=[4d0377d Add unit tests for SMB scanner,…, host_discovery.py, TestDeviceHint, TestLocallyAdministered, TestNormalizeMac, TestVendorLookup] | lang=en
- "tests_test_host_discovery_mobile_testnormalizemac": "TestNormalizeMac" | kind=code-symbol | source=probe/tests/test_host_discovery_mobile.py:L9 | neighbors=[test_host_discovery_mobile.py, .test_extracts_from_arp_line(), .test_lowercases(), .test_rejects_broadcast(), .test_rejects_garbage(), .test_rejects_multicast()] | lang=en
- "tests_test_job_result_service": "test_job_result_service.py" | kind=code-symbol | source=manager/backend/tests/test_job_result_service.py:L1 | neighbors=[b4b12a9 Rename project and update files, b5ffcb0 Refactor Vedha probe installer …, test_out_of_scope_result_is_rejected_be…, test_result_scope_accepts_authorized_ta…, test_result_scope_fails_closed(), test_stale_attempt_gets_terminal_receip…] | lang=en
- "tests_test_main_scripts_completeness_rec": "_rec()" | kind=code-symbol | source=probe/tests/test_main_scripts_completeness.py:L20 | neighbors=[test_main_scripts_completeness.py, test_duplicate_port_is_detected(), test_fallback_count_based_when_no_reque…, test_full_scan_is_complete(), test_missing_port_is_detected(), test_skip_plus_duplicate_is_not_falsely…] | lang=en
- "tests_test_main_scripts_coverage_testprofiles": "TestProfiles" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L41 | neighbors=[test_main_scripts_coverage.py, .test_custom_dedups_and_requires_ports(), .test_full_is_entire_tcp_space(), .test_quick_is_small_and_contains_smb(), .test_top1000_covers_windows_ground_tru…, .test_top100_is_100_unique()] | lang=en
- "tests_test_main_scripts_coverage_testworkerpoolandmetrics": "TestWorkerPoolAndMetrics" | kind=code-symbol | source=probe/tests/test_main_scripts_coverage.py:L81 | neighbors=[test_main_scripts_coverage.py, .test_all_65535_ports_scheduled_exactly…, .test_concurrency_is_bounded_by_the_poo…, .test_every_port_scanned_exactly_once(), .test_local_resource_error_marks_scan_d…, .test_metrics_counts_every_state()] | lang=en
- "tests_test_main_scripts_device": "test_main_scripts_device.py" | kind=code-symbol | source=probe/tests/test_main_scripts_device.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, 4d0377d Add unit tests for SMB scanner,…, device_classifier.py, scanner_base.py, TestClassifyDevice, TestClassifyFromResults] | lang=en
- "tests_test_main_scripts_rdp_cc": "_cc()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L15 | neighbors=[test_main_scripts_rdp.py, A TPKT + X.224 Connection Confirm, opti…, test_cc_without_negotiation_is_standard…, test_negotiation_failure(), test_nla_when_hybrid_selected(), test_standard_rdp_security_no_nla()] | lang=en
- "tests_test_nuclei_background": "test_nuclei_background.py" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L1 | neighbors=[b4b12a9 Rename project and update files, _FakeSession, _NestedTransaction, _ScalarResult, _SessionFactory, test_fatal_nuclei_error_marks_backgroun…] | lang=en
- "tests_test_nuclei_background_nestedtransaction": "_NestedTransaction" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L22 | neighbors=[test_nuclei_background.py, .begin_nested(), .__aenter__(), .__aexit__(), ScanJobStatus, NucleiRunReport] | lang=en
- "tests_test_nuclei_background_scalarresult": "_ScalarResult" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L14 | neighbors=[test_nuclei_background.py, .execute(), .__init__(), .scalar_one_or_none(), ScanJobStatus, NucleiRunReport] | lang=en
- "tests_test_os_fingerprint_testfingerprintos": "TestFingerprintOs" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L126 | neighbors=[test_os_fingerprint.py, .test_network_device_from_ttl_255(), .test_no_signals_is_unknown(), .test_signals_recorded(), .test_ttl_and_window_agree_boosts_confi…, .test_ttl_only_linux()] | lang=en
- "tests_test_portal_read_db_list": "_db_list()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L35 | neighbors=[test_portal_read.py, Each db.execute(...) → result whose .sc…, .test_findings_scoped_and_serialized(), .test_operator_is_forbidden(), .test_posture_scores_open_findings(), .test_lists_approved_reports()] | lang=en
- "tests_test_portal_read_engagement": "_engagement()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L237 | neighbors=[test_portal_read.py, .test_creates_pending_request_with_targ…, .test_excluded_target_is_422(), .test_out_of_scope_target_is_422(), .test_queue_cap_is_conflict(), .test_unknown_scan_type_is_422()] | lang=en
- "tests_test_probe_auto_enroll": "test_probe_auto_enroll.py" | kind=code-symbol | source=manager/backend/tests/test_probe_auto_enroll.py:L1 | neighbors=[c0f3b4c feat(probe-enroll): trust-on-fi…, config.py, test_auto_enroll_cidrs_defaults_to_rfc1…, test_auto_enroll_cidrs_parses_and_trims…, test_auto_enroll_is_off_by_default(), test_auto_enroll_site_name_is_stable()] | lang=en
- "tests_test_probe_core_testclassifycertainty": "TestClassifyCertainty" | kind=code-symbol | source=probe/tests/test_probe_core.py:L706 | neighbors=[test_probe_core.py, .test_error_overrides(), .test_host_discovery_uncertain(), .test_service_banner_deterministic(), .test_tcp_port_scan_deterministic(), .test_udp_port_scan_uncertain()] | lang=en
- "tests_test_risk_rank_rank": "_rank()" | kind=code-symbol | source=manager/backend/tests/test_risk_rank.py:L6 | neighbors=[test_risk_rank.py, test_bounds(), test_confirmed_exploitable_outranks_con…, test_contradicted_sinks_below_inferred(), test_internet_facing_raises_and_auth_lo…, test_kev_raises_rank()] | lang=en
- "tests_test_scope_validator_testmergeexclusions": "TestMergeExclusions" | kind=code-symbol | source=probe/tests/test_scope_validator.py:L144 | neighbors=[test_scope_validator.py, .test_both_empty(), .test_empty_engagement_excludes(), .test_empty_job_excludes(), .test_merges_no_duplicates(), .test_none_job_excludes()] | lang=en
- "tests_test_syn_scanner_testsynretransmit": "TestSynRetransmit" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L204 | neighbors=[test_syn_scanner.py, The raw SYN path resends ONLY still-sil…, ._patch(), .test_answered_ports_are_not_retransmit…, .test_retries_zero_sends_one_syn_per_po…, .test_silent_ports_are_retried_retries_…] | lang=en
- "tests_test_tls_fingerprint_testdigest": "TestDigest" | kind=code-symbol | source=probe/tests/test_tls_fingerprint.py:L83 | neighbors=[test_tls_fingerprint.py, .test_cipher_code_known_and_unknown(), .test_digest_differs_with_cipher(), .test_digest_is_62_chars(), .test_digest_is_deterministic(), .test_version_code()] | lang=en
- "tests_test_tls_integration_tlsserver": "_TLSServer" | kind=code-symbol | source=probe/tests/test_tls_integration.py:L50 | neighbors=[test_tls_integration.py, test_tls_fingerprint_is_nonzero_and_sta…, test_tls_scanner_reports_posture_grade(), .__enter__(), .__exit__(), .__init__()] | lang=en
- "tests_test_udp_amplifiers": "test_udp_amplifiers.py" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L1 | neighbors=[fe868e6 feat(probe): real UDP amplifica…, udp_scanner.py, test_dns_open_recursion(), test_memcached_exposed(), test_ntp_monlist_absent(), test_ntp_monlist_enabled()] | lang=en
- "tests_test_validation_endpoints_mock_db": "_mock_db()" | kind=code-symbol | source=manager/backend/tests/test_validation_endpoints.py:L34 | neighbors=[test_validation_endpoints.py, _exec(), test_approve_conflict_when_not_pending(), test_approve_enqueues_safe_validate_job…, test_create_rejected_when_roe_forbids(), test_create_request_is_pending_and_deri…] | lang=en
- "use_cases_route": "route.ts" | kind=code-symbol | source=manager/frontend/app/api/scan/use-cases/route.ts:L1 | neighbors=[a789cca scanner: real use-case library,…, backend(), withBackend(), GET, 0557559 scanner: real use-case library,…, backend.ts] | lang=en
- "vuln_enrichment": "enrichment.py" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, d1b4dd3 trim frontend to 7 core pages; …, TTLCache, VulnEnrichmentService, VulnEnrichmentService  External data so…, 2885afa Add comprehensive probe testing…] | lang=en
- "vuln_enrichment_ttlcache_get": ".get()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L56 | neighbors=[TTLCache, .compute_composite_risk(), .enrich(), .fetch_epss(), .fetch_mitre_techniques(), .fetch_nvd()] | lang=en
- "vuln_enrichment_vulnenrichmentservice_fetch_all": "._fetch_all()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L341 | neighbors=[Fetch NVD, EPSS, KEV and MITRE concurre…, VulnEnrichmentService, .enrich(), .check_cisa_kev(), .fetch_epss(), .fetch_mitre_techniques()] | lang=en
- "vuln_nessus": "nessus.py" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L1 | neighbors=[10dfc80 Add comprehensive probe testing…, cac022c Everything is done and verified…, d1b4dd3 trim frontend to 7 core pages; …, NessusScanner, NessusScanner — wraps the Tenable Nessu…, 2885afa Add comprehensive probe testing…] | lang=en
- "vuln_nessus_nessusscanner_get_client": "._get_client()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L49 | neighbors=[NessusScanner, .create_scan(), .export_nessus_file(), ._auth_headers(), .get_results(), .launch_scan()] | lang=en
- "vuln_tasks_rationale_1": "Background tasks triggered after a vuln scan completes.  Pipeline:   1. Load all" | kind=entity | source=manager/backend/app/vuln/tasks.py:L1 | neighbors=[tasks.py, Asset, Engagement, FindingSeverity, FindingStatus, Finding] | lang=pt
- "vuln_tasks_rationale_168": "Deprecated — use app.utils.hash.dedup_hash instead." | kind=entity | source=manager/backend/app/vuln/tasks.py:L168 | neighbors=[_dedup_hash(), Asset, Engagement, FindingSeverity, FindingStatus, Finding] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-027.json

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
