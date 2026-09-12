# Node Description Batch 328 of 380

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

- "tests_test_integration_testwebsocketmessageprotocol_test_hello_message": ".test_hello_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L276 | neighbors=[TestWebSocketMessageProtocol] | lang=en
- "tests_test_integration_testwebsocketmessageprotocol_test_job_push_message": ".test_job_push_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L280 | neighbors=[TestWebSocketMessageProtocol] | lang=en
- "tests_test_integration_testwebsocketmessageprotocol_test_result_message": ".test_result_message()" | kind=code-symbol | source=probe/tests/test_integration.py:L294 | neighbors=[TestWebSocketMessageProtocol] | lang=en
- "tests_test_integrations_rationale_1": "test_integrations.py — operator notification-integration config (item 3)." | kind=entity | source=manager/backend/tests/test_integrations.py:L1 | neighbors=[test_integrations.py] | lang=en
- "tests_test_intensity_budget_rationale_1": "Deep intensity carries a per-host time ceiling.  `deep` sets port_profile=\"full\"" | kind=entity | source=probe/tests/test_intensity_budget.py:L1 | neighbors=[test_intensity_budget.py] | lang=pt
- "tests_test_intensity_budget_rationale_24": "Already bounded by breadth — ~15 ports." | kind=entity | source=probe/tests/test_intensity_budget.py:L24 | neighbors=[.test_light_is_unbounded()] | lang=en
- "tests_test_intensity_budget_rationale_28": "Already bounded by the profile's own port catalog." | kind=entity | source=probe/tests/test_intensity_budget.py:L28 | neighbors=[.test_standard_is_unbounded()] | lang=en
- "tests_test_intensity_budget_rationale_32": "Absent-vs-None must not be ambiguous at the call site." | kind=entity | source=probe/tests/test_intensity_budget.py:L32 | neighbors=[.test_every_preset_declares_the_key()] | lang=en
- "tests_test_intensity_budget_rationale_37": "A full 65,535-port sweep runs ~21 min at healthy throughput (~51         ports/s" | kind=entity | source=probe/tests/test_intensity_budget.py:L37 | neighbors=[.test_deep_budget_exceeds_a_healthy_ful…] | lang=pt
- "tests_test_intensity_budget_rationale_49": "A preset value that never reaches run_engagement is decoration. These     assert" | kind=entity | source=probe/tests/test_intensity_budget.py:L49 | neighbors=[TestTuningTranslation] | lang=en
- "tests_test_intensity_budget_rationale_65": "Same clamping discipline as every other tuning knob — an operator         cannot" | kind=entity | source=probe/tests/test_intensity_budget.py:L65 | neighbors=[.test_override_is_clamped_to_a_safe_env…] | lang=en
- "tests_test_intensity_budget_rationale_73": "An operator running standard against a huge estate may still want a         ceil" | kind=entity | source=probe/tests/test_intensity_budget.py:L73 | neighbors=[.test_override_can_bound_an_otherwise_u…] | lang=pt
- "tests_test_intensity_budget_rationale_79": "Guards the seam: a tuning key run_engagement does not accept would be         a" | kind=entity | source=probe/tests/test_intensity_budget.py:L79 | neighbors=[.test_run_engagement_accepts_the_kwarg()] | lang=pt
- "tests_test_intensity_budget_testbudgets_test_deep_has_a_finite_host_budget": ".test_deep_has_a_finite_host_budget()" | kind=code-symbol | source=probe/tests/test_intensity_budget.py:L20 | neighbors=[TestBudgets] | lang=en
- "tests_test_intensity_budget_testtuningtranslation_test_deep_preset_reaches_the_tuning_dict": ".test_deep_preset_reaches_the_tuning_dict()" | kind=code-symbol | source=probe/tests/test_intensity_budget.py:L52 | neighbors=[TestTuningTranslation] | lang=en
- "tests_test_intensity_budget_testtuningtranslation_test_operator_override_is_honoured": ".test_operator_override_is_honoured()" | kind=code-symbol | source=probe/tests/test_intensity_budget.py:L60 | neighbors=[TestTuningTranslation] | lang=en
- "tests_test_intensity_budget_testtuningtranslation_test_standard_stays_unbounded": ".test_standard_stays_unbounded()" | kind=code-symbol | source=probe/tests/test_intensity_budget.py:L56 | neighbors=[TestTuningTranslation] | lang=en
- "tests_test_ipmi_scanner_rationale_1": "test_ipmi_scanner.py — IPMI 2.0 cipher-zero auth-bypass detection.  Byte-exact R" | kind=entity | source=probe/tests/test_ipmi_scanner.py:L1 | neighbors=[test_ipmi_scanner.py] | lang=en
- "tests_test_ipmi_scanner_testparity_test_main_scripts": ".test_main_scripts()" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L77 | neighbors=[TestParity] | lang=en
- "tests_test_ipmi_scanner_testwireformat_test_open_session_request_offers_cipher_zero": ".test_open_session_request_offers_cipher_zero()" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L24 | neighbors=[TestWireFormat] | lang=en
- "tests_test_ipmi_scanner_testwireformat_test_parse_rejects_non_response": ".test_parse_rejects_non_response()" | kind=code-symbol | source=probe/tests/test_ipmi_scanner.py:L39 | neighbors=[TestWireFormat] | lang=en
- "tests_test_ipv6_discovery_rationale_1": "test_ipv6_discovery.py — FIX 3: IPv6 neighbor discovery (RFC 4861 ND multicast)." | kind=entity | source=probe/tests/test_ipv6_discovery.py:L1 | neighbors=[test_ipv6_discovery.py] | lang=en
- "tests_test_ipv6_discovery_testparsers_test_ignores_non_ipv6_lines": ".test_ignores_non_ipv6_lines()" | kind=code-symbol | source=probe/tests/test_ipv6_discovery.py:L33 | neighbors=[TestParsers] | lang=en
- "tests_test_ipv6_discovery_testparsers_test_parse_ip_neigh_linux": ".test_parse_ip_neigh_linux()" | kind=code-symbol | source=probe/tests/test_ipv6_discovery.py:L24 | neighbors=[TestParsers] | lang=en
- "tests_test_ipv6_discovery_testparsers_test_parse_ndp_macos": ".test_parse_ndp_macos()" | kind=code-symbol | source=probe/tests/test_ipv6_discovery.py:L14 | neighbors=[TestParsers] | lang=en
- "tests_test_ipv6_wiring_rationale_1": "test_ipv6_wiring.py — IPv6 neighbour discovery inside the engagement.  An IPv4 /" | kind=entity | source=probe/tests/test_ipv6_wiring.py:L1 | neighbors=[test_ipv6_wiring.py] | lang=en
- "tests_test_ipv6_wiring_rationale_111": "The core restraint: discovery must not widen authorization." | kind=entity | source=probe/tests/test_ipv6_wiring.py:L111 | neighbors=[test_out_of_scope_neighbour_is_reported…] | lang=en
- "tests_test_ipv6_wiring_rationale_137": "Only the scan types that opt in pay for the multicast ping." | kind=entity | source=probe/tests/test_ipv6_wiring.py:L137 | neighbors=[test_disabled_by_default()] | lang=en
- "tests_test_ipv6_wiring_rationale_28": "The neighbour cache is system-wide. Pinging en0 and then harvesting every     in" | kind=entity | source=probe/tests/test_ipv6_wiring.py:L28 | neighbors=[TestInterfaceScoping] | lang=en
- "tests_test_ipv6_wiring_test_component_is_in_the_catalog": "test_component_is_in_the_catalog()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L160 | neighbors=[test_ipv6_wiring.py] | lang=en
- "tests_test_ipv6_wiring_test_network_va_opts_in": "test_network_va_opts_in()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L172 | neighbors=[test_ipv6_wiring.py] | lang=en
- "tests_test_ipv6_wiring_test_planned_only_when_enabled": "test_planned_only_when_enabled()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L164 | neighbors=[test_ipv6_wiring.py] | lang=en
- "tests_test_ipv6_wiring_testinterfacescoping_stub": "._stub()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L42 | neighbors=[TestInterfaceScoping] | lang=en
- "tests_test_ipv6_wiring_testinterfacescoping_test_globals_are_kept_they_are_not_interface_bound": ".test_globals_are_kept_they_are_not_interface_bound()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L56 | neighbors=[TestInterfaceScoping] | lang=en
- "tests_test_ipv6_wiring_testinterfacescoping_test_iface_filters_out_other_segments": ".test_iface_filters_out_other_segments()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L47 | neighbors=[TestInterfaceScoping] | lang=en
- "tests_test_ipv6_wiring_testinterfacescoping_test_iface_keeps_its_own_neighbours": ".test_iface_keeps_its_own_neighbours()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L52 | neighbors=[TestInterfaceScoping] | lang=en
- "tests_test_ipv6_wiring_testinterfacescoping_test_link_local_keeps_its_zone_so_connect_can_route": ".test_link_local_keeps_its_zone_so_connect_can_route()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L66 | neighbors=[TestInterfaceScoping] | lang=en
- "tests_test_ipv6_wiring_testinterfacescoping_test_no_iface_keeps_everything": ".test_no_iface_keeps_everything()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L62 | neighbors=[TestInterfaceScoping] | lang=en
- "tests_test_ipv6_wiring_testinterfacescoping_test_unresolved_neighbours_are_never_returned": ".test_unresolved_neighbours_are_never_returned()" | kind=code-symbol | source=probe/tests/test_ipv6_wiring.py:L59 | neighbors=[TestInterfaceScoping] | lang=en
- "tests_test_job_admission_rationale_1": "Daemon integration — the independent admission gate wired into TaskRunner: the p" | kind=entity | source=probe/tests/test_job_admission.py:L1 | neighbors=[test_job_admission.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-327.json

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
