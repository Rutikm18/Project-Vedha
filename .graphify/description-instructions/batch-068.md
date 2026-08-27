# Node Description Batch 69 of 92

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

- "scanner_udp_scanner_snmp_probe": "_snmp_probe()" | kind=code-symbol | source=scanner/udp_scanner.py:L54 | neighbors=[udp_scanner.py] | lang=en
- "scanner_udp_scanner_udpscanner_init": ".__init__()" | kind=code-symbol | source=scanner/udp_scanner.py:L280 | neighbors=[UDPScanner] | lang=en
- "scanner_unauth_access_is_rce_capable": "is_rce_capable()" | kind=code-symbol | source=scanner/unauth_access.py:L68 | neighbors=[unauth_access.py] | lang=en
- "scanner_unauth_access_rationale_49": "Decide whether `banner` proves unauthenticated access for `service`.      True =" | kind=entity | source=scanner/unauth_access.py:L49 | neighbors=[classify_unauth_access()] | lang=en
- "scanner_vantage_matrix_rationale_1": "vantage_matrix.py — reconcile the SAME target scanned from MULTIPLE vantages.  E" | kind=entity | source=scanner/vantage_matrix.py:L1 | neighbors=[vantage_matrix.py] | lang=en
- "scanner_vantage_matrix_rationale_42": "(proto, port, status) from a ScanResult or a plain dict." | kind=entity | source=scanner/vantage_matrix.py:L42 | neighbors=[_extract()] | lang=pt
- "scanner_vantage_matrix_rationale_51": "Compare per-vantage observations of one target.      `observations` maps a vanta" | kind=entity | source=scanner/vantage_matrix.py:L51 | neighbors=[reconcile_vantages()] | lang=en
- "scanner_web_scanner_main": "main()" | kind=code-symbol | source=scanner/web_scanner.py:L166 | neighbors=[web_scanner.py] | lang=en
- "scanner_web_scanner_noredirect_redirect_request": ".redirect_request()" | kind=code-symbol | source=scanner/web_scanner.py:L56 | neighbors=[_NoRedirect] | lang=en
- "scanner_web_scanner_rationale_1": "web_scanner.py — passive HTTP(S) service fingerprinting.  METHOD (collection onl" | kind=entity | source=scanner/web_scanner.py:L1 | neighbors=[web_scanner.py] | lang=en
- "scanner_web_scanner_rationale_46": "Read the Allow header from an OPTIONS response. Read-only." | kind=entity | source=scanner/web_scanner.py:L46 | neighbors=[parse_allow_header()] | lang=en
- "scanner_web_scanner_webscanner_init": ".__init__()" | kind=code-symbol | source=scanner/web_scanner.py:L139 | neighbors=[WebScanner] | lang=en
- "scanner_windows_collector_main": "main()" | kind=code-symbol | source=scanner/windows_collector.py:L335 | neighbors=[windows_collector.py] | lang=en
- "scanner_windows_collector_rationale_1": "windows_collector.py — credentialed (authenticated) inventory for Windows hosts." | kind=entity | source=scanner/windows_collector.py:L1 | neighbors=[windows_collector.py] | lang=en
- "scanner_windows_collector_rationale_160": "Connect to RemoteRegistry over SMB and enumerate installed-software keys plus" | kind=entity | source=scanner/windows_collector.py:L160 | neighbors=[_smb_registry_collect()] | lang=en
- "scanner_windows_collector_windowscollector_init": ".__init__()" | kind=code-symbol | source=scanner/windows_collector.py:L239 | neighbors=[WindowsCollector] | lang=en
- "scanner_windows_collector_winrm_collect": "_winrm_collect()" | kind=code-symbol | source=scanner/windows_collector.py:L114 | neighbors=[windows_collector.py] | lang=en
- "tests_conftest": "conftest.py" | kind=code-symbol | source=tests/conftest.py:L1 | neighbors=[ae7a30b feat: add Posture & Patch-Compa…] | lang=en
- "tests_test_adaptive_rate_echoprotocol_connection_made": ".connection_made()" | kind=code-symbol | source=tests/test_adaptive_rate.py:L178 | neighbors=[_EchoProtocol] | lang=en
- "tests_test_adaptive_rate_echoprotocol_datagram_received": ".datagram_received()" | kind=code-symbol | source=tests/test_adaptive_rate.py:L181 | neighbors=[_EchoProtocol] | lang=en
- "tests_test_adaptive_rate_rationale_1": "test_adaptive_rate.py — Tier 1.3: adaptive congestion control + UDP retransmit." | kind=entity | source=tests/test_adaptive_rate.py:L1 | neighbors=[test_adaptive_rate.py] | lang=en
- "tests_test_adaptive_rate_testudpretransmit_test_retries_exhaust_on_silence": ".test_retries_exhaust_on_silence()" | kind=code-symbol | source=tests/test_adaptive_rate.py:L146 | neighbors=[TestUdpRetransmit] | lang=en
- "tests_test_adaptive_rate_testudpretransmit_test_retry_recovers_dropped_reply": ".test_retry_recovers_dropped_reply()" | kind=code-symbol | source=tests/test_adaptive_rate.py:L159 | neighbors=[TestUdpRetransmit] | lang=en
- "tests_test_adaptive_rate_testudpretransmit_test_returns_immediately_on_closed": ".test_returns_immediately_on_closed()" | kind=code-symbol | source=tests/test_adaptive_rate.py:L133 | neighbors=[TestUdpRetransmit] | lang=en
- "tests_test_adaptive_rate_testudpretransmit_test_returns_immediately_on_reply": ".test_returns_immediately_on_reply()" | kind=code-symbol | source=tests/test_adaptive_rate.py:L120 | neighbors=[TestUdpRetransmit] | lang=en
- "tests_test_adaptive_rate_testudpscanneradaptive_test_adaptive_scanner_creates_controller": ".test_adaptive_scanner_creates_controller()" | kind=code-symbol | source=tests/test_adaptive_rate.py:L186 | neighbors=[TestUdpScannerAdaptive] | lang=en
- "tests_test_adaptive_rate_testudpscanneradaptive_test_adaptive_scanner_detects_open_on_loopback": ".test_adaptive_scanner_detects_open_on_loopback()" | kind=code-symbol | source=tests/test_adaptive_rate.py:L198 | neighbors=[TestUdpScannerAdaptive] | lang=en
- "tests_test_adaptive_rate_testudpscanneradaptive_test_non_adaptive_scanner_has_no_controller": ".test_non_adaptive_scanner_has_no_controller()" | kind=code-symbol | source=tests/test_adaptive_rate.py:L192 | neighbors=[TestUdpScannerAdaptive] | lang=en
- "tests_test_adaptive_rate_testwindowgating_test_acquire_blocks_when_window_full": ".test_acquire_blocks_when_window_full()" | kind=code-symbol | source=tests/test_adaptive_rate.py:L80 | neighbors=[TestWindowGating] | lang=en
- "tests_test_adaptive_rate_testwindowgating_test_release_unblocks_waiter": ".test_release_unblocks_waiter()" | kind=code-symbol | source=tests/test_adaptive_rate.py:L92 | neighbors=[TestWindowGating] | lang=en
- "tests_test_adaptive_rate_testwindowgating_test_report_loss_shrinks_and_releases": ".test_report_loss_shrinks_and_releases()" | kind=code-symbol | source=tests/test_adaptive_rate.py:L108 | neighbors=[TestWindowGating] | lang=en
- "tests_test_adaptive_rate_testwindowstatemachine_test_congestion_avoidance_grows_sublinearly": ".test_congestion_avoidance_grows_sublinearly()" | kind=code-symbol | source=tests/test_adaptive_rate.py:L39 | neighbors=[TestWindowStateMachine] | lang=en
- "tests_test_adaptive_rate_testwindowstatemachine_test_initial_window": ".test_initial_window()" | kind=code-symbol | source=tests/test_adaptive_rate.py:L28 | neighbors=[TestWindowStateMachine] | lang=en
- "tests_test_adaptive_rate_testwindowstatemachine_test_loss_halves_window": ".test_loss_halves_window()" | kind=code-symbol | source=tests/test_adaptive_rate.py:L45 | neighbors=[TestWindowStateMachine] | lang=en
- "tests_test_adaptive_rate_testwindowstatemachine_test_loss_sets_ssthresh_to_half": ".test_loss_sets_ssthresh_to_half()" | kind=code-symbol | source=tests/test_adaptive_rate.py:L50 | neighbors=[TestWindowStateMachine] | lang=en
- "tests_test_adaptive_rate_testwindowstatemachine_test_recovery_after_loss_enters_congestion_avoidance": ".test_recovery_after_loss_enters_congestion_avoidance()" | kind=code-symbol | source=tests/test_adaptive_rate.py:L69 | neighbors=[TestWindowStateMachine] | lang=en
- "tests_test_adaptive_rate_testwindowstatemachine_test_slow_start_grows_by_one_per_success": ".test_slow_start_grows_by_one_per_success()" | kind=code-symbol | source=tests/test_adaptive_rate.py:L32 | neighbors=[TestWindowStateMachine] | lang=en
- "tests_test_adaptive_rate_testwindowstatemachine_test_window_never_above_max": ".test_window_never_above_max()" | kind=code-symbol | source=tests/test_adaptive_rate.py:L62 | neighbors=[TestWindowStateMachine] | lang=en
- "tests_test_adaptive_rate_testwindowstatemachine_test_window_never_below_min": ".test_window_never_below_min()" | kind=code-symbol | source=tests/test_adaptive_rate.py:L55 | neighbors=[TestWindowStateMachine] | lang=en
- "tests_test_agent_identity_test_generated_scope_identity_preserves_agent_credentials": "test_generated_scope_identity_preserves_agent_credentials()" | kind=code-symbol | source=tests/test_agent_identity.py:L19 | neighbors=[test_agent_identity.py] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/probe/.graphify/description-instructions/batch-068.json

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
