# Node Description Batch 93 of 104

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

- "tests_test_exploit_engine_testmetasploitintegration_skip_without_flag": ".skip_without_flag()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L434 | neighbors=[TestMetasploitIntegration]
- "tests_test_exploit_engine_testmetasploitintegration_test_connect_and_list_modules": ".test_connect_and_list_modules()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L441 | neighbors=[TestMetasploitIntegration]
- "tests_test_exploit_engine_testmetasploitintegration_test_run_safe_scanner_smb": ".test_run_safe_scanner_smb()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L450 | neighbors=[TestMetasploitIntegration]
- "tests_test_exploit_engine_testmetasploitrpcclient_test_call_without_connect_raises": ".test_call_without_connect_raises()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L233 | neighbors=[TestMetasploitRPCClient]
- "tests_test_exploit_engine_testnucleiexploitrunner_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L351 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_evidence_truncated_to_max_bytes": ".test_evidence_truncated_to_max_bytes()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L405 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_extract_evidence_includes_curl": ".test_extract_evidence_includes_curl()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L395 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_nonexistent_template_not_safe": ".test_nonexistent_template_not_safe()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L369 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_parse_poc_output_hit": ".test_parse_poc_output_hit()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L374 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_parse_poc_output_malformed_json_skipped": ".test_parse_poc_output_malformed_json_skipped()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L389 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_parse_poc_output_miss": ".test_parse_poc_output_miss()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L380 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_parse_poc_output_wrong_cve": ".test_parse_poc_output_wrong_cve()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L385 | neighbors=[TestNucleiExploitRunner]
- "tests_test_exploit_engine_testnucleiexploitrunner_test_safe_template_passes": ".test_safe_template_passes()" | kind=code-symbol | source=manager/backend/tests/test_exploit_engine.py:L354 | neighbors=[TestNucleiExploitRunner]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Agentic VA Scanner/.graphify/description-instructions/batch-092.json

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
