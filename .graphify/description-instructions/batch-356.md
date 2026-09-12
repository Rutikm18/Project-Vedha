# Node Description Batch 357 of 380

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
For an entity node (any other kind — e.g. a person, place, event, object),
describe what the entity is and its role, grounded in its type, its
relations (neighbors) and the provided citations/evidence — e.g.
"Lady Carfax, a wealthy heiress who disappears en route to Lausanne.".
Ground entity descriptions in the citations/evidence when present; do not
speculate beyond the context, so a node with no supporting context may be
left out of the reply.
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_service_match_testotherservices_test_vsftpd": ".test_vsftpd()" | kind=code-symbol | source=probe/tests/test_service_match.py:L59 | neighbors=[TestOtherServices]
- "tests_test_service_match_testprobeladder_test_ladder_has_http_and_generic": ".test_ladder_has_http_and_generic()" | kind=code-symbol | source=probe/tests/test_service_match.py:L102 | neighbors=[TestProbeLadder]
- "tests_test_service_match_testprobeladder_test_ladder_starts_with_null_probe": ".test_ladder_starts_with_null_probe()" | kind=code-symbol | source=probe/tests/test_service_match.py:L96 | neighbors=[TestProbeLadder]
- "tests_test_service_match_testscannerintegration_test_scanner_identifies_ssh_on_nonstandard_port": ".test_scanner_identifies_ssh_on_nonstandard_port()" | kind=code-symbol | source=probe/tests/test_service_match.py:L109 | neighbors=[TestScannerIntegration]
- "tests_test_service_match_testsshmatch_test_dropbear": ".test_dropbear()" | kind=code-symbol | source=probe/tests/test_service_match.py:L23 | neighbors=[TestSshMatch]
- "tests_test_service_match_testsshmatch_test_generic_ssh": ".test_generic_ssh()" | kind=code-symbol | source=probe/tests/test_service_match.py:L29 | neighbors=[TestSshMatch]
- "tests_test_service_match_testsshmatch_test_openssh_version": ".test_openssh_version()" | kind=code-symbol | source=probe/tests/test_service_match.py:L17 | neighbors=[TestSshMatch]
- "tests_test_service_posture_rules_rationale_1": "test_service_posture_rules.py — the service-layer rule pack.  These 14 rules cov" | kind=entity | source=manager/detection_engine/tests/test_service_posture_rules.py:L1 | neighbors=[test_service_posture_rules.py]
- "tests_test_service_posture_rules_rationale_135": "no-auth is strictly worse and is reported instead." | kind=entity | source=manager/detection_engine/tests/test_service_posture_rules.py:L135 | neighbors=[.test_vnc_weak_suppressed_when_no_auth_…]
- "tests_test_service_posture_rules_rationale_168": "The live-host case: negotiation returned RDP_NEG_FAILURE so no `nla`         key" | kind=entity | source=manager/detection_engine/tests/test_service_posture_rules.py:L168 | neighbors=[.test_fires_from_the_second_probe_when_…]
- "tests_test_service_posture_rules_rationale_188": "The regression this fixes: `nla` was declared in `requires` even though" | kind=entity | source=manager/detection_engine/tests/test_service_posture_rules.py:L188 | neighbors=[.test_no_longer_reports_schema_drift()]
- "tests_test_service_posture_rules_rationale_204": "Only codes carrying posture meaning fire; the rest are transport noise." | kind=entity | source=manager/detection_engine/tests/test_service_posture_rules.py:L204 | neighbors=[.test_ignores_uninterpreted_failure_cod…]
- "tests_test_service_posture_rules_rationale_218": "None of the new service scanners is rig-validated, so their findings must     NO" | kind=entity | source=manager/detection_engine/tests/test_service_posture_rules.py:L218 | neighbors=[test_experimental_scanner_findings_are_…]
- "tests_test_service_posture_rules_rationale_228": "The manager and the probe's own findings.py must not disagree about how     seri" | kind=entity | source=manager/detection_engine/tests/test_service_posture_rules.py:L228 | neighbors=[test_new_rules_agree_with_probe_finding…]
- "tests_test_service_posture_rules_rationale_42": "The captured fact for one scanner, straight from the probe corpus." | kind=entity | source=manager/detection_engine/tests/test_service_posture_rules.py:L42 | neighbors=[_corpus()]
- "tests_test_service_posture_rules_rationale_73": "The live Windows host offers OpenSSH 9.5 with strict-kex, so Terrapin must     N" | kind=entity | source=manager/detection_engine/tests/test_service_posture_rules.py:L73 | neighbors=[test_ssh_rules_against_live_capture()]
- "tests_test_service_posture_rules_rationale_99": "The live host REFUSED the null bind (STATUS_ACCESS_DENIED) — the secure     outc" | kind=entity | source=manager/detection_engine/tests/test_service_posture_rules.py:L99 | neighbors=[test_smb_null_session_is_silent_on_the_…]
- "tests_test_service_rationale_1": "Phase 9 — per-OS service install: units rendered FROM the config object, with re" | kind=entity | source=probe/tests/test_service.py:L1 | neighbors=[test_service.py]
- "tests_test_service_test_activation_commands_per_os": "test_activation_commands_per_os()" | kind=code-symbol | source=probe/tests/test_service.py:L38 | neighbors=[test_service.py]
- "tests_test_service_test_install_writes_unit_then_uninstall_removes_it": "test_install_writes_unit_then_uninstall_removes_it()" | kind=code-symbol | source=probe/tests/test_service.py:L52 | neighbors=[test_service.py]
- "tests_test_service_test_launchd_plist_restart_on_failure_only": "test_launchd_plist_restart_on_failure_only()" | kind=code-symbol | source=probe/tests/test_service.py:L23 | neighbors=[test_service.py]
- "tests_test_service_test_systemd_unit_has_limits_env_and_statedir": "test_systemd_unit_has_limits_env_and_statedir()" | kind=code-symbol | source=probe/tests/test_service.py:L12 | neighbors=[test_service.py]
- "tests_test_service_test_uninstall_commands_per_os": "test_uninstall_commands_per_os()" | kind=code-symbol | source=probe/tests/test_service.py:L45 | neighbors=[test_service.py]
- "tests_test_service_test_windows_task_is_a_schtasks_command": "test_windows_task_is_a_schtasks_command()" | kind=code-symbol | source=probe/tests/test_service.py:L31 | neighbors=[test_service.py]
- "tests_test_servicenow_integration_rationale_1": "ServiceNow incident creation.  \"No ticketing integration (Jira, ServiceNow)\" was" | kind=entity | source=manager/backend/tests/test_servicenow_integration.py:L1 | neighbors=[test_servicenow_integration.py]
- "tests_test_servicenow_integration_rationale_30": "Adding one must not disturb the integrations already in use." | kind=entity | source=manager/backend/tests/test_servicenow_integration.py:L30 | neighbors=[.test_existing_kinds_are_untouched()]
- "tests_test_servicenow_integration_rationale_34": "A kind the API accepts but deliver() cannot route would accept         configura" | kind=entity | source=manager/backend/tests/test_servicenow_integration.py:L34 | neighbors=[.test_sender_is_registered_for_dispatch…]
- "tests_test_servicenow_integration_rationale_78": "Not every org files security work as `incident`." | kind=entity | source=manager/backend/tests/test_servicenow_integration.py:L78 | neighbors=[.test_target_table_is_configurable()]
- "tests_test_servicenow_integration_rationale_85": "deliver() owns the catch-and-log policy; the sender must not swallow         err" | kind=entity | source=manager/backend/tests/test_servicenow_integration.py:L85 | neighbors=[.test_http_failure_propagates_to_delive…]
- "tests_test_servicenow_integration_rationale_94": "End of the path: a broken integration returns False, never raises." | kind=entity | source=manager/backend/tests/test_servicenow_integration.py:L94 | neighbors=[.test_deliver_routes_servicenow_and_rep…]
- "tests_test_servicenow_integration_testconfigvalidation_test_missing_config_raises_rather_than_silently_passing": ".test_missing_config_raises_rather_than_silently_passing()" | kind=code-symbol | source=manager/backend/tests/test_servicenow_integration.py:L47 | neighbors=[TestConfigValidation]
- "tests_test_servicenow_integration_testregistration_test_servicenow_is_an_accepted_kind": ".test_servicenow_is_an_accepted_kind()" | kind=code-symbol | source=manager/backend/tests/test_servicenow_integration.py:L26 | neighbors=[TestRegistration]
- "tests_test_setup_cli_rationale_1": "Phase 7 — brain CLI: parser wiring + doctor runs. No network required for the pa" | kind=entity | source=probe/tests/test_setup_cli.py:L1 | neighbors=[test_setup_cli.py]
- "tests_test_setup_cli_test_connect_requires_manager": "test_connect_requires_manager()" | kind=code-symbol | source=probe/tests/test_setup_cli.py:L23 | neighbors=[test_setup_cli.py]
- "tests_test_setup_cli_test_doctor_command_returns_int_and_reports": "test_doctor_command_returns_int_and_reports()" | kind=code-symbol | source=probe/tests/test_setup_cli.py:L31 | neighbors=[test_setup_cli.py]
- "tests_test_setup_cli_test_parser_accepts_all_subcommands": "test_parser_accepts_all_subcommands()" | kind=code-symbol | source=probe/tests/test_setup_cli.py:L8 | neighbors=[test_setup_cli.py]
- "tests_test_setup_cli_test_strict_and_insecure_flags_parse": "test_strict_and_insecure_flags_parse()" | kind=code-symbol | source=probe/tests/test_setup_cli.py:L16 | neighbors=[test_setup_cli.py]
- "tests_test_sla_policy_rationale_1": "test_sla_policy.py — per-tenant custom SLA windows (item 4)." | kind=entity | source=manager/backend/tests/test_sla_policy.py:L1 | neighbors=[test_sla_policy.py]
- "tests_test_smb_ldap_scanners_rationale_1": "test_smb_ldap_scanners.py — SMB null-session + LDAP anonymous-bind enumeration." | kind=entity | source=probe/tests/test_smb_ldap_scanners.py:L1 | neighbors=[test_smb_ldap_scanners.py]
- "tests_test_smb_ldap_scanners_rationale_136": "ldap3 packs receive_timeout into a struct for SO_RCVTIMEO, so it must be an" | kind=entity | source=probe/tests/test_smb_ldap_scanners.py:L136 | neighbors=[TestLDAPTimeoutTypes]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-356.json

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
