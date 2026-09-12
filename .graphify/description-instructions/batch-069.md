# Node Description Batch 70 of 380

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

- "tests_test_customer_access_pending_request": "_pending_request()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L142 | neighbors=[test_customer_access.py, .test_approve_dispatches_job_and_links_…, .test_approve_non_pending_is_conflict(), .test_approve_without_assigned_agent_is…, .test_reject_records_reason()]
- "tests_test_customer_access_testapprovescanrequest_test_approve_dispatches_job_and_links_it": ".test_approve_dispatches_job_and_links_it()" | kind=code-symbol | source=manager/backend/tests/test_customer_access.py:L151 | neighbors=[TestApproveScanRequest, _added(), _mock_db(), _operator(), _pending_request()]
- "tests_test_cve_correlation_testingestparse": "TestIngestParse" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L233 | neighbors=[test_cve_correlation.py, .test_cvss_fallback(), .test_ingest_idempotent(), .test_ingest_one_cve(), .test_parse_criteria()]
- "tests_test_cve_correlation_testmirrorage": "TestMirrorAge" | kind=code-symbol | source=probe/tests/test_cve_correlation.py:L329 | neighbors=[test_cve_correlation.py, .test_fresh_has_no_warning(), .test_stale_warns(), .test_unknown_when_no_stamp(), .test_unparseable_stamp_is_graceful()]
- "tests_test_dangling_agent_pin_testpinsemantics": "TestPinSemantics" | kind=code-symbol | source=manager/backend/tests/test_dangling_agent_pin.py:L97 | neighbors=[test_dangling_agent_pin.py, Documents the rule the claim loop imple…, .test_dangling_pin_is_logged_not_silent…, .test_fallback_still_runs_the_eligibili…, .test_live_pin_is_a_hard_constraint()]
- "tests_test_db_mongodb_auth": "test_db_mongodb_auth.py" | kind=code-symbol | source=probe/tests/test_db_mongodb_auth.py:L1 | neighbors=[198bae4 snapshot: uncommitted system/ui…, db_scanner.py, TestAuthInterpretation, TestOpMsgFraming, test_db_mongodb_auth.py — MongoDB auth …]
- "tests_test_db_mongodb_auth_testopmsgframing": "TestOpMsgFraming" | kind=code-symbol | source=probe/tests/test_db_mongodb_auth.py:L24 | neighbors=[test_db_mongodb_auth.py, .test_bson_document_is_self_consistent(), .test_db_field_is_present(), .test_declared_length_matches_actual(), .test_opcode_is_op_msg_not_op_query()]
- "tests_test_db_mysql_greeting_testtlsposture": "TestTLSPosture" | kind=code-symbol | source=probe/tests/test_db_mysql_greeting.py:L46 | neighbors=[test_db_mysql_greeting.py, .test_client_ssl_absent_means_cleartext…, .test_client_ssl_advertised(), .test_protocol_9_has_no_capability_flag…, .test_short_packet_claims_nothing()]
- "tests_test_db_posture_rules_testcleartexttransport": "TestCleartextTransport" | kind=code-symbol | source=manager/detection_engine/tests/test_db_posture_rules.py:L92 | neighbors=[test_db_posture_rules.py, .test_auth_enforced_is_not_applied(), .test_fires_when_server_says_it_cannot_…, .test_silent_on_real_tls_capable_mysql(), .test_silent_when_the_probe_never_learn…]
- "tests_test_db_tds_prelogin_testpositiveevidenceonly": "TestPositiveEvidenceOnly" | kind=code-symbol | source=probe/tests/test_db_tds_prelogin.py:L76 | neighbors=[test_db_tds_prelogin.py, .test_garbage_does_not_raise(), .test_identification_survives_a_missing…, .test_truncated_table_claims_nothing_ex…, .test_unknown_encryption_value_is_not_i…]
- "tests_test_default_cred_rule_testcatalog": "TestCatalog" | kind=code-symbol | source=manager/detection_engine/tests/test_default_cred_rule.py:L25 | neighbors=[test_default_cred_rule.py, .test_known_vendor_has_defaults(), .test_lookup_is_case_and_whitespace_ins…, .test_none_and_empty_return_none(), .test_unknown_vendor_returns_none()]
- "tests_test_default_cred_rule_testrulefires": "TestRuleFires" | kind=code-symbol | source=manager/detection_engine/tests/test_default_cred_rule.py:L63 | neighbors=[test_default_cred_rule.py, .test_evidence_explains_what_was_not_te…, .test_known_vendor_with_basic_auth(), .test_known_vendor_with_login_form(), .test_vendor_falls_back_to_the_fact_whe…]
- "tests_test_default_cred_rule_testrulestayssilent": "TestRuleStaysSilent" | kind=code-symbol | source=manager/detection_engine/tests/test_default_cred_rule.py:L92 | neighbors=[test_default_cred_rule.py, .test_malformed_auth_surface_is_surviva…, .test_no_auth_surface_at_all(), .test_scheme_none_is_not_a_login_surfac…, .test_unknown_vendor_never_fires()]
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
- "tests_test_eol_detection_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_eol_detection.py:L61 | neighbors=[test_eol_detection.py, Same shape the other posture-rule tests…, .test_fires_on_past_eol_os(), .test_silent_on_supported_os(), .test_silent_without_os_release()]
- "tests_test_exploitability_testapplytofindings_test_declared_severity_is_never_rewritten": ".test_declared_severity_is_never_rewritten()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L119 | neighbors=[Severity is the rule's judgement of the…, TestApplyToFindings, _epss(), _finding(), _kev()]
- "tests_test_exploitability_testapplytofindings_test_idempotent_across_repeated_application": ".test_idempotent_across_repeated_application()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L162 | neighbors=[The pipeline may enrich the same findin…, TestApplyToFindings, _epss(), _finding(), _kev()]
- "tests_test_fact_contract_load_corpus": "_load_corpus()" | kind=code-symbol | source=manager/detection_engine/tests/test_fact_contract.py:L27 | neighbors=[test_fact_contract.py, _ingest_corpus(), test_corpus_is_present_and_nonempty(), test_every_rule_input_is_emitted_by_its…, test_report_unconsumed_evidence()]
- "tests_test_finding_enrichment_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_finding_enrichment.py:L32 | neighbors=[test_finding_enrichment.py, test_detail_enrichment_honours_content_…, test_detail_enrichment_populates_all_se…, test_detail_enrichment_scales_business_…, test_detail_enrichment_survives_missing…]
- "tests_test_finding_metrics_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_finding_metrics.py:L86 | neighbors=[test_finding_metrics.py, The REAL CurrentUser — a SimpleNamespac…, .test_aggregates_mttr_and_owners(), .test_shape_is_stable_when_empty(), .test_unassigned_is_a_first_class_bucke…]
- "tests_test_finding_section": "test_finding_section.py" | kind=code-symbol | source=probe/tests/test_finding_section.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, findings.py, TestFindingSection, TestScannerRegistry, test_finding_section.py — the scanner-m…]
- "tests_test_ftp_scanner_testftpfindings": "TestFTPFindings" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L53 | neighbors=[test_ftp_scanner.py, ._fact(), .test_anon_denied_is_silent(), .test_anon_login_only_is_medium(), .test_anon_read_is_high()]
- "tests_test_ftp_scanner_testftpscanner": "TestFTPScanner" | kind=code-symbol | source=probe/tests/test_ftp_scanner.py:L28 | neighbors=[test_ftp_scanner.py, ._sc(), .test_anon_login_and_read_open(), .test_ftp_present_anon_denied_open_but_…, .test_no_ftp_filtered()]
- "tests_test_host_discovery_udp_nbstat_reply": "_nbstat_reply()" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L24 | neighbors=[test_host_discovery_udp.py, Build a NetBIOS node-status response (R…, test_netbios_reply_proves_life_and_name…, .test_msbrowse_control_chars_dropped(), .test_names_hostname_domain_mac()]
- "tests_test_host_discovery_udp_responder": "_Responder" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L90 | neighbors=[test_host_discovery_udp.py, .connection_made(), .datagram_received(), .__init__(), _udp_server()]
- "tests_test_host_discovery_udp_testfusewithudp": "TestFuseWithUdp" | kind=code-symbol | source=probe/tests/test_host_discovery_udp.py:L59 | neighbors=[test_host_discovery_udp.py, .test_icmp_unreachable_alone(), .test_no_signals_unchanged(), .test_tcp_plus_udp_corroborate(), .test_udp_reply_alone_is_confirmed_aliv…]
- "tests_test_host_health_testsafetyproperty": "TestSafetyProperty" | kind=code-symbol | source=probe/tests/test_host_health.py:L130 | neighbors=[test_host_health.py, .test_healthy_host_produces_no_facts_at…, .test_offline_fact_marks_the_scan_incom…, .test_offline_host_stops_accumulating_o…, .test_one_offline_host_does_not_implica…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-069.json

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
