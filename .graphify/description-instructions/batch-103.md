# Node Description Batch 104 of 209

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

- "tests_test_main_scripts_errno_test_unknown_errno_is_self_identifying_and_never_filtered": "test_unknown_errno_is_self_identifying_and_never_filtered()" | kind=code-symbol | source=probe/tests/test_main_scripts_errno.py:L36 | neighbors=[test_main_scripts_errno.py, _oserr()]
- "tests_test_main_scripts_findings_test_accepts_scanresult_objects_not_just_dicts": "test_accepts_scanresult_objects_not_just_dicts()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L282 | neighbors=[test_main_scripts_findings.py, _ids()]
- "tests_test_main_scripts_findings_test_confirmed_and_port_hint_do_not_double_report": "test_confirmed_and_port_hint_do_not_double_report()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L199 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_confirmed_ftp_cleartext_is_high_confidence": "test_confirmed_ftp_cleartext_is_high_confidence()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L190 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_confirmed_redis_is_high_confidence_even_on_nonstandard_port": "test_confirmed_redis_is_high_confidence_even_on_nonstandard_port()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L172 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_dangerous_http_methods_medium": "test_dangerous_http_methods_medium()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L210 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_every_finding_is_evidence_backed": "test_every_finding_is_evidence_backed()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L265 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_exposed_redis_is_high_exposure_medium_confidence": "test_exposed_redis_is_high_exposure_medium_confidence()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L133 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_findings_are_deduped_by_rule_target_port": "test_findings_are_deduped_by_rule_target_port()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L245 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_findings_sorted_most_severe_first": "test_findings_sorted_most_severe_first()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L251 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_missing_security_headers_is_low": "test_missing_security_headers_is_low()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L222 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_no_finding_carries_a_cve_id": "test_no_finding_carries_a_cve_id()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L259 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_port_only_datastore_is_medium_confidence_and_labeled_unconfirmed": "test_port_only_datastore_is_medium_confidence_and_labeled_unconfirmed()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L183 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_rdp_exposed_medium": "test_rdp_exposed_medium()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L140 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_server_version_disclosure_is_info": "test_server_version_disclosure_is_info()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L216 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_smbv1_enabled_is_high": "test_smbv1_enabled_is_high()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L63 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_snmp_default_community_is_high": "test_snmp_default_community_is_high()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L84 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_snmp_nondefault_community_is_medium": "test_snmp_nondefault_community_is_medium()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L91 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_summarize_counts_by_severity_and_actionable": "test_summarize_counts_by_severity_and_actionable()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L273 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_telnet_is_high_cleartext": "test_telnet_is_high_cleartext()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L127 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_tls_obsolete_protocol_is_high": "test_tls_obsolete_protocol_is_high()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L24 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_tls_weak_cipher_is_high_with_reasons": "test_tls_weak_cipher_is_high_with_reasons()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L47 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_x_powered_by_disclosure_is_info": "test_x_powered_by_disclosure_is_info()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L238 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_hardening_scope": "_scope()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L32 | neighbors=[test_main_scripts_hardening.py, ._scanner()]
- "tests_test_main_scripts_hardening_testsmbparsing_test_error_response_not_trusted": ".test_error_response_not_trusted()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L132 | neighbors=[TestSmbParsing, make_smb2_error()]
- "tests_test_main_scripts_hardening_testsmbparsing_test_success_response_signing_and_dialect": ".test_success_response_signing_and_dialect()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L139 | neighbors=[TestSmbParsing, make_smb2_success()]
- "tests_test_main_scripts_hardening_testsmbparsing_test_success_signing_supported_not_required": ".test_success_signing_supported_not_required()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L147 | neighbors=[TestSmbParsing, make_smb2_success()]
- "tests_test_main_scripts_ja4s_ext": "_ext()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4s.py:L17 | neighbors=[test_main_scripts_ja4s.py, _serverhello()]
- "tests_test_main_scripts_ja4s_test_ja4s_from_serverhello_tls13": "test_ja4s_from_serverhello_tls13()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4s.py:L62 | neighbors=[test_main_scripts_ja4s.py, _serverhello()]
- "tests_test_main_scripts_ja4x_fake_cert": "_fake_cert()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L52 | neighbors=[test_main_scripts_ja4x.py, test_ja4x_from_cert_matches_pure_core()]
- "tests_test_main_scripts_ja4x_test_ja4x_from_cert_matches_pure_core": "test_ja4x_from_cert_matches_pure_core()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L59 | neighbors=[test_main_scripts_ja4x.py, _fake_cert()]
- "tests_test_main_scripts_rdp_test_cc_without_negotiation_is_standard_rdp": "test_cc_without_negotiation_is_standard_rdp()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L53 | neighbors=[test_main_scripts_rdp.py, _cc()]
- "tests_test_main_scripts_rdp_test_confirmed_rdp_wins_dedup_over_port_hint": "test_confirmed_rdp_wins_dedup_over_port_hint()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L84 | neighbors=[test_main_scripts_rdp.py, _run()]
- "tests_test_main_scripts_rdp_test_confirmed_rdp_with_nla_has_no_nla_finding": "test_confirmed_rdp_with_nla_has_no_nla_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L77 | neighbors=[test_main_scripts_rdp.py, _run()]
- "tests_test_main_scripts_rdp_test_confirmed_rdp_without_nla_is_high_finding": "test_confirmed_rdp_without_nla_is_high_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L68 | neighbors=[test_main_scripts_rdp.py, _run()]
- "tests_test_main_scripts_rdp_test_negotiation_failure": "test_negotiation_failure()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L48 | neighbors=[test_main_scripts_rdp.py, _cc()]
- "tests_test_main_scripts_rdp_test_nla_when_hybrid_selected": "test_nla_when_hybrid_selected()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L32 | neighbors=[test_main_scripts_rdp.py, _cc()]
- "tests_test_main_scripts_rdp_test_standard_rdp_security_no_nla": "test_standard_rdp_security_no_nla()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L43 | neighbors=[test_main_scripts_rdp.py, _cc()]
- "tests_test_main_scripts_rdp_test_tls_only_is_not_nla": "test_tls_only_is_not_nla()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L38 | neighbors=[test_main_scripts_rdp.py, _cc()]
- "tests_test_main_scripts_unauth_test_protected_redis_raises_no_unauth_finding": "test_protected_redis_raises_no_unauth_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_unauth.py:L71 | neighbors=[test_main_scripts_unauth.py, _run()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-103.json

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
