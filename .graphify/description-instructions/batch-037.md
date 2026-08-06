# Node Description Batch 38 of 134

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

- "tests_test_outbox_reclaim_mock_session": "_mock_session()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L104 | neighbors=[test_outbox_reclaim.py, test_reclaim_handles_none_rowcount_from…, test_reclaim_is_noop_when_nothing_is_st…, test_reclaim_runs_both_sweeps_commits_a…]
- "tests_test_outbox_reclaim_sql": "_sql()" | kind=code-symbol | source=manager/backend/tests/test_outbox_reclaim.py:L20 | neighbors=[test_outbox_reclaim.py, test_dead_letter_and_requeue_are_mutual…, test_dead_letter_stmt_targets_exhausted…, test_requeue_stmt_makes_retryable_stran…]
- "tests_test_posture_fv": "_fv()" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L12 | neighbors=[test_posture.py, test_build_posture_buckets_resolved_new…, test_build_posture_single_run_has_no_pr…, test_compute_scores_uses_risk_epss_expl…]
- "tests_test_posture_row": "_Row" | kind=code-symbol | source=manager/backend/tests/test_posture.py:L109 | neighbors=[test_posture.py, .__init__(), test_finding_views_handles_null_asset_a…, test_finding_views_maps_columns_and_ass…]
- "tests_test_probe_core_testassetneedsrechecklive": "TestAssetNeedsRecheckLive" | kind=code-symbol | source=probe/tests/test_probe_core.py:L475 | neighbors=[test_probe_core.py, .test_never_seen(), .test_recently_seen(), .test_stale()]
- "tests_test_probe_core_testgate0": "TestGate0" | kind=code-symbol | source=probe/tests/test_probe_core.py:L265 | neighbors=[test_probe_core.py, .test_iot_not_passive(), .test_it_not_passive(), .test_ot_is_passive()]
- "tests_test_probe_core_testgate3": "TestGate3" | kind=code-symbol | source=probe/tests/test_probe_core.py:L294 | neighbors=[test_probe_core.py, .test_not_alive(), .test_ot_always_false(), .test_requires_alive()]
- "tests_test_probe_core_testgate4": "TestGate4" | kind=code-symbol | source=probe/tests/test_probe_core.py:L308 | neighbors=[test_probe_core.py, .test_all_closed(), .test_no_open_ports(), .test_with_open_ports()]
- "tests_test_probe_core_testratelimiter": "TestRateLimiter" | kind=code-symbol | source=probe/tests/test_probe_core.py:L247 | neighbors=[test_probe_core.py, .test_min_interval(), .test_wait_returns_immediately_at_zero_…, .test_zero_rate()]
- "tests_test_probe_core_testroutebranches": "TestRouteBranches" | kind=code-symbol | source=probe/tests/test_probe_core.py:L419 | neighbors=[test_probe_core.py, .test_http_banner_routes_web(), .test_no_banners_no_routing(), .test_silent_nonstandard_port_routes_tl…]
- "tests_test_probe_core_testscanresult": "TestScanResult" | kind=code-symbol | source=probe/tests/test_probe_core.py:L227 | neighbors=[test_probe_core.py, .test_default_status_observed(), .test_default_timestamp_present(), .test_to_json_roundtrip()]
- "tests_test_reaper": "test_reaper.py" | kind=code-symbol | source=manager/backend/tests/test_reaper.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, _objects(), test_expired_attempt_fails_job_when_ret…, test_expired_attempt_requeues_with_fenc…]
- "tests_test_seed_admin_testhashhelpers": "TestHashHelpers" | kind=code-symbol | source=manager/backend/tests/test_seed_admin.py:L77 | neighbors=[test_seed_admin.py, .test_different_calls_produce_different…, .test_hash_and_verify_round_trip(), .test_wrong_password_fails_verify()]
- "tests_test_service_identifier": "test_service_identifier.py" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, TestServiceIdentifier, Unit tests for ServiceIdentifier., 298a9d4 trim frontend to 7 core pages; …]
- "tests_test_transport_testheartbeat": "TestHeartbeat" | kind=code-symbol | source=probe/tests/test_transport.py:L316 | neighbors=[test_transport.py, .test_heartbeat_401_returns_false(), .test_heartbeat_sends_current_job(), .test_successful_heartbeat()]
- "tests_test_transport_testhttpget": "TestHttpGet" | kind=code-symbol | source=probe/tests/test_transport.py:L478 | neighbors=[test_transport.py, .test_exception_returns_none(), .test_non_200_returns_none(), .test_successful_get()]
- "tests_test_transport_testpolljobs": "TestPollJobs" | kind=code-symbol | source=probe/tests/test_transport.py:L349 | neighbors=[test_transport.py, .test_poll_401_raises(), .test_poll_uses_limit_param(), .test_returns_jobs()]
- "tests_test_transport_testrefreshregistration": "TestRefreshRegistration" | kind=code-symbol | source=probe/tests/test_transport.py:L271 | neighbors=[test_transport.py, .test_cached_agent_refreshes_capabiliti…, .test_old_manager_returns_compatibility…, .test_rejected_cached_identity_raises()]
- "tests_test_transport_testregister": "TestRegister" | kind=code-symbol | source=probe/tests/test_transport.py:L129 | neighbors=[test_transport.py, .test_registration_401_raises(), .test_registration_sends_public_key(), .test_successful_registration()]
- "tests_test_validation_preflight_responses": "_preflight_responses()" | kind=code-symbol | source=probe/tests/test_validation.py:L165 | neighbors=[test_validation.py, test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…, test_cmd_validate_refuses_ambiguous_mul…]
- "tests_test_validation_test_cmd_validate_dry_run_performs_no_mutating_requests": "test_cmd_validate_dry_run_performs_no_mutating_requests()" | kind=code-symbol | source=probe/tests/test_validation.py:L190 | neighbors=[test_validation.py, FakeClient, _preflight_responses(), _validation_args()]
- "tests_test_validation_test_cmd_validate_executes_one_bounded_job_and_protects_results": "test_cmd_validate_executes_one_bounded_job_and_protects_results()" | kind=code-symbol | source=probe/tests/test_validation.py:L214 | neighbors=[test_validation.py, FakeClient, _preflight_responses(), _validation_args()]
- "tests_test_validation_test_cmd_validate_refuses_ambiguous_multi_probe_scheduling": "test_cmd_validate_refuses_ambiguous_multi_probe_scheduling()" | kind=code-symbol | source=probe/tests/test_validation.py:L206 | neighbors=[test_validation.py, FakeClient, _preflight_responses(), _validation_args()]
- "tests_test_validation_validation_args": "_validation_args()" | kind=code-symbol | source=probe/tests/test_validation.py:L120 | neighbors=[test_validation.py, test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…, test_cmd_validate_refuses_ambiguous_mul…]
- "tests_test_workflow_execution_concurrencyscanner": "_ConcurrencyScanner" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L46 | neighbors=[test_workflow_execution.py, .__init__(), .scan_target(), test_host_fanout_is_bounded()]
- "tests_test_xml_parser": "test_xml_parser.py" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, TestNmapXMLParser, Unit tests for NmapXMLParser., 298a9d4 trim frontend to 7 core pages; …]
- "tools_installer_installall": "installAll()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L226 | neighbors=[tools.ts, installer.ts, getInstalledRecord(), installTool()]
- "utils_db": "db.py" | kind=code-symbol | source=manager/backend/app/utils/db.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, get_or_404(), Shared database helpers — single source…, 298a9d4 trim frontend to 7 core pages; …]
- "utils_hash": "hash.py" | kind=code-symbol | source=manager/backend/app/utils/hash.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, dedup_hash(), Shared hashing utilities — deduplicatio…, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0015_finding_risk_score_scale": "0015_finding_risk_score_scale.py" | kind=code-symbol | source=manager/backend/alembic/versions/0015_finding_risk_score_scale.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, downgrade(), upgrade(), Allow the documented 0-1000 finding ris…]
- "versions_0016_user_tenant_is_active": "0016_user_tenant_is_active.py" | kind=code-symbol | source=manager/backend/alembic/versions/0016_user_tenant_is_active.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, downgrade(), upgrade(), Add is_active to users and tenants; add…]
- "versions_0017_scan_job_attempts": "0017_scan_job_attempts.py" | kind=code-symbol | source=manager/backend/alembic/versions/0017_scan_job_attempts.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, downgrade(), upgrade(), Add fenced execution attempts for agent…]
- "versions_0018_probe_enrollment": "0018_probe_enrollment.py" | kind=code-symbol | source=manager/backend/alembic/versions/0018_probe_enrollment.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, downgrade(), upgrade(), Add Manager-approved device-key probe e…]
- "vuln_enrichment_vulnenrichmentservice_check_cisa_kev": ".check_cisa_kev()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L244 | neighbors=[True if CVE is in the CISA Known Exploi…, VulnEnrichmentService, ._get_kev_catalog(), ._fetch_all()]
- "vuln_enrichment_vulnenrichmentservice_compute_composite_risk": ".compute_composite_risk()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L297 | neighbors=[Returns composite risk score on 0-1000 …, VulnEnrichmentService, .get(), .enrich()]
- "vuln_enrichment_vulnenrichmentservice_fetch_epss": ".fetch_epss()" | kind=code-symbol | source=manager/backend/app/vuln/enrichment.py:L215 | neighbors=[Returns {epss_score: float, percentile:…, VulnEnrichmentService, ._fetch_all(), .get()]
- "vuln_nessus_nessusscanner_export_nessus_file": ".export_nessus_file()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L256 | neighbors=[NessusScanner, ._get_client(), Request + poll + download .nessus XML f…, Request + poll + download .nessus XML f…]
- "vuln_nessus_nessusscanner_launch_scan": ".launch_scan()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L139 | neighbors=[NessusScanner, ._get_client(), Returns scan_uuid (token for tracking)., Returns scan_uuid (token for tracking).]
- "vuln_nessus_nessusscanner_poll_status": ".poll_status()" | kind=code-symbol | source=manager/backend/app/vuln/nessus.py:L150 | neighbors=[NessusScanner, ._get_client(), Returns {status, progress_percent, host…, Returns {status, progress_percent, host…]
- "vuln_nuclei_nucleiscanner_partial_or_raise": "._partial_or_raise()" | kind=code-symbol | source=manager/backend/app/vuln/nuclei.py:L337 | neighbors=[NucleiScanner, NucleiRunReport, NucleiScanError, .run_scan()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-037.json

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
