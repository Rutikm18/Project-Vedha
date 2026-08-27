# Node Description Batch 46 of 92

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

- "tests_test_main_scripts_findings_test_rdp_exposed_medium": "test_rdp_exposed_medium()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L180 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_server_version_disclosure_is_info": "test_server_version_disclosure_is_info()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L256 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_smbv1_enabled_is_high": "test_smbv1_enabled_is_high()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L103 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_snmp_default_community_is_high": "test_snmp_default_community_is_high()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L124 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_snmp_nondefault_community_is_medium": "test_snmp_nondefault_community_is_medium()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L131 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_summarize_counts_by_severity_and_actionable": "test_summarize_counts_by_severity_and_actionable()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L313 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_telnet_is_high_cleartext": "test_telnet_is_high_cleartext()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L167 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_tls_obsolete_protocol_is_high": "test_tls_obsolete_protocol_is_high()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L24 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_tls_under_strength_rsa_key_is_flagged": "test_tls_under_strength_rsa_key_is_flagged()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L78 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_tls_weak_cipher_is_high_with_reasons": "test_tls_weak_cipher_is_high_with_reasons()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L47 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_tls_weak_signature_hash_is_flagged": "test_tls_weak_signature_hash_is_flagged()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L62 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_findings_test_x_powered_by_disclosure_is_info": "test_x_powered_by_disclosure_is_info()" | kind=code-symbol | source=tests/test_main_scripts_findings.py:L278 | neighbors=[test_main_scripts_findings.py, _run()]
- "tests_test_main_scripts_hardening_scope": "_scope()" | kind=code-symbol | source=tests/test_main_scripts_hardening.py:L32 | neighbors=[test_main_scripts_hardening.py, ._scanner()]
- "tests_test_main_scripts_hardening_testsmbparsing_test_error_response_not_trusted": ".test_error_response_not_trusted()" | kind=code-symbol | source=tests/test_main_scripts_hardening.py:L132 | neighbors=[TestSmbParsing, make_smb2_error()]
- "tests_test_main_scripts_hardening_testsmbparsing_test_success_response_signing_and_dialect": ".test_success_response_signing_and_dialect()" | kind=code-symbol | source=tests/test_main_scripts_hardening.py:L139 | neighbors=[TestSmbParsing, make_smb2_success()]
- "tests_test_main_scripts_hardening_testsmbparsing_test_success_signing_supported_not_required": ".test_success_signing_supported_not_required()" | kind=code-symbol | source=tests/test_main_scripts_hardening.py:L147 | neighbors=[TestSmbParsing, make_smb2_success()]
- "tests_test_main_scripts_ja4s_ext": "_ext()" | kind=code-symbol | source=tests/test_main_scripts_ja4s.py:L17 | neighbors=[test_main_scripts_ja4s.py, _serverhello()]
- "tests_test_main_scripts_ja4s_test_ja4s_from_serverhello_tls13": "test_ja4s_from_serverhello_tls13()" | kind=code-symbol | source=tests/test_main_scripts_ja4s.py:L62 | neighbors=[test_main_scripts_ja4s.py, _serverhello()]
- "tests_test_main_scripts_ja4x_fake_cert": "_fake_cert()" | kind=code-symbol | source=tests/test_main_scripts_ja4x.py:L52 | neighbors=[test_main_scripts_ja4x.py, test_ja4x_from_cert_matches_pure_core()]
- "tests_test_main_scripts_ja4x_test_ja4x_from_cert_matches_pure_core": "test_ja4x_from_cert_matches_pure_core()" | kind=code-symbol | source=tests/test_main_scripts_ja4x.py:L59 | neighbors=[test_main_scripts_ja4x.py, _fake_cert()]
- "tests_test_main_scripts_rdp_test_cc_without_negotiation_is_standard_rdp": "test_cc_without_negotiation_is_standard_rdp()" | kind=code-symbol | source=tests/test_main_scripts_rdp.py:L53 | neighbors=[test_main_scripts_rdp.py, _cc()]
- "tests_test_main_scripts_rdp_test_confirmed_rdp_wins_dedup_over_port_hint": "test_confirmed_rdp_wins_dedup_over_port_hint()" | kind=code-symbol | source=tests/test_main_scripts_rdp.py:L84 | neighbors=[test_main_scripts_rdp.py, _run()]
- "tests_test_main_scripts_rdp_test_confirmed_rdp_with_nla_has_no_nla_finding": "test_confirmed_rdp_with_nla_has_no_nla_finding()" | kind=code-symbol | source=tests/test_main_scripts_rdp.py:L77 | neighbors=[test_main_scripts_rdp.py, _run()]
- "tests_test_main_scripts_rdp_test_confirmed_rdp_without_nla_is_high_finding": "test_confirmed_rdp_without_nla_is_high_finding()" | kind=code-symbol | source=tests/test_main_scripts_rdp.py:L68 | neighbors=[test_main_scripts_rdp.py, _run()]
- "tests_test_main_scripts_rdp_test_negotiation_failure": "test_negotiation_failure()" | kind=code-symbol | source=tests/test_main_scripts_rdp.py:L48 | neighbors=[test_main_scripts_rdp.py, _cc()]
- "tests_test_main_scripts_rdp_test_nla_when_hybrid_selected": "test_nla_when_hybrid_selected()" | kind=code-symbol | source=tests/test_main_scripts_rdp.py:L32 | neighbors=[test_main_scripts_rdp.py, _cc()]
- "tests_test_main_scripts_rdp_test_standard_rdp_security_no_nla": "test_standard_rdp_security_no_nla()" | kind=code-symbol | source=tests/test_main_scripts_rdp.py:L43 | neighbors=[test_main_scripts_rdp.py, _cc()]
- "tests_test_main_scripts_rdp_test_tls_only_is_not_nla": "test_tls_only_is_not_nla()" | kind=code-symbol | source=tests/test_main_scripts_rdp.py:L38 | neighbors=[test_main_scripts_rdp.py, _cc()]
- "tests_test_main_scripts_unauth_test_protected_redis_raises_no_unauth_finding": "test_protected_redis_raises_no_unauth_finding()" | kind=code-symbol | source=tests/test_main_scripts_unauth.py:L71 | neighbors=[test_main_scripts_unauth.py, _run()]
- "tests_test_main_scripts_unauth_test_unauth_elasticsearch_is_high": "test_unauth_elasticsearch_is_high()" | kind=code-symbol | source=tests/test_main_scripts_unauth.py:L63 | neighbors=[test_main_scripts_unauth.py, _run()]
- "tests_test_main_scripts_unauth_test_unauth_redis_is_critical_and_rce_flagged": "test_unauth_redis_is_critical_and_rce_flagged()" | kind=code-symbol | source=tests/test_main_scripts_unauth.py:L55 | neighbors=[test_main_scripts_unauth.py, _run()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_ambiguous_when_only_open_filtered": ".test_ambiguous_when_only_open_filtered()" | kind=code-symbol | source=tests/test_main_scripts_vantage.py:L44 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_auto_detects_external_by_name": ".test_auto_detects_external_by_name()" | kind=code-symbol | source=tests/test_main_scripts_vantage.py:L63 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_explicit_external_vantage_by_name_override": ".test_explicit_external_vantage_by_name_override()" | kind=code-symbol | source=tests/test_main_scripts_vantage.py:L56 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_external_exposure_is_flagged": ".test_external_exposure_is_flagged()" | kind=code-symbol | source=tests/test_main_scripts_vantage.py:L17 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_internal_only_not_called_external": ".test_internal_only_not_called_external()" | kind=code-symbol | source=tests/test_main_scripts_vantage.py:L26 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_not_exposed_everywhere": ".test_not_exposed_everywhere()" | kind=code-symbol | source=tests/test_main_scripts_vantage.py:L39 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_main_scripts_vantage_testreconcilevantages_test_vantages_are_not_collapsed": ".test_vantages_are_not_collapsed()" | kind=code-symbol | source=tests/test_main_scripts_vantage.py:L49 | neighbors=[TestReconcileVantages, _r()]
- "tests_test_new_scanners_testdeltaengine_test_load_jsonl_skips_invalid_json": ".test_load_jsonl_skips_invalid_json()" | kind=code-symbol | source=tests/test_new_scanners.py:L502 | neighbors=[TestDeltaEngine, _make_scan_record()]
- "tests_test_os_fingerprint_testacceptechoreply_test_accepts_echo_reply_from_target": ".test_accepts_echo_reply_from_target()" | kind=code-symbol | source=tests/test_os_fingerprint.py:L173 | neighbors=[TestAcceptEchoReply, ._reply()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-045.json

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
