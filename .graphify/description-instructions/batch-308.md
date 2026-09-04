# Node Description Batch 309 of 330

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

- "tests_test_smb_ldap_scanners_testsmbenumscanner_test_impacket_missing_is_error": ".test_impacket_missing_is_error()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L94 | neighbors=[TestSMBEnumScanner]
- "tests_test_smb_ldap_scanners_testsmbenumscanner_test_no_smb_is_filtered": ".test_no_smb_is_filtered()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L88 | neighbors=[TestSMBEnumScanner]
- "tests_test_smb_ldap_scanners_testsmbenumscanner_test_null_refused_is_open_but_secure": ".test_null_refused_is_open_but_secure()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L78 | neighbors=[TestSMBEnumScanner]
- "tests_test_smb_ldap_scanners_testsmbenumscanner_test_null_session_open_with_shares_and_users": ".test_null_session_open_with_shares_and_users()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L67 | neighbors=[TestSMBEnumScanner]
- "tests_test_smb_ldap_scanners_testsmbldapfindings_test_ldap_anon_bind_and_search": ".test_ldap_anon_bind_and_search()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L225 | neighbors=[TestSMBLDAPFindings]
- "tests_test_smb_ldap_scanners_testsmbldapfindings_test_ldap_anon_bind_only_no_search": ".test_ldap_anon_bind_only_no_search()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L235 | neighbors=[TestSMBLDAPFindings]
- "tests_test_smb_ldap_scanners_testsmbldapfindings_test_ldap_secure_is_silent": ".test_ldap_secure_is_silent()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L243 | neighbors=[TestSMBLDAPFindings]
- "tests_test_smb_ldap_scanners_testsmbldapfindings_test_smb_null_session_and_users": ".test_smb_null_session_and_users()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L206 | neighbors=[TestSMBLDAPFindings]
- "tests_test_smb_ldap_scanners_testsmbldapfindings_test_smb_secure_is_silent": ".test_smb_secure_is_silent()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L220 | neighbors=[TestSMBLDAPFindings]
- "tests_test_smb_ntlm_build_rationale_1": "test_smb_ntlm_build.py — Card 5: exact Windows build from the SMB2 pre-auth NTLM" | kind=entity | source=probe/tests/test_smb_ntlm_build.py:L1 | neighbors=[test_smb_ntlm_build.py]
- "tests_test_smb_ntlm_build_rationale_18": "Synthesize an NTLMSSP CHALLENGE (Type-2). TargetName payload sits right after" | kind=entity | source=probe/tests/test_smb_ntlm_build.py:L18 | neighbors=[_challenge()]
- "tests_test_smb_ntlm_build_rationale_80": "Regression: _recv_smb_frame STRIPS the 4-byte NBT prefix, so the SMB2 header" | kind=entity | source=probe/tests/test_smb_ntlm_build.py:L80 | neighbors=[TestNtlmFingerprintFraming]
- "tests_test_smb_ntlm_build_testbuildmap_test_client_server_shared_build_surfaces_both": ".test_client_server_shared_build_surfaces_both()" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L134 | neighbors=[TestBuildMap]
- "tests_test_smb_ntlm_build_testbuildmap_test_confidence_high_on_exact_match": ".test_confidence_high_on_exact_match()" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L139 | neighbors=[TestBuildMap]
- "tests_test_smb_ntlm_build_testparsechallenge_test_non_challenge_returns_none": ".test_non_challenge_returns_none()" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L72 | neighbors=[TestParseChallenge]
- "tests_test_smb_ntlm_build_testtype1andspnego_test_session_setup_packet_shape": ".test_session_setup_packet_shape()" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L158 | neighbors=[TestType1AndSpnego]
- "tests_test_smb_ntlm_build_testtype1andspnego_test_spnego_wraps_and_contains_type1": ".test_spnego_wraps_and_contains_type1()" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L151 | neighbors=[TestType1AndSpnego]
- "tests_test_smb_ntlm_build_testtype1andspnego_test_type1_sets_negotiate_version": ".test_type1_sets_negotiate_version()" | kind=code-symbol | source=probe/tests/test_smb_ntlm_build.py:L144 | neighbors=[TestType1AndSpnego]
- "tests_test_smb_scanner_rationale_15": "An SMB2 ERROR response (e.g. STATUS_INVALID_PARAMETER). Windows returns     this" | kind=entity | source=probe/tests/test_smb_scanner.py:L15 | neighbors=[_smb2_error_response()]
- "tests_test_smb_scanner_rationale_51": "The confirmed bug: an SMB2 error response (STATUS_INVALID_PARAMETER) was     rea" | kind=entity | source=probe/tests/test_smb_scanner.py:L51 | neighbors=[test_error_response_not_parsed_as_signi…]
- "tests_test_smb_scanner_rationale_63": "A response with the wrong body StructureSize is not a valid NEGOTIATE." | kind=entity | source=probe/tests/test_smb_scanner.py:L63 | neighbors=[test_truncated_negotiate_body_not_parse…]
- "tests_test_smb_scanner_rationale_72": "Step 13: expose signing_supported (protocol-precise), not only the     ambiguous" | kind=entity | source=probe/tests/test_smb_scanner.py:L72 | neighbors=[test_signing_supported_field_present()]
- "tests_test_smb_scanner_test_garbage_response": "test_garbage_response()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L44 | neighbors=[test_smb_scanner.py]
- "tests_test_smtp_scanner_rationale_1": "test_smtp_scanner.py — SMTP hygiene (VRFY/EXPN user-enum + STARTTLS presence)." | kind=entity | source=probe/tests/test_smtp_scanner.py:L1 | neighbors=[test_smtp_scanner.py]
- "tests_test_smtp_scanner_testparity_test_main_scripts": ".test_main_scripts()" | kind=code-symbol | source=probe/tests/test_smtp_scanner.py:L74 | neighbors=[TestParity]
- "tests_test_smtp_scanner_testpurelogic_test_parse_ehlo_capabilities": ".test_parse_ehlo_capabilities()" | kind=code-symbol | source=probe/tests/test_smtp_scanner.py:L18 | neighbors=[TestPureLogic]
- "tests_test_smtp_scanner_testpurelogic_test_vrfy_leaks": ".test_vrfy_leaks()" | kind=code-symbol | source=probe/tests/test_smtp_scanner.py:L23 | neighbors=[TestPureLogic]
- "tests_test_ssh_scanner_rationale_1": "test_ssh_scanner.py — SSH configuration audit (Tier 2.x, §6 of the VA checklist)" | kind=entity | source=probe/tests/test_ssh_scanner.py:L1 | neighbors=[test_ssh_scanner.py]
- "tests_test_ssh_scanner_rationale_30": "Encode an SSH name-list: uint32 length + comma-joined ASCII." | kind=entity | source=probe/tests/test_ssh_scanner.py:L30 | neighbors=[_nl()]
- "tests_test_ssh_scanner_testevaluate_test_arcfour_is_rc4_failure": ".test_arcfour_is_rc4_failure()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L114 | neighbors=[TestEvaluate]
- "tests_test_ssh_scanner_testevaluate_test_cbc_cipher_is_warning_not_failure": ".test_cbc_cipher_is_warning_not_failure()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L108 | neighbors=[TestEvaluate]
- "tests_test_ssh_scanner_testevaluate_test_group1_sha1_is_failure_with_modulus_and_sha1_reasons": ".test_group1_sha1_is_failure_with_modulus_and_sha1_reasons()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L99 | neighbors=[TestEvaluate]
- "tests_test_ssh_scanner_testevaluate_test_hmac_md5_is_failure": ".test_hmac_md5_is_failure()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L119 | neighbors=[TestEvaluate]
- "tests_test_ssh_scanner_testevaluate_test_modern_set_is_clean": ".test_modern_set_is_clean()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L129 | neighbors=[TestEvaluate]
- "tests_test_ssh_scanner_testevaluate_test_ssh_rsa_hostkey_is_sha1_failure": ".test_ssh_rsa_hostkey_is_sha1_failure()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L124 | neighbors=[TestEvaluate]
- "tests_test_ssh_scanner_testevaluate_test_unknown_algorithm_is_recorded_not_failed": ".test_unknown_algorithm_is_recorded_not_failed()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L135 | neighbors=[TestEvaluate]
- "tests_test_ssh_scanner_testfulldbcoverage_test_3des_ctr_cipher_is_failure": ".test_3des_ctr_cipher_is_failure()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L252 | neighbors=[TestFullDBCoverage]
- "tests_test_ssh_scanner_testfulldbcoverage_test_gss_kex_offered_by_server_is_failure": ".test_gss_kex_offered_by_server_is_failure()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L262 | neighbors=[TestFullDBCoverage]
- "tests_test_ssh_scanner_testfulldbcoverage_test_hmac_ripemd160_is_failure": ".test_hmac_ripemd160_is_failure()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L257 | neighbors=[TestFullDBCoverage]
- "tests_test_ssh_scanner_testfulldbcoverage_test_rijndael_cbc_cipher_is_failure": ".test_rijndael_cbc_cipher_is_failure()" | kind=code-symbol | source=probe/tests/test_ssh_scanner.py:L247 | neighbors=[TestFullDBCoverage]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-308.json

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
