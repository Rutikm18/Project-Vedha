# Node Description Batch 110 of 227

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

- "tests_test_e2e_engagement_to_findings_test_correlated_findings_cite_their_base_findings": "test_correlated_findings_cite_their_base_findings()" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L161 | neighbors=[test_e2e_engagement_to_findings.py, _vulnerable_host_facts()]
- "tests_test_e2e_engagement_to_findings_test_engagement_dispatch_reaches_probe_and_enforces_scope": "test_engagement_dispatch_reaches_probe_and_enforces_scope()" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L67 | neighbors=[test_e2e_engagement_to_findings.py, _manager()]
- "tests_test_e2e_engagement_to_findings_test_manager_correlation_finds_all_three_attack_paths": "test_manager_correlation_finds_all_three_attack_paths()" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L148 | neighbors=[test_e2e_engagement_to_findings.py, _vulnerable_host_facts()]
- "tests_test_e2e_engagement_to_findings_test_ntlm_relay_is_high_when_smbv1_present_medium_otherwise": "test_ntlm_relay_is_high_when_smbv1_present_medium_otherwise()" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L169 | neighbors=[test_e2e_engagement_to_findings.py, _vulnerable_host_facts()]
- "tests_test_e2e_engagement_to_findings_test_out_of_scope_target_is_refused_end_to_end": "test_out_of_scope_target_is_refused_end_to_end()" | kind=code-symbol | source=probe/tests/test_e2e_engagement_to_findings.py:L88 | neighbors=[test_e2e_engagement_to_findings.py, _manager()]
- "tests_test_engine_bridge_regression": "test_engine_bridge_regression.py" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_regression.py:L1 | neighbors=[937737b feat(resolution): reopen + flag…, test_reopen_flips_remediated_to_open_an…]
- "tests_test_engine_bridge_resolution": "test_engine_bridge_resolution.py" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_resolution.py:L1 | neighbors=[8cf23c2 feat(resolution): wire coverage…, test_run_records_coverage_and_invokes_r…]
- "tests_test_engine_bridge_verification": "test_engine_bridge_verification.py" | kind=code-symbol | source=manager/backend/tests/test_engine_bridge_verification.py:L1 | neighbors=[2fcec73 feat(verification): stamp verdi…, test_stamp_verification_sets_columns_wh…]
- "tests_test_exploit_engine_engagement": "_engagement()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L49 | neighbors=[test_exploit_engine.py, .test_validate_scope_out_of_range()]
- "tests_test_exploit_engine_pytest_addoption": "pytest_addoption()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L464 | neighbors=[test_exploit_engine.py, Register --msf-host CLI option for inte…]
- "tests_test_exploit_engine_testexploitorchestrator_test_generate_dns_callback_token_format": ".test_generate_dns_callback_token_format()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L290 | neighbors=[TestExploitOrchestrator, ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_generate_dns_callback_token_unique": ".test_generate_dns_callback_token_unique()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L298 | neighbors=[TestExploitOrchestrator, ._make_orchestrator()]
- "tests_test_exploit_engine_testexploitorchestrator_test_validate_safety_meterpreter_raises": ".test_validate_safety_meterpreter_raises()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L275 | neighbors=[TestExploitOrchestrator, ._make_orchestrator()]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_get_job_status_running": ".test_get_job_status_running()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L218 | neighbors=[TestMetasploitRPCClient, ._make_client()]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_kill_job": ".test_kill_job()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L227 | neighbors=[TestMetasploitRPCClient, ._make_client()]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_list_modules_exploit": ".test_list_modules_exploit()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L198 | neighbors=[TestMetasploitRPCClient, ._make_client()]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_run_module_error_raises": ".test_run_module_error_raises()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L212 | neighbors=[TestMetasploitRPCClient, ._make_client()]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_run_module_returns_job_id": ".test_run_module_returns_job_id()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L204 | neighbors=[TestMetasploitRPCClient, ._make_client()]
- "tests_test_finding_out_computed_test_confirmed_exploited_outranks_contradicted": "test_confirmed_exploited_outranks_contradicted()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L32 | neighbors=[test_finding_out_computed.py, _base()]
- "tests_test_finding_out_computed_test_explicit_risk_rank_is_preserved": "test_explicit_risk_rank_is_preserved()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L38 | neighbors=[test_finding_out_computed.py, _base()]
- "tests_test_finding_out_computed_test_lifecycle_fields_round_trip": "test_lifecycle_fields_round_trip()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L43 | neighbors=[test_finding_out_computed.py, _base()]
- "tests_test_finding_out_computed_test_risk_rank_is_computed_not_none": "test_risk_rank_is_computed_not_none()" | kind=code-symbol | source=manager/backend/tests/test_finding_out_computed.py:L26 | neighbors=[test_finding_out_computed.py, _base()]
- "tests_test_finding_reopen_endpoint_test_reopen_non_remediated_is_conflict": "test_reopen_non_remediated_is_conflict()" | kind=code-symbol | source=manager/backend/tests/test_finding_reopen_endpoint.py:L40 | neighbors=[test_finding_reopen_endpoint.py, _db_with()]
- "tests_test_finding_reopen_endpoint_test_reopen_remediated_finding_sets_open_and_audits": "test_reopen_remediated_finding_sets_open_and_audits()" | kind=code-symbol | source=manager/backend/tests/test_finding_reopen_endpoint.py:L23 | neighbors=[test_finding_reopen_endpoint.py, _db_with()]
- "tests_test_finding_resolution_schema": "test_finding_resolution_schema.py" | kind=code-symbol | source=manager/backend/tests/test_finding_resolution_schema.py:L1 | neighbors=[ddb51f2 feat(resolution): add finding r…, test_finding_has_resolution_lifecycle_c…]
- "tests_test_finding_risk_rank_api": "test_finding_risk_rank_api.py" | kind=code-symbol | source=manager/backend/tests/test_finding_risk_rank_api.py:L1 | neighbors=[85e4537 feat(risk-rank): expose risk_ra…, test_finding_schema_exposes_risk_rank()]
- "tests_test_finding_verification_api": "test_finding_verification_api.py" | kind=code-symbol | source=manager/backend/tests/test_finding_verification_api.py:L1 | neighbors=[72f68af feat(verification): expose veri…, test_finding_schema_exposes_verificatio…]
- "tests_test_finding_verification_schema": "test_finding_verification_schema.py" | kind=code-symbol | source=manager/backend/tests/test_finding_verification_schema.py:L1 | neighbors=[0fbec7d feat(verification): add finding…, test_finding_has_verification_columns()]
- "tests_test_installer_contract_test_installer_accepts_enroll_token_and_insecure_for_http_manager": "test_installer_accepts_enroll_token_and_insecure_for_http_manager()" | kind=code-symbol | source=probe/tests/test_installer_contract.py:L62 | neighbors=[test_installer_contract.py, _dry_run()]
- "tests_test_installer_contract_test_installer_without_token_still_shows_manual_approval": "test_installer_without_token_still_shows_manual_approval()" | kind=code-symbol | source=probe/tests/test_installer_contract.py:L76 | neighbors=[test_installer_contract.py, _dry_run()]
- "tests_test_integration_fake_run_scan": "_fake_run_scan()" | kind=code-symbol | source=probe/tests/test_integration.py:L41 | neighbors=[test_integration.py, Return a minimal valid scan result (no …]
- "tests_test_integration_testfulljoblifecycle_test_complete_flow_with_encrypted_scope": ".test_complete_flow_with_encrypted_scope()" | kind=code-symbol | source=probe/tests/test_integration.py:L314 | neighbors=[Simulate the full probe lifecycle from …, TestFullJobLifecycle]
- "tests_test_integration_testfulljoblifecycle_test_job_ot_passive_profile": ".test_job_ot_passive_profile()" | kind=code-symbol | source=probe/tests/test_integration.py:L408 | neighbors=[OT passive profile resolves correctly., TestFullJobLifecycle]
- "tests_test_integration_testfulljoblifecycle_test_job_rejected_all_targets_out_of_scope": ".test_job_rejected_all_targets_out_of_scope()" | kind=code-symbol | source=probe/tests/test_integration.py:L382 | neighbors=[All targets outside scope → job is reje…, TestFullJobLifecycle]
- "tests_test_integration_testidentityandencryption_test_different_key_cannot_decrypt": ".test_different_key_cannot_decrypt()" | kind=code-symbol | source=probe/tests/test_integration.py:L91 | neighbors=[A different probe cannot decrypt scope …, TestIdentityAndEncryption]
- "tests_test_integration_testidentityandencryption_test_full_identity_lifecycle": ".test_full_identity_lifecycle()" | kind=code-symbol | source=probe/tests/test_integration.py:L67 | neighbors=[Generate identity → encrypt scope → dec…, TestIdentityAndEncryption]
- "tests_test_integration_testidentityandencryption_test_scope_encryption_roundtrip": ".test_scope_encryption_roundtrip()" | kind=code-symbol | source=probe/tests/test_integration.py:L78 | neighbors=[Manager encrypts → probe decrypts., TestIdentityAndEncryption]
- "tests_test_integration_teststartupgauntlet_test_gauntlet_hw_bind_blocks": ".test_gauntlet_hw_bind_blocks()" | kind=code-symbol | source=probe/tests/test_integration.py:L442 | neighbors=[Wrong HW fingerprint blocks startup., TestStartupGauntlet]
- "tests_test_integration_teststartupgauntlet_test_gauntlet_skips_in_dev_mode": ".test_gauntlet_skips_in_dev_mode()" | kind=code-symbol | source=probe/tests/test_integration.py:L434 | neighbors=[With LICENSE_ENFORCED=false, gauntlet r…, TestStartupGauntlet]
- "tests_test_integration_testtaskrunnerwithencryptedscope_test_decrypts_encrypted_scope_from_job": ".test_decrypts_encrypted_scope_from_job()" | kind=code-symbol | source=probe/tests/test_integration.py:L103 | neighbors=[Job carries encrypted_scope → TaskRunne…, TestTaskRunnerWithEncryptedScope]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-109.json

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
