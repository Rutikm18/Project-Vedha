# Node Description Batch 87 of 336

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

- "tests_test_tls_legacy_versions_test_legacy_version_is_detected_not_masked_by_client_policy": "test_legacy_version_is_detected_not_masked_by_client_policy()" | kind=code-symbol | source=probe/tests/test_tls_legacy_versions.py:L113 | neighbors=[test_tls_legacy_versions.py, _LegacyTLSServer, _self_signed(), _server_supports()]
- "tests_test_tls_legacy_versions_test_untested_versions_are_surfaced_in_the_fact": "test_untested_versions_are_surfaced_in_the_fact()" | kind=code-symbol | source=probe/tests/test_tls_legacy_versions.py:L144 | neighbors=[test_tls_legacy_versions.py, When the probe genuinely cannot test a …, _LegacyTLSServer, _self_signed()]
- "tests_test_tls_port_coverage_testsinglesourceoftruth": "TestSingleSourceOfTruth" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L31 | neighbors=[test_tls_port_coverage.py, .test_branch_port_table_reuses_it_too(), .test_branch_spec_matches_the_gate(), .test_gates_reuses_the_same_object()]
- "tests_test_tls_port_coverage_testwidenedcoverage": "TestWidenedCoverage" | kind=code-symbol | source=probe/tests/test_tls_port_coverage.py:L44 | neighbors=[test_tls_port_coverage.py, .test_classic_implicit_tls_still_covere…, .test_management_and_api_surfaces_now_c…, .test_the_set_actually_grew()]
- "tests_test_transport_testheartbeat": "TestHeartbeat" | kind=code-symbol | source=probe/tests/test_transport.py:L396 | neighbors=[test_transport.py, .test_heartbeat_401_returns_false(), .test_heartbeat_sends_current_job(), .test_successful_heartbeat()]
- "tests_test_transport_testhttpget": "TestHttpGet" | kind=code-symbol | source=probe/tests/test_transport.py:L558 | neighbors=[test_transport.py, .test_exception_returns_none(), .test_non_200_returns_none(), .test_successful_get()]
- "tests_test_transport_testpolljobs": "TestPollJobs" | kind=code-symbol | source=probe/tests/test_transport.py:L429 | neighbors=[test_transport.py, .test_poll_401_raises(), .test_poll_uses_limit_param(), .test_returns_jobs()]
- "tests_test_transport_testrefreshregistration": "TestRefreshRegistration" | kind=code-symbol | source=probe/tests/test_transport.py:L351 | neighbors=[test_transport.py, .test_cached_agent_refreshes_capabiliti…, .test_old_manager_returns_compatibility…, .test_rejected_cached_identity_raises()]
- "tests_test_transport_testregister": "TestRegister" | kind=code-symbol | source=probe/tests/test_transport.py:L157 | neighbors=[test_transport.py, .test_registration_401_raises(), .test_registration_sends_public_key(), .test_successful_registration()]
- "tests_test_va_campaign_detect_stage": "_detect_stage()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L242 | neighbors=[test_va_campaign.py, _scope(), test_detect_stage_skipped_when_nothing_…, test_detect_stage_turns_facts_into_weak…]
- "tests_test_validation_preflight_responses": "_preflight_responses()" | kind=code-symbol | source=probe/tests/test_validation.py:L165 | neighbors=[test_validation.py, test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…, test_cmd_validate_refuses_ambiguous_mul…]
- "tests_test_validation_test_cmd_validate_dry_run_performs_no_mutating_requests": "test_cmd_validate_dry_run_performs_no_mutating_requests()" | kind=code-symbol | source=probe/tests/test_validation.py:L190 | neighbors=[test_validation.py, FakeClient, _preflight_responses(), _validation_args()]
- "tests_test_validation_test_cmd_validate_executes_one_bounded_job_and_protects_results": "test_cmd_validate_executes_one_bounded_job_and_protects_results()" | kind=code-symbol | source=probe/tests/test_validation.py:L214 | neighbors=[test_validation.py, FakeClient, _preflight_responses(), _validation_args()]
- "tests_test_validation_test_cmd_validate_refuses_ambiguous_multi_probe_scheduling": "test_cmd_validate_refuses_ambiguous_multi_probe_scheduling()" | kind=code-symbol | source=probe/tests/test_validation.py:L206 | neighbors=[test_validation.py, FakeClient, _preflight_responses(), _validation_args()]
- "tests_test_validation_validation_args": "_validation_args()" | kind=code-symbol | source=probe/tests/test_validation.py:L120 | neighbors=[test_validation.py, test_cmd_validate_dry_run_performs_no_m…, test_cmd_validate_executes_one_bounded_…, test_cmd_validate_refuses_ambiguous_mul…]
- "tests_test_verification_llm": "test_verification_llm.py" | kind=code-symbol | source=manager/backend/tests/test_verification_llm.py:L1 | neighbors=[de2d1c9 feat(verification): optional fa…, test_llm_can_flag_false_positive_and_lo…, test_llm_error_falls_back_to_determinis…, test_no_llm_matches_deterministic()]
- "tests_test_vnc_scanner_testvncfindings_fact": "._fact()" | kind=code-symbol | source=probe/tests/test_vnc_scanner.py:L53 | neighbors=[TestVNCFindings, .test_no_auth_is_critical(), .test_strong_auth_silent(), .test_weak_only_is_medium()]
- "tests_test_vnc_scanner_testvncscanner": "TestVNCScanner" | kind=code-symbol | source=probe/tests/test_vnc_scanner.py:L33 | neighbors=[test_vnc_scanner.py, ._sc(), .test_no_auth_open(), .test_no_vnc_filtered()]
- "tests_test_weakness_map_testclicorrelatemerges": "TestCliCorrelateMerges" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L180 | neighbors=[test_weakness_map.py, ._disk_db(), .test_correlate_includes_weakness_findi…, .test_no_weakness_map_flag_disables_it()]
- "tests_test_weakness_map_testfindingview": "TestFindingView" | kind=code-symbol | source=probe/tests/test_weakness_map.py:L56 | neighbors=[test_weakness_map.py, .test_non_finding_ignored(), .test_raw_shape(), .test_wrapped_shape()]
- "tests_test_wire_identity_testmoduleconstantsunbranded": "TestModuleConstantsUnbranded" | kind=code-symbol | source=probe/tests/test_wire_identity.py:L80 | neighbors=[test_wire_identity.py, Import-time probe constants built from …, .test_iot_rtsp_options(), .test_service_banner_http_probe()]
- "tests_test_workflow_execution_concurrencyscanner": "_ConcurrencyScanner" | kind=code-symbol | source=probe/tests/test_workflow_execution.py:L46 | neighbors=[test_workflow_execution.py, .__init__(), .scan_target(), test_host_fanout_is_bounded()]
- "tests_test_xml_parser": "test_xml_parser.py" | kind=code-symbol | source=manager/backend/tests/test_xml_parser.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, TestNmapXMLParser, Unit tests for NmapXMLParser., 298a9d4 trim frontend to 7 core pages; …]
- "tools_installer_installall": "installAll()" | kind=code-symbol | source=manager/frontend/lib/tools/installer.ts:L226 | neighbors=[tools.ts, installer.ts, getInstalledRecord(), installTool()]
- "tools_issue_license_main": "main()" | kind=code-symbol | source=probe/tools/issue_license.py:L75 | neighbors=[issue_license.py, issue(), keygen(), pubkey()]
- "utils_db": "db.py" | kind=code-symbol | source=manager/backend/app/utils/db.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, get_or_404(), Shared database helpers — single source…, 298a9d4 trim frontend to 7 core pages; …]
- "utils_hash": "hash.py" | kind=code-symbol | source=manager/backend/app/utils/hash.py:L1 | neighbors=[d1b4dd3 trim frontend to 7 core pages; …, dedup_hash(), Shared hashing utilities — deduplicatio…, 298a9d4 trim frontend to 7 core pages; …]
- "versions_0015_finding_risk_score_scale": "0015_finding_risk_score_scale.py" | kind=code-symbol | source=manager/backend/alembic/versions/0015_finding_risk_score_scale.py:L1 | neighbors=[1fe16c8 stable but some dead code, need…, downgrade(), upgrade(), Allow the documented 0-1000 finding ris…]
- "versions_0016_user_tenant_is_active": "0016_user_tenant_is_active.py" | kind=code-symbol | source=manager/backend/alembic/versions/0016_user_tenant_is_active.py:L1 | neighbors=[65f22a7 Add comprehensive tests for aut…, downgrade(), upgrade(), Add is_active to users and tenants; add…]
- "versions_0017_scan_job_attempts": "0017_scan_job_attempts.py" | kind=code-symbol | source=manager/backend/alembic/versions/0017_scan_job_attempts.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, downgrade(), upgrade(), Add fenced execution attempts for agent…]
- "versions_0018_probe_enrollment": "0018_probe_enrollment.py" | kind=code-symbol | source=manager/backend/alembic/versions/0018_probe_enrollment.py:L1 | neighbors=[b5ffcb0 Refactor Vedha probe installer …, downgrade(), upgrade(), Add Manager-approved device-key probe e…]
- "versions_0020_finding_resolution_lifecycle": "0020_finding_resolution_lifecycle.py" | kind=code-symbol | source=manager/backend/alembic/versions/0020_finding_resolution_lifecycle.py:L1 | neighbors=[ddb51f2 feat(resolution): add finding r…, downgrade(), upgrade(), Finding resolution lifecycle: coverage-…]
- "versions_0021_finding_verification": "0021_finding_verification.py" | kind=code-symbol | source=manager/backend/alembic/versions/0021_finding_verification.py:L1 | neighbors=[0fbec7d feat(verification): add finding…, downgrade(), upgrade(), Finding verification verdict columns (P…]
- "versions_0022_validation_requests": "0022_validation_requests.py" | kind=code-symbol | source=manager/backend/alembic/versions/0022_validation_requests.py:L1 | neighbors=[58c2d10 feat(active-validation): Valida…, downgrade(), upgrade(), Approval-gated safe active-validation r…]
- "versions_0023_customer_portal_foundation": "0023_customer_portal_foundation.py" | kind=code-symbol | source=manager/backend/alembic/versions/0023_customer_portal_foundation.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, downgrade(), upgrade(), Customer portal foundation (Part 2, Pha…]
- "versions_0025_service_exposure": "0025_service_exposure.py" | kind=code-symbol | source=manager/backend/alembic/versions/0025_service_exposure.py:L1 | neighbors=[22701ea Add tests for scanner parity an…, downgrade(), upgrade(), Service exposure: persist the exposure_…]
- "versions_0026_client_portal_slug": "0026_client_portal_slug.py" | kind=code-symbol | source=manager/backend/alembic/versions/0026_client_portal_slug.py:L1 | neighbors=[c4386e4 feat(customers): operator Custo…, downgrade(), upgrade(), Client portal slug — the customer's sta…]
- "versions_0027_scan_request_targets_intensity": "0027_scan_request_targets_intensity.py" | kind=code-symbol | source=manager/backend/alembic/versions/0027_scan_request_targets_intensity.py:L1 | neighbors=[35f02a9 feat(portal): rich scan request…, downgrade(), upgrade(), Scan-request targets + intensity — the …]
- "versions_0028_remediation_plans": "0028_remediation_plans.py" | kind=code-symbol | source=manager/backend/alembic/versions/0028_remediation_plans.py:L1 | neighbors=[fd5dc96 feat(remediation): AI + determi…, downgrade(), upgrade(), Remediation plans — cached, OS-specific…]
- "versions_0030_sla_policies": "0030_sla_policies.py" | kind=code-symbol | source=manager/backend/alembic/versions/0030_sla_policies.py:L1 | neighbors=[c5ebd38 feat(sla): per-tenant custom SL…, downgrade(), upgrade(), SLA policies — per-tenant custom remedi…]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-086.json

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
