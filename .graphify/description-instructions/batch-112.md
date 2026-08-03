# Node Description Batch 113 of 131

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

- "tests_test_exploit_engine_testnucleiexploitrunner_test_unsafe_template_blocked": ".test_unsafe_template_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L362 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testrequiresapproval_test_adcs_server": ".test_adcs_server()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L170 | neighbors=[TestRequiresApproval]
- "tests_test_exploit_engine_testrequiresapproval_test_critical_asset_needs_approval": ".test_critical_asset_needs_approval()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L155 | neighbors=[TestRequiresApproval]
- "tests_test_exploit_engine_testrequiresapproval_test_dc_hostname_needs_approval": ".test_dc_hostname_needs_approval()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L161 | neighbors=[TestRequiresApproval]
- "tests_test_exploit_engine_testrequiresapproval_test_dc02_pattern": ".test_dc02_pattern()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L164 | neighbors=[TestRequiresApproval]
- "tests_test_exploit_engine_testrequiresapproval_test_exchange_server": ".test_exchange_server()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L167 | neighbors=[TestRequiresApproval]
- "tests_test_exploit_engine_testrequiresapproval_test_medium_non_dc_no_approval": ".test_medium_non_dc_no_approval()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L158 | neighbors=[TestRequiresApproval]
- "tests_test_exploit_engine_testrequiresapproval_test_normal_workstation": ".test_normal_workstation()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L173 | neighbors=[TestRequiresApproval]
- "tests_test_exploit_engine_testvalidatemodule_test_dos_blocked": ".test_dos_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L108 | neighbors=[TestValidateModule]
- "tests_test_exploit_engine_testvalidatemodule_test_encoder_blocked": ".test_encoder_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L123 | neighbors=[TestValidateModule]
- "tests_test_exploit_engine_testvalidatemodule_test_exploit_module_allowed": ".test_exploit_module_allowed()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L120 | neighbors=[TestValidateModule]
- "tests_test_exploit_engine_testvalidatemodule_test_fuzzer_blocked": ".test_fuzzer_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L112 | neighbors=[TestValidateModule]
- "tests_test_exploit_engine_testvalidatemodule_test_scanner_module_allowed": ".test_scanner_module_allowed()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L105 | neighbors=[TestValidateModule]
- "tests_test_exploit_engine_testvalidatemodule_test_shell_to_meterpreter_blocked": ".test_shell_to_meterpreter_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L116 | neighbors=[TestValidateModule]
- "tests_test_exploit_engine_testvalidatepayload_test_allowed_payload_passes": ".test_allowed_payload_passes()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L64 | neighbors=[TestValidatePayload]
- "tests_test_exploit_engine_testvalidatepayload_test_bind_shell_blocked": ".test_bind_shell_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L76 | neighbors=[TestValidatePayload]
- "tests_test_exploit_engine_testvalidatepayload_test_encrypt_payload_blocked": ".test_encrypt_payload_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L98 | neighbors=[TestValidatePayload]
- "tests_test_exploit_engine_testvalidatepayload_test_generic_none_always_allowed": ".test_generic_none_always_allowed()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L95 | neighbors=[TestValidatePayload]
- "tests_test_exploit_engine_testvalidatepayload_test_meterpreter_blocked": ".test_meterpreter_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L68 | neighbors=[TestValidatePayload]
- "tests_test_exploit_engine_testvalidatepayload_test_reverse_tcp_blocked": ".test_reverse_tcp_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L72 | neighbors=[TestValidatePayload]
- "tests_test_exploit_engine_testvalidatepayload_test_unknown_payload_blocked": ".test_unknown_payload_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L80 | neighbors=[TestValidatePayload]
- "tests_test_exploit_engine_testvalidatepayload_test_windows_exec_bad_command_blocked": ".test_windows_exec_bad_command_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L87 | neighbors=[TestValidatePayload]
- "tests_test_exploit_engine_testvalidatepayload_test_windows_exec_rm_rf_blocked": ".test_windows_exec_rm_rf_blocked()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L91 | neighbors=[TestValidatePayload]
- "tests_test_exploit_engine_testvalidatepayload_test_windows_exec_whoami_allowed": ".test_windows_exec_whoami_allowed()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L84 | neighbors=[TestValidatePayload]
- "tests_test_exploit_engine_testvalidatescope_test_excluded_cidr_takes_priority": ".test_excluded_cidr_takes_priority()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L148 | neighbors=[TestValidateScope]
- "tests_test_exploit_engine_testvalidatescope_test_invalid_ip_fails": ".test_invalid_ip_fails()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L144 | neighbors=[TestValidateScope]
- "tests_test_exploit_engine_testvalidatescope_test_ip_in_excluded_fails": ".test_ip_in_excluded_fails()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L137 | neighbors=[TestValidateScope]
- "tests_test_exploit_engine_testvalidatescope_test_ip_in_scope_passes": ".test_ip_in_scope_passes()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L130 | neighbors=[TestValidateScope]
- "tests_test_exploit_engine_testvalidatescope_test_ip_out_of_scope_fails": ".test_ip_out_of_scope_fails()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L133 | neighbors=[TestValidateScope]
- "tests_test_exploit_engine_testvalidatescope_test_multiple_scope_cidrs": ".test_multiple_scope_cidrs()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L141 | neighbors=[TestValidateScope]
- "tests_test_external_engine_wrappers_test_masscan_nonzero_with_valid_output_is_degraded": "test_masscan_nonzero_with_valid_output_is_degraded()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L103 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_masscan_range_must_be_fully_in_scope": "test_masscan_range_must_be_fully_in_scope()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L123 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_masscan_timeout_is_not_zero_findings": "test_masscan_timeout_is_not_zero_findings()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L91 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_masscan_tolerates_partial_json_and_counts_bad_records": "test_masscan_tolerates_partial_json_and_counts_bad_records()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L82 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_nmap_empty_failure_is_not_zero_findings": "test_nmap_empty_failure_is_not_zero_findings()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L42 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_nmap_extra_args_accept_bounded_tuning": "test_nmap_extra_args_accept_bounded_tuning()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L29 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_nmap_extra_args_cannot_replace_validated_targets": "test_nmap_extra_args_cannot_replace_validated_targets()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L21 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_nmap_malformed_xml_is_an_explicit_parse_error": "test_nmap_malformed_xml_is_an_explicit_parse_error()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L60 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_external_engine_wrappers_test_nmap_xml_error_state_is_preserved_as_result": "test_nmap_xml_error_state_is_preserved_as_result()" | kind=code-symbol | source=probe/tests/test_external_engine_wrappers.py:L67 | neighbors=[test_external_engine_wrappers.py]
- "tests_test_finding_schema_test_finding_patch_accepts_documented_maximum_risk_score": "test_finding_patch_accepts_documented_maximum_risk_score()" | kind=code-symbol | source=manager/backend/tests/test_finding_schema.py:L9 | neighbors=[test_finding_schema.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-112.json

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
