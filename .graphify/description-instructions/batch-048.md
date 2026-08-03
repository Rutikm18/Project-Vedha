# Node Description Batch 49 of 131

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

- "tests_test_ad_assessment_testldapenumeratorparsing_test_get_computers_flags_dc": ".test_get_computers_flags_dc()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L132 | neighbors=[TestLDAPEnumeratorParsing, _enum_with_entries(), _FakeEntry]
- "tests_test_ad_assessment_testldapenumeratorparsing_test_get_groups_marks_privileged": ".test_get_groups_marks_privileged()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L150 | neighbors=[TestLDAPEnumeratorParsing, _enum_with_entries(), _FakeEntry]
- "tests_test_ad_assessment_testldapenumeratorparsing_test_get_users_disabled_account": ".test_get_users_disabled_account()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L123 | neighbors=[TestLDAPEnumeratorParsing, _enum_with_entries(), _FakeEntry]
- "tests_test_ad_assessment_testldapenumeratorparsing_test_get_users_parses_uac_and_spn": ".test_get_users_parses_uac_and_spn()" | kind=code-symbol | source=manager/backend/tests/test_ad_assessment.py:L103 | neighbors=[TestLDAPEnumeratorParsing, _enum_with_entries(), _FakeEntry]
- "tests_test_agent_auth_boundary_boundary_test_client": "_boundary_test_client()" | kind=code-symbol | source=manager/backend/tests/test_agent_auth_boundary.py:L47 | neighbors=[test_agent_auth_boundary.py, test_agent_jwt_is_blocked_before_human_…, test_human_jwt_still_reaches_human_rout…]
- "tests_test_agents_testaccesstokenexpiry": "TestAccessTokenExpiry" | kind=code-symbol | source=manager/backend/tests/test_agents.py:L759 | neighbors=[test_agents.py, .test_custom_expiry_overrides_default(), ScanJobType]
- "tests_test_ai_engine_testllmreportgenerator_test_complete_retries_then_succeeds": ".test_complete_retries_then_succeeds()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L226 | neighbors=[TestLLMReportGenerator, _mock_db(), _resp()]
- "tests_test_ai_engine_testllmreportgenerator_test_detection_rule_explanation": ".test_detection_rule_explanation()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L243 | neighbors=[TestLLMReportGenerator, _mock_db(), _resp()]
- "tests_test_ai_engine_testllmreportgenerator_test_executive_summary_persists_pending": ".test_executive_summary_persists_pending()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L180 | neighbors=[TestLLMReportGenerator, _mock_db(), _resp()]
- "tests_test_ai_engine_testllmreportgenerator_test_unavailable_without_client": ".test_unavailable_without_client()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L217 | neighbors=[TestLLMReportGenerator, _finding(), _mock_db()]
- "tests_test_ai_engine_testvulnprioritizer_test_explain_prediction_fallback_shape": ".test_explain_prediction_fallback_shape()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L78 | neighbors=[TestVulnPrioritizer, _asset(), _finding()]
- "tests_test_ai_engine_testvulnprioritizer_test_extract_features_order_and_values": ".test_extract_features_order_and_values()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L55 | neighbors=[TestVulnPrioritizer, _asset(), _finding()]
- "tests_test_ai_engine_testvulnprioritizer_test_higher_cvss_scores_higher": ".test_higher_cvss_scores_higher()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L73 | neighbors=[TestVulnPrioritizer, _asset(), _finding()]
- "tests_test_ai_engine_testvulnprioritizer_test_predict_priority_uses_fallback_when_untrained": ".test_predict_priority_uses_fallback_when_untrained()" | kind=code-symbol | source=manager/backend/tests/test_ai_engine.py:L67 | neighbors=[TestVulnPrioritizer, _asset(), _finding()]
- "tests_test_auth_login_testauthenticatedisableduser_test_raises_disabled_user": ".test_raises_disabled_user()" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L111 | neighbors=[TestAuthenticateDisabledUser, _make_db(), _make_user()]
- "tests_test_auth_login_testauthenticateexpiredpassword": "TestAuthenticateExpiredPassword" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L135 | neighbors=[test_auth_login.py, .test_not_expired_when_future(), .test_raises_expired_password()]
- "tests_test_auth_login_testauthenticatesuccess": "TestAuthenticateSuccess" | kind=code-symbol | source=manager/backend/tests/test_auth_login.py:L193 | neighbors=[test_auth_login.py, .test_null_password_expires_at_never_ex…, .test_returns_user_on_valid_credentials…]
- "tests_test_db_scanner_testmysqlxvsoracle_test_mysqlx_identified": ".test_mysqlx_identified()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L54 | neighbors=[TestMysqlxVsOracle, _probe(), _xproto_frame()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_mysqlx_not_misread_as_oracle": ".test_mysqlx_not_misread_as_oracle()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L59 | neighbors=[TestMysqlxVsOracle, _probe(), _xproto_frame()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_oracle_reply_not_misread_as_mysqlx": ".test_oracle_reply_not_misread_as_mysqlx()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L70 | neighbors=[TestMysqlxVsOracle, _probe(), _tns_packet()]
- "tests_test_db_scanner_testmysqlxvsoracle_test_oracle_still_identified": ".test_oracle_still_identified()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L64 | neighbors=[TestMysqlxVsOracle, _probe(), _tns_packet()]
- "tests_test_db_scanner_tns_packet": "_tns_packet()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L44 | neighbors=[test_db_scanner.py, .test_oracle_reply_not_misread_as_mysql…, .test_oracle_still_identified()]
- "tests_test_db_scanner_xproto_frame": "_xproto_frame()" | kind=code-symbol | source=probe/tests/test_db_scanner.py:L39 | neighbors=[test_db_scanner.py, .test_mysqlx_identified(), .test_mysqlx_not_misread_as_oracle()]
- "tests_test_detection_core_testmatchcandidate_test_ai_assisted_carried_through": ".test_ai_assisted_carried_through()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L463 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_authoritative_source_confirms": ".test_authoritative_source_confirms()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L420 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_inferred_match_has_backport_note": ".test_inferred_match_has_backport_note()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L435 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_match_produces_finding": ".test_match_produces_finding()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L404 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_no_match_returns_empty": ".test_no_match_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L449 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_no_version_returns_empty": ".test_no_version_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L392 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testmatchcandidate_test_unknown_product_returns_empty": ".test_unknown_product_returns_empty()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L399 | neighbors=[TestMatchCandidate, _candidate(), _mock_vuln_db()]
- "tests_test_detection_core_testsuppressnegated_test_keeps_inferred_when_auth_version_lower": ".test_keeps_inferred_when_auth_version_lower()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L541 | neighbors=[TestSuppressNegated, _candidate(), _finding()]
- "tests_test_detection_core_testsuppressnegated_test_suppresses_inferred_when_authoritative_contradicts": ".test_suppresses_inferred_when_authoritative_contradicts()" | kind=code-symbol | source=manager/detection_engine/tests/test_detection_core.py:L517 | neighbors=[TestSuppressNegated, _candidate(), _finding()]
- "tests_test_engagement_lists_scalars": "_scalars()" | kind=code-symbol | source=manager/backend/tests/test_engagement_lists.py:L17 | neighbors=[test_engagement_lists.py, test_list_assets_groups_services(), test_list_jobs_returns_results()]
- "tests_test_engagement_lists_test_list_assets_groups_services": "test_list_assets_groups_services()" | kind=code-symbol | source=manager/backend/tests/test_engagement_lists.py:L39 | neighbors=[test_engagement_lists.py, _scalars(), _user()]
- "tests_test_engagement_lists_test_list_jobs_returns_results": "test_list_jobs_returns_results()" | kind=code-symbol | source=manager/backend/tests/test_engagement_lists.py:L22 | neighbors=[test_engagement_lists.py, _scalars(), _user()]
- "tests_test_engagement_lists_user": "_user()" | kind=code-symbol | source=manager/backend/tests/test_engagement_lists.py:L13 | neighbors=[test_engagement_lists.py, test_list_assets_groups_services(), test_list_jobs_returns_results()]
- "tests_test_exploit_engine_testexploitorchestrator_test_select_exploit_by_cve": ".test_select_exploit_by_cve()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L256 | neighbors=[TestExploitOrchestrator, _finding(), ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_select_exploit_fallback_no_cve": ".test_select_exploit_fallback_no_cve()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L269 | neighbors=[TestExploitOrchestrator, _finding(), ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_select_exploit_log4shell": ".test_select_exploit_log4shell()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L263 | neighbors=[TestExploitOrchestrator, _finding(), ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_validate_scope_out_of_range": ".test_validate_scope_out_of_range()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L284 | neighbors=[TestExploitOrchestrator, _engagement(), ._make_orchestrator()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-048.json

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
