# Node Description Batch 166 of 336

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
- "tests_test_sla_policy_testpolicyawarecompute_test_custom_window_relaxes_state": ".test_custom_window_relaxes_state()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L27 | neighbors=[TestPolicyAwareCompute, _finding()]
- "tests_test_sla_policy_testpolicyawarecompute_test_default_window_breaches": ".test_default_window_breaches()" | kind=code-symbol | source=manager/backend/tests/test_sla_policy.py:L24 | neighbors=[TestPolicyAwareCompute, _finding()]
- "tests_test_smb_ntlm_build_testntlmfingerprintframing_test_end_to_end_framing_extracts_build": ".test_end_to_end_framing_extracts_build()" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L85 | neighbors=[TestNtlmFingerprintFraming, _challenge()]
- "tests_test_smb_ntlm_build_testntlmfingerprintframing_test_ntlm_os_build_shared_function": ".test_ntlm_os_build_shared_function()" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L113 | neighbors=[TestNtlmFingerprintFraming, _challenge()]
- "tests_test_smb_ntlm_build_testparsechallenge_test_legacy_6_1_is_win7": ".test_legacy_6_1_is_win7()" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L63 | neighbors=[TestParseChallenge, _challenge()]
- "tests_test_smb_ntlm_build_testparsechallenge_test_no_version_field_yields_name_but_no_build": ".test_no_version_field_yields_name_but_no_build()" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L66 | neighbors=[TestParseChallenge, _challenge()]
- "tests_test_smb_ntlm_build_testparsechallenge_test_server_2022_build_20348": ".test_server_2022_build_20348()" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L55 | neighbors=[TestParseChallenge, _challenge()]
- "tests_test_smb_ntlm_build_testparsechallenge_test_unknown_build_still_classified_win11_vs_win10": ".test_unknown_build_still_classified_win11_vs_win10()" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L59 | neighbors=[TestParseChallenge, _challenge()]
- "tests_test_smb_ntlm_build_testparsechallenge_test_win10_22h2": ".test_win10_22h2()" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L51 | neighbors=[TestParseChallenge, _challenge()]
- "tests_test_smb_ntlm_build_testparsechallenge_test_win11_24h2_build_26100": ".test_win11_24h2_build_26100()" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L39 | neighbors=[TestParseChallenge, _challenge()]
- "tests_test_smb_scanner_rationale_81": "FIX 4: 3.1.1 IS now advertised, together with the mandatory preauth-integrity" | kind=entity | source=probe/tests/test_smb_scanner.py:L81 | neighbors=[test_request_offers_311_with_preauth_co…, test_request_omits_311_without_preauth_…]
- "tests_test_smb_scanner_test_request_offers_311_with_preauth_context": "test_request_offers_311_with_preauth_context()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L80 | neighbors=[test_smb_scanner.py, FIX 4: 3.1.1 IS now advertised, togethe…]
- "tests_test_smb_scanner_test_request_omits_311_without_preauth_context": "test_request_omits_311_without_preauth_context()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L80 | neighbors=[test_smb_scanner.py, FIX 4: 3.1.1 IS now advertised, togethe…]
- "tests_test_smb_scanner_test_signing_not_required": "test_signing_not_required()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L38 | neighbors=[test_smb_scanner.py, _smb2_negotiate_response()]
- "tests_test_smb_scanner_test_signing_required_smb311": "test_signing_required_smb311()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L29 | neighbors=[test_smb_scanner.py, _smb2_negotiate_response()]
- "tests_test_smb_scanner_test_truncated_negotiate_body_not_parsed": "test_truncated_negotiate_body_not_parsed()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L62 | neighbors=[test_smb_scanner.py, A response with the wrong body Structur…]
- "tests_test_smtp_scanner_testparity": "TestParity" | kind=code-symbol | source=probe/tests/test_smtp_scanner.py:L73 | neighbors=[test_smtp_scanner.py, .test_main_scripts()]
- "tests_test_smtp_scanner_testsmtpfindings_test_expn_alone_triggers_enum": ".test_expn_alone_triggers_enum()" | kind=code-symbol | source=probe/tests/test_smtp_scanner.py:L67 | neighbors=[TestSMTPFindings, ._fact()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-165.json

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
