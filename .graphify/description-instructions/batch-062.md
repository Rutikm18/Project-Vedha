# Node Description Batch 63 of 336

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_campaign_progress_scalars": "_scalars()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L17 | neighbors=[test_campaign_progress.py, _progress(), _run_scenario(), test_campaign_progress_aggregates_jobs_…, test_campaign_progress_no_detection_yet…]
- "tests_test_campaign_progress_terminal": "test_campaign_progress_terminal.py" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress_terminal.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, _status(), TestNormalPipelineUnaffected, TestTerminalWithoutResults, A campaign whose jobs all ended without…]
- "tests_test_campaign_progress_test_a_briefly_running_run_is_not_called_stalled": "test_a_briefly_running_run_is_not_called_stalled()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L283 | neighbors=[test_campaign_progress.py, A run that started seconds ago is busy,…, _job(), _progress(), _run()]
- "tests_test_campaign_progress_test_a_wedged_detection_run_explains_itself": "test_a_wedged_detection_run_explains_itself()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L267 | neighbors=[test_campaign_progress.py, The other way a campaign never finishes…, _job(), _progress(), _run()]
- "tests_test_campaign_progress_test_naive_started_at_does_not_crash_the_page": "test_naive_started_at_does_not_crash_the_page()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L294 | neighbors=[test_campaign_progress.py, started_at can come back tz-naive depen…, _job(), _progress(), _run()]
- "tests_test_campaign_progress_test_percent_reaches_100_exactly_when_the_campaign_is_complete": "test_percent_reaches_100_exactly_when_the_campaign_is_complete()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L217 | neighbors=[test_campaign_progress.py, The invariant. Checked across the state…, _job(), _progress(), _run()]
- "tests_test_campaign_progress_test_uncovered_submission_holds_progress_below_100": "test_uncovered_submission_holds_progress_below_100()" | kind=code-symbol | source=manager/backend/tests/test_campaign_progress.py:L238 | neighbors=[test_campaign_progress.py, The exact regression: the newest submis…, _job(), _progress(), _run()]
- "tests_test_customer_access_pending_request": "_pending_request()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L142 | neighbors=[test_customer_access.py, .test_approve_dispatches_job_and_links_…, .test_approve_non_pending_is_conflict(), .test_approve_without_assigned_agent_is…, .test_reject_records_reason()]
- "tests_test_customer_access_testapprovescanrequest_test_approve_dispatches_job_and_links_it": ".test_approve_dispatches_job_and_links_it()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L151 | neighbors=[TestApproveScanRequest, _added(), _mock_db(), _operator(), _pending_request()]
- "tests_test_cve_correlation_testingestparse": "TestIngestParse" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L233 | neighbors=[test_cve_correlation.py, .test_cvss_fallback(), .test_ingest_idempotent(), .test_ingest_one_cve(), .test_parse_criteria()]
- "tests_test_cve_correlation_testmirrorage": "TestMirrorAge" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L329 | neighbors=[test_cve_correlation.py, .test_fresh_has_no_warning(), .test_stale_warns(), .test_unknown_when_no_stamp(), .test_unparseable_stamp_is_graceful()]
- "tests_test_detection_core_testenrichfinding_test_enriches_cvss_from_vuln_db": ".test_enriches_cvss_from_vuln_db()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L856 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_enriches_epss": ".test_enriches_epss()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L878 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_enriches_kev": ".test_enriches_kev()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L870 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_idempotent": ".test_idempotent()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L894 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_core_testenrichfinding_test_no_data_still_sets_priority": ".test_no_data_still_sets_priority()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L886 | neighbors=[TestEnrichFinding, _finding(), _mock_epss_db(), _mock_kev_db(), _mock_vuln_db()]
- "tests_test_detection_coverage_run": "_run()" | kind=code-symbol | source=manager/backend/tests/test_detection_coverage.py:L38 | neighbors=[test_detection_coverage.py, test_completed_no_blind_is_plain_comple…, test_completed_with_blind_rules_is_comp…, test_explain_all_rules_sorts_gaps_first…, test_explain_single_rule_reports_schema…]
- "tests_test_detection_coverage_test_aggregating_reason_names_the_outbox_worker": "test_aggregating_reason_names_the_outbox_worker()" | kind=code-symbol | source=manager/backend/tests/test_detection_coverage.py:L92 | neighbors=[test_detection_coverage.py, _job(), _rows(), _scalars(), _user()]
- "tests_test_device_identity": "test_device_identity.py" | kind=code-symbol | source=probe/tests/test_device_identity.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, device_identity.py, test_device_identity_rejects_invalid_pr…, test_device_identity_round_trip_and_sig…, test_site_policy_signature_and_tofu_pin…]
- "tests_test_dns_scanner_testdnsfindings": "TestDNSFindings" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L125 | neighbors=[test_dns_scanner.py, ._fact(), .test_dnssec_absent_only_for_confirmed_…, .test_secure_server_silent(), .test_zone_transfer_version_and_unsigne…]
- "tests_test_dns_scanner_testdnsscanner": "TestDNSScanner" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L97 | neighbors=[test_dns_scanner.py, ._sc(), .test_dnspython_missing_is_error(), .test_no_dns_is_filtered(), .test_zone_transfer_open()]
- "tests_test_dualstack_fallback_testsmbnegotiatefallback": "TestSmbNegotiateFallback" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L46 | neighbors=[test_dualstack_fallback.py, ._fake_socket(), ._patch_candidates(), .test_falls_back_to_ipv4_when_ipv6_is_b…, .test_returns_none_only_when_every_fami…]
- "tests_test_e2e_engagement_to_findings_manager": "_manager()" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L51 | neighbors=[test_e2e_engagement_to_findings.py, Return (http_get, submit_result, captur…, test_engagement_dispatch_reaches_probe_…, test_out_of_scope_target_is_refused_end…, test_real_scan_of_open_datastore_yields…]
- "tests_test_e2e_engagement_to_findings_vulnerable_host_facts": "_vulnerable_host_facts()" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L137 | neighbors=[test_e2e_engagement_to_findings.py, Exactly what the probe's smb/port scann…, test_correlated_findings_cite_their_bas…, test_manager_correlation_finds_all_thre…, test_ntlm_relay_is_high_when_smbv1_pres…]
- "tests_test_engagement_validation": "test_engagement_validation.py" | kind=code-symbol | source=manager/backend/tests/test_engagement_validation.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, test_create_normalizes_name_scopes_and_…, test_create_rejects_invalid_scope_entri…, test_create_rejects_reversed_date_range…, test_update_rejects_blank_name_invalid_…]
- "tests_test_exploitability_testapplytofindings_test_declared_severity_is_never_rewritten": ".test_declared_severity_is_never_rewritten()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L119 | neighbors=[Severity is the rule's judgement of the…, TestApplyToFindings, _epss(), _finding(), _kev()]
- "tests_test_exploitability_testapplytofindings_test_idempotent_across_repeated_application": ".test_idempotent_across_repeated_application()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L162 | neighbors=[The pipeline may enrich the same findin…, TestApplyToFindings, _epss(), _finding(), _kev()]
- "tests_test_fact_contract_load_corpus": "_load_corpus()" | kind=code-symbol | source=manager/detection_engine/tests/test_fact_contract.py:L27 | neighbors=[test_fact_contract.py, _ingest_corpus(), test_corpus_is_present_and_nonempty(), test_every_rule_input_is_emitted_by_its…, test_report_unconsumed_evidence()]
- "tests_test_finding_section": "test_finding_section.py" | kind=code-symbol | source=probe/tests/test_finding_section.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, findings.py, TestFindingSection, TestScannerRegistry, test_finding_section.py — the scanner-m…]
- "tests_test_ftp_scanner_testftpfindings": "TestFTPFindings" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L53 | neighbors=[test_ftp_scanner.py, ._fact(), .test_anon_denied_is_silent(), .test_anon_login_only_is_medium(), .test_anon_read_is_high()]
- "tests_test_ftp_scanner_testftpscanner": "TestFTPScanner" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L28 | neighbors=[test_ftp_scanner.py, ._sc(), .test_anon_login_and_read_open(), .test_ftp_present_anon_denied_open_but_…, .test_no_ftp_filtered()]
- "tests_test_host_discovery_udp_nbstat_reply": "_nbstat_reply()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L24 | neighbors=[test_host_discovery_udp.py, Build a NetBIOS node-status response (R…, test_netbios_reply_proves_life_and_name…, .test_msbrowse_control_chars_dropped(), .test_names_hostname_domain_mac()]
- "tests_test_host_discovery_udp_responder": "_Responder" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L90 | neighbors=[test_host_discovery_udp.py, .connection_made(), .datagram_received(), .__init__(), _udp_server()]
- "tests_test_host_discovery_udp_testfusewithudp": "TestFuseWithUdp" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L59 | neighbors=[test_host_discovery_udp.py, .test_icmp_unreachable_alone(), .test_no_signals_unchanged(), .test_tcp_plus_udp_corroborate(), .test_udp_reply_alone_is_confirmed_aliv…]
- "tests_test_host_health_testsafetyproperty": "TestSafetyProperty" | kind=code-symbol | source=probe/tests/test_host_health.py:L130 | neighbors=[test_host_health.py, .test_healthy_host_produces_no_facts_at…, .test_offline_fact_marks_the_scan_incom…, .test_offline_host_stops_accumulating_o…, .test_one_offline_host_does_not_implica…]
- "tests_test_host_health_testudpnoreplyisnotcontact": "TestUdpNoReplyIsNotContact" | kind=code-symbol | source=probe/tests/test_host_health.py:L185 | neighbors=[test_host_health.py, Regression: "open|filtered" is the UDP …, .test_a_real_open_port_still_counts_as_…, .test_mixed_udp_silence_and_a_real_open…, .test_udp_no_reply_counts_as_silence()]
- "tests_test_hw_bind_testcheckhwbind": "TestCheckHwBind" | kind=code-symbol | source=probe/tests/test_hw_bind.py:L21 | neighbors=[test_hw_bind.py, .test_passes_when_match(), .test_raises_on_mismatch(), .test_raises_when_unset_and_enforced(), .test_skips_when_unset_and_dev_mode()]
- "tests_test_integration_testfulljoblifecycle": "TestFullJobLifecycle" | kind=code-symbol | source=probe/tests/test_integration.py:L311 | neighbors=[test_integration.py, End-to-end: identity → register → job →…, .test_complete_flow_with_encrypted_scop…, .test_job_ot_passive_profile(), .test_job_rejected_all_targets_out_of_s…]
- "tests_test_integration_testidentityandencryption": "TestIdentityAndEncryption" | kind=code-symbol | source=probe/tests/test_integration.py:L64 | neighbors=[test_integration.py, Phase 4: identity generation + scope en…, .test_different_key_cannot_decrypt(), .test_full_identity_lifecycle(), .test_scope_encryption_roundtrip()]
- "tests_test_integration_testresultspoolwithretry": "TestResultSpoolWithRetry" | kind=code-symbol | source=probe/tests/test_integration.py:L197 | neighbors=[test_integration.py, Phase 1: result spool with upload retry., .test_spool_persists_and_flushes(), .test_submit_exhausts_retries(), .test_submit_retries_on_failure()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-062.json

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
