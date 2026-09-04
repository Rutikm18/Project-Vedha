# Node Description Batch 156 of 330

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

- "tests_test_manager_ai_test_fallback_never_includes_local_ollama": "test_fallback_never_includes_local_ollama()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L337 | neighbors=[test_manager_ai.py, _cloud()]
- "tests_test_manager_ai_test_generate_fails_closed_when_no_cloud_provider_configured": "test_generate_fails_closed_when_no_cloud_provider_configured()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L328 | neighbors=[test_manager_ai.py, _cloud()]
- "tests_test_manager_ai_test_status_fails_safe_without_cloud_key": "test_status_fails_safe_without_cloud_key()" | kind=code-symbol | source=manager/backend/tests/test_manager_ai.py:L349 | neighbors=[test_manager_ai.py, _cloud()]
- "tests_test_manual_reopen": "test_manual_reopen.py" | kind=code-symbol | source=manager/backend/tests/test_manual_reopen.py:L1 | neighbors=[3c7740e feat(lifecycle): pure manual-re…, test_manual_reopen_restores_open_and_au…]
- "tests_test_msrpc_scanner_testmsrpcfindings_test_endpoints_low": ".test_endpoints_low()" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L86 | neighbors=[TestMSRPCFindings, ._fact()]
- "tests_test_msrpc_scanner_testmsrpcfindings_test_zero_endpoints_silent": ".test_zero_endpoints_silent()" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L92 | neighbors=[TestMSRPCFindings, ._fact()]
- "tests_test_msrpc_scanner_testmsrpcscanner_test_impacket_missing_is_error": ".test_impacket_missing_is_error()" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L74 | neighbors=[TestMSRPCScanner, ._sc()]
- "tests_test_msrpc_scanner_testmsrpcscanner_test_no_msrpc_filtered": ".test_no_msrpc_filtered()" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L69 | neighbors=[TestMSRPCScanner, ._sc()]
- "tests_test_msrpc_scanner_testmsrpcscanner_test_open": ".test_open()" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L61 | neighbors=[TestMSRPCScanner, ._sc()]
- "tests_test_msrpc_scanner_testparity": "TestParity" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L97 | neighbors=[test_msrpc_scanner.py, .test_main_scripts()]
- "tests_test_msrpc_scanner_testsummarize": "TestSummarize" | kind=code-symbol | source=probe/tests/test_msrpc_scanner.py:L18 | neighbors=[test_msrpc_scanner.py, .test_distinct_interfaces_and_named()]
- "tests_test_nessus_scanner_test_create_scan": "test_create_scan()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L48 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_nessus_scanner_test_create_scan_with_credentials": "test_create_scan_with_credentials()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L65 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_nessus_scanner_test_launch_scan": "test_launch_scan()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L85 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_nessus_scanner_test_poll_status_completed": "test_poll_status_completed()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L114 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_nessus_scanner_test_poll_status_running": "test_poll_status_running()" | kind=code-symbol | source=manager/backend/tests/test_nessus_scanner.py:L99 | neighbors=[test_nessus_scanner.py, _mock_response()]
- "tests_test_network_va_accuracy_listener_loop": "._loop()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L48 | neighbors=[_Listener, .start()]
- "tests_test_network_va_accuracy_listener_stop": ".stop()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L72 | neighbors=[_Listener, va_scan()]
- "tests_test_network_va_accuracy_test_every_planted_risk_port_is_found": "test_every_planted_risk_port_is_found()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L119 | neighbors=[test_network_va_accuracy.py, The regression this guards: these ports…]
- "tests_test_network_va_accuracy_test_irc_is_identified_by_protocol_not_port": "test_irc_is_identified_by_protocol_not_port()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L140 | neighbors=[test_network_va_accuracy.py, Positive protocol evidence turns the bo…]
- "tests_test_network_va_accuracy_test_no_branch_runs_without_evidence": "test_no_branch_runs_without_evidence()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L168 | neighbors=[test_network_va_accuracy.py, Every deep branch that ran must have pr…]
- "tests_test_network_va_accuracy_test_post_stages_ran": "test_post_stages_ran()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L188 | neighbors=[test_network_va_accuracy.py, network_va composes device classificati…]
- "tests_test_network_va_accuracy_test_silent_port_reports_no_banner_honestly": "test_silent_port_reports_no_banner_honestly()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L156 | neighbors=[test_network_va_accuracy.py, 4444 says nothing. The scanner must rec…]
- "tests_test_network_va_accuracy_test_tls_branch_is_not_routed_by_silence": "test_tls_branch_is_not_routed_by_silence()" | kind=code-symbol | source=probe/tests/test_network_va_accuracy.py:L180 | neighbors=[test_network_va_accuracy.py, service_banner now proves non-TLS by at…]
- "tests_test_new_scanners_testdeltaengine_test_load_jsonl_skips_invalid_json": ".test_load_jsonl_skips_invalid_json()" | kind=code-symbol | source=probe/tests/test_new_scanners.py:L502 | neighbors=[TestDeltaEngine, _make_scan_record()]
- "tests_test_nfs_scanner_portmap_dump_reply": "_portmap_dump_reply()" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L41 | neighbors=[test_nfs_scanner.py, .test_portmap_dump_parse()]
- "tests_test_nfs_scanner_testnfsfindings_test_restricted_exports_no_high_finding": ".test_restricted_exports_no_high_finding()" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L133 | neighbors=[TestNFSFindings, ._fact()]
- "tests_test_nfs_scanner_testnfsfindings_test_world_readable_and_portmapper": ".test_world_readable_and_portmapper()" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L122 | neighbors=[TestNFSFindings, ._fact()]
- "tests_test_nfs_scanner_testnfsscanner_test_no_rpc_is_filtered": ".test_no_rpc_is_filtered()" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L109 | neighbors=[TestNFSScanner, ._sc()]
- "tests_test_nfs_scanner_testnfsscanner_test_world_readable_export_open": ".test_world_readable_export_open()" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L99 | neighbors=[TestNFSScanner, ._sc()]
- "tests_test_nfs_scanner_testparity": "TestParity" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L142 | neighbors=[test_nfs_scanner.py, .test_main_scripts()]
- "tests_test_nfs_scanner_testparity_test_main_scripts": ".test_main_scripts()" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L143 | neighbors=[TestParity, _mount_export_reply()]
- "tests_test_nfs_scanner_testxdrparsers_test_mount_export_parse_and_world_flag": ".test_mount_export_parse_and_world_flag()" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L52 | neighbors=[TestXdrParsers, _mount_export_reply()]
- "tests_test_nfs_scanner_testxdrparsers_test_portmap_dump_parse": ".test_portmap_dump_parse()" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L62 | neighbors=[TestXdrParsers, _portmap_dump_reply()]
- "tests_test_nfs_scanner_testxdrparsers_test_rpc_reply_header_stripping": ".test_rpc_reply_header_stripping()" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L68 | neighbors=[TestXdrParsers, _mount_export_reply()]
- "tests_test_nfs_scanner_xstr": "_xstr()" | kind=code-symbol | source=probe/tests/test_nfs_scanner.py:L25 | neighbors=[test_nfs_scanner.py, _mount_export_reply()]
- "tests_test_nuclei_background_fakesession_begin_nested": ".begin_nested()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L43 | neighbors=[_FakeSession, _NestedTransaction]
- "tests_test_nuclei_background_fakesession_execute": ".execute()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L40 | neighbors=[_FakeSession, _ScalarResult]
- "tests_test_nuclei_background_sessionfactory_call": ".__call__()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L71 | neighbors=[_SessionFactory, _FakeSession]
- "tests_test_nuclei_background_test_fatal_nuclei_error_marks_background_job_failed": "test_fatal_nuclei_error_marks_background_job_failed()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L76 | neighbors=[test_nuclei_background.py, _SessionFactory]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-155.json

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
