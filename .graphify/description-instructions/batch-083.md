# Node Description Batch 84 of 336

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

- "tests_test_portal_read_added": "_added()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L173 | neighbors=[test_portal_read.py, .test_creates_pending_request_with_targ…, .test_whole_scope_when_no_targets(), .test_creates_pending_request_and_audit…]
- "tests_test_portal_read_finding_with_internal": "_finding_with_internal()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L58 | neighbors=[test_portal_read.py, A finding-like ORM object carrying BOTH…, .test_serialization_drops_internal_fiel…, .test_findings_scoped_and_serialized()]
- "tests_test_portal_read_testcreatescanrequest_test_creates_pending_request_and_audits": ".test_creates_pending_request_and_audits()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L181 | neighbors=[TestCreateScanRequest, _added(), _client(), _db_first()]
- "tests_test_portal_read_testcreatescanrequest_test_excluded_target_is_422": ".test_excluded_target_is_422()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L284 | neighbors=[TestCreateScanRequest, _client(), _db_for_create(), _engagement()]
- "tests_test_portal_read_testcreatescanrequest_test_out_of_scope_target_is_422": ".test_out_of_scope_target_is_422()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L275 | neighbors=[TestCreateScanRequest, _client(), _db_for_create(), _engagement()]
- "tests_test_portal_read_testcreatescanrequest_test_queue_cap_is_conflict": ".test_queue_cap_is_conflict()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L294 | neighbors=[TestCreateScanRequest, _client(), _db_for_create(), _engagement()]
- "tests_test_portal_read_testcreatescanrequest_test_unknown_scan_type_is_422": ".test_unknown_scan_type_is_422()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L267 | neighbors=[TestCreateScanRequest, _client(), _db_for_create(), _engagement()]
- "tests_test_portal_read_testportalfindings": "TestPortalFindings" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L97 | neighbors=[test_portal_read.py, .test_findings_scoped_and_serialized(), .test_operator_is_forbidden(), .test_single_finding_404_when_out_of_sc…]
- "tests_test_portal_read_testportalfindings_test_findings_scoped_and_serialized": ".test_findings_scoped_and_serialized()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L98 | neighbors=[TestPortalFindings, _client(), _db_list(), _finding_with_internal()]
- "tests_test_portal_read_testportalreports": "TestPortalReports" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L114 | neighbors=[test_portal_read.py, .test_download_returns_content_for_appr…, .test_lists_approved_reports(), .test_unapproved_or_missing_report_is_4…]
- "tests_test_portal_read_testtrends_test_returns_severity_and_timeline": ".test_returns_severity_and_timeline()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L209 | neighbors=[TestTrends, _client(), _db_list(), _finding()]
- "tests_test_portal_remediation_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_portal_remediation.py:L27 | neighbors=[test_portal_remediation.py, .test_serves_kb_when_no_stored_plan(), .test_serves_reviewed_ai_plan_stripping…, .test_unreviewed_ai_plan_does_not_leak()]
- "tests_test_portal_remediation_testportalremediation_test_serves_kb_when_no_stored_plan": ".test_serves_kb_when_no_stored_plan()" | kind=code-symbol | source=manager/backend/tests/test_portal_remediation.py:L45 | neighbors=[TestPortalRemediation, _client(), _db_scalar(), _finding()]
- "tests_test_portal_remediation_testportalremediation_test_serves_reviewed_ai_plan_stripping_operator_metadata": ".test_serves_reviewed_ai_plan_stripping_operator_metadata()" | kind=code-symbol | source=manager/backend/tests/test_portal_remediation.py:L53 | neighbors=[TestPortalRemediation, _client(), _db_scalar(), _finding()]
- "tests_test_portal_remediation_testportalremediation_test_unreviewed_ai_plan_does_not_leak": ".test_unreviewed_ai_plan_does_not_leak()" | kind=code-symbol | source=manager/backend/tests/test_portal_remediation.py:L64 | neighbors=[TestPortalRemediation, _client(), _db_scalar(), _finding()]
- "tests_test_portal_scope_testassertclient": "TestAssertClient" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L41 | neighbors=[test_portal_scope.py, .test_bound_client_returns_engagement(), .test_client_without_engagement_is_forb…, .test_operator_is_forbidden()]
- "tests_test_portal_scope_testportaltokenclaims": "TestPortalTokenClaims" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L88 | neighbors=[test_portal_scope.py, .test_client_role_enum_exists(), .test_client_token_carries_portal_aud_a…, .test_operator_and_portal_audiences_dif…]
- "tests_test_portal_scope_testrefreshpreservesaudienceandscope_db_returning": "._db_returning()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L152 | neighbors=[TestRefreshPreservesAudienceAndScope, .test_client_refresh_keeps_portal_aud_a…, .test_operator_refresh_keeps_manager_au…, .test_unbound_client_cannot_refresh_int…]
- "tests_test_portal_scope_testresolvescope": "TestResolveScope" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L59 | neighbors=[test_portal_scope.py, .test_matching_request_ok(), .test_mismatched_request_is_403_idor_de…, .test_no_request_returns_bound()]
- "tests_test_posture_confidence_by_rule": "_by_rule()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L33 | neighbors=[test_posture_confidence.py, .test_corroborated_host_gets_floored_co…, .test_filtered_port_lowers_confidence(), .test_lone_finding_keeps_base_confidenc…]
- "tests_test_posture_confidence_testendtoend_test_corroborated_host_gets_floored_confidence_and_factors": ".test_corroborated_host_gets_floored_confidence_and_factors()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L94 | neighbors=[TestEndToEnd, _asset(), _by_rule(), _fact()]
- "tests_test_posture_confidence_testendtoend_test_filtered_port_lowers_confidence": ".test_filtered_port_lowers_confidence()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L114 | neighbors=[TestEndToEnd, _asset(), _by_rule(), _fact()]
- "tests_test_posture_confidence_testendtoend_test_lone_finding_keeps_base_confidence": ".test_lone_finding_keeps_base_confidence()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L107 | neighbors=[TestEndToEnd, _asset(), _by_rule(), _fact()]
- "tests_test_posture_fv": "_fv()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L12 | neighbors=[test_posture.py, test_build_posture_buckets_resolved_new…, test_build_posture_single_run_has_no_pr…, test_compute_scores_uses_risk_epss_expl…]
- "tests_test_posture_row": "_Row" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L109 | neighbors=[test_posture.py, .__init__(), test_finding_views_handles_null_asset_a…, test_finding_views_maps_columns_and_ass…]
- "tests_test_posture_rules_testinvariants": "TestInvariants" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L154 | neighbors=[test_posture_rules.py, .test_dedup_same_rule_same_port(), .test_detect_all_sorts_by_risk_desc(), .test_deterministic_id_across_runs()]
- "tests_test_posture_rules_testtrusttier": "TestTrustTier" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L30 | neighbors=[test_posture_rules.py, .test_registry_contains_user_validated_…, .test_unvalidated_scanner_only_suspects…, .test_validated_scanner_confirms()]
- "tests_test_posture_rules_testvulnerablehost_test_deprecated_tls_version_underscore_labels": ".test_deprecated_tls_version_underscore_labels()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L95 | neighbors=[The live tls_scanner labels its probe l…, TestVulnerableHost, _asset(), _fact()]
- "tests_test_posture_trace_testabsentversusclean_test_key_absent_is_missing_input_not_clean": ".test_key_absent_is_missing_input_not_clean()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L50 | neighbors=[TestAbsentVersusClean, _asset(), _fact(), _outcome()]
- "tests_test_posture_trace_testabsentversusclean_test_key_present_false_is_clean_no_match": ".test_key_present_false_is_clean_no_match()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L44 | neighbors=[TestAbsentVersusClean, _asset(), _fact(), _outcome()]
- "tests_test_posture_trace_testabsentversusclean_test_key_present_true_is_match": ".test_key_present_true_is_match()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L39 | neighbors=[TestAbsentVersusClean, _asset(), _fact(), _outcome()]
- "tests_test_posture_trace_testbehaviourpreserved": "TestBehaviourPreserved" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L110 | neighbors=[test_posture_trace.py, ._mixed(), .test_dedup_still_one_finding_per_rule_…, .test_detect_posture_matches_traced_fin…]
- "tests_test_posture_trace_testbehaviourpreserved_mixed": "._mixed()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L111 | neighbors=[TestBehaviourPreserved, _asset(), _fact(), .test_detect_posture_matches_traced_fin…]
- "tests_test_posture_trace_testnoevidence_test_scanner_absent_yields_no_evidence": ".test_scanner_absent_yields_no_evidence()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L78 | neighbors=[TestNoEvidence, _asset(), _fact(), _outcome()]
- "tests_test_posture_trace_testruleisolation_test_raising_rule_is_error_and_others_still_fire": ".test_raising_rule_is_error_and_others_still_fire()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L96 | neighbors=[TestRuleIsolation, _asset(), _fact(), _outcome()]
- "tests_test_printer_scanner_testprinterscanner": "TestPrinterScanner" | kind=code-symbol | source=probe/tests/test_printer_scanner.py:L34 | neighbors=[test_printer_scanner.py, ._sc(), .test_no_printer_filtered(), .test_open()]
- "tests_test_printer_scanner_testpurelogic": "TestPureLogic" | kind=code-symbol | source=probe/tests/test_printer_scanner.py:L18 | neighbors=[test_printer_scanner.py, .test_build_ipp(), .test_parse_ipp_make_model(), .test_parse_pjl_id()]
- "tests_test_probe_core_testassetneedsrechecklive": "TestAssetNeedsRecheckLive" | kind=code-symbol | source=probe/tests/test_probe_core.py:L475 | neighbors=[test_probe_core.py, .test_never_seen(), .test_recently_seen(), .test_stale()]
- "tests_test_probe_core_testgate0": "TestGate0" | kind=code-symbol | source=probe/tests/test_probe_core.py:L265 | neighbors=[test_probe_core.py, .test_iot_not_passive(), .test_it_not_passive(), .test_ot_is_passive()]
- "tests_test_probe_core_testgate3": "TestGate3" | kind=code-symbol | source=probe/tests/test_probe_core.py:L294 | neighbors=[test_probe_core.py, .test_not_alive(), .test_ot_always_false(), .test_requires_alive()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-083.json

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
