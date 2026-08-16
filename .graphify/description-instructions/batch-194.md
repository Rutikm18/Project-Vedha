# Node Description Batch 195 of 209

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

- "tests_test_service_match_testotherservices_test_mariadb_handshake": ".test_mariadb_handshake()" | kind=code-symbol | source=probe/tests/test_service_match.py:L70 | neighbors=[TestOtherServices]
- "tests_test_service_match_testotherservices_test_redis_info": ".test_redis_info()" | kind=code-symbol | source=probe/tests/test_service_match.py:L77 | neighbors=[TestOtherServices]
- "tests_test_service_match_testotherservices_test_redis_noauth": ".test_redis_noauth()" | kind=code-symbol | source=probe/tests/test_service_match.py:L82 | neighbors=[TestOtherServices]
- "tests_test_service_match_testotherservices_test_smtp_postfix": ".test_smtp_postfix()" | kind=code-symbol | source=probe/tests/test_service_match.py:L65 | neighbors=[TestOtherServices]
- "tests_test_service_match_testotherservices_test_vsftpd": ".test_vsftpd()" | kind=code-symbol | source=probe/tests/test_service_match.py:L59 | neighbors=[TestOtherServices]
- "tests_test_service_match_testprobeladder_test_ladder_has_http_and_generic": ".test_ladder_has_http_and_generic()" | kind=code-symbol | source=probe/tests/test_service_match.py:L102 | neighbors=[TestProbeLadder]
- "tests_test_service_match_testprobeladder_test_ladder_starts_with_null_probe": ".test_ladder_starts_with_null_probe()" | kind=code-symbol | source=probe/tests/test_service_match.py:L96 | neighbors=[TestProbeLadder]
- "tests_test_service_match_testscannerintegration_test_scanner_identifies_ssh_on_nonstandard_port": ".test_scanner_identifies_ssh_on_nonstandard_port()" | kind=code-symbol | source=probe/tests/test_service_match.py:L109 | neighbors=[TestScannerIntegration]
- "tests_test_service_match_testsshmatch_test_dropbear": ".test_dropbear()" | kind=code-symbol | source=probe/tests/test_service_match.py:L23 | neighbors=[TestSshMatch]
- "tests_test_service_match_testsshmatch_test_generic_ssh": ".test_generic_ssh()" | kind=code-symbol | source=probe/tests/test_service_match.py:L29 | neighbors=[TestSshMatch]
- "tests_test_service_match_testsshmatch_test_openssh_version": ".test_openssh_version()" | kind=code-symbol | source=probe/tests/test_service_match.py:L17 | neighbors=[TestSshMatch]
- "tests_test_smb_scanner_rationale_15": "An SMB2 ERROR response (e.g. STATUS_INVALID_PARAMETER). Windows returns     this" | kind=entity | source=probe/tests/test_smb_scanner.py:L15 | neighbors=[_smb2_error_response()]
- "tests_test_smb_scanner_rationale_51": "The confirmed bug: an SMB2 error response (STATUS_INVALID_PARAMETER) was     rea" | kind=entity | source=probe/tests/test_smb_scanner.py:L51 | neighbors=[test_error_response_not_parsed_as_signi…]
- "tests_test_smb_scanner_rationale_63": "A response with the wrong body StructureSize is not a valid NEGOTIATE." | kind=entity | source=probe/tests/test_smb_scanner.py:L63 | neighbors=[test_truncated_negotiate_body_not_parse…]
- "tests_test_smb_scanner_rationale_72": "Step 13: expose signing_supported (protocol-precise), not only the     ambiguous" | kind=entity | source=probe/tests/test_smb_scanner.py:L72 | neighbors=[test_signing_supported_field_present()]
- "tests_test_smb_scanner_rationale_81": "Offering SMB 3.1.1 with no preauth-integrity negotiate context makes     Windows" | kind=entity | source=probe/tests/test_smb_scanner.py:L81 | neighbors=[test_request_omits_311_without_preauth_…]
- "tests_test_smb_scanner_test_garbage_response": "test_garbage_response()" | kind=code-symbol | source=probe/tests/test_smb_scanner.py:L44 | neighbors=[test_smb_scanner.py]
- "tests_test_syn_scanner_rationale_1": "test_syn_scanner.py — stateless SYN scan (Tier 1.1).  The raw-socket send/receiv" | kind=entity | source=probe/tests/test_syn_scanner.py:L1 | neighbors=[test_syn_scanner.py]
- "tests_test_syn_scanner_rationale_205": "The raw SYN path resends ONLY still-silent ports — the direct fix for the     fa" | kind=entity | source=probe/tests/test_syn_scanner.py:L205 | neighbors=[TestSynRetransmit]
- "tests_test_syn_scanner_rationale_208": "The raw SYN path resends ONLY still-silent ports — the direct fix for the     fa" | kind=entity | source=probe/tests/test_syn_scanner.py:L208 | neighbors=[TestSynRetransmit]
- "tests_test_syn_scanner_rationale_327": "A SYN/ACK carrying an MSS option (data offset 6 = 24-byte TCP header)." | kind=entity | source=probe/tests/test_syn_scanner.py:L327 | neighbors=[_synack_with_options()]
- "tests_test_syn_scanner_testadaptivetimeouttoggle_test_adaptive_on_by_default": ".test_adaptive_on_by_default()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L382 | neighbors=[TestAdaptiveTimeoutToggle]
- "tests_test_syn_scanner_testadaptivetimeouttoggle_test_can_disable": ".test_can_disable()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L386 | neighbors=[TestAdaptiveTimeoutToggle]
- "tests_test_syn_scanner_testcapabilitydetection_test_linux_with_raw_socket_is_supported": ".test_linux_with_raw_socket_is_supported()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L148 | neighbors=[TestCapabilityDetection]
- "tests_test_syn_scanner_testcapabilitydetection_test_linux_without_privilege_is_unsupported": ".test_linux_without_privilege_is_unsupported()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L143 | neighbors=[TestCapabilityDetection]
- "tests_test_syn_scanner_testcapabilitydetection_test_non_linux_is_unsupported": ".test_non_linux_is_unsupported()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L139 | neighbors=[TestCapabilityDetection]
- "tests_test_syn_scanner_testchecksum_test_checksum_handles_odd_length": ".test_checksum_handles_odd_length()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L34 | neighbors=[TestChecksum]
- "tests_test_syn_scanner_testchecksum_test_checksum_of_valid_ip_header_is_zero": ".test_checksum_of_valid_ip_header_is_zero()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L28 | neighbors=[TestChecksum]
- "tests_test_syn_scanner_testchecksum_test_tcp_checksum_verifies_to_zero": ".test_tcp_checksum_verifies_to_zero()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L38 | neighbors=[TestChecksum]
- "tests_test_syn_scanner_testclassify_test_other_flags_are_none": ".test_other_flags_are_none()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L102 | neighbors=[TestClassify]
- "tests_test_syn_scanner_testclassify_test_rst_is_closed": ".test_rst_is_closed()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L98 | neighbors=[TestClassify]
- "tests_test_syn_scanner_testclassify_test_syn_ack_is_open": ".test_syn_ack_is_open()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L95 | neighbors=[TestClassify]
- "tests_test_syn_scanner_testoptionparsing_test_malformed_options_never_raise": ".test_malformed_options_never_raise()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L317 | neighbors=[TestOptionParsing]
- "tests_test_syn_scanner_testoptionparsing_test_mss_absent_returns_none": ".test_mss_absent_returns_none()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L314 | neighbors=[TestOptionParsing]
- "tests_test_syn_scanner_testoptionparsing_test_mss_after_nop_padding": ".test_mss_after_nop_padding()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L307 | neighbors=[TestOptionParsing]
- "tests_test_syn_scanner_testoptionparsing_test_mss_extracted": ".test_mss_extracted()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L304 | neighbors=[TestOptionParsing]
- "tests_test_syn_scanner_testoptionparsing_test_mss_skips_other_options": ".test_mss_skips_other_options()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L310 | neighbors=[TestOptionParsing]
- "tests_test_syn_scanner_testpacketroundtrip_test_ip_checksum_valid_in_full_packet": ".test_ip_checksum_valid_in_full_packet()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L84 | neighbors=[TestPacketRoundTrip]
- "tests_test_syn_scanner_testpacketroundtrip_test_parse_rejects_short_packet": ".test_parse_rejects_short_packet()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L88 | neighbors=[TestPacketRoundTrip]
- "tests_test_syn_scanner_testpacketroundtrip_test_syn_flag_is_set": ".test_syn_flag_is_set()" | kind=code-symbol | source=probe/tests/test_syn_scanner.py:L79 | neighbors=[TestPacketRoundTrip]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /Users/rutikmangale/Documents/DRIVE T -Var/Security-projects/Vedha/.graphify/description-instructions/batch-194.json

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
