# Node Description Batch 311 of 330

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

- "tests_test_syn_scanner_testoptionparsing_test_mss_after_nop_padding": ".test_mss_after_nop_padding()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L308 | neighbors=[TestOptionParsing] | lang=en
- "tests_test_syn_scanner_testoptionparsing_test_mss_extracted": ".test_mss_extracted()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L305 | neighbors=[TestOptionParsing] | lang=en
- "tests_test_syn_scanner_testoptionparsing_test_mss_skips_other_options": ".test_mss_skips_other_options()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L311 | neighbors=[TestOptionParsing] | lang=en
- "tests_test_syn_scanner_testpacketroundtrip_test_ip_checksum_valid_in_full_packet": ".test_ip_checksum_valid_in_full_packet()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L84 | neighbors=[TestPacketRoundTrip] | lang=en
- "tests_test_syn_scanner_testpacketroundtrip_test_parse_rejects_short_packet": ".test_parse_rejects_short_packet()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L88 | neighbors=[TestPacketRoundTrip] | lang=en
- "tests_test_syn_scanner_testpacketroundtrip_test_syn_flag_is_set": ".test_syn_flag_is_set()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L79 | neighbors=[TestPacketRoundTrip] | lang=en
- "tests_test_syn_scanner_testpacketroundtrip_test_syn_packet_parses_back_to_fields": ".test_syn_packet_parses_back_to_fields()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L69 | neighbors=[TestPacketRoundTrip] | lang=en
- "tests_test_syn_scanner_testparsepacketsignals_test_no_options_gives_none_mss": ".test_no_options_gives_none_mss()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L342 | neighbors=[TestParsePacketSignals] | lang=en
- "tests_test_syn_scanner_testsyncookie_test_cookie_is_32_bit": ".test_cookie_is_32_bit()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L53 | neighbors=[TestSynCookie] | lang=en
- "tests_test_syn_scanner_testsyncookie_test_cookie_is_deterministic": ".test_cookie_is_deterministic()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L48 | neighbors=[TestSynCookie] | lang=en
- "tests_test_syn_scanner_testsyncookie_test_cookie_varies_with_key": ".test_cookie_varies_with_key()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L61 | neighbors=[TestSynCookie] | lang=en
- "tests_test_syn_scanner_testsyncookie_test_cookie_varies_with_port": ".test_cookie_varies_with_port()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L57 | neighbors=[TestSynCookie] | lang=en
- "tests_test_syn_scanner_testsyndefaults_test_default_ports_are_nmap_top100": ".test_default_ports_are_nmap_top100()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L289 | neighbors=[TestSynDefaults] | lang=en
- "tests_test_syn_scanner_testsyndefaults_test_default_retries_is_two": ".test_default_retries_is_two()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L296 | neighbors=[TestSynDefaults] | lang=en
- "tests_test_syn_scanner_testsynscannerfallback_test_fallback_detects_open_port_on_loopback": ".test_fallback_detects_open_port_on_loopback()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L164 | neighbors=[TestSynScannerFallback] | lang=en
- "tests_test_syn_scanner_testsynscannerfallback_test_fallback_labels_scanner_name": ".test_fallback_labels_scanner_name()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L184 | neighbors=[TestSynScannerFallback] | lang=en
- "tests_test_syn_scanner_testsynscannerfallback_test_forced_fallback_builds_connect_scanner": ".test_forced_fallback_builds_connect_scanner()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L158 | neighbors=[TestSynScannerFallback] | lang=en
- "tests_test_syn_scanner_testtcpoptionprofile_test_malformed_options_do_not_raise": ".test_malformed_options_do_not_raise()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L423 | neighbors=[TestTcpOptionProfile] | lang=en
- "tests_test_syn_scanner_testtcpoptionprofile_test_parse_linux_syn_ack_options": ".test_parse_linux_syn_ack_options()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L411 | neighbors=[TestTcpOptionProfile] | lang=en
- "tests_test_syn_scanner_testtcpoptionprofile_test_parse_mss_shim_still_works": ".test_parse_mss_shim_still_works()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L419 | neighbors=[TestTcpOptionProfile] | lang=en
- "tests_test_syn_scanner_testtcpoptionprofile_test_parse_windows_syn_ack_options": ".test_parse_windows_syn_ack_options()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L404 | neighbors=[TestTcpOptionProfile] | lang=en
- "tests_test_tarpit_rationale_1": "test_tarpit.py — tarpit / honeypot detection (task C5).  A tarpit (LaBrea), hone" | kind=entity | source=probe/tests/test_tarpit.py:L1 | neighbors=[test_tarpit.py] | lang=pt
- "tests_test_tarpit_testassesstarpit_test_boundary_floor_and_ratio_trip_exactly": ".test_boundary_floor_and_ratio_trip_exactly()" | kind=code-symbol | source=probe/tests/test_tarpit.py:L33 | neighbors=[TestAssessTarpit] | lang=en
- "tests_test_tarpit_testassesstarpit_test_busy_real_host_is_not_flagged": ".test_busy_real_host_is_not_flagged()" | kind=code-symbol | source=probe/tests/test_tarpit.py:L23 | neighbors=[TestAssessTarpit] | lang=en
- "tests_test_tarpit_testassesstarpit_test_nearly_all_open_large_scan_is_flagged": ".test_nearly_all_open_large_scan_is_flagged()" | kind=code-symbol | source=probe/tests/test_tarpit.py:L18 | neighbors=[TestAssessTarpit] | lang=en
- "tests_test_tarpit_testassesstarpit_test_tiny_all_open_scan_is_below_the_floor": ".test_tiny_all_open_scan_is_below_the_floor()" | kind=code-symbol | source=probe/tests/test_tarpit.py:L28 | neighbors=[TestAssessTarpit] | lang=en
- "tests_test_tarpit_testassesstarpit_test_zero_attempted_is_safe": ".test_zero_attempted_is_safe()" | kind=code-symbol | source=probe/tests/test_tarpit.py:L37 | neighbors=[TestAssessTarpit] | lang=en
- "tests_test_task_runner_rationale_1": "Tests for agent/task_runner.py" | kind=entity | source=probe/tests/test_task_runner.py:L1 | neighbors=[test_task_runner.py] | lang=en
- "tests_test_task_runner_rationale_105": "When scope is fetched and targets are outside it." | kind=entity | source=probe/tests/test_task_runner.py:L105 | neighbors=[.test_rejects_out_of_scope_target()] | lang=en
- "tests_test_task_runner_rationale_13": "Return a minimal successful result without doing any real I/O." | kind=entity | source=probe/tests/test_task_runner.py:L13 | neighbors=[_fake_run_scan()] | lang=pt
- "tests_test_task_runner_rationale_152": "When scope fetch fails, manager-embedded scope is still enforced." | kind=entity | source=probe/tests/test_task_runner.py:L152 | neighbors=[.test_scope_fallback_when_fetch_fails()] | lang=en
- "tests_test_task_runner_rationale_201": "Verify the submit callback is called with the correct payload." | kind=entity | source=probe/tests/test_task_runner.py:L201 | neighbors=[.test_calls_submit_with_result()] | lang=en
- "tests_test_task_runner_rationale_206": "When scope is fetched and targets are outside it." | kind=entity | source=probe/tests/test_task_runner.py:L206 | neighbors=[.test_rejects_out_of_scope_target()] | lang=en
- "tests_test_task_runner_rationale_226": "When spool_submit is provided, it's used instead of direct submit." | kind=entity | source=probe/tests/test_task_runner.py:L226 | neighbors=[.test_uses_spool_when_available()] | lang=en
- "tests_test_task_runner_rationale_319": "When scope fetch fails, manager-embedded scope is still enforced." | kind=entity | source=probe/tests/test_task_runner.py:L319 | neighbors=[.test_scope_fallback_when_fetch_fails()] | lang=en
- "tests_test_task_runner_rationale_38": "TaskRunner with no-op dependencies (no real scanning)." | kind=entity | source=probe/tests/test_task_runner.py:L38 | neighbors=[runner()] | lang=en
- "tests_test_task_runner_rationale_391": "Verify the submit callback is called with the correct payload." | kind=entity | source=probe/tests/test_task_runner.py:L391 | neighbors=[.test_calls_submit_with_result()] | lang=en
- "tests_test_task_runner_rationale_416": "When spool_submit is provided, it's used instead of direct submit." | kind=entity | source=probe/tests/test_task_runner.py:L416 | neighbors=[.test_uses_spool_when_available()] | lang=en
- "tests_test_task_runner_rationale_47": "Tests that use the real engine but with no-op callbacks." | kind=entity | source=probe/tests/test_task_runner.py:L47 | neighbors=[TestRunnerHeadless] | lang=en
- "tests_test_task_runner_testrunnerheadless_test_explicit_empty_targets_never_expand_to_engagement_scope": ".test_explicit_empty_targets_never_expand_to_engagement_scope()" | kind=code-symbol | source=probe/tests/test_task_runner.py:L71 | neighbors=[TestRunnerHeadless] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-310.json

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
