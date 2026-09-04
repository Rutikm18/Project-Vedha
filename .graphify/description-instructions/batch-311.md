# Node Description Batch 312 of 332

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

- "tests_test_stage2_reconcile_cm_aenter": ".__aenter__()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L170 | neighbors=[_CM]
- "tests_test_stage2_reconcile_cm_aexit": ".__aexit__()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L171 | neighbors=[_CM]
- "tests_test_stage2_reconcile_cm_init": ".__init__()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L169 | neighbors=[_CM]
- "tests_test_stage2_reconcile_rationale_1": "Stage 2 — reconciled campaign completion + worker liveness.  Proves the correctn" | kind=entity | source=manager/backend/tests/test_stage2_reconcile.py:L1 | neighbors=[test_stage2_reconcile.py]
- "tests_test_stage2_reconcile_test_reap_stmt_targets_running_detection_runs": "test_reap_stmt_targets_running_detection_runs()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L186 | neighbors=[test_stage2_reconcile.py]
- "tests_test_stage2_reconcile_test_reconcile_dead_letter_wins_over_a_completed_run": "test_reconcile_dead_letter_wins_over_a_completed_run()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L81 | neighbors=[test_stage2_reconcile.py]
- "tests_test_stage2_reconcile_test_reconcile_status_precedence": "test_reconcile_status_precedence()" | kind=code-symbol | source=manager/backend/tests/test_stage2_reconcile.py:L76 | neighbors=[test_stage2_reconcile.py]
- "tests_test_syn_scanner_rationale_1": "test_syn_scanner.py — stateless SYN scan (Tier 1.1).  The raw-socket send/receiv" | kind=entity | source=probe/tests/test_syn_scanner.py:L1 | neighbors=[test_syn_scanner.py]
- "tests_test_syn_scanner_rationale_205": "The raw SYN path resends ONLY still-silent ports — the direct fix for the     fa" | kind=entity | source=probe/tests/test_syn_scanner.py:L205 | neighbors=[TestSynRetransmit]
- "tests_test_syn_scanner_rationale_208": "The raw SYN path resends ONLY still-silent ports — the direct fix for the     fa" | kind=entity | source=probe/tests/test_syn_scanner.py:L208 | neighbors=[TestSynRetransmit]
- "tests_test_syn_scanner_rationale_327": "A SYN/ACK carrying an MSS option (data offset 6 = 24-byte TCP header)." | kind=entity | source=probe/tests/test_syn_scanner.py:L327 | neighbors=[_synack_with_options()]
- "tests_test_syn_scanner_rationale_328": "A SYN/ACK carrying an MSS option (data offset 6 = 24-byte TCP header)." | kind=entity | source=probe/tests/test_syn_scanner.py:L328 | neighbors=[_synack_with_options()]
- "tests_test_syn_scanner_testadaptivetimeouttoggle_test_adaptive_on_by_default": ".test_adaptive_on_by_default()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L430 | neighbors=[TestAdaptiveTimeoutToggle]
- "tests_test_syn_scanner_testadaptivetimeouttoggle_test_can_disable": ".test_can_disable()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L434 | neighbors=[TestAdaptiveTimeoutToggle]
- "tests_test_syn_scanner_testcapabilitydetection_test_linux_with_raw_socket_is_supported": ".test_linux_with_raw_socket_is_supported()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L148 | neighbors=[TestCapabilityDetection]
- "tests_test_syn_scanner_testcapabilitydetection_test_linux_without_privilege_is_unsupported": ".test_linux_without_privilege_is_unsupported()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L143 | neighbors=[TestCapabilityDetection]
- "tests_test_syn_scanner_testcapabilitydetection_test_non_linux_is_unsupported": ".test_non_linux_is_unsupported()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L139 | neighbors=[TestCapabilityDetection]
- "tests_test_syn_scanner_testchecksum_test_checksum_handles_odd_length": ".test_checksum_handles_odd_length()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L34 | neighbors=[TestChecksum]
- "tests_test_syn_scanner_testchecksum_test_checksum_of_valid_ip_header_is_zero": ".test_checksum_of_valid_ip_header_is_zero()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L28 | neighbors=[TestChecksum]
- "tests_test_syn_scanner_testchecksum_test_tcp_checksum_verifies_to_zero": ".test_tcp_checksum_verifies_to_zero()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L38 | neighbors=[TestChecksum]
- "tests_test_syn_scanner_testclassify_test_other_flags_are_none": ".test_other_flags_are_none()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L102 | neighbors=[TestClassify]
- "tests_test_syn_scanner_testclassify_test_rst_is_closed": ".test_rst_is_closed()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L98 | neighbors=[TestClassify]
- "tests_test_syn_scanner_testclassify_test_syn_ack_is_open": ".test_syn_ack_is_open()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L95 | neighbors=[TestClassify]
- "tests_test_syn_scanner_testoptionparsing_test_malformed_options_never_raise": ".test_malformed_options_never_raise()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L318 | neighbors=[TestOptionParsing]
- "tests_test_syn_scanner_testoptionparsing_test_mss_absent_returns_none": ".test_mss_absent_returns_none()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L315 | neighbors=[TestOptionParsing]
- "tests_test_syn_scanner_testoptionparsing_test_mss_after_nop_padding": ".test_mss_after_nop_padding()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L308 | neighbors=[TestOptionParsing]
- "tests_test_syn_scanner_testoptionparsing_test_mss_extracted": ".test_mss_extracted()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L305 | neighbors=[TestOptionParsing]
- "tests_test_syn_scanner_testoptionparsing_test_mss_skips_other_options": ".test_mss_skips_other_options()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L311 | neighbors=[TestOptionParsing]
- "tests_test_syn_scanner_testpacketroundtrip_test_ip_checksum_valid_in_full_packet": ".test_ip_checksum_valid_in_full_packet()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L84 | neighbors=[TestPacketRoundTrip]
- "tests_test_syn_scanner_testpacketroundtrip_test_parse_rejects_short_packet": ".test_parse_rejects_short_packet()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L88 | neighbors=[TestPacketRoundTrip]
- "tests_test_syn_scanner_testpacketroundtrip_test_syn_flag_is_set": ".test_syn_flag_is_set()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L79 | neighbors=[TestPacketRoundTrip]
- "tests_test_syn_scanner_testpacketroundtrip_test_syn_packet_parses_back_to_fields": ".test_syn_packet_parses_back_to_fields()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L69 | neighbors=[TestPacketRoundTrip]
- "tests_test_syn_scanner_testparsepacketsignals_test_no_options_gives_none_mss": ".test_no_options_gives_none_mss()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L342 | neighbors=[TestParsePacketSignals]
- "tests_test_syn_scanner_testsyncookie_test_cookie_is_32_bit": ".test_cookie_is_32_bit()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L53 | neighbors=[TestSynCookie]
- "tests_test_syn_scanner_testsyncookie_test_cookie_is_deterministic": ".test_cookie_is_deterministic()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L48 | neighbors=[TestSynCookie]
- "tests_test_syn_scanner_testsyncookie_test_cookie_varies_with_key": ".test_cookie_varies_with_key()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L61 | neighbors=[TestSynCookie]
- "tests_test_syn_scanner_testsyncookie_test_cookie_varies_with_port": ".test_cookie_varies_with_port()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L57 | neighbors=[TestSynCookie]
- "tests_test_syn_scanner_testsyndefaults_test_default_ports_are_nmap_top100": ".test_default_ports_are_nmap_top100()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L289 | neighbors=[TestSynDefaults]
- "tests_test_syn_scanner_testsyndefaults_test_default_retries_is_two": ".test_default_retries_is_two()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L296 | neighbors=[TestSynDefaults]
- "tests_test_syn_scanner_testsynscannerfallback_test_fallback_detects_open_port_on_loopback": ".test_fallback_detects_open_port_on_loopback()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L164 | neighbors=[TestSynScannerFallback]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-311.json

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
