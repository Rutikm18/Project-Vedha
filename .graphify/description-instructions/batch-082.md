# Node Description Batch 83 of 227

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
- "tests_test_portal_scope_operator": "_operator()" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L33 | neighbors=[test_portal_scope.py, .test_operator_is_forbidden(), .test_operator_cannot_scope()]
- "tests_test_portal_scope_testclientscoped": "TestClientScoped" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L70 | neighbors=[test_portal_scope.py, .test_applies_engagement_filter_for_bou…, .test_operator_cannot_scope()]
- "tests_test_probe_core_testassetmergecredentialed": "TestAssetMergeCredentialed" | kind=code-symbol | source=probe/tests/test_probe_core.py:L568 | neighbors=[test_probe_core.py, .test_ssh_inventory(), .test_windows_inventory()]
- "tests_test_probe_core_testassetmergecredentialed_test_ssh_inventory": ".test_ssh_inventory()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L569 | neighbors=[TestAssetMergeCredentialed, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergecredentialed_test_windows_inventory": ".test_windows_inventory()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L576 | neighbors=[TestAssetMergeCredentialed, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergehostdiscovery": "TestAssetMergeHostDiscovery" | kind=code-symbol | source=probe/tests/test_probe_core.py:L502 | neighbors=[test_probe_core.py, .test_alive_sets_timestamp(), .test_responding_ports()]
- "tests_test_probe_core_testassetmergehostdiscovery_test_alive_sets_timestamp": ".test_alive_sets_timestamp()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L503 | neighbors=[TestAssetMergeHostDiscovery, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergehostdiscovery_test_responding_ports": ".test_responding_ports()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L510 | neighbors=[TestAssetMergeHostDiscovery, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergepassivecollect_test_passive_facts_appended": ".test_passive_facts_appended()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L584 | neighbors=[TestAssetMergePassiveCollect, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeportscan": "TestAssetMergePortScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L521 | neighbors=[test_probe_core.py, .test_tcp_open(), .test_udp_uncertain()]
- "tests_test_probe_core_testassetmergeportscan_test_tcp_open": ".test_tcp_open()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L522 | neighbors=[TestAssetMergePortScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeportscan_test_udp_uncertain": ".test_udp_uncertain()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L528 | neighbors=[TestAssetMergePortScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeservicebanner_test_banner_stored": ".test_banner_stored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L535 | neighbors=[TestAssetMergeServiceBanner, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergesmbscan_test_smb_state_host_level": ".test_smb_state_host_level()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L560 | neighbors=[TestAssetMergeSmbScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergetlsscan_test_tls_facts_stored": ".test_tls_facts_stored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L544 | neighbors=[TestAssetMergeTlsScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergeunknownscanner_test_unknown_scanner_ignored": ".test_unknown_scanner_ignored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L593 | neighbors=[TestAssetMergeUnknownScanner, _asset(), _scan_result()]
- "tests_test_probe_core_testassetmergewebscan_test_web_facts_stored": ".test_web_facts_stored()" | kind=code-symbol | source=probe/tests/test_probe_core.py:L552 | neighbors=[TestAssetMergeWebScan, _asset(), _scan_result()]
- "tests_test_probe_core_testassetopenportsfordeepscan": "TestAssetOpenPortsForDeepScan" | kind=code-symbol | source=probe/tests/test_probe_core.py:L489 | neighbors=[test_probe_core.py, .test_empty(), .test_only_open()]
- "tests_test_probe_core_testcapabilities": "TestCapabilities" | kind=code-symbol | source=probe/tests/test_probe_core.py:L893 | neighbors=[test_probe_core.py, .test_capabilities_sorted(), .test_known_scan_types()]
- "tests_test_probe_simple_approve_testsimpleapproveinput": "TestSimpleApproveInput" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L33 | neighbors=[test_probe_simple_approve.py, .test_defaults_are_all_optional(), .test_overrides_accepted()]
- "tests_test_reaper_objects": "_objects()" | kind=code-symbol | source=manager/backend/tests/test_reaper.py:L8 | neighbors=[test_reaper.py, test_expired_attempt_fails_job_when_ret…, test_expired_attempt_requeues_with_fenc…]
- "tests_test_remediation_generator_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L26 | neighbors=[test_remediation_generator.py, .test_unparseable_output_raises_value_e…, .test_valid_output_returns_ai_plan_with…]
- "tests_test_remediation_generator_testgenerateremediationplan_gen": "._gen()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L117 | neighbors=[TestGenerateRemediationPlan, .test_unparseable_output_raises_value_e…, .test_valid_output_returns_ai_plan_with…]
- "tests_test_remediation_generator_testgenerateremediationplan_test_unparseable_output_raises_value_error": ".test_unparseable_output_raises_value_error()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L122 | neighbors=[TestGenerateRemediationPlan, _finding(), ._gen()]
- "tests_test_remediation_generator_testgenerateremediationplan_test_valid_output_returns_ai_plan_with_model": ".test_valid_output_returns_ai_plan_with_model()" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L127 | neighbors=[TestGenerateRemediationPlan, _finding(), ._gen()]
- "tests_test_remediation_generator_testsafecommands": "TestSafeCommands" | kind=code-symbol | source=manager/backend/tests/test_remediation_generator.py:L55 | neighbors=[test_remediation_generator.py, .test_drops_destructive_keeps_safe(), .test_null_command_yields_nothing()]
- "tests_test_remediation_kb_testrecipeshape": "TestRecipeShape" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L43 | neighbors=[test_remediation_kb.py, .test_every_recipe_has_required_fields(), .test_every_recipe_step_has_all_os_keys…]
- "tests_test_remediation_routes_genai": "_GenAI" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L84 | neighbors=[test_remediation_routes.py, .generate_remediation_plan(), .__init__()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-082.json

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
