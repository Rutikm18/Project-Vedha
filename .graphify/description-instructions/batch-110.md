# Node Description Batch 111 of 330

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

- "tests_test_db_scanner_testmysqlxvsoracle_test_mysqlx_identified": ".test_mysqlx_identified()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L54 | neighbors=[TestMysqlxVsOracle, _probe(), _xproto_frame()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_mysqlx_not_misread_as_oracle": ".test_mysqlx_not_misread_as_oracle()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L59 | neighbors=[TestMysqlxVsOracle, _probe(), _xproto_frame()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_oracle_reply_not_misread_as_mysqlx": ".test_oracle_reply_not_misread_as_mysqlx()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L70 | neighbors=[TestMysqlxVsOracle, _probe(), _tns_packet()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_oracle_still_identified": ".test_oracle_still_identified()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L64 | neighbors=[TestMysqlxVsOracle, _probe(), _tns_packet()]
- "tests_test_db_scanner_tns_packet": "_tns_packet()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L44 | neighbors=[test_db_scanner.py, .test_oracle_reply_not_misread_as_mysql…, .test_oracle_still_identified()]
- "tests_test_db_scanner_xproto_frame": "_xproto_frame()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L39 | neighbors=[test_db_scanner.py, .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle()]
- "tests_test_detection_core_testmatchcandidate_test_ai_assisted_carried_through": ".test_ai_assisted_carried_through()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L505 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_authoritative_source_confirms": ".test_authoritative_source_confirms()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L462 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_inferred_match_has_backport_note": ".test_inferred_match_has_backport_note()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L477 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_match_produces_finding": ".test_match_produces_finding()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L446 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_no_match_returns_empty": ".test_no_match_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L491 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_no_version_returns_empty": ".test_no_version_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L434 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_unknown_product_returns_empty": ".test_unknown_product_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L441 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testsuppressnegated_test_keeps_inferred_when_auth_version_lower": ".test_keeps_inferred_when_auth_version_lower()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L610 | neighbors=[TestSuppressNegated, _candidate(), _finding()]
- "tests_test_detection_core_testsuppressnegated_test_suppresses_inferred_when_authoritative_contradicts": ".test_suppresses_inferred_when_authoritative_contradicts()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L559 | neighbors=[TestSuppressNegated, _candidate(), _finding()]
- "tests_test_detection_core_testsuppressnegated_test_suppression_produces_an_evidence_preserving_audit_record": ".test_suppression_produces_an_evidence_preserving_audit_record()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L569 | neighbors=[TestSuppressNegated, _candidate(), _finding()]
- "tests_test_detection_coverage_test_explain_all_rules_sorts_gaps_first": "test_explain_all_rules_sorts_gaps_first()" | kind=code-symbol | source=manager/backend/tests/test_detection_coverage.py:L126 | neighbors=[test_detection_coverage.py, _run(), _user()]
- "tests_test_detection_coverage_test_explain_single_rule_reports_schema_drift": "test_explain_single_rule_reports_schema_drift()" | kind=code-symbol | source=manager/backend/tests/test_detection_coverage.py:L110 | neighbors=[test_detection_coverage.py, _run(), _user()]
- "tests_test_detection_pipeline_gaps_test_a_non_dict_data_payload_is_quarantined_not_fatal": "test_a_non_dict_data_payload_is_quarantined_not_fatal()" | kind=code-symbol | source=manager/backend/tests/test_detection_pipeline_gaps.py:L45 | neighbors=[test_detection_pipeline_gaps.py, `data` is read with .get() by every rul…, _fact()]
- "tests_test_detection_pipeline_gaps_test_accepted_facts_excludes_what_ingest_rejected": "test_accepted_facts_excludes_what_ingest_rejected()" | kind=code-symbol | source=manager/backend/tests/test_detection_pipeline_gaps.py:L64 | neighbors=[test_detection_pipeline_gaps.py, attack_path_findings runs on meta['acce…, _fact()]
- "tests_test_detection_pipeline_gaps_test_accepted_facts_falls_back_to_raw_when_there_is_no_verdict": "test_accepted_facts_falls_back_to_raw_when_there_is_no_verdict()" | kind=code-symbol | source=manager/backend/tests/test_detection_pipeline_gaps.py:L84 | neighbors=[test_detection_pipeline_gaps.py, No engine means no ingest verdict. With…, _fact()]
- "tests_test_dns_scanner_testaxfrbounded": "TestAxfrBounded" | kind=code-symbol | source=probe/tests/test_dns_scanner.py:L49 | neighbors=[test_dns_scanner.py, .test_axfr_refused_reports_not_transfer…, .test_axfr_stops_at_cap()]
- "tests_test_dualstack_fallback_testresolveipcandidates": "TestResolveIpCandidates" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L31 | neighbors=[test_dualstack_fallback.py, .test_returns_ips_in_order(), .test_unresolvable_returns_empty_not_ra…]
- "tests_test_dualstack_fallback_testsmbnegotiatefallback_fake_socket": "._fake_socket()" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L51 | neighbors=[A socket whose connect() fails for `dea…, TestSmbNegotiateFallback, .test_falls_back_to_ipv4_when_ipv6_is_b…]
- "tests_test_dualstack_fallback_testsmbnegotiatefallback_patch_candidates": "._patch_candidates()" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L47 | neighbors=[TestSmbNegotiateFallback, .test_falls_back_to_ipv4_when_ipv6_is_b…, .test_returns_none_only_when_every_fami…]
- "tests_test_dualstack_fallback_testsmbnegotiatefallback_test_falls_back_to_ipv4_when_ipv6_is_blackholed": ".test_falls_back_to_ipv4_when_ipv6_is_blackholed()" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L70 | neighbors=[TestSmbNegotiateFallback, ._fake_socket(), ._patch_candidates()]
- "tests_test_dualstack_fallback_testsmbntlmfallback": "TestSmbNtlmFallback" | kind=code-symbol | source=probe/tests/test_dualstack_fallback.py:L96 | neighbors=[test_dualstack_fallback.py, .test_empty_when_no_address_answers(), .test_first_answering_address_wins()]
- "tests_test_e2e_engagement_to_findings_test_real_scan_of_open_datastore_yields_manager_finding": "test_real_scan_of_open_datastore_yields_manager_finding()" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L109 | neighbors=[test_e2e_engagement_to_findings.py, _manager(), _plant()]
- "tests_test_engagement_lists_scalars": "_scalars()" | kind=code-symbol | source=manager/backend/tests/test_engagement_lists.py:L17 | neighbors=[test_engagement_lists.py, test_list_assets_groups_services(), test_list_jobs_returns_results()]
- "tests_test_engagement_lists_test_list_assets_groups_services": "test_list_assets_groups_services()" | kind=code-symbol | source=manager/backend/tests/test_engagement_lists.py:L39 | neighbors=[test_engagement_lists.py, _scalars(), _user()]
- "tests_test_engagement_lists_test_list_jobs_returns_results": "test_list_jobs_returns_results()" | kind=code-symbol | source=manager/backend/tests/test_engagement_lists.py:L22 | neighbors=[test_engagement_lists.py, _scalars(), _user()]
- "tests_test_engagement_lists_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_engagement_lists.py:L13 | neighbors=[test_engagement_lists.py, test_list_assets_groups_services(), test_list_jobs_returns_results()]
- "tests_test_exploit_engine_testexploitorchestrator_test_select_exploit_by_cve": ".test_select_exploit_by_cve()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L256 | neighbors=[TestExploitOrchestrator, _finding(), ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_select_exploit_fallback_no_cve": ".test_select_exploit_fallback_no_cve()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L269 | neighbors=[TestExploitOrchestrator, _finding(), ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_select_exploit_log4shell": ".test_select_exploit_log4shell()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L263 | neighbors=[TestExploitOrchestrator, _finding(), ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_validate_scope_out_of_range": ".test_validate_scope_out_of_range()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L284 | neighbors=[TestExploitOrchestrator, _engagement(), ._make_orchestrator()]
- "tests_test_exploitability_testneverclaimsthecveispresent_test_refs_carry_the_relation_and_kev_status": ".test_refs_carry_the_relation_and_kev_status()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L54 | neighbors=[TestNeverClaimsTheCveIsPresent, _epss(), _kev()]
- "tests_test_exploitability_testtiers_test_elevated_epss_band": ".test_elevated_epss_band()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L84 | neighbors=[TestTiers, _epss(), _kev()]
- "tests_test_exploitability_testtiers_test_epss_max_takes_the_worst_linked_cve": ".test_epss_max_takes_the_worst_linked_cve()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L102 | neighbors=[TestTiers, _epss(), _kev()]
- "tests_test_exploitability_testtiers_test_high_epss_without_kev_is_likely": ".test_high_epss_without_kev_is_likely()" | kind=code-symbol | source=manager/detection_engine/tests/test_exploitability.py:L79 | neighbors=[TestTiers, _epss(), _kev()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-110.json

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
