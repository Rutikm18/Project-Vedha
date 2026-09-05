# Node Description Batch 292 of 336

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
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "tests_test_main_scripts_findings_rationale_1": "test_main_scripts_findings.py — the findings interpretation layer.  Pure-logic," | kind=entity | source=probe/tests/test_main_scripts_findings.py:L1 | neighbors=[test_main_scripts_findings.py] | lang=en
- "tests_test_main_scripts_findings_test_build_service_index_extracts_confirmed_services": "test_build_service_index_extracts_confirmed_services()" | kind=code-symbol | source=probe/tests/test_main_scripts_findings.py:L198 | neighbors=[test_main_scripts_findings.py] | lang=en
- "tests_test_main_scripts_hardening_rationale_1": "test_main_scripts_hardening.py — verifies the Phase-1 correctness fixes applied" | kind=entity | source=probe/tests/test_main_scripts_hardening.py:L1 | neighbors=[test_main_scripts_hardening.py] | lang=en
- "tests_test_main_scripts_hardening_rationale_101": "A 64-byte SMB2 header. Caller prepends a 4-byte NBT transport prefix, so     Pro" | kind=entity | source=probe/tests/test_main_scripts_hardening.py:L101 | neighbors=[_smb2_header()] | lang=pt
- "tests_test_main_scripts_hardening_rationale_123": "STATUS_INVALID_PARAMETER error response: same header, body StructureSize 9," | kind=entity | source=probe/tests/test_main_scripts_hardening.py:L123 | neighbors=[make_smb2_error()] | lang=en
- "tests_test_main_scripts_hardening_testosconfidence_test_linux_ttl_only_capped": ".test_linux_ttl_only_capped()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L92 | neighbors=[TestOsConfidence] | lang=en
- "tests_test_main_scripts_hardening_testosconfidence_test_no_signal_is_unknown": ".test_no_signal_is_unknown()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L87 | neighbors=[TestOsConfidence] | lang=en
- "tests_test_main_scripts_hardening_testosconfidence_test_ttl_only_is_not_absolute": ".test_ttl_only_is_not_absolute()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L74 | neighbors=[TestOsConfidence] | lang=en
- "tests_test_main_scripts_hardening_testosconfidence_test_two_signals_beat_one": ".test_two_signals_beat_one()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L81 | neighbors=[TestOsConfidence] | lang=en
- "tests_test_main_scripts_hardening_testsmbparsing_test_negotiate_request_excludes_smb311": ".test_negotiate_request_excludes_smb311()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L152 | neighbors=[TestSmbParsing] | lang=en
- "tests_test_main_scripts_hardening_testsmbparsing_test_negotiate_request_offers_smb311_with_preauth_context": ".test_negotiate_request_offers_smb311_with_preauth_context()" | kind=code-symbol | source=probe/tests/test_main_scripts_hardening.py:L152 | neighbors=[TestSmbParsing] | lang=en
- "tests_test_main_scripts_ja4s_rationale_1": "test_main_scripts_ja4s.py — JA4S TLS ServerHello fingerprint (advanced capabilit" | kind=entity | source=probe/tests/test_main_scripts_ja4s.py:L1 | neighbors=[test_main_scripts_ja4s.py] | lang=en
- "tests_test_main_scripts_ja4s_test_empty_extensions_sentinel": "test_empty_extensions_sentinel()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4s.py:L48 | neighbors=[test_main_scripts_ja4s.py] | lang=en
- "tests_test_main_scripts_ja4s_test_extension_hash_is_order_sensitive": "test_extension_hash_is_order_sensitive()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4s.py:L53 | neighbors=[test_main_scripts_ja4s.py] | lang=en
- "tests_test_main_scripts_ja4s_test_ja4s_from_bad_serverhello_is_none": "test_ja4s_from_bad_serverhello_is_none()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4s.py:L73 | neighbors=[test_main_scripts_ja4s.py] | lang=en
- "tests_test_main_scripts_ja4s_test_ja4s_from_fields_shape_and_parts": "test_ja4s_from_fields_shape_and_parts()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4s.py:L31 | neighbors=[test_main_scripts_ja4s.py] | lang=en
- "tests_test_main_scripts_ja4s_test_suspicious_ja4s_finding_fires_only_on_match": "test_suspicious_ja4s_finding_fires_only_on_match()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4s.py:L78 | neighbors=[test_main_scripts_ja4s.py] | lang=en
- "tests_test_main_scripts_ja4s_test_version_and_alpn_encodings": "test_version_and_alpn_encodings()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4s.py:L40 | neighbors=[test_main_scripts_ja4s.py] | lang=en
- "tests_test_main_scripts_ja4x_rationale_1": "test_main_scripts_ja4x.py — JA4X X.509 certificate fingerprinting (advanced capa" | kind=entity | source=probe/tests/test_main_scripts_ja4x.py:L1 | neighbors=[test_main_scripts_ja4x.py] | lang=en
- "tests_test_main_scripts_ja4x_test_empty_list_hashes_to_sentinel": "test_empty_list_hashes_to_sentinel()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L38 | neighbors=[test_main_scripts_ja4x.py] | lang=en
- "tests_test_main_scripts_ja4x_test_ja4x_format_is_three_12hex_fields": "test_ja4x_format_is_three_12hex_fields()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L30 | neighbors=[test_main_scripts_ja4x.py] | lang=en
- "tests_test_main_scripts_ja4x_test_ja4x_from_cert_handles_garbage": "test_ja4x_from_cert_handles_garbage()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L65 | neighbors=[test_main_scripts_ja4x.py] | lang=en
- "tests_test_main_scripts_ja4x_test_ja4x_is_deterministic_and_order_sensitive": "test_ja4x_is_deterministic_and_order_sensitive()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L43 | neighbors=[test_main_scripts_ja4x.py] | lang=en
- "tests_test_main_scripts_ja4x_test_match_suspicious_registry": "test_match_suspicious_registry()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L94 | neighbors=[test_main_scripts_ja4x.py] | lang=en
- "tests_test_main_scripts_ja4x_test_oid_to_hex_known_values": "test_oid_to_hex_known_values()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L21 | neighbors=[test_main_scripts_ja4x.py] | lang=en
- "tests_test_main_scripts_ja4x_test_real_self_signed_cert_round_trip": "test_real_self_signed_cert_round_trip()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L72 | neighbors=[test_main_scripts_ja4x.py] | lang=en
- "tests_test_main_scripts_ja4x_test_self_signed_finding_carries_ja4x_for_correlation": "test_self_signed_finding_carries_ja4x_for_correlation()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L123 | neighbors=[test_main_scripts_ja4x.py] | lang=en
- "tests_test_main_scripts_ja4x_test_suspicious_fingerprint_finding_fires_only_on_match": "test_suspicious_fingerprint_finding_fires_only_on_match()" | kind=code-symbol | source=probe/tests/test_main_scripts_ja4x.py:L104 | neighbors=[test_main_scripts_ja4x.py] | lang=en
- "tests_test_main_scripts_rdp_rationale_1": "test_main_scripts_rdp.py — Phase 18: protocol-level RDP confirmation + NLA detec" | kind=entity | source=probe/tests/test_main_scripts_rdp.py:L1 | neighbors=[test_main_scripts_rdp.py] | lang=en
- "tests_test_main_scripts_rdp_rationale_16": "A TPKT + X.224 Connection Confirm, optionally carrying an rdpNeg PDU." | kind=entity | source=probe/tests/test_main_scripts_rdp.py:L16 | neighbors=[_cc()] | lang=en
- "tests_test_main_scripts_rdp_rationale_18": "A TPKT + X.224 Connection Confirm, optionally carrying an rdpNeg PDU." | kind=entity | source=probe/tests/test_main_scripts_rdp.py:L18 | neighbors=[_cc()] | lang=en
- "tests_test_main_scripts_rdp_test_connection_request_is_valid_tpkt_and_requests_protocols": "test_connection_request_is_valid_tpkt_and_requests_protocols()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L25 | neighbors=[test_main_scripts_rdp.py] | lang=en
- "tests_test_main_scripts_rdp_test_main_cli_runs_and_writes_finding": "test_main_cli_runs_and_writes_finding()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L108 | neighbors=[test_main_scripts_rdp.py] | lang=en
- "tests_test_main_scripts_rdp_test_nla_not_required_when_rdp_only_accepted": "test_nla_not_required_when_rdp_only_accepted()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L74 | neighbors=[test_main_scripts_rdp.py] | lang=en
- "tests_test_main_scripts_rdp_test_nla_required_when_rdp_only_probe_refused": "test_nla_required_when_rdp_only_probe_refused()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L61 | neighbors=[test_main_scripts_rdp.py] | lang=en
- "tests_test_main_scripts_rdp_test_non_rdp_data_is_none": "test_non_rdp_data_is_none()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L100 | neighbors=[test_main_scripts_rdp.py] | lang=en
- "tests_test_main_scripts_rdp_test_posture_map_matches_spec": "test_posture_map_matches_spec()" | kind=code-symbol | source=probe/tests/test_main_scripts_rdp.py:L53 | neighbors=[test_main_scripts_rdp.py] | lang=en
- "tests_test_main_scripts_statemodel_rationale_1": "test_main_scripts_statemodel.py — Phase 1: the normalized ScanResult state model" | kind=entity | source=probe/tests/test_main_scripts_statemodel.py:L1 | neighbors=[test_main_scripts_statemodel.py] | lang=en
- "tests_test_main_scripts_statemodel_test_backward_compatible_old_style_construction_still_works": "test_backward_compatible_old_style_construction_still_works()" | kind=code-symbol | source=probe/tests/test_main_scripts_statemodel.py:L57 | neighbors=[test_main_scripts_statemodel.py] | lang=en
- "tests_test_main_scripts_statemodel_test_canonical_states_are_the_six_documented_states": "test_canonical_states_are_the_six_documented_states()" | kind=code-symbol | source=probe/tests/test_main_scripts_statemodel.py:L16 | neighbors=[test_main_scripts_statemodel.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-291.json

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
