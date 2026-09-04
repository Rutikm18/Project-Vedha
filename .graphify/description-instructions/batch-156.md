# Node Description Batch 157 of 332

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
- "tests_test_nuclei_background_test_partial_nuclei_run_preserves_findings_and_diagnostics": "test_partial_nuclei_run_preserves_findings_and_diagnostics()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_background.py:L117 | neighbors=[test_nuclei_background.py, _SessionFactory]
- "tests_test_nuclei_scanner_test_nonzero_exit_without_findings_raises_with_stderr": "test_nonzero_exit_without_findings_raises_with_stderr()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L108 | neighbors=[test_nuclei_scanner.py, FakeProcess]
- "tests_test_nuclei_scanner_test_template_initialization_failure_cannot_be_clean_zero": "test_template_initialization_failure_cannot_be_clean_zero()" | kind=code-symbol | source=manager/backend/tests/test_nuclei_scanner.py:L177 | neighbors=[test_nuclei_scanner.py, FakeProcess]
- "tests_test_online_nvd_empty": "_nvd_empty()" | kind=code-symbol | source=probe/tests/test_online.py:L39 | neighbors=[test_online.py, .test_empty_result_is_none()]
- "tests_test_online_testenrichfindings_test_caches_per_cve_id": ".test_caches_per_cve_id()" | kind=code-symbol | source=probe/tests/test_online.py:L159 | neighbors=[TestEnrichFindings, _finding()]
- "tests_test_online_testenrichfindings_test_only_missing_skips_already_scored": ".test_only_missing_skips_already_scored()" | kind=code-symbol | source=probe/tests/test_online.py:L128 | neighbors=[TestEnrichFindings, _finding()]
- "tests_test_online_testenrichfindings_test_vulners_exploit_flags_finding": ".test_vulners_exploit_flags_finding()" | kind=code-symbol | source=probe/tests/test_online.py:L148 | neighbors=[TestEnrichFindings, _finding()]
- "tests_test_online_testlookupnvd_test_garbage_json_is_fail_open": ".test_garbage_json_is_fail_open()" | kind=code-symbol | source=probe/tests/test_online.py:L94 | neighbors=[TestLookupNvd, _get_returning()]
- "tests_test_online_testlookupnvd_test_network_error_is_fail_open": ".test_network_error_is_fail_open()" | kind=code-symbol | source=probe/tests/test_online.py:L89 | neighbors=[TestLookupNvd, _get_raising()]
- "tests_test_online_testlookupvulners_test_error_is_none": ".test_error_is_none()" | kind=code-symbol | source=probe/tests/test_online.py:L112 | neighbors=[TestLookupVulners, _get_raising()]
- "tests_test_online_testlookupvulners_test_no_key_returns_none": ".test_no_key_returns_none()" | kind=code-symbol | source=probe/tests/test_online.py:L101 | neighbors=[TestLookupVulners, _get_returning()]
- "tests_test_os_fingerprint_testacceptechoreply_test_accepts_echo_reply_from_target": ".test_accepts_echo_reply_from_target()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L173 | neighbors=[TestAcceptEchoReply, ._reply()]
- "tests_test_os_fingerprint_testacceptechoreply_test_accepts_when_source_unknown": ".test_accepts_when_source_unknown()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L186 | neighbors=[TestAcceptEchoReply, ._reply()]
- "tests_test_os_fingerprint_testacceptechoreply_test_rejects_non_echo_type": ".test_rejects_non_echo_type()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L180 | neighbors=[TestAcceptEchoReply, ._reply()]
- "tests_test_os_fingerprint_testacceptechoreply_test_rejects_reply_from_a_different_host": ".test_rejects_reply_from_a_different_host()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L176 | neighbors=[TestAcceptEchoReply, ._reply()]
- "tests_test_os_fingerprint_testicmpparse_ip_icmp": "._ip_icmp()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L63 | neighbors=[TestIcmpParse, .test_parse_extracts_ttl_and_type()]
- "tests_test_os_fingerprint_testicmpparse_test_parse_extracts_ttl_and_type": ".test_parse_extracts_ttl_and_type()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L72 | neighbors=[TestIcmpParse, ._ip_icmp()]
- "tests_test_os_fingerprint_testicmptimestamps_test_parse_datagram_delivery_has_no_ttl": ".test_parse_datagram_delivery_has_no_ttl()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L113 | neighbors=[TestIcmpTimestamps, ._ts_reply()]
- "tests_test_os_fingerprint_testicmptimestamps_test_parse_extracts_ttl_and_transmit": ".test_parse_extracts_ttl_and_transmit()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L107 | neighbors=[TestIcmpTimestamps, ._ts_reply()]
- "tests_test_os_fingerprint_testtimestampfallback_test_both_filtered_reports_no_reply": ".test_both_filtered_reports_no_reply()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L158 | neighbors=[TestTimestampFallback, ._scanner()]
- "tests_test_os_fingerprint_testtimestampfallback_test_timestamp_reply_when_echo_is_filtered": ".test_timestamp_reply_when_echo_is_filtered()" | kind=code-symbol | source=probe/tests/test_os_fingerprint.py:L144 | neighbors=[TestTimestampFallback, ._scanner()]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-156.json

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
