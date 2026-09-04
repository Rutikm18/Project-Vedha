# Node Description Batch 310 of 332

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

- "tests_test_service_posture_rules_rationale_188": "The regression this fixes: `nla` was declared in `requires` even though" | kind=entity | source=manager/detection_engine/tests/test_service_posture_rules.py:L188 | neighbors=[.test_no_longer_reports_schema_drift()]
- "tests_test_service_posture_rules_rationale_204": "Only codes carrying posture meaning fire; the rest are transport noise." | kind=entity | source=manager/detection_engine/tests/test_service_posture_rules.py:L204 | neighbors=[.test_ignores_uninterpreted_failure_cod…]
- "tests_test_service_posture_rules_rationale_218": "None of the new service scanners is rig-validated, so their findings must     NO" | kind=entity | source=manager/detection_engine/tests/test_service_posture_rules.py:L218 | neighbors=[test_experimental_scanner_findings_are_…]
- "tests_test_service_posture_rules_rationale_228": "The manager and the probe's own findings.py must not disagree about how     seri" | kind=entity | source=manager/detection_engine/tests/test_service_posture_rules.py:L228 | neighbors=[test_new_rules_agree_with_probe_finding…]
- "tests_test_service_posture_rules_rationale_42": "The captured fact for one scanner, straight from the probe corpus." | kind=entity | source=manager/detection_engine/tests/test_service_posture_rules.py:L42 | neighbors=[_corpus()]
- "tests_test_service_posture_rules_rationale_73": "The live Windows host offers OpenSSH 9.5 with strict-kex, so Terrapin must     N" | kind=entity | source=manager/detection_engine/tests/test_service_posture_rules.py:L73 | neighbors=[test_ssh_rules_against_live_capture()]
- "tests_test_service_posture_rules_rationale_99": "The live host REFUSED the null bind (STATUS_ACCESS_DENIED) — the secure     outc" | kind=entity | source=manager/detection_engine/tests/test_service_posture_rules.py:L99 | neighbors=[test_smb_null_session_is_silent_on_the_…]
- "tests_test_sla_policy_rationale_1": "test_sla_policy.py — per-tenant custom SLA windows (item 4)." | kind=entity | source=manager/backend/tests/test_sla_policy.py:L1 | neighbors=[test_sla_policy.py]
- "tests_test_smb_ldap_scanners_rationale_1": "test_smb_ldap_scanners.py — SMB null-session + LDAP anonymous-bind enumeration." | kind=entity | source=probe/tests/test_smb_ldap_scanners.py:L1 | neighbors=[test_smb_ldap_scanners.py]
- "tests_test_smb_ldap_scanners_rationale_136": "ldap3 packs receive_timeout into a struct for SO_RCVTIMEO, so it must be an" | kind=entity | source=probe/tests/test_smb_ldap_scanners.py:L136 | neighbors=[TestLDAPTimeoutTypes]
- "tests_test_smb_ldap_scanners_testldapscanner_sc": "._sc()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L104 | neighbors=[TestLDAPScanner]
- "tests_test_smb_ldap_scanners_testldapscanner_test_anon_refused_is_filtered": ".test_anon_refused_is_filtered()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L117 | neighbors=[TestLDAPScanner]
- "tests_test_smb_ldap_scanners_testldapscanner_test_anonymous_bind_open": ".test_anonymous_bind_open()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L108 | neighbors=[TestLDAPScanner]
- "tests_test_smb_ldap_scanners_testldapscanner_test_no_ldap_is_filtered": ".test_no_ldap_is_filtered()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L126 | neighbors=[TestLDAPScanner]
- "tests_test_smb_ldap_scanners_testldaptimeouttypes_test_receive_timeout_is_an_int": ".test_receive_timeout_is_an_int()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L142 | neighbors=[TestLDAPTimeoutTypes]
- "tests_test_smb_ldap_scanners_testldaptimeouttypes_test_sub_second_timeout_does_not_floor_to_zero": ".test_sub_second_timeout_does_not_floor_to_zero()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L175 | neighbors=[TestLDAPTimeoutTypes]
- "tests_test_smb_ldap_scanners_testmainscriptsparity_test_main_scripts_findings_derive_smb_and_ldap": ".test_main_scripts_findings_derive_smb_and_ldap()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L258 | neighbors=[TestMainScriptsParity]
- "tests_test_smb_ldap_scanners_testmainscriptsparity_test_scanners_import_in_both_trees": ".test_scanners_import_in_both_trees()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L252 | neighbors=[TestMainScriptsParity]
- "tests_test_smb_ldap_scanners_testmergeusers_test_decode_strips_nul": ".test_decode_strips_nul()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L56 | neighbors=[TestMergeUsers]
- "tests_test_smb_ldap_scanners_testmergeusers_test_dedup_samr_wins": ".test_dedup_samr_wins()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L47 | neighbors=[TestMergeUsers]
- "tests_test_smb_ldap_scanners_testridranges_test_is_bounded_no_brute_sweep": ".test_is_bounded_no_brute_sweep()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L41 | neighbors=[TestRidRanges]
- "tests_test_smb_ldap_scanners_testridranges_test_parses_enum4linux_default": ".test_parses_enum4linux_default()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L29 | neighbors=[TestRidRanges]
- "tests_test_smb_ldap_scanners_testridranges_test_reversed_range_tolerated": ".test_reversed_range_tolerated()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L38 | neighbors=[TestRidRanges]
- "tests_test_smb_ldap_scanners_testridranges_test_single_and_bad_tokens": ".test_single_and_bad_tokens()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L34 | neighbors=[TestRidRanges]
- "tests_test_smb_ldap_scanners_testsmbenumscanner_sc": "._sc()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L63 | neighbors=[TestSMBEnumScanner]
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

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-309.json

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
