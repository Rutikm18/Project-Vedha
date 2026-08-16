# Node Description Batch 55 of 209

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

- "tests_test_portal_metrics_teststatustimeline": "TestStatusTimeline" | kind=code-symbol | source=manager/backend/tests/test_portal_metrics.py:L41 | neighbors=[test_portal_metrics.py, .test_activity_outside_window_is_ignore…, .test_buckets_opened_and_closed(), .test_emits_continuous_zero_filled_mont…]
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
- "tests_test_portal_scope_testassertclient": "TestAssertClient" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L37 | neighbors=[test_portal_scope.py, .test_bound_client_returns_engagement(), .test_client_without_engagement_is_forb…, .test_operator_is_forbidden()]
- "tests_test_portal_scope_testportaltokenclaims": "TestPortalTokenClaims" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L84 | neighbors=[test_portal_scope.py, .test_client_role_enum_exists(), .test_client_token_carries_portal_aud_a…, .test_operator_and_portal_audiences_dif…]
- "tests_test_portal_scope_testresolvescope": "TestResolveScope" | kind=code-symbol | source=manager/backend/tests/test_portal_scope.py:L55 | neighbors=[test_portal_scope.py, .test_matching_request_ok(), .test_mismatched_request_is_403_idor_de…, .test_no_request_returns_bound()]
- "tests_test_posture_fv": "_fv()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L12 | neighbors=[test_posture.py, test_build_posture_buckets_resolved_new…, test_build_posture_single_run_has_no_pr…, test_compute_scores_uses_risk_epss_expl…]
- "tests_test_posture_row": "_Row" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L109 | neighbors=[test_posture.py, .__init__(), test_finding_views_handles_null_asset_a…, test_finding_views_maps_columns_and_ass…]
- "tests_test_probe_core_testassetneedsrechecklive": "TestAssetNeedsRecheckLive" | kind=code-symbol | source=probe/tests/test_probe_core.py:L475 | neighbors=[test_probe_core.py, .test_never_seen(), .test_recently_seen(), .test_stale()]
- "tests_test_probe_core_testgate0": "TestGate0" | kind=code-symbol | source=probe/tests/test_probe_core.py:L265 | neighbors=[test_probe_core.py, .test_iot_not_passive(), .test_it_not_passive(), .test_ot_is_passive()]
- "tests_test_probe_core_testgate3": "TestGate3" | kind=code-symbol | source=probe/tests/test_probe_core.py:L294 | neighbors=[test_probe_core.py, .test_not_alive(), .test_ot_always_false(), .test_requires_alive()]
- "tests_test_probe_core_testgate4": "TestGate4" | kind=code-symbol | source=probe/tests/test_probe_core.py:L308 | neighbors=[test_probe_core.py, .test_all_closed(), .test_no_open_ports(), .test_with_open_ports()]
- "tests_test_probe_core_testratelimiter": "TestRateLimiter" | kind=code-symbol | source=probe/tests/test_probe_core.py:L247 | neighbors=[test_probe_core.py, .test_min_interval(), .test_wait_returns_immediately_at_zero_…, .test_zero_rate()]
- "tests_test_probe_core_testroutebranches": "TestRouteBranches" | kind=code-symbol | source=probe/tests/test_probe_core.py:L419 | neighbors=[test_probe_core.py, .test_http_banner_routes_web(), .test_no_banners_no_routing(), .test_silent_nonstandard_port_routes_tl…]
- "tests_test_probe_core_testscanresult": "TestScanResult" | kind=code-symbol | source=probe/tests/test_probe_core.py:L227 | neighbors=[test_probe_core.py, .test_default_status_observed(), .test_default_timestamp_present(), .test_to_json_roundtrip()]
- "tests_test_probe_manifest_manifest": "_manifest()" | kind=code-symbol | source=probe/tests/test_probe_manifest.py:L20 | neighbors=[test_probe_manifest.py, test_manifest_is_clean_parseable_json(), test_manifest_is_deterministic(), test_manifest_surfaces_the_capability_c…]
- "tests_test_reaper": "test_reaper.py" | kind=code-symbol | source=manager/backend/tests/test_reaper.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, _objects(), test_expired_attempt_fails_job_when_ret…, test_expired_attempt_requeues_with_fenc…]
- "tests_test_resolution_apply_db_returning": "_db_returning()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L26 | neighbors=[test_resolution_apply.py, test_covered_clean_medium_finding_is_au…, test_db_version_change_blocks_resolutio…, test_uncovered_finding_is_left_open()]
- "tests_test_resolution_apply_finding": "_finding()" | kind=code-symbol | source=manager/backend/tests/test_resolution_apply.py:L16 | neighbors=[test_resolution_apply.py, test_covered_clean_medium_finding_is_au…, test_db_version_change_blocks_resolutio…, test_uncovered_finding_is_left_open()]
- "tests_test_resolution_coverage": "test_resolution_coverage.py" | kind=code-symbol | source=manager/backend/tests/test_resolution_coverage.py:L1 | neighbors=[9a36729 feat(resolution): coverage buil…, test_coverage_counts_only_completed_sca…, test_coverage_empty_when_no_scanner_run…, test_host_of_strips_single_port()]
- "tests_test_scan_funnel_fakediscovery": "FakeDiscovery" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L22 | neighbors=[test_scan_funnel.py, .__init__(), .scan_target(), _make_funnel()]
- "tests_test_scan_funnel_fakeportscanner": "FakePortScanner" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L34 | neighbors=[test_scan_funnel.py, .__init__(), .scan_target(), _make_funnel()]
- "tests_test_scan_funnel_scope": "_scope()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L60 | neighbors=[test_scan_funnel.py, _make_funnel(), .test_constructs_and_wires_real_scanner…, .test_port_scanner_is_syn_scanner()]
- "tests_test_scan_funnel_testbuilddefaultfunnel": "TestBuildDefaultFunnel" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L190 | neighbors=[test_scan_funnel.py, .test_candidate_ports_cover_all_routes(), .test_constructs_and_wires_real_scanner…, .test_port_scanner_is_syn_scanner()]
- "tests_test_scan_health_summary": "_summary()" | kind=code-symbol | source=manager/backend/tests/test_scan_health.py:L13 | neighbors=[test_scan_health.py, test_clean_scan_is_healthy_and_does_not…, test_local_resource_errors_flag_degrade…, test_missing_ports_flag_incomplete()]
- "tests_test_scope_targets_testexclusions": "TestExclusions" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L70 | neighbors=[test_scope_targets.py, .test_target_clear_of_exclusions_is_all…, .test_target_inside_an_exclusion_is_rej…, .test_target_overlapping_an_exclusion_i…]
- "tests_test_seed_admin_testhashhelpers": "TestHashHelpers" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L77 | neighbors=[test_seed_admin.py, .test_different_calls_produce_different…, .test_hash_and_verify_round_trip(), .test_wrong_password_fails_verify()]
- "tests_test_service_identifier": "test_service_identifier.py" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, TestServiceIdentifier, Unit tests for ServiceIdentifier., 298a9d4 trim frontend to 7 core pages; …]
- "tests_test_service_match_testsshmatch": "TestSshMatch" | kind=code-symbol | source=probe/tests/test_service_match.py:L16 | neighbors=[test_service_match.py, .test_dropbear(), .test_generic_ssh(), .test_openssh_version()]
- "tests_test_smb_scanner_smb2_negotiate_response": "_smb2_negotiate_response()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L5 | neighbors=[test_smb_scanner.py, test_signing_not_required(), test_signing_required_smb311(), test_signing_supported_field_present()]
- "tests_test_syn_scanner_testcapabilitydetection": "TestCapabilityDetection" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L138 | neighbors=[test_syn_scanner.py, .test_linux_with_raw_socket_is_supporte…, .test_linux_without_privilege_is_unsupp…, .test_non_linux_is_unsupported()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-054.json

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
