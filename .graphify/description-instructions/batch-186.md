# Node Description Batch 187 of 380

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

- "tests_test_service_identifier_testserviceidentifier_test_http_server_header": ".test_http_server_header()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L19 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_kerberos_banner": ".test_kerberos_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L48 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_ldap_banner": ".test_ldap_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L52 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_mssql_banner": ".test_mssql_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L44 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_mysql_banner": ".test_mysql_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L36 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_rdp_port_hint": ".test_rdp_port_hint()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L56 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_redis_pong": ".test_redis_pong()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L40 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_smb_detection": ".test_smb_detection()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L32 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_smtp_banner": ".test_smtp_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L24 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_ssh_banner": ".test_ssh_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L13 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_unknown_service_empty_banner": ".test_unknown_service_empty_banner()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L65 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_identifier_testserviceidentifier_test_version_extraction": ".test_version_extraction()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L61 | neighbors=[TestServiceIdentifier, ._id()]
- "tests_test_service_match_testscannerintegration": "TestScannerIntegration" | kind=code-symbol | source=probe/tests/test_service_match.py:L108 | neighbors=[test_service_match.py, .test_scanner_identifies_ssh_on_nonstan…]
- "tests_test_service_posture_rules_test_new_rules_agree_with_probe_findings_severity": "test_new_rules_agree_with_probe_findings_severity()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L227 | neighbors=[test_service_posture_rules.py, The manager and the probe's own finding…]
- "tests_test_service_posture_rules_test_smb_null_session_fires_when_permitted": "test_smb_null_session_fires_when_permitted()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L106 | neighbors=[test_service_posture_rules.py, _fire()]
- "tests_test_service_posture_rules_test_ssh_terrapin_fires_when_strict_kex_absent": "test_ssh_terrapin_fires_when_strict_kex_absent()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L80 | neighbors=[test_service_posture_rules.py, _fire()]
- "tests_test_service_posture_rules_test_ssh_weak_algorithms": "test_ssh_weak_algorithms()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L87 | neighbors=[test_service_posture_rules.py, _fire()]
- "tests_test_service_posture_rules_testnegatives_test_dns_refused_transfer": ".test_dns_refused_transfer()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L121 | neighbors=[TestNegatives, _fire()]
- "tests_test_service_posture_rules_testnegatives_test_ftp_without_anonymous": ".test_ftp_without_anonymous()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L117 | neighbors=[TestNegatives, _fire()]
- "tests_test_service_posture_rules_testnegatives_test_ipmi_cipher_zero_rejected": ".test_ipmi_cipher_zero_rejected()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L158 | neighbors=[TestNegatives, _fire()]
- "tests_test_service_posture_rules_testnegatives_test_ldap_bind_refused": ".test_ldap_bind_refused()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L130 | neighbors=[TestNegatives, _fire()]
- "tests_test_service_posture_rules_testnegatives_test_nfs_restricted_exports": ".test_nfs_restricted_exports()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L126 | neighbors=[TestNegatives, _fire()]
- "tests_test_service_posture_rules_testnegatives_test_rsync_auth_required": ".test_rsync_auth_required()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L153 | neighbors=[TestNegatives, _fire()]
- "tests_test_service_posture_rules_testnegatives_test_smtp_with_starttls": ".test_smtp_with_starttls()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L149 | neighbors=[TestNegatives, _fire()]
- "tests_test_service_posture_rules_testnegatives_test_vnc_weak_fires_when_it_is_the_only_option": ".test_vnc_weak_fires_when_it_is_the_only_option()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L144 | neighbors=[TestNegatives, _fire()]
- "tests_test_service_posture_rules_testnegatives_test_vnc_weak_suppressed_when_strong_type_offered": ".test_vnc_weak_suppressed_when_strong_type_offered()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L139 | neighbors=[TestNegatives, _fire()]
- "tests_test_service_posture_rules_testrdpnonla_test_fires_from_the_first_probe_when_it_negotiated": ".test_fires_from_the_first_probe_when_it_negotiated()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L176 | neighbors=[TestRdpNoNla, _fire()]
- "tests_test_service_posture_rules_testrdpnonla_test_silent_when_nla_is_required": ".test_silent_when_nla_is_required()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L182 | neighbors=[TestRdpNoNla, _fire()]
- "tests_test_service_posture_rules_testrdpnotls_test_silent_when_negotiation_succeeded": ".test_silent_when_negotiation_succeeded()" | kind=code-symbol | source=manager/detection_engine/tests/test_service_posture_rules.py:L209 | neighbors=[TestRdpNoTls, _fire()]
- "tests_test_servicenow_integration_testconfigvalidation": "TestConfigValidation" | kind=code-symbol | source=manager/backend/tests/test_servicenow_integration.py:L39 | neighbors=[test_servicenow_integration.py, .test_missing_config_raises_rather_than…]
- "tests_test_servicenow_integration_testincidentcreation_test_authenticates_with_the_stored_secret": ".test_authenticates_with_the_stored_secret()" | kind=code-symbol | source=manager/backend/tests/test_servicenow_integration.py:L72 | neighbors=[TestIncidentCreation, ._config()]
- "tests_test_servicenow_integration_testincidentcreation_test_deliver_routes_servicenow_and_reports_failure": ".test_deliver_routes_servicenow_and_reports_failure()" | kind=code-symbol | source=manager/backend/tests/test_servicenow_integration.py:L93 | neighbors=[End of the path: a broken integration r…, TestIncidentCreation]
- "tests_test_servicenow_integration_testincidentcreation_test_posts_an_incident_to_the_table_api": ".test_posts_an_incident_to_the_table_api()" | kind=code-symbol | source=manager/backend/tests/test_servicenow_integration.py:L59 | neighbors=[TestIncidentCreation, ._config()]
- "tests_test_servicenow_integration_testincidentcreation_test_subject_and_body_map_to_servicenow_fields": ".test_subject_and_body_map_to_servicenow_fields()" | kind=code-symbol | source=manager/backend/tests/test_servicenow_integration.py:L65 | neighbors=[TestIncidentCreation, ._config()]
- "tests_test_servicenow_integration_testregistration_test_existing_kinds_are_untouched": ".test_existing_kinds_are_untouched()" | kind=code-symbol | source=manager/backend/tests/test_servicenow_integration.py:L29 | neighbors=[Adding one must not disturb the integra…, TestRegistration]
- "tests_test_servicenow_integration_testregistration_test_sender_is_registered_for_dispatch": ".test_sender_is_registered_for_dispatch()" | kind=code-symbol | source=manager/backend/tests/test_servicenow_integration.py:L33 | neighbors=[A kind the API accepts but deliver() ca…, TestRegistration]
- "tests_test_sla_policy_testpolicyawarecompute_test_custom_window_relaxes_state": ".test_custom_window_relaxes_state()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L27 | neighbors=[TestPolicyAwareCompute, _finding()]
- "tests_test_sla_policy_testpolicyawarecompute_test_default_window_breaches": ".test_default_window_breaches()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L24 | neighbors=[TestPolicyAwareCompute, _finding()]
- "tests_test_smb_ntlm_build_testntlmfingerprintframing_test_end_to_end_framing_extracts_build": ".test_end_to_end_framing_extracts_build()" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L85 | neighbors=[TestNtlmFingerprintFraming, _challenge()]
- "tests_test_smb_ntlm_build_testntlmfingerprintframing_test_ntlm_os_build_shared_function": ".test_ntlm_os_build_shared_function()" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L113 | neighbors=[TestNtlmFingerprintFraming, _challenge()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-186.json

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
