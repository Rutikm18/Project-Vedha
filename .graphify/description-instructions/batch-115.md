# Node Description Batch 116 of 336

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

- "tests_test_portal_read_operator": "_operator()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L31 | neighbors=[test_portal_read.py, .test_operator_cannot_create(), .test_operator_is_forbidden()]
- "tests_test_portal_read_testclientfindingwhitelist": "TestClientFindingWhitelist" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L82 | neighbors=[test_portal_read.py, .test_schema_is_a_whitelist(), .test_serialization_drops_internal_fiel…]
- "tests_test_portal_read_testcreatescanrequest_test_duplicate_pending_is_conflict": ".test_duplicate_pending_is_conflict()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L190 | neighbors=[TestCreateScanRequest, _client(), _db_first()]
- "tests_test_portal_read_testcreatescanrequest_test_operator_cannot_create": ".test_operator_cannot_create()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L303 | neighbors=[TestCreateScanRequest, _operator(), _db_first()]
- "tests_test_portal_read_testportalfindings_test_operator_is_forbidden": ".test_operator_is_forbidden()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L103 | neighbors=[TestPortalFindings, _db_list(), _operator()]
- "tests_test_portal_read_testportalfindings_test_single_finding_404_when_out_of_scope": ".test_single_finding_404_when_out_of_scope()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L108 | neighbors=[TestPortalFindings, _client(), _db_scalar()]
- "tests_test_portal_read_testportalpostureandengagement": "TestPortalPostureAndEngagement" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L133 | neighbors=[test_portal_read.py, .test_engagement_summary(), .test_posture_scores_open_findings()]
- "tests_test_portal_read_testportalpostureandengagement_test_engagement_summary": ".test_engagement_summary()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L143 | neighbors=[TestPortalPostureAndEngagement, _client(), _db_scalar()]
- "tests_test_portal_read_testportalpostureandengagement_test_posture_scores_open_findings": ".test_posture_scores_open_findings()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L134 | neighbors=[TestPortalPostureAndEngagement, _client(), _db_list()]
- "tests_test_portal_read_testportalreports_test_download_returns_content_for_approved": ".test_download_returns_content_for_approved()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L126 | neighbors=[TestPortalReports, _client(), _db_scalar()]
- "tests_test_portal_read_testportalreports_test_lists_approved_reports": ".test_lists_approved_reports()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L120 | neighbors=[TestPortalReports, _client(), _db_list()]
- "tests_test_portal_read_testportalreports_test_unapproved_or_missing_report_is_404": ".test_unapproved_or_missing_report_is_404()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L115 | neighbors=[TestPortalReports, _client(), _db_scalar()]
- "tests_test_portal_read_testsummary_test_aggregates_posture_counts_and_queue": ".test_aggregates_posture_counts_and_queue()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L190 | neighbors=[TestSummary, _client(), _finding()]
- "tests_test_portal_remediation_testportalremediation_test_missing_or_out_of_scope_finding_is_404": ".test_missing_or_out_of_scope_finding_is_404()" | kind=code-symbol | source=manager/backend/tests/test_portal_remediation.py:L75 | neighbors=[TestPortalRemediation, _client(), _db_scalar()]
- "tests_test_portal_scope_operator": "_operator()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L37 | neighbors=[test_portal_scope.py, .test_operator_is_forbidden(), .test_operator_cannot_scope()]
- "tests_test_portal_scope_testclientscoped": "TestClientScoped" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L74 | neighbors=[test_portal_scope.py, .test_applies_engagement_filter_for_bou…, .test_operator_cannot_scope()]
- "tests_test_portal_scope_testrefreshpreservesaudienceandscope_test_unbound_client_cannot_refresh_into_an_unscoped_token": ".test_unbound_client_cannot_refresh_into_an_unscoped_token()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L186 | neighbors=[Same rule as login: never mint an unsco…, TestRefreshPreservesAudienceAndScope, ._db_returning()]
- "tests_test_posture_confidence_testchains": "TestChains" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L73 | neighbors=[test_posture_confidence.py, .test_chain_floor_never_lowers_confiden…, .test_ntlm_relay_chain_floors_both()]
- "tests_test_posture_confidence_testendtoend_test_confidence_is_serialized": ".test_confidence_is_serialized()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L121 | neighbors=[TestEndToEnd, _asset(), _fact()]
- "tests_test_posture_rules_testinvariants_test_dedup_same_rule_same_port": ".test_dedup_same_rule_same_port()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L161 | neighbors=[TestInvariants, _asset(), _fact()]
- "tests_test_posture_rules_testinvariants_test_detect_all_sorts_by_risk_desc": ".test_detect_all_sorts_by_risk_desc()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L167 | neighbors=[TestInvariants, _asset(), _fact()]
- "tests_test_posture_rules_testinvariants_test_deterministic_id_across_runs": ".test_deterministic_id_across_runs()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L155 | neighbors=[TestInvariants, _asset(), _fact()]
- "tests_test_posture_rules_testtrusttier_test_unvalidated_scanner_only_suspects": ".test_unvalidated_scanner_only_suspects()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L37 | neighbors=[TestTrustTier, _asset(), _fact()]
- "tests_test_posture_rules_testtrusttier_test_validated_scanner_confirms": ".test_validated_scanner_confirms()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L31 | neighbors=[TestTrustTier, _asset(), _fact()]
- "tests_test_posture_rules_testudphonesty": "TestUdpHonesty" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L120 | neighbors=[test_posture_rules.py, .test_amplifier_fires_only_when_it_answ…, .test_no_reply_udp_raises_nothing()]
- "tests_test_posture_rules_testudphonesty_test_amplifier_fires_only_when_it_answered": ".test_amplifier_fires_only_when_it_answered()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L121 | neighbors=[TestUdpHonesty, _asset(), _fact()]
- "tests_test_posture_rules_testudphonesty_test_no_reply_udp_raises_nothing": ".test_no_reply_udp_raises_nothing()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L125 | neighbors=[TestUdpHonesty, _asset(), _fact()]
- "tests_test_posture_rules_testvulnerablehost_test_deprecated_tls_version": ".test_deprecated_tls_version()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L90 | neighbors=[TestVulnerableHost, _asset(), _fact()]
- "tests_test_posture_rules_testvulnerablehost_test_modern_only_tls_raises_nothing": ".test_modern_only_tls_raises_nothing()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L106 | neighbors=[TestVulnerableHost, _asset(), _fact()]
- "tests_test_posture_rules_testvulnerablehost_test_rdp_no_nla_confirmed_high_and_unauth": ".test_rdp_no_nla_confirmed_high_and_unauth()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L82 | neighbors=[TestVulnerableHost, _asset(), _fact()]
- "tests_test_posture_rules_testvulnerablehost_test_self_signed_and_expired_cert": ".test_self_signed_and_expired_cert()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L112 | neighbors=[TestVulnerableHost, _asset(), _fact()]
- "tests_test_posture_rules_testvulnerablehost_test_smbv1_is_confirmed_critical": ".test_smbv1_is_confirmed_critical()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L76 | neighbors=[TestVulnerableHost, _asset(), _fact()]
- "tests_test_posture_trace_testbehaviourpreserved_test_dedup_still_one_finding_per_rule_port_but_trace_per_eval": ".test_dedup_still_one_finding_per_rule_port_but_trace_per_eval()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L129 | neighbors=[TestBehaviourPreserved, _asset(), _fact()]
- "tests_test_posture_trace_testnoevidence": "TestNoEvidence" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L77 | neighbors=[test_posture_trace.py, .test_no_evidence_is_asset_scoped_not_p…, .test_scanner_absent_yields_no_evidence…]
- "tests_test_posture_trace_testnoevidence_test_no_evidence_is_asset_scoped_not_per_fact": ".test_no_evidence_is_asset_scoped_not_per_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L84 | neighbors=[TestNoEvidence, _asset(), _fact()]
- "tests_test_posture_trace_testsummarize": "TestSummarize" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L141 | neighbors=[test_posture_trace.py, .test_every_verdict_is_reachable(), .test_summarize_counts_blind_rules()]
- "tests_test_posture_trace_testsummarize_test_every_verdict_is_reachable": ".test_every_verdict_is_reachable()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L153 | neighbors=[TestSummarize, _asset(), _fact()]
- "tests_test_posture_trace_testsummarize_test_summarize_counts_blind_rules": ".test_summarize_counts_blind_rules()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L142 | neighbors=[TestSummarize, _asset(), _fact()]
- "tests_test_printer_scanner_testprinterscanner_sc": "._sc()" | kind=code-symbol | source=probe/tests/test_printer_scanner.py:L35 | neighbors=[TestPrinterScanner, .test_no_printer_filtered(), .test_open()]
- "tests_test_probe_core_testassetmergecredentialed": "TestAssetMergeCredentialed" | kind=code-symbol | source=probe/tests/test_probe_core.py:L568 | neighbors=[test_probe_core.py, .test_ssh_inventory(), .test_windows_inventory()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-115.json

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
