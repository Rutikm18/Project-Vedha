# Node Description Batch 65 of 336

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

- "tests_test_portal_remediation_client": "_client()" | kind=code-symbol | source=manager/backend/tests/test_portal_remediation.py:L22 | neighbors=[test_portal_remediation.py, .test_missing_or_out_of_scope_finding_i…, .test_serves_kb_when_no_stored_plan(), .test_serves_reviewed_ai_plan_stripping…, .test_unreviewed_ai_plan_does_not_leak()]
- "tests_test_portal_remediation_testportalremediation": "TestPortalRemediation" | kind=code-symbol | source=manager/backend/tests/test_portal_remediation.py:L44 | neighbors=[test_portal_remediation.py, .test_missing_or_out_of_scope_finding_i…, .test_serves_kb_when_no_stored_plan(), .test_serves_reviewed_ai_plan_stripping…, .test_unreviewed_ai_plan_does_not_leak()]
- "tests_test_posture_confidence_asset": "_asset()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L26 | neighbors=[test_posture_confidence.py, .test_confidence_is_serialized(), .test_corroborated_host_gets_floored_co…, .test_filtered_port_lowers_confidence(), .test_lone_finding_keeps_base_confidenc…]
- "tests_test_posture_confidence_fact": "_fact()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L19 | neighbors=[test_posture_confidence.py, .test_confidence_is_serialized(), .test_corroborated_host_gets_floored_co…, .test_filtered_port_lowers_confidence(), .test_lone_finding_keeps_base_confidenc…]
- "tests_test_posture_confidence_testendtoend": "TestEndToEnd" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_confidence.py:L93 | neighbors=[test_posture_confidence.py, .test_confidence_is_serialized(), .test_corroborated_host_gets_floored_co…, .test_filtered_port_lowers_confidence(), .test_lone_finding_keeps_base_confidenc…]
- "tests_test_posture_rules_testhardenedgroundtruth": "TestHardenedGroundTruth" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L50 | neighbors=[test_posture_rules.py, ._host(), .test_hardened_smb_and_rdp_raise_no_mis…, .test_no_critical_or_high_findings(), .test_rdp_exposed_is_low_because_nla_re…]
- "tests_test_posture_rules_testriskmodel": "TestRiskModel" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_rules.py:L132 | neighbors=[test_posture_rules.py, .test_auth_enforced_deescalates(), .test_internet_facing_unauth_escalates(), .test_priority_buckets(), .test_suspected_scores_below_confirmed()]
- "tests_test_posture_trace_testabsentversusclean": "TestAbsentVersusClean" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L36 | neighbors=[test_posture_trace.py, .test_key_absent_is_missing_input_not_c…, .test_key_present_false_is_clean_no_mat…, .test_key_present_true_is_match(), .test_missing_input_invariant_across_al…]
- "tests_test_posture_trace_testabsentversusclean_test_missing_input_invariant_across_all_rules": ".test_missing_input_invariant_across_all_rules()" | kind=code-symbol | source=manager/detection_engine/tests/test_posture_trace.py:L62 | neighbors=[I10 structurally: for EVERY rule with a…, TestAbsentVersusClean, _asset(), _fact(), _outcome()]
- "tests_test_probe_core_testgate2": "TestGate2" | kind=code-symbol | source=probe/tests/test_probe_core.py:L276 | neighbors=[test_probe_core.py, .test_never_seen_alive(), .test_ot_always_false(), .test_recently_seen_alive(), .test_stale_seen_alive()]
- "tests_test_probe_core_testgate6": "TestGate6" | kind=code-symbol | source=probe/tests/test_probe_core.py:L368 | neighbors=[test_probe_core.py, .test_already_collected(), .test_no_creds(), .test_not_alive(), .test_ssh_creds_alive_uncollected()]
- "tests_test_probe_core_testlookslikehttp": "TestLooksLikeHttp" | kind=code-symbol | source=probe/tests/test_probe_core.py:L390 | neighbors=[test_probe_core.py, .test_empty(), .test_http_1_1(), .test_http_2(), .test_not_http()]
- "tests_test_probe_core_testlooksliketls": "TestLooksLikeTls" | kind=code-symbol | source=probe/tests/test_probe_core.py:L405 | neighbors=[test_probe_core.py, .test_banner_present(), .test_client_first_port_not_tls(), .test_no_banner_attempt(), .test_silent_non_client_first_port()]
- "tests_test_probe_core_testresolvescantype": "TestResolveScanType" | kind=code-symbol | source=probe/tests/test_probe_core.py:L853 | neighbors=[test_probe_core.py, .test_default(), .test_from_job_type(), .test_from_params(), .test_params_override_job_type()]
- "tests_test_probe_core_testtargets": "TestTargets" | kind=code-symbol | source=probe/tests/test_probe_core.py:L884 | neighbors=[test_probe_core.py, .test_empty(), .test_list(), .test_scope_cidrs(), .test_single_string()]
- "tests_test_probe_simple_approve_testnextprobename": "TestNextProbeName" | kind=code-symbol | source=manager/backend/tests/test_probe_simple_approve.py:L20 | neighbors=[test_probe_simple_approve.py, .test_first_is_01(), .test_ignores_non_matching_and_non_nume…, .test_increments_past_highest_with_gaps…, .test_legacy_probe_names_still_advance_…]
- "tests_test_project_time_testrendering": "TestRendering" | kind=code-symbol | source=manager/backend/tests/test_project_time.py:L23 | neighbors=[test_project_time.py, .test_default_is_ist(), .test_same_instant_as_utc(), .test_still_orders_against_utc_rows(), .test_timestamp_carries_an_offset()]
- "tests_test_project_timezone_testprojecttimezone": "TestProjectTimezone" | kind=code-symbol | source=probe/tests/test_project_timezone.py:L26 | neighbors=[test_project_timezone.py, .test_aware_timestamps_still_compare_ag…, .test_default_is_ist(), .test_timestamp_is_iso_with_offset_not_…, .test_timestamp_is_the_same_instant_as_…]
- "tests_test_reference_testshape": "TestShape" | kind=code-symbol | source=manager/backend/tests/test_reference.py:L27 | neighbors=[test_reference.py, .test_an_unknown_prefix_is_refused(), .test_naive_created_at_is_treated_as_ut…, .test_reads_as_prefix_date_code(), .test_uses_the_rows_own_date_not_today()]
- "tests_test_remediation_kb_testclassify": "TestClassify" | kind=code-symbol | source=manager/backend/tests/test_remediation_kb.py:L16 | neighbors=[test_remediation_kb.py, .test_cve_without_keyword_is_patch(), .test_keyword_categories(), .test_order_specificity_anon_ftp_beats_…, .test_unmatched_is_generic()]
- "tests_test_remediation_routes_one_result": "_one_result()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L53 | neighbors=[test_remediation_routes.py, A result whose .one() yields the RETURN…, .test_ai_available_caches_ai_plan(), .test_ai_unavailable_falls_back_to_kb_a…, A result whose .one() yields the RETURN…]
- "tests_test_remediation_routes_testgenerateremediation": "TestGenerateRemediation" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L145 | neighbors=[test_remediation_routes.py, .test_ai_available_caches_ai_plan(), .test_ai_unavailable_falls_back_to_kb_a…, .test_cached_hit_without_force_returns_…, .test_cross_tenant_is_404()]
- "tests_test_remediation_routes_testgenerateremediation_test_cached_hit_without_force_returns_cached_and_publish_flips_reviewed": ".test_cached_hit_without_force_returns_cached_and_publish_flips_reviewed()" | kind=code-symbol | source=manager/backend/tests/test_remediation_routes.py:L166 | neighbors=[TestGenerateRemediation, _FakeDB, _finding(), _operator(), _scalar_result()]
- "tests_test_remediation_upsert_integration": "test_remediation_upsert_integration.py" | kind=code-symbol | source=manager/backend/tests/test_remediation_upsert_integration.py:L1 | neighbors=[fbe7450 Add comprehensive documentation…, _run(), _stmt(), test_upsert_resets_gate_and_is_race_saf…, test_remediation_upsert_integration.py …]
- "tests_test_resolve_asset_cache": "test_resolve_asset_cache.py" | kind=code-symbol | source=manager/backend/tests/test_resolve_asset_cache.py:L1 | neighbors=[26ea68c Add comprehensive tests for OS …, test_cache_resolves_each_host_once(), test_host_port_target_normalized(), test_no_cache_keeps_old_behavior(), Perf/N+1: _resolve_asset memoizes per-r…]
- "tests_test_resolve_infos": "_infos()" | kind=code-symbol | source=probe/tests/test_resolve.py:L11 | neighbors=[test_resolve.py, Fake getaddrinfo results: (family, sock…, .test_default_no_family_is_backward_com…, .test_requested_family_absent_falls_bac…, .test_requested_ipv4_selected_over_v6_f…]
- "tests_test_resolve_testresolvefamily": "TestResolveFamily" | kind=code-symbol | source=probe/tests/test_resolve.py:L20 | neighbors=[test_resolve.py, .test_default_no_family_is_backward_com…, .test_requested_family_absent_falls_bac…, .test_requested_ipv4_selected_over_v6_f…, .test_unresolvable_raises()]
- "tests_test_result_archive_testarchiveisbesteffort_test_unwritable_directory_does_not_fail_the_job": ".test_unwritable_directory_does_not_fail_the_job()" | kind=code-symbol | source=probe/tests/test_result_archive.py:L129 | neighbors=[A read-only filesystem must cost a warn…, TestArchiveIsBestEffort, _job(), _ok_result(), _runner()]
- "tests_test_router_db": "test_router_db.py" | kind=code-symbol | source=probe/tests/test_router_db.py:L1 | neighbors=[bb0ef3d feat(probe): route DB services …, test_mysql_greeting_on_odd_port(), test_plain_http_is_not_db(), test_redis_noauth_signature(), router.py]
- "tests_test_rsync_scanner_testrsyncfindings": "TestRsyncFindings" | kind=code-symbol | source=probe/tests/test_rsync_scanner.py:L99 | neighbors=[test_rsync_scanner.py, ._fact(), .test_anon_modules_high(), .test_auth_only_is_low_disclosure(), .test_no_modules_silent()]
- "tests_test_run_scoped_fact_scope": "test_run_scoped_fact_scope.py" | kind=code-symbol | source=manager/backend/tests/test_run_scoped_fact_scope.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, _fact(), TestRunScopedFactsAreExempt, TestTheScopeGateStillWorks, Run-scoped facts must not be scope-chec…]
- "tests_test_run_scoped_fact_scope_testrunscopedfactsareexempt": "TestRunScopedFactsAreExempt" | kind=code-symbol | source=manager/backend/tests/test_run_scoped_fact_scope.py:L43 | neighbors=[test_run_scoped_fact_scope.py, .test_a_real_result_with_one_run_scoped…, .test_ipv6_discovery_auto_target_is_not…, .test_ipv6_discovery_interface_name_is_…, .test_run_scoped_fact_is_not_collected_…]
- "tests_test_runtime_requirements_coverage": "test_runtime_requirements_coverage.py" | kind=code-symbol | source=probe/tests/test_runtime_requirements_coverage.py:L1 | neighbors=[8f6bf49 Refactor code structure and rem…, _declared(), test_runtime_image_installs_every_wired…, test_runtime_is_a_subset_of_the_develop…, test_runtime_requirements_coverage.py —…]
- "tests_test_runtime_topology": "test_runtime_topology.py" | kind=code-symbol | source=manager/backend/tests/test_runtime_topology.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, main.py, test_manager_does_not_mount_a_static_da…, test_manager_root_is_service_metadata(), Product-boundary tests for the single-d…]
- "tests_test_scan_funnel_fakediscovery": "FakeDiscovery" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L24 | neighbors=[test_scan_funnel.py, .__init__(), .scan_target(), _make_funnel(), ._funnel()]
- "tests_test_scan_funnel_fakemsrpc": "_FakeMSRPC" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L254 | neighbors=[test_scan_funnel.py, .__init__(), .scan_target(), A deep scanner on 135 that returns EPM-…, ._funnel()]
- "tests_test_scan_funnel_opensetportfactory": "_OpenSetPortFactory" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L232 | neighbors=[test_scan_funnel.py, .__call__(), .__init__(), Port-scanner factory whose scanners rep…, ._funnel()]
- "tests_test_scan_funnel_scope": "_scope()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L62 | neighbors=[test_scan_funnel.py, _make_funnel(), .test_constructs_and_wires_real_scanner…, .test_port_scanner_is_syn_scanner(), ._funnel()]
- "tests_test_scan_funnel_testrouteports": "TestRoutePorts" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L100 | neighbors=[test_scan_funnel.py, .test_intersection_only(), .test_no_match_returns_empty(), .test_port_in_multiple_routes(), .test_sorted_output()]
- "tests_test_scanner_congestion_fake_gai": "_fake_gai()" | kind=code-symbol | source=probe/tests/test_scanner_congestion.py:L287 | neighbors=[test_scanner_congestion.py, .test_deduplicates_repeated_addresses(), .test_family_filter_restricts_results(), .test_returns_every_family_in_order(), .test_v4_is_reachable_even_when_aaaa_so…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-064.json

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
