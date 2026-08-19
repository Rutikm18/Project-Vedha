# Node Description Batch 210 of 227

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

- "tests_test_scan_funnel_rationale_1": "test_scan_funnel.py — per-host scan funnel orchestrator (Tier 1.4).  The funnel" | kind=entity | source=probe/tests/test_scan_funnel.py:L1 | neighbors=[test_scan_funnel.py]
- "tests_test_scan_funnel_rationale_65": "Build a funnel with fakes; return (funnel, discovery, port_scanner, created)." | kind=entity | source=probe/tests/test_scan_funnel.py:L65 | neighbors=[_make_funnel()]
- "tests_test_scan_funnel_recordingdeep_init": ".__init__()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L48 | neighbors=[RecordingDeep]
- "tests_test_scan_funnel_recordingdeep_scan_target": ".scan_target()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L53 | neighbors=[RecordingDeep]
- "tests_test_scan_funnel_testbuilddefaultfunnel_test_candidate_ports_cover_all_routes": ".test_candidate_ports_cover_all_routes()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L210 | neighbors=[TestBuildDefaultFunnel]
- "tests_test_scan_funnel_testrouteports_test_intersection_only": ".test_intersection_only()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L99 | neighbors=[TestRoutePorts]
- "tests_test_scan_funnel_testrouteports_test_no_match_returns_empty": ".test_no_match_returns_empty()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L103 | neighbors=[TestRoutePorts]
- "tests_test_scan_funnel_testrouteports_test_port_in_multiple_routes": ".test_port_in_multiple_routes()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L107 | neighbors=[TestRoutePorts]
- "tests_test_scan_funnel_testrouteports_test_sorted_output": ".test_sorted_output()" | kind=code-symbol | source=probe/tests/test_scan_funnel.py:L112 | neighbors=[TestRoutePorts]
- "tests_test_scan_health_rationale_1": "test_scan_health.py — the probe scan-metrics → coverage/health verdict.  Guards" | kind=entity | source=manager/backend/tests/test_scan_health.py:L1 | neighbors=[test_scan_health.py]
- "tests_test_scan_health_test_aggregates_across_hosts": "test_aggregates_across_hosts()" | kind=code-symbol | source=manager/backend/tests/test_scan_health.py:L48 | neighbors=[test_scan_health.py]
- "tests_test_scan_health_test_no_metrics_means_nothing_to_attest": "test_no_metrics_means_nothing_to_attest()" | kind=code-symbol | source=manager/backend/tests/test_scan_health.py:L40 | neighbors=[test_scan_health.py]
- "tests_test_scanner_parity_rationale_1": "test_scanner_parity.py — the no-drift guard.  Decision (probe_next plan, Phase 1" | kind=entity | source=probe/tests/test_scanner_parity.py:L1 | neighbors=[test_scanner_parity.py]
- "tests_test_scanner_parity_rationale_30": "Every scanner module authored in main_scripts must exist in scanner/." | kind=entity | source=probe/tests/test_scanner_parity.py:L30 | neighbors=[test_scanner_is_superset_of_no_missing_…]
- "tests_test_scanner_parity_rationale_39": "scanner/ must not carry modules that main_scripts/ does not — otherwise the" | kind=entity | source=probe/tests/test_scanner_parity.py:L39 | neighbors=[test_no_extra_scanner_files()]
- "tests_test_scanner_parity_rationale_49": "Each scanner/<mod>.py is byte-identical to main_scripts/<mod>.py." | kind=entity | source=probe/tests/test_scanner_parity.py:L49 | neighbors=[test_scanner_module_matches_main_script…]
- "tests_test_scope_crypt_rationale_1": "Tests for agent/scope_crypt.py" | kind=entity | source=probe/tests/test_scope_crypt.py:L1 | neighbors=[test_scope_crypt.py]
- "tests_test_scope_crypt_rationale_79": "Each encryption uses a fresh ephemeral key, so blobs are different." | kind=entity | source=probe/tests/test_scope_crypt.py:L79 | neighbors=[.test_multiple_encrypts_different()]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_b64_roundtrip": ".test_b64_roundtrip()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L70 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_different_plaintexts_are_distinct": ".test_different_plaintexts_are_distinct()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L64 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_different_recipient_cannot_decrypt": ".test_different_recipient_cannot_decrypt()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L43 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_roundtrip_empty_scope": ".test_roundtrip_empty_scope()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L36 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_roundtrip_plaintext": ".test_roundtrip_plaintext()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L29 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_tampered_blob": ".test_tampered_blob()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L51 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testencryptdecryptroundtrip_test_too_short_blob": ".test_too_short_blob()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L59 | neighbors=[TestEncryptDecryptRoundtrip]
- "tests_test_scope_crypt_testkeygeneration_test_generates_32_byte_keys": ".test_generates_32_byte_keys()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L16 | neighbors=[TestKeyGeneration]
- "tests_test_scope_crypt_testkeygeneration_test_generates_different_keys_each_call": ".test_generates_different_keys_each_call()" | kind=code-symbol | source=probe/tests/test_scope_crypt.py:L21 | neighbors=[TestKeyGeneration]
- "tests_test_scope_targets_rationale_1": "test_scope_targets.py — the pure scope-authorization core shared by the dispatch" | kind=entity | source=manager/backend/tests/test_scope_targets.py:L1 | neighbors=[test_scope_targets.py]
- "tests_test_scope_targets_rationale_99": "Whatever the validator accepts must be provably inside the scope." | kind=entity | source=manager/backend/tests/test_scope_targets.py:L99 | neighbors=[test_property_every_accepted_target_is_…]
- "tests_test_scope_targets_testexclusions_test_target_clear_of_exclusions_is_allowed": ".test_target_clear_of_exclusions_is_allowed()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L82 | neighbors=[TestExclusions]
- "tests_test_scope_targets_testexclusions_test_target_inside_an_exclusion_is_rejected": ".test_target_inside_an_exclusion_is_rejected()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L71 | neighbors=[TestExclusions]
- "tests_test_scope_targets_testexclusions_test_target_overlapping_an_exclusion_is_rejected": ".test_target_overlapping_an_exclusion_is_rejected()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L76 | neighbors=[TestExclusions]
- "tests_test_scope_targets_testipversionsafety_test_v6_in_v6_scope": ".test_v6_in_v6_scope()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L92 | neighbors=[TestIpVersionSafety]
- "tests_test_scope_targets_testipversionsafety_test_v6_target_against_v4_scope_is_rejected": ".test_v6_target_against_v4_scope_is_rejected()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L89 | neighbors=[TestIpVersionSafety]
- "tests_test_scope_targets_testnoscopeauthorizesnothing_test_empty_scope_denies_all": ".test_empty_scope_denies_all()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L17 | neighbors=[TestNoScopeAuthorizesNothing]
- "tests_test_scope_targets_testoutofscopeisrejected_test_blank_token_is_rejected": ".test_blank_token_is_rejected()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L63 | neighbors=[TestOutOfScopeIsRejected]
- "tests_test_scope_targets_testoutofscopeisrejected_test_cidr_broader_than_scope": ".test_cidr_broader_than_scope()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L48 | neighbors=[TestOutOfScopeIsRejected]
- "tests_test_scope_targets_testoutofscopeisrejected_test_explicit_empty_list_is_rejected": ".test_explicit_empty_list_is_rejected()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L57 | neighbors=[TestOutOfScopeIsRejected]
- "tests_test_scope_targets_testoutofscopeisrejected_test_hostname_is_not_routable": ".test_hostname_is_not_routable()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L60 | neighbors=[TestOutOfScopeIsRejected]
- "tests_test_scope_targets_testoutofscopeisrejected_test_ip_outside_scope": ".test_ip_outside_scope()" | kind=code-symbol | source=manager/backend/tests/test_scope_targets.py:L45 | neighbors=[TestOutOfScopeIsRejected]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-209.json

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
