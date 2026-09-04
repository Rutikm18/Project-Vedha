# Node Description Batch 159 of 332

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

- "tests_test_pipeline_concurrency_test_the_same_engagement_always_maps_to_the_same_key": "test_the_same_engagement_always_maps_to_the_same_key()" | kind=code-symbol | source=manager/backend/tests/test_pipeline_concurrency.py:L57 | neighbors=[test_pipeline_concurrency.py, Two concurrent handlers must contend, s…]
- "tests_test_pipeline_empty_jsonl": "_empty_jsonl()" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L119 | neighbors=[test_pipeline.py, .test_empty_jsonl_returns_no_findings()]
- "tests_test_pipeline_testrunpipelinereturnvalue": "TestRunPipelineReturnValue" | kind=code-symbol | source=manager/detection_engine/tests/test_pipeline.py:L306 | neighbors=[test_pipeline.py, .test_returns_tuple_of_findings_and_ing…]
- "tests_test_portal_assistant_test_a_non_client_user_is_refused": "test_a_non_client_user_is_refused()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L158 | neighbors=[test_portal_assistant.py, _ask()]
- "tests_test_portal_assistant_test_request_body_cannot_carry_context": "test_request_body_cannot_carry_context()" | kind=code-symbol | source=manager/backend/tests/test_portal_assistant.py:L113 | neighbors=[test_portal_assistant.py, The schema has no context field, so a c…]
- "tests_test_portal_metrics_testopenclosed": "TestOpenClosed" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L34 | neighbors=[test_portal_metrics.py, .test_counts_by_status_and_resolved_at()]
- "tests_test_portal_metrics_testopenclosed_test_counts_by_status_and_resolved_at": ".test_counts_by_status_and_resolved_at()" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L35 | neighbors=[TestOpenClosed, _f()]
- "tests_test_portal_metrics_testseveritybreakdown_test_open_only_excludes_closed": ".test_open_only_excludes_closed()" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L24 | neighbors=[TestSeverityBreakdown, _f()]
- "tests_test_portal_metrics_testseveritybreakdown_test_unknown_severity_falls_into_info": ".test_unknown_severity_falls_into_info()" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L30 | neighbors=[TestSeverityBreakdown, _f()]
- "tests_test_portal_metrics_teststatustimeline_test_activity_outside_window_is_ignored": ".test_activity_outside_window_is_ignored()" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L60 | neighbors=[TestStatusTimeline, _f()]
- "tests_test_portal_metrics_teststatustimeline_test_buckets_opened_and_closed": ".test_buckets_opened_and_closed()" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L49 | neighbors=[TestStatusTimeline, _f()]
- "tests_test_portal_read_testclientfindingwhitelist_test_serialization_drops_internal_fields": ".test_serialization_drops_internal_fields()" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L89 | neighbors=[TestClientFindingWhitelist, _finding_with_internal()]
- "tests_test_portal_read_testsummary": "TestSummary" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L189 | neighbors=[test_portal_read.py, .test_aggregates_posture_counts_and_que…]
- "tests_test_portal_read_testtrends": "TestTrends" | kind=code-symbol | source=manager/backend/tests/test_portal_read.py:L208 | neighbors=[test_portal_read.py, .test_returns_severity_and_timeline()]
- "tests_test_portal_scope_testassertclient_test_bound_client_returns_engagement": ".test_bound_client_returns_engagement()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L38 | neighbors=[TestAssertClient, _client()]
- "tests_test_portal_scope_testassertclient_test_operator_is_forbidden": ".test_operator_is_forbidden()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L42 | neighbors=[TestAssertClient, _operator()]
- "tests_test_portal_scope_testclientscoped_test_applies_engagement_filter_for_bound_id": ".test_applies_engagement_filter_for_bound_id()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L71 | neighbors=[TestClientScoped, _client()]
- "tests_test_portal_scope_testclientscoped_test_operator_cannot_scope": ".test_operator_cannot_scope()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L79 | neighbors=[TestClientScoped, _operator()]
- "tests_test_portal_scope_testresolvescope_test_matching_request_ok": ".test_matching_request_ok()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L60 | neighbors=[TestResolveScope, _client()]
- "tests_test_portal_scope_testresolvescope_test_mismatched_request_is_403_idor_defense": ".test_mismatched_request_is_403_idor_defense()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L64 | neighbors=[TestResolveScope, _client()]
- "tests_test_portal_scope_testresolvescope_test_no_request_returns_bound": ".test_no_request_returns_bound()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L56 | neighbors=[TestResolveScope, _client()]
- "tests_test_posture_rules_testhardenedgroundtruth_test_hardened_smb_and_rdp_raise_no_misconfig": ".test_hardened_smb_and_rdp_raise_no_misconfig()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L67 | neighbors=[TestHardenedGroundTruth, ._host()]
- "tests_test_posture_rules_testhardenedgroundtruth_test_no_critical_or_high_findings": ".test_no_critical_or_high_findings()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L59 | neighbors=[TestHardenedGroundTruth, ._host()]
- "tests_test_posture_rules_testhardenedgroundtruth_test_rdp_exposed_is_low_because_nla_required": ".test_rdp_exposed_is_low_because_nla_required()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L63 | neighbors=[TestHardenedGroundTruth, ._host()]
- "tests_test_posture_test_build_posture_buckets_resolved_new_persisting": "test_build_posture_buckets_resolved_new_persisting()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L89 | neighbors=[test_posture.py, _fv()]
- "tests_test_posture_test_build_posture_single_run_has_no_prev": "test_build_posture_single_run_has_no_prev()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L76 | neighbors=[test_posture.py, _fv()]
- "tests_test_posture_test_compute_scores_uses_risk_epss_exploit_and_asset_criticality": "test_compute_scores_uses_risk_epss_exploit_and_asset_criticality()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L53 | neighbors=[test_posture.py, _fv()]
- "tests_test_posture_test_finding_views_handles_null_asset_and_scores": "test_finding_views_handles_null_asset_and_scores()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L128 | neighbors=[test_posture.py, _Row]
- "tests_test_posture_test_finding_views_maps_columns_and_asset_criticality": "test_finding_views_maps_columns_and_asset_criticality()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L114 | neighbors=[test_posture.py, _Row]
- "tests_test_posture_trace_testbehaviourpreserved_test_detect_posture_matches_traced_findings": ".test_detect_posture_matches_traced_findings()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L119 | neighbors=[TestBehaviourPreserved, ._mixed()]
- "tests_test_posture_trace_testruleisolation": "TestRuleIsolation" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L95 | neighbors=[test_posture_trace.py, .test_raising_rule_is_error_and_others_…]
- "tests_test_printer_scanner_testparity": "TestParity" | kind=code-symbol | source=probe/tests/test_printer_scanner.py:L61 | neighbors=[test_printer_scanner.py, .test_main_scripts()]
- "tests_test_printer_scanner_testprinterfindings": "TestPrinterFindings" | kind=code-symbol | source=probe/tests/test_printer_scanner.py:L52 | neighbors=[test_printer_scanner.py, .test_exposed_low()]
- "tests_test_printer_scanner_testprinterscanner_test_no_printer_filtered": ".test_no_printer_filtered()" | kind=code-symbol | source=probe/tests/test_printer_scanner.py:L46 | neighbors=[TestPrinterScanner, ._sc()]
- "tests_test_printer_scanner_testprinterscanner_test_open": ".test_open()" | kind=code-symbol | source=probe/tests/test_printer_scanner.py:L39 | neighbors=[TestPrinterScanner, ._sc()]
- "tests_test_probe_core_testassetmergepassivecollect": "TestAssetMergePassiveCollect" | kind=code-symbol | source=probe/tests/test_probe_core.py:L583 | neighbors=[test_probe_core.py, .test_passive_facts_appended()]
- "tests_test_probe_core_testassetmergeservicebanner": "TestAssetMergeServiceBanner" | kind=code-symbol | source=probe/tests/test_probe_core.py:L534 | neighbors=[test_probe_core.py, .test_banner_stored()]
- "tests_test_probe_core_testassetmergesmbscan": "TestAssetMergeSmbScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L559 | neighbors=[test_probe_core.py, .test_smb_state_host_level()]
- "tests_test_probe_core_testassetmergetlsscan": "TestAssetMergeTlsScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L543 | neighbors=[test_probe_core.py, .test_tls_facts_stored()]
- "tests_test_probe_core_testassetmergeunknownscanner": "TestAssetMergeUnknownScanner" | kind=code-symbol | source=probe/tests/test_probe_core.py:L592 | neighbors=[test_probe_core.py, .test_unknown_scanner_ignored()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-158.json

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
