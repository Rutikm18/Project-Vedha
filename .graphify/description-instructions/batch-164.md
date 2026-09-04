# Node Description Batch 165 of 332

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
- "tests_test_smtp_scanner_testsmtpfindings_test_hardened_is_silent": ".test_hardened_is_silent()" | kind=code-symbol | source=probe/tests/test_smtp_scanner.py:L62 | neighbors=[TestSMTPFindings, ._fact()]
- "tests_test_smtp_scanner_testsmtpfindings_test_user_enum_and_no_starttls": ".test_user_enum_and_no_starttls()" | kind=code-symbol | source=probe/tests/test_smtp_scanner.py:L55 | neighbors=[TestSMTPFindings, ._fact()]
- "tests_test_smtp_scanner_testsmtpscanner_test_no_smtp_filtered": ".test_no_smtp_filtered()" | kind=code-symbol | source=probe/tests/test_smtp_scanner.py:L44 | neighbors=[TestSMTPScanner, ._sc()]
- "tests_test_smtp_scanner_testsmtpscanner_test_open": ".test_open()" | kind=code-symbol | source=probe/tests/test_smtp_scanner.py:L36 | neighbors=[TestSMTPScanner, ._sc()]
- "tests_test_ssh_scanner_testevaluate_eval": "._eval()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L95 | neighbors=[TestEvaluate, _kexinit()]
- "tests_test_ssh_scanner_testfulldbcoverage_eval": "._eval()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L243 | neighbors=[TestFullDBCoverage, _kexinit()]
- "tests_test_ssh_scanner_testmainscriptsparity_test_main_scripts_scanner_and_findings_agree": ".test_main_scripts_scanner_and_findings_agree()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L316 | neighbors=[TestMainScriptsParity, _kexinit()]
- "tests_test_ssh_scanner_testnofalsepositives_eval": "._eval()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L272 | neighbors=[TestNoFalsePositives, _kexinit()]
- "tests_test_ssh_scanner_testparsekexinit_test_empty_language_list": ".test_empty_language_list()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L85 | neighbors=[TestParseKexinit, _kexinit()]
- "tests_test_ssh_scanner_testparsekexinit_test_handles_payload_without_leading_type_byte": ".test_handles_payload_without_leading_type_byte()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L79 | neighbors=[TestParseKexinit, _kexinit()]
- "tests_test_ssh_scanner_testparsekexinit_test_parses_all_name_lists": ".test_parses_all_name_lists()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L70 | neighbors=[TestParseKexinit, _kexinit()]
- "tests_test_ssh_scanner_testsshfindings_test_clean_server_raises_nothing": ".test_clean_server_raises_nothing()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L211 | neighbors=[TestSSHFindings, ._fact()]
- "tests_test_ssh_scanner_testsshfindings_test_terrapin_raises_finding": ".test_terrapin_raises_finding()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L206 | neighbors=[TestSSHFindings, ._fact()]
- "tests_test_ssh_scanner_testsshfindings_test_weak_algorithms_raise_finding": ".test_weak_algorithms_raise_finding()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L198 | neighbors=[TestSSHFindings, ._fact()]
- "tests_test_ssh_scanner_testsshscanner_test_weak_server_reports_open_with_failures": ".test_weak_server_reports_open_with_failures()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L169 | neighbors=[TestSSHScanner, _kexinit()]
- "tests_test_ssh_scanner_testsshstatustaxonomy_test_confirmed_ssh_open_with_parsed_banner": ".test_confirmed_ssh_open_with_parsed_banner()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L361 | neighbors=[TestSSHStatusTaxonomy, _kexinit()]
- "tests_test_ssh_scanner_testterrapin_test_chacha20_without_strict_kex_is_vulnerable": ".test_chacha20_without_strict_kex_is_vulnerable()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L153 | neighbors=[TestTerrapin, _kexinit()]
- "tests_test_ssh_scanner_testterrapin_test_strict_kex_present_is_not_vulnerable": ".test_strict_kex_present_is_not_vulnerable()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L145 | neighbors=[TestTerrapin, _kexinit()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-164.json

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
