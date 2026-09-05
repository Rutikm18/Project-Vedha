# Node Description Batch 314 of 336

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

- "tests_test_service_banner_ident_testparsehttphead_test_basic_auth_challenge": ".test_basic_auth_challenge()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L118 | neighbors=[TestParseHttpHead]
- "tests_test_service_banner_ident_testparsehttphead_test_non_http_is_empty": ".test_non_http_is_empty()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L128 | neighbors=[TestParseHttpHead]
- "tests_test_service_banner_ident_testparsehttphead_test_rtsp_is_http_shaped": ".test_rtsp_is_http_shaped()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L132 | neighbors=[TestParseHttpHead]
- "tests_test_service_banner_ident_testparsehttphead_test_status_server_title": ".test_status_server_title()" | kind=code-symbol | source=probe/tests/test_service_banner_ident.py:L109 | neighbors=[TestParseHttpHead]
- "tests_test_service_identifier_testserviceidentifier_setup_method": ".setup_method()" | kind=code-symbol | source=manager/backend/tests/test_service_identifier.py:L7 | neighbors=[TestServiceIdentifier]
- "tests_test_service_match_rationale_1": "test_service_match.py — Tier 2.5: service soft-matching (banner -> product/versi" | kind=entity | source=probe/tests/test_service_match.py:L1 | neighbors=[test_service_match.py]
- "tests_test_service_match_testhttpmatch_test_apache_version": ".test_apache_version()" | kind=code-symbol | source=probe/tests/test_service_match.py:L42 | neighbors=[TestHttpMatch]
- "tests_test_service_match_testhttpmatch_test_iis_version": ".test_iis_version()" | kind=code-symbol | source=probe/tests/test_service_match.py:L47 | neighbors=[TestHttpMatch]
- "tests_test_service_match_testhttpmatch_test_nginx_version": ".test_nginx_version()" | kind=code-symbol | source=probe/tests/test_service_match.py:L36 | neighbors=[TestHttpMatch]
- "tests_test_service_match_testhttpmatch_test_nginx_without_version": ".test_nginx_without_version()" | kind=code-symbol | source=probe/tests/test_service_match.py:L52 | neighbors=[TestHttpMatch]
- "tests_test_service_match_testnomatch_test_empty_returns_none": ".test_empty_returns_none()" | kind=code-symbol | source=probe/tests/test_service_match.py:L91 | neighbors=[TestNoMatch]
- "tests_test_service_match_testnomatch_test_unrecognized_returns_none": ".test_unrecognized_returns_none()" | kind=code-symbol | source=probe/tests/test_service_match.py:L88 | neighbors=[TestNoMatch]
- "tests_test_service_match_testotherservices_test_mariadb_handshake": ".test_mariadb_handshake()" | kind=code-symbol | source=probe/tests/test_service_match.py:L70 | neighbors=[TestOtherServices]
- "tests_test_service_match_testotherservices_test_redis_info": ".test_redis_info()" | kind=code-symbol | source=probe/tests/test_service_match.py:L77 | neighbors=[TestOtherServices]
- "tests_test_service_match_testotherservices_test_redis_noauth": ".test_redis_noauth()" | kind=code-symbol | source=probe/tests/test_service_match.py:L82 | neighbors=[TestOtherServices]
- "tests_test_service_match_testotherservices_test_smtp_postfix": ".test_smtp_postfix()" | kind=code-symbol | source=probe/tests/test_service_match.py:L65 | neighbors=[TestOtherServices]
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
- "tests_test_sla_policy_rationale_1": "test_sla_policy.py — per-tenant custom SLA windows (item 4)." | kind=entity | source=manager/backend/tests/test_sla_policy.py:L1 | neighbors=[test_sla_policy.py]
- "tests_test_smb_ldap_scanners_rationale_1": "test_smb_ldap_scanners.py — SMB null-session + LDAP anonymous-bind enumeration." | kind=entity | source=probe/tests/test_smb_ldap_scanners.py:L1 | neighbors=[test_smb_ldap_scanners.py]
- "tests_test_smb_ldap_scanners_rationale_136": "ldap3 packs receive_timeout into a struct for SO_RCVTIMEO, so it must be an" | kind=entity | source=probe/tests/test_smb_ldap_scanners.py:L136 | neighbors=[TestLDAPTimeoutTypes]
- "tests_test_smb_ldap_scanners_testldapscanner_sc": "._sc()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L104 | neighbors=[TestLDAPScanner]
- "tests_test_smb_ldap_scanners_testldapscanner_test_anon_refused_is_filtered": ".test_anon_refused_is_filtered()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L117 | neighbors=[TestLDAPScanner]
- "tests_test_smb_ldap_scanners_testldapscanner_test_anonymous_bind_open": ".test_anonymous_bind_open()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L108 | neighbors=[TestLDAPScanner]
- "tests_test_smb_ldap_scanners_testldapscanner_test_no_ldap_is_filtered": ".test_no_ldap_is_filtered()" | kind=code-symbol | source=probe/tests/test_smb_ldap_scanners.py:L126 | neighbors=[TestLDAPScanner]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-313.json

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
