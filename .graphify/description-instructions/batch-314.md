# Node Description Batch 315 of 330

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

- "tests_test_transport_testwebsocket_test_ws_requires_token": ".test_ws_requires_token()" | kind=code-symbol | source=probe/tests/test_transport.py:L549 | neighbors=[TestWebSocket] | lang=en
- "tests_test_transport_testwebsocket_test_ws_url_http": ".test_ws_url_http()" | kind=code-symbol | source=probe/tests/test_transport.py:L535 | neighbors=[TestWebSocket] | lang=en
- "tests_test_transport_testwebsocket_test_ws_url_https": ".test_ws_url_https()" | kind=code-symbol | source=probe/tests/test_transport.py:L542 | neighbors=[TestWebSocket] | lang=en
- "tests_test_trust_alignment_rationale_1": "test_trust_alignment.py — cross-tree invariant: the manager's VALIDATED_SCANNERS" | kind=entity | source=manager/detection_engine/tests/test_trust_alignment.py:L1 | neighbors=[test_trust_alignment.py] | lang=en
- "tests_test_trust_alignment_test_manager_and_probe_trust_sets_match": "test_manager_and_probe_trust_sets_match()" | kind=code-symbol | source=manager/detection_engine/tests/test_trust_alignment.py:L22 | neighbors=[test_trust_alignment.py] | lang=en
- "tests_test_two_tree_parity_rationale_1": "test_two_tree_parity.py — the guard the architecture review (#4) demanded.  `sca" | kind=entity | source=probe/tests/test_two_tree_parity.py:L1 | neighbors=[test_two_tree_parity.py] | lang=en
- "tests_test_two_tree_parity_rationale_34": "Every .py present in BOTH trees (the mirrored set), excluding caches." | kind=entity | source=probe/tests/test_two_tree_parity.py:L34 | neighbors=[_mirrored_py_files()] | lang=en
- "tests_test_two_tree_parity_rationale_57": "A scanner that exists in only one tree is a wiring bug: one orchestrator     fam" | kind=entity | source=probe/tests/test_two_tree_parity.py:L57 | neighbors=[test_no_unmirrored_scanner_files()] | lang=en
- "tests_test_two_tree_parity_test_scanner_and_main_scripts_are_byte_identical": "test_scanner_and_main_scripts_are_byte_identical()" | kind=code-symbol | source=probe/tests/test_two_tree_parity.py:L46 | neighbors=[test_two_tree_parity.py] | lang=en
- "tests_test_udp_amplifiers_test_dns_open_recursion": "test_dns_open_recursion()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L18 | neighbors=[test_udp_amplifiers.py] | lang=en
- "tests_test_udp_amplifiers_test_memcached_exposed": "test_memcached_exposed()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L26 | neighbors=[test_udp_amplifiers.py] | lang=en
- "tests_test_udp_amplifiers_test_ntp_monlist_absent": "test_ntp_monlist_absent()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L13 | neighbors=[test_udp_amplifiers.py] | lang=en
- "tests_test_udp_amplifiers_test_ntp_monlist_enabled": "test_ntp_monlist_enabled()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L8 | neighbors=[test_udp_amplifiers.py] | lang=en
- "tests_test_udp_amplifiers_test_probe_builders_are_bytes": "test_probe_builders_are_bytes()" | kind=code-symbol | source=probe/tests/test_udp_amplifiers.py:L31 | neighbors=[test_udp_amplifiers.py] | lang=en
- "tests_test_use_cases_rationale_1": "Use-case library guards.  FORBIDDEN is a *living* set: a phrase stays here only" | kind=entity | source=probe/tests/test_use_cases.py:L1 | neighbors=[test_use_cases.py] | lang=pt
- "tests_test_use_cases_test_codes_are_unique_and_stable": "test_codes_are_unique_and_stable()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L82 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_descriptions_do_not_overclaim": "test_descriptions_do_not_overclaim()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L25 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_every_code_maps_to_a_real_use_case": "test_every_code_maps_to_a_real_use_case()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L77 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_full_port_audit_is_deep": "test_full_port_audit_is_deep()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L64 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_intensity_code_and_name_equivalent": "test_intensity_code_and_name_equivalent()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L100 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_iot_survey_collects_banners": "test_iot_survey_collects_banners()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L45 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_new_use_cases_resolve": "test_new_use_cases_resolve()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L52 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_params_intensity_overrides_use_case": "test_params_intensity_overrides_use_case()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L69 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_resolve_accepts_string_digits_too": "test_resolve_accepts_string_digits_too()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L95 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_resolve_by_numeric_code": "test_resolve_by_numeric_code()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L90 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_string_use_case_id_still_wins_over_code": "test_string_use_case_id_still_wins_over_code()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L113 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_udp_claims_amplification": "test_udp_claims_amplification()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L36 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_unknown_code_is_rejected": "test_unknown_code_is_rejected()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L106 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_web_claims_methods": "test_web_claims_methods()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L41 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_use_cases_test_windows_estate_claims_signing": "test_windows_estate_claims_signing()" | kind=code-symbol | source=probe/tests/test_use_cases.py:L32 | neighbors=[test_use_cases.py] | lang=en
- "tests_test_va_campaign_buf_flush": ".flush()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L291 | neighbors=[_Buf] | lang=en
- "tests_test_va_campaign_buf_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L285 | neighbors=[_Buf] | lang=en
- "tests_test_va_campaign_buf_isatty": ".isatty()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L294 | neighbors=[_Buf] | lang=en
- "tests_test_va_campaign_buf_write": ".write()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L288 | neighbors=[_Buf] | lang=en
- "tests_test_va_campaign_rationale_1": "test_va_campaign.py — the VA-campaign orchestrator (scanner/va_campaign.py).  Th" | kind=entity | source=probe/tests/test_va_campaign.py:L1 | neighbors=[test_va_campaign.py] | lang=en
- "tests_test_va_campaign_test_callback_error_never_breaks_reporting": "test_callback_error_never_breaks_reporting()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L210 | neighbors=[test_va_campaign.py] | lang=en
- "tests_test_va_campaign_test_capability_list_covers_the_user_requested_set": "test_capability_list_covers_the_user_requested_set()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L233 | neighbors=[test_va_campaign.py] | lang=en
- "tests_test_va_campaign_test_ipv6_discovery_never_raises": "test_ipv6_discovery_never_raises()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L338 | neighbors=[test_va_campaign.py] | lang=en
- "tests_test_va_campaign_test_ipv6_discovery_reports_all_scans_only_in_scope": "test_ipv6_discovery_reports_all_scans_only_in_scope()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L323 | neighbors=[test_va_campaign.py] | lang=en
- "tests_test_va_campaign_test_ipv6_option_default_off": "test_ipv6_option_default_off()" | kind=code-symbol | source=probe/tests/test_va_campaign.py:L346 | neighbors=[test_va_campaign.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-314.json

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
